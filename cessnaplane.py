import numpy as np

import plane


class cessna(plane.plane):
	def __init__(self):
		super().__init__()
		# 1, alpha, beta, q_bar, *x(u, v, w, p, q, r, phi, theta, psi, x, y, z), *control (ail, ele, rud, thrust)
		# CD = 0.027 + 0.121 * alpha
		# Cy = -.393 * beta + -.075 * p + 0.214 * r + 0.187 * dr
		# CL = 0.307 + 4.41 * alpha + 3.9 * q + .43 * de
		# Cl = -0.0923 * beta + -.484 * p + .0798 * r + 0.229 * da + 0.0147 * dr
		# Cm = .04 + -.613 * alpha + -12.4 * q + -1.122 * de
		# Cn = 0.0587 * beta + -.0278 * p + -.0937 * r + -.0216 * da + -.0645 * dr
		self.EOMArray[0, :2] = 0.027, 0.121
		self.EOMArray[1, self.EOMArrayReference["beta"]] = -0.393
		self.EOMArray[1, self.EOMArrayReference["p"]] = -0.075
		self.EOMArray[1, self.EOMArrayReference["r"]] = 0.214
		self.EOMArray[1, self.EOMArrayReference["rudder"]] = 0.187
		self.EOMArray[2, :2] = 0.307, 4.41
		self.EOMArray[2, self.EOMArrayReference["q"]] = 3.9
		self.EOMArray[2, self.EOMArrayReference["elevator"]] = 0.43
		self.EOMArray[3, self.EOMArrayReference["beta"]] = -0.0923
		self.EOMArray[3, self.EOMArrayReference["p"]] = -0.484
		self.EOMArray[3, self.EOMArrayReference["r"]] = 0.0798
		self.EOMArray[3, self.EOMArrayReference["aileron"]] = 0.229
		self.EOMArray[3, self.EOMArrayReference["rudder"]] = 0.0147
		self.EOMArray[4, :2] = 0.04, -0.613
		self.EOMArray[4, self.EOMArrayReference["q"]] = -12.4
		self.EOMArray[4, self.EOMArrayReference["elevator"]] = -1.122
		self.EOMArray[3, self.EOMArrayReference["beta"]] = 0.0587
		self.EOMArray[5, self.EOMArrayReference["p"]] = -0.0278
		self.EOMArray[5, self.EOMArrayReference["r"]] = -0.0937
		self.EOMArray[5, self.EOMArrayReference["aileron"]] = -0.0216
		self.EOMArray[5, self.EOMArrayReference["rudder"]] = -0.0645

		self.throttleCoeff = 0.032

		self.S = 16.1651  # wing area [m2]
		self.c = 1.494  # mean geometric chord [m]
		self.b = 10.973  # wingspan [m]
		self.V_ref = 67.08648  # velocity [m/s]

		inertias = [1285.315, 1824.9310, 2666.893]
		for i in range(len(self.inertiaMatrix)):
			self.inertiaMatrix[i, i] =  inertias[i]

		self.mass = 1202.2  # kg

		self.x0 = [65] + [0] * 10 + [1524]
		self.xdot0 = [0] * 12
		self.c0 = [0] * 4

