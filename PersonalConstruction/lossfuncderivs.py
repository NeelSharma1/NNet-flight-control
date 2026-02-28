"""File containing the derivatives of all usable loss functions in this package, similar to afuncs.py for the activation
functions. Note that this is quite incomplete."""
from lossfuncs import *


# MSE
def mse_deriv(y_true, y_pred):
	return 2 * (y_pred - y_true) / y_true.size
