# THIS FILE ASSUMES METRIC UNITS, NOT IMPERIAL

import numpy as np
from scipy.optimize import root
import scipy.integrate as intg
import calcSupport as cs
import dofNet
import matplotlib.pyplot as plt
import torch.optim as opt
import torch.nn as nn

INDEXED_VARIABLES = ["u", "v", "w", "p", "q", "r", "phi", "theta", "psi", "x", "y", "z", "aileron", "elevator",
					 "rudder", "throttle"]


class sixDOF:

	def __init__(self, plane, unitSystem="METRIC"):
		self.plane = plane
		self.EOMorLinear = True
		self.A, self.B = np.array([]), np.array([])
		self.x0 = np.array([])
		self.xdot0 = np.array([])
		self.c0 = np.array([])
		self.units = cs.calcSupport(unitSystem)
		self.NNet = None
		self.setupExisting(plane)

	def setupExisting(self, plane):
		for attr in plane.__dict__:
			if self.__dict__.__contains__(attr):
				self.__dict__[attr] = plane.__dict__[attr]

	def fEOM(self, t, xvec, control):
		Vtotal = np.sqrt(np.sum([i ** 2 for i in xvec[:3]]))
		u, v, w, p, q, r, phi, theta, psi, x, y, z = xvec
		q_bar = 0.5 * self.units.density(z) * Vtotal ** 2
		alpha = np.arctan2(w, u)
		beta = np.arcsin(v / Vtotal)

		allvector = np.array([1, alpha, beta, q_bar, *xvec, *control])
		CD, Cy, CL, Cl, Cm, Cn = [np.dot(allvector, i) for i in self.plane.EOMArray]

		Cx = self.plane.throttleCoeff * control[self.plane.throttleIndex] - CD
		Cz = -CL

		forces = np.array([[i * q_bar * self.plane.S for i in (Cx, Cy, Cz)]]).T
		moments = np.array(
			[[x * self.plane.S * (self.plane.c if i == 1 else self.plane.b) for i, x in enumerate((Cl, Cm, Cn))]]
		).T  # ASSUMED TO BE ABOUT THE CG!!

		# applying equations of motion
		# linear accelerations
		g = self.units.g(z)
		du_dt = np.float64(-q * w + v * r - g * np.sin(theta) + forces[0] / self.plane.mass)
		dv_dt = np.float64(-r * u + p * w + g * np.cos(theta) * np.sin(phi) + forces[1] / self.plane.mass)
		dw_dt = np.float64(-p * v + q * u + g * np.cos(theta) * np.cos(phi) + forces[2] / self.plane.mass)
		# angular accelerations, weird due to coupling
		omega = np.array([[p],
						  [q],
						  [r]])
		h = self.plane.inertiaMatrix @ omega
		omega_dot = np.linalg.inv(self.plane.inertiaMatrix) @ (moments - np.cross(omega.T, h.T).T)
		# inertial velocity
		dx_dt = u * np.cos(theta) * np.cos(psi) + v * (
					np.sin(phi) * np.sin(theta) * np.cos(psi) - np.cos(phi) * np.sin(psi)) + w * (
						np.cos(phi) * np.sin(theta) * np.cos(psi) + np.sin(phi) * np.sin(psi))
		dy_dt = u * np.cos(theta) * np.sin(psi) + v * (
					np.sin(phi) * np.sin(theta) * np.sin(psi) + np.cos(phi) * np.cos(psi)) + w * (
						np.cos(phi) * np.sin(theta) * np.sin(psi) - np.sin(phi) * np.cos(psi))
		dz_dt = -(u * np.sin(theta) - v * np.sin(phi) * np.cos(theta) - w * np.cos(phi) * np.cos(theta))
		# euler angles
		dphi_dt = p + q * np.sin(phi) * np.tan(theta) + r * np.cos(phi) * np.tan(theta)
		dtheta_dt = q * np.cos(phi) - r * np.sin(phi)
		dpsi_dt = (q * np.sin(phi) + r * np.cos(phi)) / np.cos(theta)
		# dp_dt, dq_dt, dr_dt = omega_dot.T[0]

		return np.array([du_dt, dv_dt, dw_dt, *omega_dot.T[0], dphi_dt, dtheta_dt, dpsi_dt, dx_dt, dy_dt, dz_dt])

	def fIVP(self, t, x, target):
		currstate = [x[i] + self.x0[i] for i in range(len(x))]
		control = np.array([self.nnetRun(currstate, target), ]).T
		x = np.array([x, ]).T
		print(f"{t:.4f}")
		# print(A, "\n\n", x, "\n\n", B, "\n\n", control)
		# print(delxdot := (A @ x + B @ control).T[0])
		return (self.A @ x + self.B @ control).T[0] + self.xdot0

	def nnetRun(self, state, target):
		return self.NNet.forward([*state, *target])

	def getLabelCondensed(self, i):
		match i:
			case 0:
				return "Velocities (m/s)"
			case 1:
				return "Angular Velocities (deg/s)"
			case 2:
				return "Euler Angles (deg)"
			case 3:
				return "Distance from Earth (m)"
		return None

	def getLabel(self, i):
		i += 1
		match i:
			case 1:
				return "U (m/s)"
			case 2:
				return "V (m/s)"
			case 3:
				return "W (m/s)"
			case 4:
				return "P (deg/s)"
			case 5:
				return "Q (deg/s)"
			case 6:
				return "R (deg/s)"
			case 7:
				return "Roll (deg)"
			case 8:
				return "Pitch (deg)"
			case 9:
				return "Yaw (deg)"
			case 10:
				return "X from Earth (m)"
			case 11:
				return "Y from Earth (m)"
			case 12:
				return "Z from Earth (m)"
		return None

	def plotResults(self, time, states):

		def charInc(c):
			return chr(ord(c) + 1)

		# if debug:
		#     file.close()
		# unpack states
		u = states[0]
		v = states[1]
		w = states[2]
		p = states[3]
		q = states[4]
		r = states[5]
		x = states[6]
		y = states[7]
		z = states[8]
		phi = states[9]
		theta = states[10]
		psi = states[11]
		# for i in u:
		# 	print(i)
		save_array = np.array(
			[time, u, v, w, p, q, r, x, y, z, np.rad2deg(phi), np.rad2deg(theta), np.rad2deg(psi)]).T
		header = ["Time [s]", "U [m/s]", "V [m/s]", "W [m/s]", "P [m/s]", "Q [m/s]", "R [m/s]",
				  "X [m]", "Y [m]", "Z [m]", "Phi [deg]", "Theta [deg]", "Psi [deg]"]
		header = ",".join(header)
		np.savetxt(fname="states.csv", X=save_array, delimiter=",", header=header)
		# 3d plotting
		mosaic = \
			"""
			AB
			CC
			DD
			EE
			"""
		fig, axis = plt.subplot_mosaic(mosaic, constrained_layout=True)
		fig.set_size_inches(10, 10)
		plot_letter = 'A'
		axis[plot_letter].plot(time, states[0], label=self.getLabel(0))
		axis[plot_letter].set_xlabel('Time (s)')
		axis[plot_letter].set_ylabel('U Velocity (m/s)')
		axis[plot_letter].legend(loc="upper right")
		plot_letter = charInc(plot_letter)
		axis[plot_letter].plot(time, states[1], label=self.getLabel(1))
		axis[plot_letter].plot(time, states[2], label=self.getLabel(2))
		axis[plot_letter].set_xlabel('Time (s)')
		axis[plot_letter].set_ylabel('V and W Velocity (m/s)')
		axis[plot_letter].legend(loc="upper right")
		for i in range(1, 4):
			plot_letter = charInc(plot_letter)
			toDeg = False
			if i < 3:
				toDeg = True
			axis[plot_letter].plot(time, np.rad2deg(states[i * 3]) if toDeg else states[i * 3],
								   label=self.getLabel(i * 3))
			axis[plot_letter].plot(time, np.rad2deg(states[i * 3 + 1]) if toDeg else states[i * 3 + 1],
								   label=self.getLabel(i * 3 + 1))
			axis[plot_letter].plot(time, np.rad2deg(states[i * 3 + 2]) if toDeg else states[i * 3 + 2],
								   label=self.getLabel(i * 3 + 2))
			if toDeg:
				axis[plot_letter].set_ylim((-30, 30))
			axis[plot_letter].set_ylabel(self.getLabelCondensed(i))
			axis[plot_letter].set_xlabel("Time (s)")
			axis[plot_letter].legend(loc="upper right")
		plt.rcParams['axes.formatter.useoffset'] = False
		plt.show()
		return 0

	def pertSingle(self, index, pertValue, XorC):
		if XorC:
			x = list(self.x0.copy())
			x[index] += pertValue
			return self.fEOM(0, x, self.c0)
		c = list(self.c0.copy())
		c[index] += pertValue
		return self.fEOM(0, self.x0, c)

	def linearizer(self, perturbationConstant=1e-12):
		"""MODIFY CODE EXPRESSLY FOR THE NEW FORMAT PROVIDED"""

		A = []
		for i in range(len(self.x0)):
			arr = []
			for j in perturbationConstant, -perturbationConstant:
				arr.append(self.pertSingle(i, j, True) - self.xdot0)
			A.append((arr[0] - arr[1]) / (2 * perturbationConstant))
		A = np.array(A).T
		B = []
		for i in range(len(self.x0), len(INDEXED_VARIABLES)):
			arr = []
			for j in perturbationConstant, -perturbationConstant:
				arr.append(self.pertSingle(i, j, False) - self.xdot0)
			B.append((arr[0] - arr[1]) / (2 * perturbationConstant))
		B = np.array(B).T

		self.A = A
		self.B = B
		return A, B

	def setEOMorLinear(self, EOMorLinear):
		self.EOMorLinear = EOMorLinear
		if EOMorLinear:
			print("Please ensure you have properly set a linearization point, including a control and state vector.")

	def matrixTest(self):
		A, B = self.linearizer()
		print(A, "\n\n", B)

		for i in range(len(A)):
			print(INDEXED_VARIABLES[i] + ":", A.T[i])
		for i in range(len(A.T), len(A.T) + len(B.T)):
			print(INDEXED_VARIABLES[i] + ":", B.T[i - len(A)])

	def trimFinder(self, stateGuess, controlGuess, trimWith=(0, 12, 13, 14, 15)):
		def f(t, s):
			c = controlGuess.copy()
			state = stateGuess.copy()
			for i in range(len(trimWith)):
				if trimWith[i] >= len(stateGuess):
					c[trimWith[i] - len(stateGuess)] = s[i]
				else:
					state[trimWith[i]] = s[i]
			return self.fEOM(t, stateGuess, c)[:6] ** 2

		actualguess = []
		for i in trimWith:
			if i < len(stateGuess):
				actualguess.append(stateGuess[i])
			else:
				actualguess.append(controlGuess[i - len(stateGuess)])
		actualguess = np.array(actualguess)
		sol = root(f, actualguess, args=stateGuess)
		if sol.message == "The solution converged.":
			trimstate = stateGuess.copy()
			for i in range(len(sol.x)):
				trimstate[trimWith[i]] = sol.x[i]
			self.x0 = np.array(trimstate)
			self.c0 = np.array(controlGuess)
			self.xdot0 = np.array(self.fEOM(0, self.x0, self.c0))
			return trimstate
		else:
			print("The solution failed to converge, try another set of trim0s.")
			return None

	def runSim(self, tf=(0, 10), plot=True):
		xdot = self.xdot0.copy()
		solvedata = intg.solve_ivp(self.fEOM if self.EOMorLinear else self.fIVP, tf, self.x0, "RK45", args=(self.c0,))
		print(solvedata)
		if plot:
			self.plotResults(solvedata.t, solvedata.y)
		return solvedata.t, solvedata.y
	# FIX THIS SOON!
	def establishNNet(self, sequence):
		nnet = dofNet.Net(sequence)
		optimizer = opt.SGD(nnet.parameters(), 0.1)
		for i in range(num := 30000):
			optimizer.zero_grad()
			criterion = nn.MSELoss()
			loss = criterion(nnet.forward(1), 1)
			loss.backward()
			optimizer.step()
			if not i % 100:
				print("Epoch:", i, "Loss:", loss)
		print(f"\n\nXOR OUTPUT ({num} epochs)\n")
		print("X:", 1)
		print("y:", 1)
		print("predictions:", preds := nnet.forward(1))
		print("MSE Loss:", criterion(preds, 1))



