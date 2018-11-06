"""
run.py
Scope: The entrance point for our program.
Authors: Jeffrey Smith, Bill Cramer, Evan French
"""
import sys, getopt, os, subprocess, re
import agent
from classes import SentenceStructure, Annotation
from random import sample
import numpy as np

np.set_printoptions(threshold=np.nan)

#CONSTANTS
MAX_SENTENCE_LENGTH = 205

#Author: Jeffrey Smith
def main():
	"""
	Main function of the application. Call -h or --help for command line inputs.
	"""
	dict_ = CreateAnnotatedSentenceStructures("./subtest_an", "./subtest_in")
	
	AddModifiedSentenceArray(dict_)

	bx, by, bs, mapping = GenerateEmbeddings(dict_)
	
	confusionMatrixList = trainNetwork(bx,by,bs,mapping,dict_,buckets=10,epochs=20)
	

#Author: Jeffrey Smith
def trainNetwork(batchX, batchY, seqLen, fileMap, dict, buckets=10, epochs=20):
	"""
	Trains a neural network model. If one is not given, creates one.
	"""		
	#Setup Buckets for 10 fold cross validation
	batchX, batchY, seqLen, batchMap = kFoldBucketGenerator(batchX, batchY, seqLen, buckets)
	
	#batchMap and fileMap are used later for evaluation.
	
	#Create and train the model 10x for 10FoldCrossValidation
	confusionMatrixList = []
	for k in range(0, buckets):
		myAgent = agent.Agent(200,4,MAX_SENTENCE_LENGTH)
		
		#Train for 20 epochs.
		for j in range(0, epochs):
		
			loss = 0
			
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
		
		cf_ = myAgent.evalWithStructure(batchX[k], batchY[k], seqLen[k], k, fileMap, batchMap, dict)
		file = open("./outCFS", 'a')
		outstr = np.array2string(cf_)
		file.write(outstr)
		file.write("\n")
		file.close()
					
		myAgent.cleanUp()

	return confusionMatrixList
	

#Author: Jeffrey Smith
def kFoldBucketGenerator(batchX, batchY, seqLen, k):
	"""
	Takes a batch and shuffles it, then creates 10 subbatches of each.
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
def GenerateEmbeddings(d):

	if not os.path.isdir('./_arff'):
		os.mkdir('_arff')

	#Launch perl pipe
	args = ['perl', './w2v.pl']
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
				#print("START SENTENCE")
				tArray = np.zeros((MAX_SENTENCE_LENGTH,200), dtype=np.float32)
				cArray = np.zeros((MAX_SENTENCE_LENGTH), dtype=np.float32)

				"""
				print("\n Original Sentence: " + str(x.originalSentence))
				print("Debug1")
				for q in x.originalSentenceArray:
					print(q[0])				
				print("Debug2")
				for q in x.modifiedSentenceArray:
					print(q[0])
				print("DebugDone")	
				"""		
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
							f.write(("0.0 " * 200) + str(class_) + "\n")
							break
						elif len(t) > 2:
							#Temp Generate Embeddings
							tSplit = t.split();
							tArray[z][0:200] = tSplit[1:201]
							cArray[z] = class_
							
							f.write(t + " " + str(class_) + "\n")
							break
						else:
							print(t)
				
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

	return embeddingList, classList, seqList, mapping
	
#Author: Jeffrey Smith
def AddModifiedSentenceArray(d):

	if not os.path.isdir('./_tin'):
		os.mkdir('_tin')
	if not os.path.isdir('./_tout'):
		os.mkdir('_tout')
	
	#Get each list of SentenceStructures from map.
	v = d.values()

	for x in v:
		#Create a temp file.
		f = open('_tin/o.txt','w+')

		#Write every sentence to a file.
		for y in x:
			tSentence = y.originalSentence
			regTemp = re.compile(r'\b([\d]+-?)+\b')
			regTemp2 = re.compile(r'\b([\d]+)\b')
			outSentence = regTemp.sub('NUM', tSentence)
			outSentence = regTemp2.sub('NUM', outSentence)
			f.write(outSentence)

		f.close()
		
		r = subprocess.run(["python3", "preprocess.py", "-i", "./_tin", "-o", "./_tout"], stdout=None, stderr=subprocess.DEVNULL) 
		if r.returncode != 0:
			print("Program did not exit correctly.")

		
		f = open('_tout/o.txt', 'r+')
		
		#Read every sentence back to modified sentence array.
		for y in x:
			y.generateModifiedSentenceArray(f.readline())

		f.close()
		os.remove('_tin/o.txt')
		os.remove('_tout/o.txt')
	
	os.rmdir('_tin')
	os.rmdir('_tout')


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

		#Iterate over sentences in the document
		for sentence in doc.readlines():

			#Create a SentenceStructure obj
			ss = SentenceStructure(sentence)

			#Add SentenceStructure obj to the list
			docSentenceStructureList.append(ss)        

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

if __name__ == "__main__":
	main()
