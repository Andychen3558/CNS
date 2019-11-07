from pwn import *
from functools import reduce
import gmpy2

def CRT(items):
	N = reduce(lambda x, y: x * y, (i[1] for i in items))
	result = 0
	for a, n in items:
		m = N // n
		d, r, s = gmpy2.gcdext(n, m)
		result += a * s * m
	return result % N, N

if __name__=="__main__":
	N = []
	c = []
	for _ in range(3):
		r = remote("140.112.31.96", 10155)

		e = int(r.recvline().strip().decode().split('= ')[1])
		N .append(int(r.recvline().strip().decode().split('= ')[1]))
		c.append(int(r.recvline().strip().decode().split('= ')[1]))

	data = zip(c, N)
	x, n = CRT(list(data))
	result = gmpy2.iroot(gmpy2.mpz(x), e)
	flag = result[0].digits(16)
	print(bytes.fromhex(flag).decode('ascii'))