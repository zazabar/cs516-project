"""
function_SentenceStructures.py
Scope: Defines functions using SentenceStructure objects
Authors: Evan French
"""

# Import packages
import os
import function_Annotations
import function_SentenceStructures
from classes import SentenceStructure
from class_annotation import Annotation

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
	for document in os.listdir(raw_file_path):

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

def CreateAnnotatedSentenceStructures(ann_file_path, raw_file_path):
	"""
	Create SentenceStructures from raw documents and annotate them
	
	:param ann_file_path: Path to directory where annotation documents are located
	:param raw_file_path: Path to directory where raw documents are located
	:return: Dictionary of lists of annotated SentenceStructure objects keyed on document name stripped of extension
	"""
	#create annotation dictionary
	annDict = function_Annotations.CreateAnnotationDictionary(ann_file_path)

	#create sentence structure dictionary
	ssDict = function_SentenceStructures.CreateSentenceStructures(raw_file_path)

	#Iterate over documents
	for key, value in ssDict.items():
		docAnnotations = annDict[key]
		docSentenceStructures = ssDict[key]

		#Annotate each sentence
		for index, ss in enumerate(docSentenceStructures):
			#Annotations only for this sentence
			annotations = [ann for ann in annDict[key] if ann.line == index + 1]

			#Updated SentenceStructure
			ss = function_SentenceStructures.AnnotateSentenceStructure(ss, annotations)

	#Return the updated ssDict
	return ssDict

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