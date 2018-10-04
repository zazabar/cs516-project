"""
function_SentenceStructures.py
Scope: Defines functions using SentenceStructure objects
Authors: Evan French
"""

# Import packages
import os
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
		
	#Return the dictionary
	return docDictionary

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