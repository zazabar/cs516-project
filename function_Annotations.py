"""
function_Annotations.py
Scope: Defines functions related to Annotations
Authors: Evan French
"""

# Import packages
import os
from class_annotation import Annotation

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
	os.chdir(annotation_file_path)

	#Iterate over documents in the annotation_file_path directory
	for document in os.listdir(annotation_file_path):

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
		
	#Return the dictionary
	return docDictionary
