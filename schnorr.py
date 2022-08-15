# Schnorr signature built using:
# Elliptic Curve Cryptography using the BitCoin curve, SECG secp256k1
#  This version uses the X,Y,Z "Jacobi coordinates" representation, for speed
#  Dr. Orion Lawlor, lawlor@alaska.edu, 2015-03-25 (Public Domain)

import tools
import pickle
from math import log, pi
from copy import copy
from time import time # timing
from hashlib import sha256
from secrets import randbelow as rand_sec #for private and public key generation

#from fractions import gcd # Greatest Common Denominator
#edited to import from math as gcd was found there

from math import gcd


from random import SystemRandom # cryptographic random byte generator
rand=SystemRandom() # create strong random number generator

# Convert a string with hex digits, colons, and whitespace to a long integer
def hex2int(hexString):
	return int("".join(hexString.replace(":","").split()),16)

# Half the extended Euclidean algorithm:
#    Computes   gcd(a,b) = a*x + b*y  
#    Returns only gcd, x (not y)
# From http://rosettacode.org/wiki/Modular_inverse#Python
def half_extended_gcd(aa, bb):
	lastrem, rem = abs(aa), abs(bb)
	x, lastx = 0, 1
	while rem:
		lastrem, (quotient, rem) = rem, divmod(lastrem, rem)
		x, lastx = lastx - quotient*x, x
	return lastrem, lastx 

# Modular inverse: compute the multiplicative inverse i of a mod m:
#     i*a = a*i = 1 mod m
def modular_inverse(a, m):
	g, x = half_extended_gcd(a, m)
	if g != 1:
		raise ValueError
	return x % m


# An elliptic curve has these fields:
#   p: the prime used to mod all coordinates
#   a: linear part of curve: y^2 = x^3 + ax + b
#   b: constant part of curve
#   G: a curve point (G.x,G.y) used as a "generator"
#   n: the order of the generator
class ECcurve:
	def __init__(self):
		return

	# Prime field multiplication: return a*b mod p
	def field_mul(self,a,b):        
		return (a*b)%self.p

	# Prime field division: return num/den mod p
	def field_div(self,num,den):
		inverse_den=modular_inverse(den%self.p,self.p)
		return self.field_mul(num%self.p,inverse_den)

	# Prime field exponentiation: raise num to power mod p
	def field_exp(self,num,power):
		return pow(num%self.p,power,self.p)

	# Return the special identity point
	#   We pick x=p, y=0
	def identity(self):
		return ECpoint(self,self.p,0,1)

	# Return true if point Q lies on our curve
	def touches(self,Q):
		x=Q.get_x()
		y=Q.get_y()
		y2=(y*y)%self.p
		x3ab=(self.field_mul((x*x)%self.p+self.a,x)+self.b)%self.p
		return y2==(x3ab)%self.p

	# Return the slope of the tangent of this curve at point Q
	def tangent(self,Q):
		return self.field_div(Q.x*Q.x*3+self.a,Q.y*2)

	# Return a doubled version of this elliptic curve point
	#  Closely follows Gueron & Krasnov 2013 figure 2
	def double(self,Q):
		if (Q.x==self.p): # doubling the identity
			return Q
		S=(4*Q.x*Q.y*Q.y)%self.p
		Z2=Q.z*Q.z
		Z4=(Z2*Z2)%self.p
		M=(3*Q.x*Q.x+self.a*Z4)
		x=(M*M-2*S)%self.p
		Y2=Q.y*Q.y
		y=(M*(S-x)-8*Y2*Y2)%self.p
		z=(2*Q.y*Q.z)%self.p
		return ECpoint(self,x,y,z)

	# Return the "sum" of these elliptic curve points
	#  Closely follows Gueron & Krasnov 2013 figure 2
	def add(self,Q1,Q2):
		# Identity special cases
		if (Q1.x==self.p): # Q1 is identity
			return Q2
		if (Q2.x==self.p): # Q2 is identity
			return Q1
		Q1z2=Q1.z*Q1.z
		Q2z2=Q2.z*Q2.z
		xs1=(Q1.x*Q2z2)%self.p
		xs2=(Q2.x*Q1z2)%self.p
		ys1=(Q1.y*Q2z2*Q2.z)%self.p
		ys2=(Q2.y*Q1z2*Q1.z)%self.p
		
		# Equality special cases
		if (xs1==xs2): 
			if (ys1==ys2): # adding point to itself
				return self.double(Q1)
			else: # vertical pair--result is the identity
				return self.identity()

		# Ordinary case
		xd=(xs2-xs1)%self.p   # caution: if not python, negative result?
		yd=(ys2-ys1)%self.p
		xd2=(xd*xd)%self.p
		xd3=(xd2*xd)%self.p
		x=(yd*yd-xd3-2*xs1*xd2)%self.p
		y=(yd*(xs1*xd2-x)-ys1*xd3)%self.p
		z=(xd*Q1.z*Q2.z)%self.p
		return ECpoint(self,x,y,z)

	# "Multiply" this elliptic curve point Q by the scalar (integer) m
	#    Often the point Q will be the generator G
	def mul(self,m,Q):
		R=self.identity() # return point
		while m!=0:  # binary multiply loop
			if m&1: # bit is set
				#print("  mul: adding Q to R =",R);
				R=self.add(R,Q)
				#print("  mul: added Q to R =",R);
			m=m>>1
			if (m!=0):
				#print("  mul: doubling Q =",Q);
				Q=self.double(Q)
		
		return R
			

