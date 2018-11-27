"""
run.py
Scope: The entrance point for our program.
Authors: Jeffrey Smith, Bill Cramer, Evan French
"""
import sys, getopt, os, subprocess, re, configparser
import agent
from classes import SentenceStructure, Annotation, BatchContainer
from preprocess import preprocess
from random import sample
import numpy as np

np.set_printoptions(threshold=np.nan)

configFile = configparser.ConfigParser()
configFile.read_file(open('config.ini'))
config = configFile['Main']

#CONSTANTS
if not 'MAX_SENTENCE_LENGTH' in config:
	print("Missing MAX_SENTENCE_LENGTH in config.ini.")
	sys.exit(0)
	
if not 'EMBEDDING_SIZE' in config:
	print("Missing EMBEDDING_SIZE in config.ini")
	sys.exit(0)
	
if not 'EMBEDDING_FILE' in config:
	print("Missing EMBEDDING_FILE in config.ini")
	sys.exit(0)	

if not 'ANNOTATION_FILE_PATH' in config:
	print("Missing ANNOTATION_FILE_PATH in config.ini")
	sys.exit(0)	
	
if not 'RAW_FILE_PATH' in config:
	print("Missing RAW_FILE_PATH in config.ini")
	sys.exit(0)	

if not 'BUCKETS' in config:
	print("Missing BUCKETS in config.ini")
	sys.exit(0)	

if not 'EPOCHS' in config:
	print("Missing EPOCHS in config.ini")
	sys.exit(0)		
	
if not 'CLASSES' in config:
	print("Missing CLASSES in config.ini")
	sys.exit(0)		
	
FEATURE_INDEX_MAP = {"PUNC_OTHER" : 0,
					"PUNC_COMMA" : 1,
					"PUNC_PERIOD" : 2,
					"IS_NUM" : 3,
					"IS_DATE" : 4}

EXTRA_FEATURE_SIZE = len(FEATURE_INDEX_MAP)

CLASSES = config['CLASSES'].split(',')

#Author: Jeffrey Smith
def main():
	"""
	Main function of the application. Call -h or --help for command line inputs.
	"""
	dict_ = CreateAnnotatedSentenceStructures(config['ANNOTATION_FILE_PATH'], config['RAW_FILE_PATH'])
	#TEST
	dict_supplemental = CreateSupplementalSentenceStructures("./supplemental_data")
	
	AddModifiedSentenceArray(dict_)
	#TEST
	AddModifiedSentenceArray(dict_supplemental)

	tx,ty,ts,tm = GenerateEmbeddings(dict_, config['EMBEDDING_FILE'])
	trainBatch = BatchContainer(tx,ty,ts,tm)
	sx,sy,ss,sm = GenerateEmbeddings(dict_supplemental, config['EMBEDDING_FILE'])
	supplementalBatch = BatchContainer(sx,sy,ss,sm)
	
	trainNetwork(trainBatch,dict_,int(config['EMBEDDING_SIZE']) + EXTRA_FEATURE_SIZE, CLASSES, int(config['BUCKETS']),int(config['EPOCHS']), supplementalBatch)
	

