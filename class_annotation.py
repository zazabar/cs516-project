"""
class_annotation.py
Scope: Class representing an annotation
Authors: Evan French
"""

#Import packages
import re

class Annotation:
	"""
	Annotation represents a line from the annotation file.
	"""
	def __init__(self, inString):
		"""
		Constructor for Annotation.
		
		:param inString: The string that this object will represent.
		:return: Nothing.
		:var concept: String representing concept (i.e. "the sickness").
		:var label: Classification label (i.e. "problem").
		:var line: Line number on which the concept appears.
		:var startWord: Index of first word in the concept.
		:var endWord: Index of the word after the concept ends.
		"""
		
		#Clean up inString into segments we can use
		parse = re.sub(r'c="', '', inString)
		concept = re.sub(r'" \d+:\d+.*$', '', parse)
		after_concept = re.sub(r'c=".*" ', '', inString)
		segments = after_concept.replace(':', ' ').replace('||t=', ' ').replace('"', '').split()

		#Define Annotation properties
		self.concept = concept		
		self.line = segments[0]
		self.startWord = segments[1]
		self.endWord = segments[3]
		self.label = segments[4]
		