# A point on an elliptic curve: (x,y)
#   Using special (X,Y,Z) Jacobian point representation
class ECpoint:
	"""A point on an elliptic curve (x/z^2,y/z^3)"""
	def __init__(self,curve, x,y,z):
		self.curve=curve
		self.x=x
		self.y=y
		self.z=z
		# This self-check has a big performance cost.
		#if not x==curve.p and not curve.touches(self):
		#	print(" ECpoint left curve: ",self)

	# "Add" this point to another point on the same curve
	def add(self,Q2):
		return self.curve.add(self,Q2)

	# "Multiply" this point by a scalar
	def mul(self,m):
		return self.curve.mul(m,self)
	
	# Extract non-projective X and Y coordinates
	#   This is the only time we need the expensive modular inverse
	def get_x(self):
		return self.curve.field_div(self.x,(self.z*self.z)%self.curve.p);
	def get_y(self):
		return self.curve.field_div(self.y,(self.z*self.z*self.z)%self.curve.p);

	# Print this ECpoint
	def __str__(self):
		if (self.x==self.curve.p):
			return "identity_point"
		else:
			return "("+str(self.get_x())+", "+str(self.get_y())+")"



# This is the BitCoin elliptic curve, SECG secp256k1
#   See http://www.secg.org/SEC2-Ver-1.0.pdf
secp256k1=ECcurve()
secp256k1.p=hex2int("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F");
secp256k1.a=0 # it's a Koblitz curve, with no linear part
secp256k1.b=7 
# n is the order of the curve, used for ECDSA
secp256k1.n=hex2int("FFFFFFFF FFFFFFFF FFFFFFFF FFFFFFFE BAAEDCE6 AF48A03B BFD25E8C D0364141");

# SEC's "04" means they're representing the generator point's X,Y parts explicitly.
secp256k1.G=ECpoint(curve=secp256k1,
  x = hex2int("79BE667E F9DCBBAC 55A06295 CE870B07 029BFCDB 2DCE28D9 59F2815B 16F81798"),
  y = hex2int("483ADA77 26A3C465 5DA4FBFC 0E1108A8 FD17B448 A6855419 9C47D08F FB10D4B8"),
  z = 1  # projective coordinates, start with Z==1
);

#class signature, sign and verify methods start here

class Signature:	

	def __init__(self):
		self.curve = secp256k1		
		self.Q = self.curve.G
		self.G = self.curve.G
		self.R = ""
		self.gen_pk()
			
	def gen_pk(self):
		
		self.sig_key = rand_sec(99999999999999999999999999999999999999999999999999)	

		for i in range(rand_sec(999)):
			self.sig_key = self.sig_key * int(time())
			self.sig_key = self.sig_key * rand_sec(99999999999999999999999999999999999999999999999999)			
			

		self.Q = self.G.mul(self.sig_key) # move down curve by x to make public key
		print(self.Q)

		with open("pvk.txt", "wb") as lf:
			lf.write(pickle.dumps(self.sig_key))
    	
		with open("pbk.txt", "wb") as lf:
			lf.write(pickle.dumps(self.Q))

	def sign(self, msg):	

		with open("pvk.txt", "rb") as lf:
				#pbk = pickle.loads(lf.read())
				content = lf.read()
				pvk =  pickle.loads(content)			
		
		n = self.curve.n; # order of curve						
		k = rand.getrandbits(256)%n; # message nonce
		self.R = self.G.mul(k); # used to encode
		#e = self.hash(msg, self.R); # part 1 of signature
		e = tools.hash_sig(msg, self.R); # part 1 of signature
		s=(k-e*pvk)%n; # part 2 of signature

		return(e, s)


	def verify(self, msg, e, s, pbk = None):

		if pbk == None:
			with open("pbk.txt", "rb") as lf:
				#pbk = pickle.loads(lf.read())
				content = lf.read()
				pbk =  pickle.loads(content)				
		
		Rv=self.G.mul(s).add(pbk.mul(e));		
		ev=tools.hash_sig(msg,Rv); # check signature 

		if (e==ev):			
			tools.log(f"\n [Valid Signature] \n {msg} \n \n e= {e} \nand \n ev= {ev}")
		else:
			tools.log(f"\n [Invalid Signature] \n e= {e} \nand \n ev= {ev}")

if __name__ == "__main__":
	#test function

	print("\n This is a test program to demonstrate signature process \n")

	new_sig = Signature()	#create the signature function with private key = 1

	test_msg = "hello"

	blk_tx = {"send_add": "Sender Address", "recv_add": "Receiver Address", 
            "amount": "Amount Tx", "time_stamp": "Time Stamp",
            "tx_id": "Transaction ID", "tx_sig": "Transaction Signature"}

	signed = new_sig.sign(blk_tx)	#send message to be signed
	print(signed)
	
	#verification process with message and signature received from sign method
	new_sig.verify(blk_tx, signed[0], signed[1]) 