#Author: Jeffrey Smith
def trainNetwork(trainBatch, dict, numFeatures, classes, buckets, epochs, supplementalBatch = None):
	"""
	Trains a neural network model. If one is not given, creates one.
	"""		
	#Setup Buckets for 10 fold cross validation
	batchX, batchY, seqLen, batchMap = kFoldBucketGenerator(trainBatch.bx, trainBatch.by, trainBatch.bs, buckets)
	if not supplementalBatch == None:
		supBatchX, supBatchY, supSeqLen, _ = kFoldBucketGenerator(supplementalBatch.bx, supplementalBatch.by, supplementalBatch.bs, 10)
	
	#batchMap and fileMap are used later for evaluation.
	
	#Create and train the model 10x for 10FoldCrossValidation
	confusionMatrixList = []
	sentenceLenienceList = []
	
	for k in range(0, buckets):
		myAgent = agent.Agent(numFeatures,4,int(config['MAX_SENTENCE_LENGTH']))
		
		#Train for j epochs.
		for j in range(0, epochs):
		
			loss = 0
			
			#Train Supplemental
			if not supplementalBatch == None:
				for l in range(0, 10):
					loss += myAgent.train(supBatchX[l], supBatchY[l], supSeqLen[l])

			#Train each bucket where l != currentK
			for l in range(0, buckets):
				if l == k:
					continue
				loss += myAgent.train(batchX[l], batchY[l], seqLen[l])
	
			print("Loss for Epoch " + str(j) + " is " + str(loss) + ".")
			
		#Evaluate after training.
		cf = myAgent.eval(batchX[k], batchY[k], seqLen[k])
		confusionMatrixList.append(cf)
		
		print(cf)
		
		file = open("./outCF", 'a')
		outstr = np.array2string(cf)
		file.write(outstr)
		file.write("\n")
		file.close()
		
		cf_ = myAgent.evalWithStructure(batchX[k], batchY[k], seqLen[k], k, trainBatch.mapping, batchMap, dict)
		sentenceLenienceList.append(cf_)
		file = open("./outCFS", 'a')
		outstr = np.array2string(cf_)
		file.write(outstr)
		file.write("\n")
		file.close()
					
		myAgent.cleanUp()
		
	#Run analysis generation.
	
	#Start with Majority Sense Baseline
	classCount = len(confusionMatrixList[0])
	majoritySenseData = np.zeros((1, classCount), dtype=np.int32)
	
	for i in confusionMatrixList:
		for j in range(0, classCount):
			for k in range(0, classCount):
				majoritySenseData[0,k] += i[j,k]
				
	classNoneMicroPrecision = 1.0 * majoritySenseData[0,0] / np.sum(majoritySenseData[0,:])
	classNoneMicroRecall = 1.0
	classNoneMicroF1Score = 2 * (classNoneMicroPrecision/(classNoneMicroPrecision+1.0))
	
	classNoneMacroPrecision = classNoneMicroPrecision/classCount
	classNoneMacroRecall = 1.0/classCount
	classNoneMacroF1Score = classNoneMicroF1Score/classCount
	
	#Now for all the individual buckets.
	precisionMicroList = np.zeros((classCount, len(confusionMatrixList)), dtype=np.float32)
	recallMicroList = np.zeros((classCount, len(confusionMatrixList)), dtype=np.float32)
	f1MicroList = np.zeros((classCount, len(confusionMatrixList)), dtype=np.float32)
	precisionMacroList = []
	recallMacroList = []
	f1MacroList = []
	
	for i in range(0,len(confusionMatrixList)):
		for j in range(0, classCount):
			precisionMicroList[j,i] = 1.0 * confusionMatrixList[i][j,j] / np.sum(confusionMatrixList[i][j,:])
			recallMicroList[j,i] = 1.0 * confusionMatrixList[i][j,j] / np.sum(confusionMatrixList[i][:,j])
			f1MicroList[j,i] = 2.0 * ((precisionMicroList[j,i] * recallMicroList[j,i]) / (precisionMicroList[j,i] + recallMicroList[j,i]))
			
		precisionMacroList.append((np.sum(precisionMicroList[:,i])/classCount))
		recallMacroList.append((np.sum(recallMicroList[:,i])/classCount))
		f1MacroList.append((np.sum(f1MicroList[:,i])/classCount))
		
	#Process Sentence Lenience Lists
	totalSentenceLenience = np.zeros((classCount, 3), dtype=np.int32)
	
	for i in sentenceLenienceList:
		totalSentenceLenience[:,:] += i[:,:]
			
	#Write Information to file
	file = open("./analysis.txt", 'a')
	
	file.write("===Majority Sense Baseline===\n")
	file.write("Micro Precision: \t" + str(classNoneMicroPrecision) + "\n")
	file.write("Micro Recall: \t" + str(classNoneMicroRecall) + "\n")
	file.write("Micro F1: \t" + str(classNoneMicroF1Score) + "\n")
	file.write("Macro Precision: \t" + str(classNoneMacroPrecision) + "\n")
	file.write("Macro Recall: \t" + str(classNoneMacroRecall) + "\n")
	file.write("Macro F1: \t" + str(classNoneMacroF1Score) + "\n\n")
	
	file.write("===Summary===\n\n")
	
	file.write("=Macro=\n")
	file.write("Macro F1 Total Average: \t" + str(sum(f1MacroList)/buckets) + "\n")
	file.write("Macro F1 Minimum: \t" + str(min(f1MacroList)) + "\n")
	file.write("Macro F1 Maximum: \t" + str(max(f1MacroList)) + "\n\n")
	
	file.write("=Sentence Level=\n")
	file.write("CLASS \tSTRICT \tLENIENT \tMISS \tS% \tL%\n")
	for i in range(0, classCount):
		file.write(str(classes[i]) + " \t" + str(totalSentenceLenience[i,0]) + " \t" + str(totalSentenceLenience[i,1]) + " \t" + str(totalSentenceLenience[i,2]) + str(totalSentenceLenience[i,0]/np.sum(totalSentenceLenience[i,:])) + "\t" + str(np.sum(totalSentenceLenience[i,0:2])/np.sum(totalSentenceLenience[i,:])) + "\n")
	file.write("\n")	
		
	for i in range(0, classCount):
		file.write("=" + str(classes[i]) + "=\n")
		file.write("Micro Precision Average: \t" + str(np.sum(precisionMicroList[i,:])/buckets) + "\n")
		file.write("Micro Recall Average: \t" + str(np.sum(recallMicroList[i,:])/buckets) + "\n")
		file.write("Micro F1 Average: \t" + str(np.sum(f1MicroList[i,:])/buckets) + "\n")
		file.write("\n")
		
	file.close()

	return
	

