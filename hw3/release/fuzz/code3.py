from pwn import *
import os
import random

dict = {}
flag = []

def update_dict(input):
	r.sendline(input)
	tmp_path = r.recv().decode().split('\n')
	isChange = False
	### load to dict
	for p in tmp_path:
		if p.find('BALSN') != -1:
			if p not in flag:
				flag.append(p)
		else:
			if dict.get(p) is None:
				isChange = True
				dict[p] = input
	return isChange


r = remote("140.112.31.97", 10160)

data = os.urandom(20)
update_dict(data)

### fuzzing
iteration = 10000
threshold = 10
for t in range(iteration):
	### choose path and dimension
	path = str(random.choice(list(dict.keys())))
	dimension = [i for i in range(20)]
	random.shuffle(dimension)
	dimension = dimension[:threshold]
	
	blist = list(dict[path])
	for i in range(threshold):
		blist[dimension[i]] = random.randint(0, 255)
		tmp_data = bytes(blist)

		### try another input
		if update_dict(tmp_data):
			break

print(flag)