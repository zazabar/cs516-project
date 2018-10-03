"""
class_annotation.py
Scope: Class representing an annotation
Authors: Evan French
"""

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
		
		segments = inString.split('"')
		self.concept = segments[1]
		indexes = segments[2].strip('||t=').strip().split()
		self.label = segments[3]

		start = indexes[0].split(':')
		end = indexes[1].split(':')

		self.line = start[0]
		self.startWord = start[1]
		self.endWord = end[1]
		