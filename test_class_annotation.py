"""
test_class_annotation.py
Scope: Unit test for Annotation class
Authors: Evan French
"""
from class_annotation import Annotation
import unittest

class AnnotationTestClass(unittest.TestCase):
	def test_AnnotationInit(self):
		an = Annotation('c="his home regimen" 111:8 111:10||t="treatment"')
		self.assertEqual(an.concept, "his home regimen")
		self.assertEqual(an.label, "treatment")
		self.assertEqual(an.line, 111)
		self.assertEqual(an.startWord, 8)
		self.assertEqual(an.endWord, 10)

	def test_AnnotationInit_double_quotes(self):
		an = Annotation('c=""leaky valve"" 31:13 31:14||t="problem"')
		self.assertEqual(an.concept, '"leaky valve"')
		self.assertEqual(an.label, "problem")
		self.assertEqual(an.line, 31)
		self.assertEqual(an.startWord, 13)
		self.assertEqual(an.endWord, 14)
		
if __name__ == '__main__':
	unittest.main()
		