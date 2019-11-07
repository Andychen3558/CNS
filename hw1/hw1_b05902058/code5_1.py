from pwn import *
import random
import time
import base64

if __name__=="__main__":
	r = remote("140.112.31.96", 10152)
	c = str(r.recv())[2:-3]
	tmp = list(base64.b64decode(c))
	#print(tmp)
	seed = int(time.time())
	while True:
		random.seed(seed)
		flag = ""
		for i in tmp:
			flag += chr(i ^ random.randint(0, 255))
		if flag.find("BALSN") != -1:
			print(flag)
			break
		seed -= 1