import afuncs
import lossfuncs
import inspect
import lossfuncderivs
import afuncderivs


def activation(x, function, deriv=False):
	for i in (inspect.getmembers(afuncderivs, inspect.isfunction) if deriv else inspect.getmembers(afuncs, inspect.isfunction)):
		if (function + "_deriv" if deriv else function) == i[0]:
			return i[1](x)
	print("Activation function not found!")
	return None

def loss(y_true, y_pred, function, deriv=False):
	for i in (inspect.getmembers(lossfuncderivs, inspect.isfunction) if deriv else inspect.getmembers(lossfuncs, inspect.isfunction)):
		if (function + "_deriv" if deriv else function) == i[0]:
			return i[1](y_true, y_pred)
	print("Loss function not found!")
	return None
