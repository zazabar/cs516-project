"""
classes.py
Scope: Defines the major classes used by the module.
Authors: Jeffrey Smith, Bill Cramer, Evan French
"""

class SentenceStructure:
	"""
	SentenceStructure represents a sentence taken from an input file. It splits the string based on whitespace and adds an END tag.
	"""
	def __init__(self, inString):
		"""
		Constructor for SentenceStructure.
		
		:param inString: The string that this object will represent.
		:return: Nothing.
		:var originalSentence: Copy of the original string.
		:var originalSentenceArray: An array of [string,string] tuples. The first string is a token, and the second is a holder for tags.
		"""
		self.originalSentence = inString
		self.originalSentenceArray = []
		
		#Split the string by whitespace and add it to the array.
		for x in inString.split():
			token = [x,""]
			self.originalSentenceArray.append(token)
			
		#Add an end tag to the end of the array.
		self.originalSentenceArray.append(["END",""])
		