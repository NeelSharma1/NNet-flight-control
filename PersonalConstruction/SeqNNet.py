from functionpuller import *
from layer import *


class SequentialNeuralNetwork:
	def __init__(self, layer_sizes, lossfunc="mse"):
		"""
		layer_sizes: List of integers, where each integer represents the size of a layer.
		Example: [2, 4, 3, 1] means 2 input neurons, 4 hidden neurons in the first hidden layer, 3 in the second hidden
		layer, and 1 output neuron.
		"""
		self.lfunc = lossfunc
		self.num_layers = len(layer_sizes)
		self.NNet = [Layer(layer_sizes[i], (False if i == 0 or i == self.num_layers - 1 else True)) for i in range(self.num_layers)]
		self.weights = [np.random.standard_normal((self.NNet[i + 1].getSize(), self.NNet[i].getSize())).T for i in range(self.num_layers - 1)]
		# print(self.weights)
		self.bias = [np.zeros((self.NNet[i].getSize(), )) if self.NNet[i].hasBias() else [] for i in range(self.num_layers)]
		# print(self.bias)

	def forward(self, X):
		"""
		Perform a forward pass through the network.
		"""
		intermediates = [X]
		preActs = [X]
		layernum = 1
		# print("forward weights", self.weights)
		for i in self.weights:
			# print("inters", intermediates[-1])
			# print("weights", i)
			inputArray = np.dot(intermediates[-1], i)
			# print("iArr", inputArray)
			# print("bias", self.bias[layernum])
			if self.NNet[layernum].hasBias():
				inputArray += np.array([self.bias[layernum]])
			# print("iArr", inputArray)
			preActs.append(inputArray)
			intermediates.append(self.NNet[layernum].applyActivation(inputArray))

			layernum += 1
		return intermediates[-1], preActs


	def backward(self, preActs, y, learning_rate):
		"""
		Perform backpropagation and update weights and biases.
		"""
		y_pred = self.unpack(activation(preActs[-1], self.NNet[-1].getAFunc()))
		y = self.unpack(y)
		lval = loss(y, y_pred, self.lfunc, True)
		# print(preActs)
		layernum = self.num_layers - 2
		while layernum > 0:
			# print(activation(preActs[layernum], self.NNet[layernum].getAFunc(), True))
			layerloss = (np.dot(lval, self.weights[layernum].T) * activation(preActs[layernum], self.NNet[layernum].getAFunc(), True))[0]
			# print("LLoss", layerloss)
			# print("bias", self.bias[layernum])
			if self.NNet[layernum].hasBias():
				self.bias[layernum] -= learning_rate * layerloss
			# print("updated bias", self.bias[layernum])
			# print("LL x preActs", layerloss * preActs[layernum])
			# print("Alltogether", learning_rate * layerloss * preActs[layernum])
			# print("weights", self.weights[layernum])
			self.weights[layernum] = (self.weights[layernum].T - learning_rate * layerloss * preActs[layernum]).T
			# print("Updated Weights", self.weights[layernum])
			lval = layerloss
			layernum -= 1
		# print(lval)
		# print(self.bias)

	def train(self, X, y, epochs, learning_rate):
		"""
		Train the neural network using Stochastic Gradient Descent (SGD).
		Now we process each example (stochastically) and update weights.
		"""
		# print(X[0])
		for epoch in range(epochs):
			# Shuffle the data to ensure we get a different order for each epoch
			p = np.random.permutation(X.shape[0])
			X_shuffled = X[p]
			y_shuffled = y[p]

			# Iterate over each training example
			for i in range(X.shape[0]):
				# Take one sample at a time (stochastic gradient descent)
				xi = X_shuffled[i:i + 1]  # single sample
				yi = y_shuffled[i:i + 1]  # corresponding label
				# print(xi, y)
				# Forward pass
				f = self.forward(xi)
				preActs = f[1]
				# print(f[0])

				# Backward pass and weight update
				self.backward(preActs, yi, learning_rate)

			# Optionally, print loss for every epoch
			if epoch % 100 == 0:
				l = 0
				for i in X:
					l += loss(y, self.forward(np.array([i]))[0], "mse")
				print(f"Epoch {epoch}, Loss: {l / len(X)}")

	def predict(self, X):
		"""
		Predict the output for new data.
		"""
		for i in X:
			print(str(i) + ":", self.unpack(self.forward(np.array([i]))[0]))


	def unpack(self, X, vector=False):
		lastLayer = self.NNet[-1]
		if lastLayer.getSize() == 1:
			return X[-1][0]


# XOR problem (input and expected output)
X = np.array([[0, 0],
			  [0, 1],
			  [1, 0],
			  [1, 1]])

y = np.array([[0], [1], [1], [0]])  # XOR outputs

# Create a network with 2 input neurons, 4 neurons in the first hidden layer,
# 3 neurons in the second hidden layer, and 1 output neuron
nn = SequentialNeuralNetwork(layer_sizes=[2, 8, 1])

# Train the neural network
nn.train(X, y, epochs=10000, learning_rate=0.01)

# Test the trained model
print("Predictions after training:")
print(nn.predict(X))
