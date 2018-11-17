"""
test.py
Scope: Performs unit testing on the system to ensure proper functionality.
Authors: Jeffrey Smith, Bill Cramer, Evan French
"""
import classes, run
import unittest, os

#Author: Jeffrey Smith
class ClassesTestClass(unittest.TestCase):
	def test_SentenceStructureInitTest(self):
		x = classes.SentenceStructure("I am a test string")
		self.assertEqual(x.originalSentence, "I am a test string")
		self.assertEqual(len(x.originalSentenceArray), 6)
		self.assertEqual(x.originalSentenceArray[0][0], "I")
		self.assertEqual(x.originalSentenceArray[1][0], "am")
		self.assertEqual(x.originalSentenceArray[2][0], "a")
		self.assertEqual(x.originalSentenceArray[3][0], "test")
		self.assertEqual(x.originalSentenceArray[4][0], "string")
		self.assertEqual(x.originalSentenceArray[5][0], "END")

#Author: Evan French
class AnnotationTestClass(unittest.TestCase):
	def test_AnnotationInit(self):
		an = classes.Annotation('c="his home regimen" 111:8 111:10||t="treatment"')
		self.assertEqual(an.concept, "his home regimen")
		self.assertEqual(an.label, "treatment")
		self.assertEqual(an.line, 111)
		self.assertEqual(an.startWord, 8)
		self.assertEqual(an.endWord, 10)

	def test_AnnotationInit_double_quotes(self):
		an = classes.Annotation('c=""leaky valve"" 31:13 31:14||t="problem"')
		self.assertEqual(an.concept, '"leaky valve"')
		self.assertEqual(an.label, "problem")
		self.assertEqual(an.line, 31)
		self.assertEqual(an.startWord, 13)
		self.assertEqual(an.endWord, 14)

#Author: Evan French
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

		result = run.CreateAnnotationDictionary('.')
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

#Author: Evan French
class TestSentenceStructures(unittest.TestCase):
	def test_CreateSentenceStructures(self):
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

		result = run.CreateSentenceStructures('.')
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
	
	def test_AnnotateSentenceStructure(self):
		ss = classes.SentenceStructure("Pt took his medicine")
		an = classes.Annotation('c="his medicine" 1:2 1:3||t="treatment"')
		annotations = [an]

		modified_ss = run.AnnotateSentenceStructure(ss, annotations)
		self.assertEqual(modified_ss.originalSentenceArray[0], ['Pt', ''])
		self.assertEqual(modified_ss.originalSentenceArray[1], ['took', ''])
		self.assertEqual(modified_ss.originalSentenceArray[2], ['his', 'treatment:Start'])
		self.assertEqual(modified_ss.originalSentenceArray[3], ['medicine', 'treatment'])
		self.assertEqual(modified_ss.originalSentenceArray[4], ['END', 'treatment:End'])

	def test_CreateAnnotatedSentenceStructures(self):
		ann_file_path = os.getcwd() + 'unit_test_ann_docs'
		raw_file_path = os.getcwd() + 'unit_test_raw_docs'
		
		#Make a directory for annotation docs if it doesn't already exist
		if not os.path.exists(ann_file_path):
			os.mkdir(ann_file_path)
			
		# cd into ann_file_path directory
		os.chdir(ann_file_path)
		
		#Create annotation document
		f = open('test.con','w+')
		f.write('c="his medicine" 1:2 1:3||t="treatment"')
		f.close()

		#Make a directory for raw docs if it doesn't already exist
		if not os.path.exists(raw_file_path):
			os.mkdir(raw_file_path)
			
		# cd into raw_file_path directory
		os.chdir(raw_file_path)
		
		#Create raw document
		f = open('test.txt','w+')
		f.write('Pt took his medicine')
		f.close()

		# cd back into main
		os.chdir('..')

		result = run.CreateAnnotatedSentenceStructures(ann_file_path, raw_file_path)
		modified_ss = result['test'][0]

		#Tests
		self.assertEqual(modified_ss.originalSentenceArray[0], ['Pt', ''])
		self.assertEqual(modified_ss.originalSentenceArray[1], ['took', ''])
		self.assertEqual(modified_ss.originalSentenceArray[2], ['his', 'treatment:Start'])
		self.assertEqual(modified_ss.originalSentenceArray[3], ['medicine', 'treatment'])
		self.assertEqual(modified_ss.originalSentenceArray[4], ['END', 'treatment:End'])
		
		#Cleanup
		os.remove(raw_file_path + '/test.txt')
		os.remove(ann_file_path + '/test.con')
		os.rmdir(raw_file_path)
		os.rmdir(ann_file_path)
	
