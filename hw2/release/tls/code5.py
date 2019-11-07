from Crypto.PublicKey import RSA
import gmpy2


n = int('009aede5abaa81316ca5d08b1b31a6b899562e1319dd9fe18bedf2269c505816700336f5d2de3c45ddd07d41cb16540f005ccb34d1df549aac30aa8f4d972f09460ef113d433c281be26240087b2eec16a491a74048cd91efa158435db8cdff8dd37a7b8e723ac13f8851eab4b96841d84ea72047e5eec559bba50e44f42250e8efc5dbbf6862248101d0a86889f2c67f3e1f729357150817bac214fb25a0b7a36b787ff34e51d64c1a57e00728886069442b53ba7cea4a9fdc24c05b50776473556a0cd58ff920b82b0e9e8d0de8070ada88737dac9237abee30bdf6e132813cf323f56e4108ad737a311883b8d7ee90673713aad3a28632ed9d02a2428eae0fd', 16)
e = 65537


def fermatFactor(n):
	a = gmpy2.iroot(gmpy2.mpz(n), 2)[0] + 1
	b2 = a**2 - n
	while gmpy2.is_square(b2) is False:
		a += 1
		b2 = a**2 - n
	return (a - gmpy2.iroot(b2, 2)[0], a + gmpy2.iroot(b2, 2)[0])

p, q = fermatFactor(n)
priv = RSA.construct((n, e, int(gmpy2.invert(e, (p-1)*(q-1)))))
open('private.pem', 'wb').write(priv.exportKey('PEM'))
