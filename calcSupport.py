# THIS FILE IS EVENTUALLY MEANT TO STANDARDIZE UNIT CALCULATIONS AND CONVERSIONS FOR CONSISTENCY ACROSS THE PROGRAM
from ctypes import cdll, c_double


class calcSupport():
	def __init__(self, units):
		if units == "METRIC":
			self.qc = cdll.LoadLibrary("./qcmetric.dll")
		else:
			self.qc = cdll.LoadLibrary("./qcimperial.dll")
		self.qc.temp.argtypes = (c_double,)
		self.qc.temp.restype = c_double
		self.qc.pressure.argtypes = (c_double,)
		self.qc.pressure.restype = c_double
		self.qc.density.argtypes = (c_double,)
		self.qc.density.restype = c_double
		self.qc.sos.argtypes = (c_double,)
		self.qc.sos.restype = c_double
		self.qc.currA.argtypes = (c_double,)
		self.qc.currA.restype = c_double
		self.qc.g.argtypes = (c_double,)
		self.qc.g.restype = c_double

	def g(self, h):
		return self.qc.g(h)  # m/s^2 for metric, ft/s^2 for imperial

	def pressure(self, h):
		return self.qc.pressure(h)  # kPa for metric, psf for imperial

	def density(self, h):
		return self.qc.density(h)  # kg/m^3 for metric, lbf/ft^3 for imperial

	def temp(self, h):
		return self.qc.temp(h)  # Kelvin for metric, Rankine for imperial

	def M(self, h):
		return self.qc.sos(h)  # m/s for metric, ft/s for imperial

	def tempRate(self, h):
		return self.qc.currA(h)  # K/m for metric, deg R/ft for imperial

# cs = calcSupport("METRIC")
# print(cs.density(91.44))
