from sys import stdin
n=int(input())
a=list(map(int,stdin.readlines()))
def z(l,r):
	m=(l+r)/2
	if l==r:return a[l],l,l
	u=y(m+1,r+1,1)
	d=y(m,l-1,-1)
	b=(u[0]+d[0],d[1],u[1])
	return max(z(l,m),z(m+1,r),b,key=lambda x:x[0])
def y(f,t,s):
	r=[(0,f)]
	for i in range(f,t,s):r.append((r[-1][0]+a[i],i))
	return max(r,key=lambda x:x[0])
t=z(0,n-1)
print t[1]
print t[2]
print t[0]