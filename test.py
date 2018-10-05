"""
test.py
Scope: Performs unit testing on the system to ensure proper functionality.
Authors: Jeffrey Smith, Bill Cramer, Evan French
"""
import classes
import unittest

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
		
if __name__ == '__main__':
	unittest.main()
		