#Author: Jeffrey Smith
def kFoldBucketGenerator(batchX, batchY, seqLen, k):
	"""
	Takes a batch and shuffles it, then creates k subbatches of each.
	"""		
	
	indicies = sample(range(0, len(batchX)), len(batchX))
	
	nBatchX, nBatchY, nSeqLen = [], [], []
	batchMapping = []
	
	#Create K Buckets
	for i in range(0, k):
		m = int(len(indicies) / (k-i))
		
		x, y, z, map = [], [], [], []
		
		for n in range(0, m):
			index = indicies.pop(0)
			x.append(batchX[index])
			y.append(batchY[index])
			z.append(seqLen[index])
			map.append(index)
			
		nBatchX.append(x)
		nBatchY.append(y)
		nSeqLen.append(z)
		batchMapping.append(map)
		
	return nBatchX, nBatchY, nSeqLen, batchMapping
		
	
	
	
	
#Author: Jeffrey Smith		
def printHelp():
	"""
	Prints out the command line help information.
	"""	
	print("Options:")
	print("-m/--mode [test,train,eval] : Specify the mode of the system.")
	print("-i/--input DIR : Specify the input directory to read from.")
	print("-a/--annotations DIR : Specify the annotations directory to read from.")
	print("-o/--output DIR : Specify the output directory to write to.")
	print("-d/--model FILE : Specify a model to use when running in eval mode.")
	
	return

