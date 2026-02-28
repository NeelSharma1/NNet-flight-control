import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as opt


class Net(nn.Module):

	def __init__(self, *args, **kwargs):
		# 1 input image channel, 6 output channels, 5x5 square convolution
		# kernel
		super().__init__(*args, **kwargs)
		self.model = nn.Sequential(
			nn.Linear(2, 20),
			nn.LeakyReLU(0.1),
			nn.Linear(20, 1),
			nn.LeakyReLU(0.1)
		)

	def forward(self, input):
		return F.sigmoid(self.model(input))


net = Net()
print(net)

# OR problem (input and expected output)
X = torch.tensor([[0, 0],
				  [0, 1],
				  [1, 0],
				  [1, 1]]).to(torch.float32)

y = torch.tensor([[0], [1], [1], [0]]).to(torch.float32)  # OR outputs

# Create a network with 2 input neurons, 4 neurons in the first hidden layer,
# 3 neurons in the second hidden layer, and 1 output neuron
nnet = Net()
optimizer = opt.SGD(nnet.parameters(), 0.2)
for i in range(num := 30000):
	optimizer.zero_grad()
	criterion = nn.MSELoss()
	loss = criterion(nnet.forward(X), y)
	loss.backward()
	optimizer.step()
	if not i % 100:
		print("Epoch:", i, "Loss:", loss)
print(f"\n\nXOR OUTPUT ({num} epochs)\n")
print("X:", X)
print("y:", y)
print("predictions:", preds := nnet.forward(X))
print("MSE Loss:", criterion(preds, y))

# Test the trained model
# print("Predictions after training:")
# print(nn.predict(X))
