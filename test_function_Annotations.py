"""
test_function_Annotations.py
Scope: Performs unit testing on functions related to Annotations
Authors: Evan French
"""
import function_Annotations
import unittest
import os

class CreateAnnotationDictionary(unittest.TestCase):
	def test_CreateAnnotationDictionary(self):
		self.assertEqual(1,1)
		directory = 'unit_test_docs'
		
		#Make a directory for unit test documents if it doesn't already exist
		if not os.path.exists(directory):
			os.mkdir(directory)
			
		# cd into test directory
		os.chdir(directory)
		
		#Create first test document
		f = open('test_doc_1.con','w+')
		f.write('c="his home regimen" 111:8 111:10||t="treatment"\n')
		f.write('c="cad/chf" 111:1 111:1||t="problem"')
		f.close()

		result = function_Annotations.CreateAnnotationDictionary('.')
		result_1 = result['test_doc_1']
		ann_1 = result_1[0]

		#Tests
		self.assertEqual(2, len(result_1))
		self.assertEqual(ann_1.concept, "his home regimen")
		self.assertEqual(ann_1.label, "treatment")
		self.assertEqual(ann_1.line, 111)
		self.assertEqual(ann_1.startWord, 8)
		self.assertEqual(ann_1.endWord, 10)

		#Cleanup
		os.remove('test_doc_1.con')
		os.chdir('..')
		os.rmdir(directory)
		
if __name__ == '__main__':
	unittest.main()
		