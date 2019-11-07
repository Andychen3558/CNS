from pwn import *
import os
from base64 import b64encode, b64decode

from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Cipher import AES

import binascii

BLOCK_SIZE = 16
KEY_SIZE = 32
NONCE_SIZE = 32

def getRandom(n):
	val = os.urandom(n)
	return val

def encrypt(msg, iv, key):
	msg = pad(msg, BLOCK_SIZE)
	aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
	ciphertext = aes.encrypt(msg)
	return b64encode(ciphertext)

def decrypt(msg, iv, key):
	aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
	msg = b64decode(msg)
	plaintext = aes.decrypt(msg)
	plaintext = unpad(plaintext, BLOCK_SIZE)
	return bytes(plaintext)


r = remote("140.112.31.97", 10158)
IV_AB = r.recvuntil('\n').decode().strip().split(': ')[1].split('\n')[0]
IV_AB = b64decode(IV_AB)


### initial_auth
r.recv()
r.send('1\n')
r.recvuntil('> ')

Nx = getRandom(NONCE_SIZE)
r.send('A||' + str(b64encode(Nx), 'utf-8') + '\n')
b_to_server = r.recv().decode().strip()
Nb = b_to_server.split('||')[1]
Nb = b64decode(Nb)

m2 = b_to_server.split('||')[2] #{A, Nx, Tb}K_BS
m1 = str(encrypt(Nb, IV_AB, Nx), 'utf-8')

server_to_a = r.recvuntil('> ').decode().strip()
msg1 = server_to_a.split('\n')[1].split(': ')[1].strip()

r.send(m1 + '||' + m2 + '\n')
flag = r.recv().decode().strip().split(': ')[1]
flag = decrypt(flag[2:-1], IV_AB, Nx).decode()
print(flag)


### subsequent_auth
r.recv()
r.send('2\n')
r.recvuntil('> ')

Nx_1 = getRandom(NONCE_SIZE)
r.send(str(b64encode(Nx_1), 'utf-8') + '||' + msg1 + '\n')
Nb_1 = r.recv().decode().split(': ')[1].strip()
r.recvuntil('> ')

## New session
r2 = remote("140.112.31.97", 10158)
IV_AB = r2.recvuntil('\n').decode().strip().split(': ')[1].split('\n')[0]
IV_AB = b64decode(IV_AB)
r2.recv()
r2.send('2\n')
r2.recvuntil('> ')

r2.send(Nb_1 + '||' + msg1 + '\n')
msg2 = r2.recvuntil('> ').decode().split('\n')[1].split(': ')[1].strip()

r.send(msg2 + '\n')
r.recv()
print(r.recvuntil('\n').decode())
