import numpy as np


class Neuron:
	def __init__(self, aFunc, bias=False):
		self.bias = bias
		self.aFunc = aFunc

	def isBias(self):
		return self.bias

	def needsLoss(self):
		return False

	def getActivation(self):
		return self.aFunc

	def hasVectorAFunc(self):
		return None
