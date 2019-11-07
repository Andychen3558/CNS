import sys
import numpy as np
import random
import matplotlib.pyplot as plt

edgeNumbers = {}
for m in range(3, 6):
	edgeNumbers[str(m)] = {}
	for ASNumber in range(100, 450, 50):
		with open("topologies/" + str(ASNumber) + "-" + str(m) + "-1.brite", 'r') as f:
			tmp = int(f.readline().split(' ')[4])
			edgeNumbers[str(m)][str(ASNumber)] = tmp


plt.axis([100, 400, 100, 2000])
for m in range(3, 6):
	x = np.linspace(100, 400, 7)
	y = []
	for ASNumber in range(100, 450, 50):
		y.append(edgeNumbers[str(m)][str(ASNumber)])
		# print(m, ASNumber, edgeNumbers[str(m)][str(ASNumber)])
	plt.plot(x, y, label=m)
plt.legend(loc='upper left')
plt.show()
