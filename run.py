import sixDOF as sd
import dofNet as dn
import cessnaplane as cessna
import matplotlib.pyplot as plt

def main():
	plane = cessna.cessna()
	simulator = sd.sixDOF(plane)
	simulator.runSim()
	trimstate = simulator.trimFinder(plane.x0, plane.c0)
	print(trimstate)
	plt.show()
	return 0

if __name__=="__main__":
	main()
