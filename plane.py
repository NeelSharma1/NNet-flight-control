# NEEDS SUPPORT FOR MUTIPLE THROTTLE INSTANCES

import numpy as np


class plane():
	def __init__(self):
		self.EOMArrayReference = {x: i for i, x in enumerate((1, "alpha", "beta", "q_bar", "u", "v", "w", "p", "q", "r",
															 "phi", "theta", "psi", "x", "y", "z", "aileron", "elevator"
															 , "rudder", "throttle"))}
		self.V_ref = 0
		self.EOMArray = np.zeros((6, 20))
		self.throttleCoeff = 0
		self.throttleIndex = 3
		self.S = 0
		self.c = 0
		self.b = 0
		self.mass = 0
		self.inertiaMatrix = np.zeros((3, 3))

	def setVal(self, var, value):
		if var in vars(self):
			self.var = value
		else:
			print("Value was not properly set, variable does not exist!")
