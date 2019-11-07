from pwn import *
import base64

r = remote("140.112.31.96", 10151)

r.recv()
r.send('2\n')

res = str(r.recv())
#print(res)
res = res.split('= ')[1].split('\\')[0]
#print(res)
r.send(res+'\n')

### Round 1
res = str(r.recv())
res = res.split('= ')[1].split('\\')[0]
for i in range(1, 26):
	m = ""
	for char in res:
		if char>='a' and char<='z':
			m += chr((ord(char)-ord('a')+i)%26 + ord('a'))
		elif char>='A' and char<='Z':
			m += chr((ord(char)-ord('A')+i)%26 + ord('A'))
		else:
			m += char
	print(m)

ans = input()
r.send(ans+'\n')


### Round 2
res = str(r.recv())
c1 = res.split('= ')[1].split('\\')[0]
m1 = res.split('= ')[2].split('\\')[0]
c1 = [ord(i) for i in c1]
m1 = [ord(i) for i in m1]
tmp_key = ""
for i in range(len(c1)):
	if c1[i]>=ord('a') and c1[i]<=ord('z'):
		tmp_key += chr((c1[i]-m1[i])%26 + ord('a'))
	elif c1[i]>=ord('A') and c1[i]<=ord('Z'):
		tmp_key += chr((c1[i]-m1[i])%26 + ord('A'))
	else:
		tmp_key += chr(c1[i])
key = [0 for _ in range(7)]
count = 0
for i in range(len(tmp_key)):
	if key[i%7]==0:
		if tmp_key[i]>='a' and tmp_key[i]<='z':
			key[i%7] = ord(tmp_key[i])
			count += 1
		elif tmp_key[i]>='A' and tmp_key[i]<='Z':
			key[i%7] = ord(tmp_key[i])
			count += 1
	if count>=7:
		break
#print(key)

c2 = res.split('= ')[3].split('\\')[0]
c2 = [ord(i) for i in c2]
m2 = ""

for i in range(len(c2)):
	if c2[i]>=ord('a') and c2[i]<=ord('z'):
		m2 += chr((c2[i]-key[i%7]+26)%26 + ord('a'))
	elif c2[i]>=ord('A') and c2[i]<=ord('Z'):
		m2 += chr((c2[i]-key[i%7]+26)%26 + ord('A'))
	else:
		m2 += chr(c2[i])
#print(m2)
r.send(m2+'\n')


### Round 3
res = str(r.recv())
c1 = res.split('= ')[1].split('\\')[0]
m1 = res.split('= ')[2].split('\\')[0]
c2 = res.split('= ')[3].split('\\')[0]
key = 0

## encryption
for k in range(2, len(m1)-1):
	rail = [['.' for i in range(len(m1))] for j in range(k)]
	dir_down = False
	row, col = 0, 0
	for i in range(len(m1)):
		# change dir if necessary
		if row == 0:
			dir_down = True
		elif row == k-1:
			dir_down = False
		# fill	
		rail[row][col] = m1[i]
		col += 1
		# find next row
		if dir_down:
			row += 1
		else:
			row -= 1
	# find cipher
	cipher = []
	for i in range(k):
		for j in range(len(m1)):
			if rail[i][j] != '.':
				cipher.append(rail[i][j])
	cipher = "".join(cipher)
	if cipher==c1:
		key = k
		break

## decryption
rail = [['.' for i in range(len(c2))] for j in range(key)]
dir_down = False
row, col = 0, 0
for i in range(len(c2)):
	if row == 0:
		dir_down = True
	elif row == key-1:
		dir_down = False
	# place the marker
	rail[row][col] = '*'
	col += 1
	# find next row
	if dir_down:
		row += 1
	else:
		row -= 1
# fill the rail matrix
index = 0
for i in range(key):
	for j in range(len(c2)):
		if rail[i][j]=='*' and index<len(c2):
			rail[i][j] = c2[index]
			index += 1
# read the matrix in zig-zag manner to construct the resultant text
m2 = []
row, col = 0, 0
for i in range(len(c2)):
	# change dir if necessary
	if row == 0:
		dir_down = True
	elif row == key-1:
		dir_down = False
	# place the marker
	if rail[row][col] != '*':
		m2.append(rail[row][col])
		col += 1
	# find next row
	if dir_down:
		row += 1
	else:
		row -= 1
m2 = "".join(m2)
r.send(m2+'\n')


### Round 4
res = str(r.recv())
c1 = res.split('= ')[1].split('\\')[0]
m1 = str(base64.b64decode(c1))[2:-1]
r.send(m1+'\n')

print(str(r.recv()))