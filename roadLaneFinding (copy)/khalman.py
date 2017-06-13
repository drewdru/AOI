# -*- coding: utf-8 -*-
import sys
import random
import math
import random
import pylab


N=50
dt=0.4
as0=[45,105,-0.05,-0.01]
a0=[50,100,-0.06,-0.02]
Rv=25
f0=[[16,0,0,0],[0,16,0,0],[0,0,0.04,0],[0,0,0,0.04]]

H=lambda t,a:a[0]*math.sin(a[2]*t)+a[1]*math.sin(a[3]*t)
ir=range(4)

#tk=[i*dt for i in k]

fek=f0

def aS(k):
	if k==0:
		return as0
	tk=k*dt
	ase=aS(k-1) #step 1
	u=H(tk,a0)+Rv**0.5*random.gauss(0,1) #step 2
	use=H(tk,ase) #step 7
	#step 4:
	z=[math.sin(ase[2]*tk),math.sin(ase[3]*tk),ase[0]*tk*math.cos(ase[2]*tk),ase[1]*tk*math.cos(ase[3]*tk)]
	b=[sum([fek[i][e]*z[e] for e in ir]) for i in ir]
	#step 5:
	puu=sum([z[m]*b[m]  for m in ir])+Rv
	#step 6:
	for i in ir:
		for e in ir:
			fek[i][e]-=b[i]*b[e]/puu

	a=[ase[i]+b[i]/puu*(u-use) for i in ir]
	print (a)
	return a


print ("start")
asn=aS(N)
pylab.plot(range(100),[H(t,asn) for t in range(100)],'r')#конечное приближение
pylab.plot(range(100),[H(t,a0) for t in range(100)])
pylab.plot(range(100),[H(t,as0) for t in range(100)],'g')#первоначальное приближение
pylab.grid(True)
pylab.show()

print ("plot")
