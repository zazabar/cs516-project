"""
agent.py
Scope: Defines the Tensorflow Neural Network code used by the module.
Authors: Jeffrey Smith, Bill Cramer, Evan French
"""
import tensorflow as tf

class Agent:
	"""
	Agent represents the neural network interface for Tensorflow that will train our data.
	"""
	def __init__(self, numFeatures, numClasses):
		"""
		Constructor for Agent.
		
		:param numFeatures: The amount of features that will be present in the data.
		:param numClasses: The number of classes that will be present in the final results.
		:return: Nothing.
		:var layerSize: Size of the hidden layers.
		:var maxSentenceLength: The max length of a sentence.
		"""
		self.layerSize = 256
		self.maxSentenceLength = 20
		self.numberOfFeatures = numFeatures
		self.numberOfClasses = numClasses
		
		self.build_network()
	
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
		self.truth = tf.placeholder(tf.int32, [None, None], name='truth') #A vector in the form [BatchSize,SentenceLength]
		self.seqLen = tf.placeholder(tf.int32, [None], name='seqLen')
		
		#LSTM Cells and RNN
		lstmFWCell = tf.nn.rnn_cell.LSTMCell(self.layerSize, forget_bias=1.0, name="ForwardCell", dtype=tf.float32)
		lstmBWCell = tf.nn.rnn_cell.LSTMCell(self.layerSize, forget_bias=1.0, name="BackwardCell", dtype=tf.float32) 
		
		(fwOut, bwOut), l1OutputStates = tf.nn.bidirectional_dynamic_rnn(lstmFWCell, lstmBWCell, inputs = self.input, sequence_length = self.seqLen, dtype=tf.float32)
		
		#Reshape data for Dense layer.
		l1Concat = tf.concat([fwOut,bwOut], axis= -1)
		l1ShapeInfo = tf.shape(l1Concat)[1]
		l1Flat = tf.reshape(l1Concat, [-1, 2*self.layerSize])
		
		#Dense Layer and Reshape
		predictionFlat = tf.layers.dense(inputs = l1Flat, units = self.numberOfClasses, activation = None, use_bias = True, bias_initializer = self.initializerBias, kernel_initializer = self.initializer, trainable = True) 
		self.prediction = tf.reshape(predictionFlat, [-1, l1ShapeInfo, self.numberOfClasses])
		
		#CRF Layer and Log Likelihood Error
		log_likelihood, transition_params = tf.contrib.crf.crf_log_likelihood(self.prediction, self.truth, self.seqLen)

		#Loss and Optimizer
		self.loss = tf.reduce_mean(-log_likelihood)
		
		self.update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
		with tf.control_dependencies(self.update_ops):
			self.optimizer = tf.train.AdamOptimizer().minimize(self.loss)
			
	def train(self, batchX, batchY, seqLen):
		"""
		Function to train the network.
		
		:param batchX: The data to be fed into the network.
		:param batchY: The labels that the batch will be trained against.
		:param seqLen: The true length of each sentence in the batch.
		:return: Nothing.
		"""
		for i in range(0, 10):
			loss, _ = self.sess.run([self.loss, self.optimizer], {self.input: batchX, self.truth: batchY, self.seqLen: seqLen})
			print(loss)

		
		
		