#Author: Jeffrey Smith
def GenerateEmbeddings(d, embedFile):

	if not os.path.isdir('./_arff'):
		os.mkdir('_arff')

	#Launch perl pipe
	args = ['perl', './w2v.pl', embedFile]
	p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
	outs, errs = [], []

	#Wait until perl is done loading file.
	loaded = False
	while p.poll() == None:
		t = p.stdout.readline() 
		if "READY" in t:
			loaded = True
			break
		elif "FAILED" in t:
			break;
		elif "EXIT" in t:
			break;

	if not loaded == True:
		print("Perl module did not load correctly. Dying.")
		sys.exit(-1)

	print("Perl loaded correctly.")

	#Generate embedding file for each thingy.
	embeddingList = []
	classList = []
	seqList = []
	mapping = [] #A map to tie things back together.
	
	undefined = []
	
	try:
		k = d.keys()
		for k_ in k:
			print(k_)
			f = open('./_arff/' + k_, 'w+')
			sentenceCounter = 0

			###Change this later, only static for the interm
			f.write("201\n")

			#x: list of sentences
			for x in d[k_]:
				f.write("START\n")
				tArray = np.zeros((int(config['MAX_SENTENCE_LENGTH']),int(config['EMBEDDING_SIZE']) + EXTRA_FEATURE_SIZE), dtype=np.float32)
				cArray = np.zeros((int(config['MAX_SENTENCE_LENGTH'])), dtype=np.float32)

				for z in range(0,len(x.modifiedSentenceArray)):
					p.stdin.write(x.modifiedSentenceArray[z][0] + "\n")
					p.stdin.flush()

					class_ = 0
					
					if not "End" in x.originalSentenceArray[z][1]:
						if "problem" in x.originalSentenceArray[z][1]:
							class_ = 1
						elif "test" in x.originalSentenceArray[z][1]:
							class_ = 2
						elif "treatment" in x.originalSentenceArray[z][1]:
							class_ = 3

					while(p.poll() == None):				
						t = p.stdout.readline()

						if "UNDEF" in t:
							f.write(("0.0 " * int(config['EMBEDDING_SIZE'])) + str(class_) + "\n")
							undefined.append(x.modifiedSentenceArray[z][0])
							break
						elif len(t) > 2:
							#Temp Generate Embeddings
							tSplit = t.split();
							tArray[z][0:int(config['EMBEDDING_SIZE'])] = tSplit[1:int(config['EMBEDDING_SIZE'])+1]
							cArray[z] = class_
							
							f.write(t + " " + str(class_) + "\n")
							break
						else:
							print(t)
							
					#Generate Extra Features
					if x.modifiedSentenceArray[z][0] == ":":
						tArray[z][int(config['EMBEDDING_SIZE']) + FEATURE_INDEX_MAP["PUNC_OTHER"]] = 1.0
					elif x.modifiedSentenceArray[z][0] == ";":
						tArray[z][int(config['EMBEDDING_SIZE']) + FEATURE_INDEX_MAP["PUNC_OTHER"]] = 1.0
					elif x.modifiedSentenceArray[z][0] == ",":
						tArray[z][int(config['EMBEDDING_SIZE']) + FEATURE_INDEX_MAP["PUNC_COMMA"]] = 1.0
					elif x.modifiedSentenceArray[z][0] == ".":
						tArray[z][int(config['EMBEDDING_SIZE']) + FEATURE_INDEX_MAP["PUNC_PERIOD"]] = 1.0
					elif x.modifiedSentenceArray[z][0] == "[" or x.modifiedSentenceArray[z][0] == "]" or x.modifiedSentenceArray[z][0] == "(" or x.modifiedSentenceArray[z][0] == ")":
						tArray[z][int(config['EMBEDDING_SIZE']) + FEATURE_INDEX_MAP["PUNC_OTHER"]] = 1.0
					elif x.modifiedSentenceArray[z][0] == "&quot;":
						tArray[z][int(config['EMBEDDING_SIZE']) + FEATURE_INDEX_MAP["PUNC_OTHER"]] = 1.0
					elif x.modifiedSentenceArray[z][0] == "'" or x.modifiedSentenceArray[z][0] == "'s":
						tArray[z][int(config['EMBEDDING_SIZE']) + FEATURE_INDEX_MAP["PUNC_OTHER"]] = 1.0				
					elif x.modifiedSentenceArray[z][0] == "num":
						tArray[z][int(config['EMBEDDING_SIZE']) + FEATURE_INDEX_MAP["IS_NUM"]] = 1.0	
					elif x.modifiedSentenceArray[z][0] == "date":
						tArray[z][int(config['EMBEDDING_SIZE']) + FEATURE_INDEX_MAP["IS_DATE"]] = 1.0			
						
				#Add embeddings to our arrays.
				embeddingList.append(tArray);
				classList.append(cArray);
				seqList.append(len(x.modifiedSentenceArray))
				
				#Add this index back to the mapping.
				mapping.append([k_, sentenceCounter])
				sentenceCounter += 1

			f.close()
	except:
		print("Failed on something. Much descriptive.")
		p.terminate()
		sys.exit(-1)
	
	finally:
		p.stdin.write("EXIT\n")
		p.stdin.flush()
		
	p.terminate()
	
	#Debug 
	#Write words to file that were undefined in embedding list.
	xF = open('undef.txt', 'a')
	for x in undefined:
		xF.write(x)
		xF.write("\n")
	xF.close()

	return embeddingList, classList, seqList, mapping
	
