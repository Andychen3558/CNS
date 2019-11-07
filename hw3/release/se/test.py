from pwn import *

r = remote("140.112.31.97", 10162)
print(r.recv())

print(len('2b59e59e-0c25-421c-96d1-4670f6baee01'))