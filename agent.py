"""
agent.py
Scope: Defines the Tensorflow Neural Network code used by the module.
Authors: Jeffrey Smith, Bill Cramer, Evan French
"""
import tensorflow as tf
import numpy as np

#Author: Jeffrey Smith
class Agent:
	"""
	Agent represents the neural network interface for Tensorflow that will train our data.
	"""
	def __init__(self, numFeatures, numClasses, maxSentenceLength):
		"""
		Constructor for Agent.
		
		:param numFeatures: The amount of features that will be present in the data.
		:param numClasses: The number of classes that will be present in the final results.
		:return: Nothing.
		:var layerSize: Size of the hidden layers.
		:var maxSentenceLength: The max length of a sentence.
		"""
		self.layerSize = 256
		self.maxSentenceLength = maxSentenceLength
		self.numberOfFeatures = numFeatures
		self.numberOfClasses = numClasses
		
		self.build_network()
		
		self.sess = tf.Session()
		self.sess.run(tf.initializers.global_variables())
	
	def build_network(self):
		"""
		Internal function to build the network of the agent.
		
		:return: Nothing.
		"""
		
		#Initializers
		self.initializer = tf.contrib.layers.variance_scaling_initializer(dtype=tf.float32)
		self.initializerBias = tf.zeros_initializer()

		#Inputs into the network.
		self.input = tf.placeholder(tf.float32, [None, self.maxSentenceLength, self.numberOfFeatures], name='input')
		self.truth = tf.placeholder(tf.int32, [None, self.maxSentenceLength], name='truth') #A vector in the form [BatchSize,SentenceLength]
		self.seqLen = tf.placeholder(tf.int32, [None], name='seqLen')
		
		#LSTM Cells and RNN
		lstmFWCell = tf.nn.rnn_cell.LSTMCell(self.layerSize, forget_bias=1.0, name="ForwardCell", dtype=tf.float32)
		lstmBWCell = tf.nn.rnn_cell.LSTMCell(self.layerSize, forget_bias=1.0, name="BackwardCell", dtype=tf.float32) 
		
		(fwOut, bwOut), l1OutputStates = tf.nn.bidirectional_dynamic_rnn(lstmFWCell, lstmBWCell, inputs = self.input, sequence_length = self.seqLen, dtype=tf.float32)
		
		#Reshape data for Dense layer.
		l1Concat = tf.concat([fwOut,bwOut], axis= -1)
		l1Flat = tf.reshape(l1Concat, [-1,2*self.layerSize])
		
		#Dense Layer and Reshape
		predictionFlat = tf.layers.dense(inputs = l1Flat, units = self.numberOfClasses, activation = None, use_bias = True, bias_initializer = self.initializerBias, kernel_initializer = self.initializer, trainable = True) 
		self.prediction = tf.reshape(predictionFlat, [-1, self.maxSentenceLength, self.numberOfClasses])
				
		#CRF Layer and Log Likelihood Error
		log_likelihood, transition_params = tf.contrib.crf.crf_log_likelihood(self.prediction, self.truth, self.seqLen)

		#Loss and Optimizer
		self.loss = tf.reduce_mean(-log_likelihood)
		
		self.update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
		with tf.control_dependencies(self.update_ops):
			self.optimizer = tf.train.AdamOptimizer(learning_rate=0.01).minimize(self.loss)
			
	def train(self, batchX, batchY, seqLen):
		"""
		Function to train the network.
		
		:param batchX: The data to be fed into the network.
		:param batchY: The labels that the batch will be trained against.
		:param seqLen: The true length of each sentence in the batch.
		:return: loss as float.
		"""
		
		loss, _ = self.sess.run([self.loss, self.optimizer], {self.input: batchX, self.truth: batchY, self.seqLen: seqLen})
		return loss
			
	def eval(self, batchX, batchY, seqLen):
		"""
		Function to evaluate the network.
		
		:param batchX: The data to be fed into the network.
		:param batchY: The labels that the batch will be tested against.
		:param seqLen: The true length of each sentence in the batch.
		:return: Numpy array representing confusion matrix.
		"""
		pred = self.sess.run(self.prediction, {self.input: batchX, self.seqLen: seqLen})
		
		cf = np.zeros((self.numberOfClasses,self.numberOfClasses), dtype=np.int32)
			
		for i in range(0, len(pred)):
			predi = pred[i,0:seqLen[i],:]
			predi_argmax = np.argmax(predi, -1)

			for j in range(0, seqLen[i]):
				myClass = int(batchY[i][j])
				predClass = int(predi_argmax[j])
				cf[predClass, myClass] += 1

		return cf		
		
	def evalWithStructure(self, batchX, batchY, seqLen, k, fileMap, batchMap, dict):
		"""
		Function to evaluate the network in regards to original sentence structure.
		
		:param batchX: The data to be fed into the network.
		:param batchY: The labels that the batch will be tested against.
		:param seqLen: The true length of each sentence in the batch.
		:param k: The current bucket index.
		:param fileMap: Map linking indices to files and sentences.
		:param batchMap: Map linking batches to indices for fileMap.
		:param dict: Dictionary of our sentence structures.
		:return: Numpy array representing confusion matrix.
		"""
		
		pred = self.sess.run(self.prediction, {self.input: batchX, self.seqLen: seqLen})
		
		#Matrix in the form class,true span, partial span, wrong
		cf = np.zeros((self.numberOfClasses,3), dtype=np.int32)
		
		##DEBUG FILE OUT##
		debugFile = open("debug.txt", 'a')
		
		#For each index in k
		for i in range(0, len(pred)):
			predi = pred[i,0:seqLen[i],:]
			predi_argmax = np.argmax(predi, -1)
			
			#Get the original filemap index.
			batchIndex = batchMap[k][i]
			originalIndex = fileMap[batchIndex]
			y = dict[originalIndex[0]][originalIndex[1]]
			y_ = []
			
			#Build the tags in the sentence
			for j in range(0, seqLen[i]):
				predClass = int(predi_argmax[j])
				if predClass == 0:
					y_.append(None)
				elif predClass == 1:
					y_.append("problem")
				elif predClass == 2:
					y_.append("test")
				elif predClass == 3:
					y_.append("treatment")
					
			#Add "END" for safe tagging.
			y_.append(None)
						
			
			#Append start/end tags
			j = 0
			#for j in range(0, len(y_)):
			while j < len(y_):
				if not y_[j] == None and not y_[j] == "":
					cls = y_[j]
					
					y_[j] = y_[j] + ":Start"
					j += 1
					while j < len(y_):
						if not y_[j] == cls:
							if y_[j] == "" or y_[j] == None:
								y_[j] = cls + ":End"
							else:
								j -= 1
							break

						j += 1
				j += 1
						
						
			##DEBUG STRINGS##
			outText = "Text: "
			outTagsTruth = "Truth: "
			outTagsPred = "Pred: "
			
			j_ = 0
			#for j_ in range(0, len(y_)):
			while j_ < (len(y_)-1):
				if y.originalSentenceArray[j_][1] == "" or y.originalSentenceArray[j_][1] == None:
					debugFile.write("Text: " + str(y.originalSentenceArray[j_][0]) +"\n") #DEBUG
					debugFile.write("Truth: None\n") #DEBUG
					debugFile.write("Pred: " + str(y_[j_]) + "\n\n") #DEBUG
					if y_[j_] == "" or y_[j_] == None:
						cf[0,0] += 1
					else:
						cf[0,2] += 1
						
				else:
					cls = ""
					if "problem" in y.originalSentenceArray[j_][1]:
						cls = 1
					elif "test" in y.originalSentenceArray[j_][1]:
						cls = 2
					elif "treatment" in y.originalSentenceArray[j_][1]:
						cls = 3
					else:
						cls = 0
						
					if "Start" in y.originalSentenceArray[j_][1]:
						#Check for same start
						if y_[j_] == y.originalSentenceArray[j_][1]:
							#We have at least a partial start.
							fullSpan = True
							
							#Check the rest
							while not "End" in y.originalSentenceArray[j_][1] and j_ < len(y_)-1:
								outText = outText + y.originalSentenceArray[j_][0] + " " #Debug
								outTagsTruth = outTagsTruth + str(y.originalSentenceArray[j_][1]) + " " #Debug
								outTagsPred = outTagsPred + str(y_[j_]) + " " #Debug
								if not y_[j_] == y.originalSentenceArray[j_][1]:
									fullSpan = False
								j_ += 1
								
							if fullSpan:
								cf[cls,0] += 1
							else:
								cf[cls,1] += 1
							
						else:
							cf[cls,2] += 1
							while not "End" in y.originalSentenceArray[j_][1] and j_ < len(y_)-1:
								outText = outText + y.originalSentenceArray[j_][0] + " " #Debug
								outTagsTruth = outTagsTruth + str(y.originalSentenceArray[j_][1]) + " " #Debug
								outTagsPred = outTagsPred + str(y_[j_]) + " " #Debug
								j_ += 1

						outText = outText + y.originalSentenceArray[j_][0] + " " #Debug
						outTagsTruth = outTagsTruth + str(y.originalSentenceArray[j_][1]) + " " #Debug
						outTagsPred = outTagsPred + str(y_[j_]) + " " #Debug								
						debugFile.write(outText + "\n")
						debugFile.write(outTagsTruth + "\n")
						debugFile.write(outTagsPred + "\n\n")
						outText = "Text: "
						outTagsTruth = "Truth: "
						outTagsPred = "Pred: "
						
					else:
						debugFile.write("Text: " + str(y.originalSentenceArray[j_][0]) +"\n") #DEBUG
						debugFile.write("Truth: " + str(y.originalSentenceArray[j_][1]) +"\n") #DEBUG
						debugFile.write("Pred: " + str(y_[j_]) + "\n\n") #DEBUG
						if y_[j_] == y.originalSentenceArray[j_][1]:
							cf[cls,0] += 1
						else:
							cf[cls,2] += 1
							
				j_ += 1
				
		debugFile.close()
		return cf
		
	def cleanUp(self):
		"""
		Function to free resources of the network and reset the default graph.
		
		:return: Nothing.
		"""
		self.sess.close()
		tf.reset_default_graph()
		
		