#Author: Jeffrey Smith
def AddModifiedSentenceArray(d):
	#Get each list of SentenceStructures from map.
	v = d.values()

	for x in v:
		for y in x:
			y.generateModifiedSentenceArray()


#Author: Evan French
"""
Iterates through all documents in the directory specified in the params and creates a SentenceStructure object for each sentence. 
Return value is a dictionary keyed on document name with lists of SentenceStructure objects as values.
"""
def CreateSentenceStructures(raw_file_path):
	"""
	Create SentenceStructures from raw documents
	
	:param raw_file_path: Path to directory where raw documents are located
	:return: Dictionary of lists of SentenceStructure objects keyed on document name stripped of extension
	"""

	#Create a dictionary of documents
	docDictionary = {}

	# cd into test file directory
	cwd = os.getcwd()
	os.chdir(raw_file_path)

	#Iterate over documents in the raw_file_path directory
	for document in os.listdir():

		#Instantiate a list to hold a SentenceStructure for each sentence(line) in the document
		docSentenceStructureList = []

		#Open the document
		doc = open(document, "r")
		
		docText = doc.read()
		docTextProcessed = preprocess(docText)
		docTextProcessedSplit = docTextProcessed.splitlines()
		
		doc.close()
		
		doc = open(document, "r")
		try:
			#Iterate over sentences in the document
			counter = 0
			for sentence in doc.readlines():
				#Create a SentenceStructure obj
				ss = SentenceStructure(sentence)
				ss.modifiedSentence = docTextProcessedSplit[counter]

				#Add SentenceStructure obj to the list
				docSentenceStructureList.append(ss)        
				
				counter += 1
		except:
			print("ERR. " + str(document))
			sys.exit(0)
			
		assert(len(docSentenceStructureList) == len(docTextProcessedSplit)), "Assertion Failed, array lengths don't match. " + str(len(docSentenceStructureList)) + " " + str(len(docTextProcessedSplit))

		#Strip the extension from the file to get the document name
		docName = os.path.splitext(document)[0]

		#Add the SentenceStructureList to the dictionary
		docDictionary[docName] = docSentenceStructureList

		#Close the document
		doc.close()
		
	#Return to original path
	os.chdir(cwd)
	
	#Return the dictionary
	return docDictionary

#Author: Evan French
def CreateAnnotatedSentenceStructures(ann_file_path, raw_file_path):
	"""
	Create SentenceStructures from raw documents and annotate them
	
	:param ann_file_path: Path to directory where annotation documents are located
	:param raw_file_path: Path to directory where raw documents are located
	:return: Dictionary of lists of annotated SentenceStructure objects keyed on document name stripped of extension
	"""
	#create annotation dictionary
	annDict = CreateAnnotationDictionary(ann_file_path)

	#create sentence structure dictionary
	ssDict = CreateSentenceStructures(raw_file_path)

	#Iterate over documents
	for key, value in ssDict.items():
		docAnnotations = annDict[key]
		docSentenceStructures = ssDict[key]

		#Annotate each sentence
		for index, ss in enumerate(docSentenceStructures):
			#Annotations only for this sentence
			annotations = [ann for ann in annDict[key] if ann.line == index + 1]

			#Updated SentenceStructure
			ss = AnnotateSentenceStructure(ss, annotations)
		
	#Return the updated ssDict
	return ssDict

