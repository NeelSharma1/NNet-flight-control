"""This file encompasses many of the possible activation functions present to work with, according to several online
sources, though it may be somewhat incomplete. There are further functions listed on Wikipedia to be implemented.
Ensure to implement the derivative of the function in the file afuncderivs.py
"""
import numpy as np


# FLOAT/INT INPUT FUNCTIONS

# Sigmoid
def sigmoid(x):
	"""Follows the function 1 / (1 + e^-x)"""
	return 1 / (1 + np.exp(-x))


# Rectified Linear Unit (ReLU)
def relu(x):
	"""Follows the function max(0, x)"""
	return max(0, x)


# Leaky Rectified Linear Unit (Leaky ReLU)
def leakyrelu(x):
	"""A better version of ReLU that prevents negative values from creating useless neurons in the network by giving
	some slight weight to them. Follows the rule 0.05x for x < 0 and x for x >= 0"""
	return 0.05 * x if x <= 0 else x


# Hyperbolic tan (tanh)

def tanh(x):
	"""Follows the function (e^x - e^-x) / (e^x + e^-x)"""
	return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))


# Linear

def linear(x):
	"""Follows the function f(x) = x, the most basic activation function, linear."""
	return x


# ELU (Exponential Linear Unit)

def elu(x):
	"""Similar to Leaky ReLU, but acting exponentially to limit negative factors. x for x >= 0, 0.05(e^x - 1) for others"""
	return x if x >= 0 else 0.05 * (np.exp(x) - 1)


# Swish, created by Google Researchers

def swish(x):
	"""Created by Google Researchers, eliminates the effects of highly negative values while still preserving some
	negative action. Follows x / (1 - e^-x)"""
	return x / (1 - np.exp(-x))


# VECTOR INPUT FUNCTIONS


# Softmax (ONLY USE FOR VECTOR INPUTS)

def softmax(x):
	"""(MEANT ONLY FOR VECTOR INPUTS) The softmax function follows the function e^x / (sum of all e^x values)"""
	s = sum(sum(np.exp(x)))
	return [np.exp(i) / s for i in x]