import torch.nn as nn
# import torch.nn.functional as F


class Net(nn.Module):
	def __init__(self, buildSequence, *args, **kwargs):
		# 1 input image channel, 6 output channels, 5x5 square convolution
		# kernel
		super().__init__(*args, **kwargs)
		self.model = nn.Sequential()
		for i in buildSequence:
			self.model.append(getattr(nn, i[0])(*i[1:]))

	def forward(self, input):
		return self.model(input)