#Author: Evan French
def AnnotateSentenceStructure(ss, annotations):
	"""
	Annotates SentenceStructure object
	
	:param ss: SentenceStructure object
	:param annotions: list of annotations for the sentence
	:return: Annotated SentenceStructure object
	"""

	#Iterate over distinct annotations for a sentence
	for m in annotations:
		for j in range(m.startWord, m.endWord + 2):
			if j == m.startWord:
				ss.originalSentenceArray[j][1] = m.label + ':Start'
			elif j == m.endWord + 1:
				ss.originalSentenceArray[j][1] = m.label + ':End'
			else:
				ss.originalSentenceArray[j][1] = m.label
	return ss

#Author: Evan French
"""
Iterates through all annotation documents in the directory specified and creates a dictionary keyed on file name 
(without extension) with a list Annotation objects as the value
"""
def CreateAnnotationDictionary(annotation_file_path):
	"""
	Create Annotations from raw documents
	
	:param annotation_file_path: Path to directory where annotation documents are located
	:return: Dictionary of lists of Annotation objects keyed on document name stripped of extension
	"""
	
	#Create a dictionary of documents
	docDictionary = {}

	# cd into annotation file directory
	cwd = os.getcwd()
	os.chdir(annotation_file_path)

	#Iterate over documents in the annotation_file_path directory
	for document in os.listdir():

		#Instantiate a list to hold Annotations for each document
		annotationList = []

		#Open the document
		doc = open(document, "r")

		#Iterate over lines in the document
		for line in doc.readlines():

			#Create an Annotation obj
			an = Annotation(line)

			#Add Annotation obj to the list
			annotationList.append(an)        

		#Strip the extension from the file to get the document name
		docName = os.path.splitext(document)[0]

		#Add the AnnotationList to the dictionary
		docDictionary[docName] = annotationList

		#Close the document
		doc.close()
		
	#Return to the original directory
	os.chdir(cwd)

	#Return the dictionary
	return docDictionary
	
#Author: Jeffrey Smith
def CreateSupplementalSentenceStructures(supp_file_path):
	"""
	Create SentenceStructures from supplemental documents
	
	:param supp_file_path: Path to directory where supplemental documents are located
	:return: Dictionary of lists of SentenceStructure objects keyed on document name stripped of extension
	"""

	#Create a dictionary of documents
	docDictionary = {}

	# cd into test file directory
	cwd = os.getcwd()
	os.chdir(supp_file_path)

	#Iterate over documents in the supp_file_path directory
	for document in os.listdir():

		#Instantiate a list to hold a SentenceStructure for each sentence(line) in the document
		docSentenceStructureList = []

		#Open the document
		doc = open(document, "r")
		
		docText = doc.read()
		docTextProcessed = preprocess(docText)
		docTextProcessedSplit = docTextProcessed.splitlines()
		
		doc.close()
		
		doc = open(document, "r")
		
		#Strip the extension from the file to get the document name
		docName = os.path.splitext(document)[0]

		#Iterate over sentences in the document
		counter = 0
		for sentence in doc.readlines():
			#Create a SentenceStructure obj
			ss = SentenceStructure(sentence, docName)
			ss.modifiedSentence = docTextProcessedSplit[counter]

			#Add SentenceStructure obj to the list
			docSentenceStructureList.append(ss)      
			counter += 1

		#Add the SentenceStructureList to the dictionary
		docDictionary[docName] = docSentenceStructureList

		#Close the document
		doc.close()
		
	#Return to original path
	os.chdir(cwd)
	
	#Return the dictionary
	return docDictionary

if __name__ == "__main__":
	main()
