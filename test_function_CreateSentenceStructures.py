"""
test_function_CreateSentenceStructures.py
Scope: Performs unit testing on the function CreateSentenceStructures
Authors: Evan French
"""
from function_CreateSentenceStructures import CreateSentenceStructures
import unittest
import os

class ConstructSentenceStructures(unittest.TestCase):
	def test_ConstructSentenceStructures(self):
		directory = 'unit_test_docs'
		
		#Make a directory for unit test documents if it doesn't already exist
		if not os.path.exists(directory):
			os.mkdir(directory)
			
		# cd into test directory
		os.chdir(directory)
		
		#Create first test document
		f = open('test_doc_1.txt','w+')
		f.write("Test doc one\n")
		f.write("second line")
		f.close()
		
		#Create second test document
		f = open('test_doc_2.txt','w+')
		f.write("Small\n")
		f.write("test")
		f.close()
		
		result = CreateSentenceStructures('.')
		result_1 = result['test_doc_1']
		result_2 = result['test_doc_2']

		#Tests
		self.assertEqual(2, len(result))
		
		self.assertEqual(result_1[0].originalSentence, "Test doc one\n")
		self.assertEqual(len(result_1[0].originalSentenceArray), 4)
		self.assertEqual(result_1[0].originalSentenceArray[0][0], "Test")
		self.assertEqual(result_1[0].originalSentenceArray[1][0], "doc")
		self.assertEqual(result_1[0].originalSentenceArray[2][0], "one")
		self.assertEqual(result_1[0].originalSentenceArray[3][0], "END")
		
		self.assertEqual(result_1[1].originalSentence, "second line")
		self.assertEqual(len(result_1[1].originalSentenceArray), 3)
		self.assertEqual(result_1[1].originalSentenceArray[0][0], "second")
		self.assertEqual(result_1[1].originalSentenceArray[1][0], "line")
		self.assertEqual(result_1[1].originalSentenceArray[2][0], "END")
		
		self.assertEqual(result_2[0].originalSentence, "Small\n")
		self.assertEqual(len(result_2[0].originalSentenceArray), 2)
		self.assertEqual(result_2[0].originalSentenceArray[0][0], "Small")
		self.assertEqual(result_2[0].originalSentenceArray[1][0], "END")
		
		self.assertEqual(result_2[1].originalSentence, "test")
		self.assertEqual(len(result_2[1].originalSentenceArray), 2)
		self.assertEqual(result_2[1].originalSentenceArray[0][0], "test")
		self.assertEqual(result_2[1].originalSentenceArray[1][0], "END")
		
		#Cleanup
		os.remove('test_doc_1.txt')
		os.remove('test_doc_2.txt')
		os.chdir('..')
		os.rmdir(directory)
		
if __name__ == '__main__':
	unittest.main()
		