#Author: Jeffrey Smith
class TestPreprocessing(unittest.TestCase):
	def test_PreProcessing(self):
		test_dict = {}
		test_list = []
		test_list.append(classes.SentenceStructure("3/13/2006 12:00:00 AM"))
		test_list.append(classes.SentenceStructure("03/19/06 AT 01:00 PM"))
		test_list.append(classes.SentenceStructure("Take with 8 oz of plain water SPIRIVA ( TIOTROPIUM ) 18"))
		test_list.append(classes.SentenceStructure("Dr. Pump 3/25/05 1:30 ,"))
		test_list.append(classes.SentenceStructure("1. TIKWELD , WILLAIDE V. , M.D. ( QT296 ) 03/19/06 10:53 AM"))
		
		test_list[0].generateModifiedSentenceArray()
		test_list[1].generateModifiedSentenceArray()
		test_list[2].generateModifiedSentenceArray()
		test_list[3].generateModifiedSentenceArray()
		test_list[4].generateModifiedSentenceArray()
		
		test_dict["0"] = test_list
		
		#Tests
		self.assertEqual(len(test_dict["0"][0].originalSentenceArray), len(test_dict["0"][0].modifiedSentenceArray))
		self.assertEqual(len(test_dict["0"][1].originalSentenceArray), len(test_dict["0"][1].modifiedSentenceArray))
		self.assertEqual(len(test_dict["0"][2].originalSentenceArray), len(test_dict["0"][2].modifiedSentenceArray))
		self.assertEqual(len(test_dict["0"][3].originalSentenceArray), len(test_dict["0"][3].modifiedSentenceArray))
		self.assertEqual(len(test_dict["0"][4].originalSentenceArray), len(test_dict["0"][4].modifiedSentenceArray))
		
		self.assertEqual(test_dict["0"][0].modifiedSentenceArray[0][0], 'date')
		self.assertEqual(test_dict["0"][0].modifiedSentenceArray[1][0], "date")
		self.assertEqual(test_dict["0"][0].modifiedSentenceArray[2][0], "am")
		
		self.assertEqual(test_dict["0"][1].modifiedSentenceArray[0][0], "date")
		self.assertEqual(test_dict["0"][1].modifiedSentenceArray[1][0], "at")
		self.assertEqual(test_dict["0"][1].modifiedSentenceArray[2][0], "date")
		self.assertEqual(test_dict["0"][1].modifiedSentenceArray[3][0], "pm")
		
		self.assertEqual(test_dict["0"][2].modifiedSentenceArray[0][0], "take")
		self.assertEqual(test_dict["0"][2].modifiedSentenceArray[1][0], "with")
		self.assertEqual(test_dict["0"][2].modifiedSentenceArray[2][0], "num")
		self.assertEqual(test_dict["0"][2].modifiedSentenceArray[3][0], "oz")
		self.assertEqual(test_dict["0"][2].modifiedSentenceArray[4][0], "of")
		self.assertEqual(test_dict["0"][2].modifiedSentenceArray[5][0], "plain")
		self.assertEqual(test_dict["0"][2].modifiedSentenceArray[6][0], "water")
		self.assertEqual(test_dict["0"][2].modifiedSentenceArray[7][0], "spiriva")
		self.assertEqual(test_dict["0"][2].modifiedSentenceArray[8][0], "(")
		self.assertEqual(test_dict["0"][2].modifiedSentenceArray[9][0], "tiotropium")
		self.assertEqual(test_dict["0"][2].modifiedSentenceArray[10][0], ")")
		self.assertEqual(test_dict["0"][2].modifiedSentenceArray[11][0], "num")
		
		self.assertEqual(test_dict["0"][3].modifiedSentenceArray[0][0], "dr.")
		self.assertEqual(test_dict["0"][3].modifiedSentenceArray[1][0], "pump")
		self.assertEqual(test_dict["0"][3].modifiedSentenceArray[2][0], "date")
		self.assertEqual(test_dict["0"][3].modifiedSentenceArray[3][0], "date")
		self.assertEqual(test_dict["0"][3].modifiedSentenceArray[4][0], ",")
		
		self.assertEqual(test_dict["0"][4].modifiedSentenceArray[0][0], "1.")
		self.assertEqual(test_dict["0"][4].modifiedSentenceArray[1][0], "tikweld")
		self.assertEqual(test_dict["0"][4].modifiedSentenceArray[2][0], ",")
		self.assertEqual(test_dict["0"][4].modifiedSentenceArray[3][0], "willaide")
		self.assertEqual(test_dict["0"][4].modifiedSentenceArray[4][0], "v.")
		self.assertEqual(test_dict["0"][4].modifiedSentenceArray[5][0], "m.d.")
		self.assertEqual(test_dict["0"][4].modifiedSentenceArray[6][0], "(")
		self.assertEqual(test_dict["0"][4].modifiedSentenceArray[7][0], "qt296")
		self.assertEqual(test_dict["0"][4].modifiedSentenceArray[8][0], ")")
		self.assertEqual(test_dict["0"][4].modifiedSentenceArray[9][0], "date")
		self.assertEqual(test_dict["0"][4].modifiedSentenceArray[10][0], "date")
		self.assertEqual(test_dict["0"][4].modifiedSentenceArray[11][0], "am")
		
if __name__ == '__main__':
	unittest.main()
		
