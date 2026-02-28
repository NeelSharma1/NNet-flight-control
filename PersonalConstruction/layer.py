"""DOES NOT HAVE COMPATIBILITY WITH VECTOR INPUTS YET"""

from neuron import *
import functionpuller as fp


class Layer:
	def __init__(self, size, bias=True, activation="leakyrelu"):
		self.size = size
		self.neurons = [Neuron(activation) for i in range(size)]
		if bias:
			self.neurons.append(Neuron(activation, bias=True))
		self.bias = bias
		self.aFunc = activation

	def getSize(self):
		return self.size

	def hasBias(self):
		return self.bias

	def getAFunc(self):
		return self.aFunc

	def applyActivation(self, inputArray):
		return [fp.activation(i, self.aFunc) for i in inputArray]