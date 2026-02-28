"""File containing the usable loss functions in this package, similar to afuncs.py for the activation functions. Note
that this is quite incomplete."""
import numpy as np


# MSE (Mean Squared Error)
def mse(y_true, y_pred):
	# print(np.mean((y_true - y_pred) ** 2))
	return np.mean((y_true - y_pred) ** 2)