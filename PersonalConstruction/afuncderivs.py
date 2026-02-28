"""This file encompasses many of the possible activation functions' derivatives present to work with, according to
several online sources, though it may be somewhat incomplete. There are further functions listed on Wikipedia to be
implemented. Ensure you have properly implemented the original activation function in afuncs.py.
"""
from afuncs import *


# FLOAT/INT INPUT FUNCTIONS

# Sigmoid
def sigmoid_deriv(x):
	"""Derivative of the function 1 / (1 + e^-x), which is sigmoid(x) * (1 - sigmoid(x))"""
	return sigmoid(x) * (1 - sigmoid(x))


# ReLU
def relu_deriv(x):
	"""Derivative of the function max(0, x), which is 1 if x > 0 and 0 otherwise"""
	return 1 * (x > 0)


# Leaky ReLU

def leakyrelu_deriv(x):
	"""Derivative of the function 0.05x for x <= 0 and x for x > 0, which is 0.05 if x <= 0 and 1 otherwise"""
	return 0.05 if x <= 0 else 1


# tanh

def tanh_deriv(x):
	"""Derivative of the function (e^x - e^-x) / (e^x + e^-x), so 1 - tanhfunc(x)^2"""
	return 1 - tanh(x) ** 2


# Linear

def linear_deriv(x):
	"""Derivative of the function f(x) = x, the most basic activation function: linear, thus its derivative returns 1"""
	return 1


# ELU

def elu_deriv(x):
	""" Similar to ReLU. Derivative of the function that follows x for x >= 0, 0.05(e^x - 1) for others,
	giving 1 if x >= 0 or 0.05e^x otherwise"""
	return 1 if x >= 0 else 0.05 * np.exp(x)


# Swish, created by Google Researchers

def swish_deriv(x):
	"""Created by Google Researchers, preserves limited negatives. Derivative of x / (1 - e^-x), so
	1 / (1 - e^x) + xe^x / (1 - e^x)^2"""
	return 1 / (1 - np.exp(x)) + x * np.exp(x) / (1 - np.exp(x)) ** 2


# VECTOR INPUT FUNCTIONS


# Softmax

def softmax_deriv(x):
	"""(MEANT ONLY FOR VECTOR INPUTS) The softmax function follows the function e^x / (sum of all e^x values), its
	derivative is a Jacobian due to its nature as a vector function. View the function itself in afuncderivs.py to see
	the logic for the derivative."""
	orig = softmax(x)
	out = []
	for i in x:
		out.append([])
		for j in x:
			out[i][j] = orig[i] * (1 - orig[j] if i == j else orig[j])
	return out
