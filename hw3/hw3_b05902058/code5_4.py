import sys
import numpy as np
import random
import matplotlib.pyplot as plt

def bfs(graph, start, end):
	queue = []
	queue.append([start])
	while queue:
		path = queue.pop(0)
		node = path[-1]
		if node == end:
			return path
		for i in graph.get(node, []):
			new_path = list(path)
			new_path.append(i)
			queue.append(new_path)


for m in range(3, 6):
	isolatedASes = []
	for ASNumber in range(100, 450, 50):
		count = 0
		for i in range(1, 4):
			graph = {}
			isolated = []
			with open("topologies/" + str(ASNumber) + "-" + str(m) + "-" + str(i) + ".brite", 'r') as f:
				edges = f.read().split('Edges:')[1].split(')')[1].split('\n')
				for line in edges:
					line = line.split('\t')
					if len(line) == 1:
						continue
					src, dst = line[1], line[2]
					# print(src, dst)
					if src not in graph:
						graph[src] = [dst]
					else:
						graph[src].append(dst)
					if dst not in graph:
						graph[dst] = [src]
					else:
						graph[dst].append(src)
			start = 2
			if ASNumber == 100:
				end = 99
			else:
				end = 100
			shortestPath = bfs(graph, str(start), str(end))

			for AS in shortestPath:
				for neighbor in graph[AS]:
					if neighbor not in isolated:
						isolated.append(neighbor)
			for AS in shortestPath:
				if AS in isolated:
					isolated.remove(AS)
			count += len(isolated)
		isolatedASes.append(count/3)

	### plot
	plt.axis([100, 400, 10, 150])
	x = np.linspace(100, 400, 7)
	plt.plot(x, isolatedASes, label=m)
plt.legend(loc='upper left')
plt.show()

