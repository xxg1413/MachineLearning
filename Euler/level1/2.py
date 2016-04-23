#1
a=[1,2]
total = 2
i=2
while(1):
   next=a[i-1]+a[i-2]
   a.append(next)
   if next % 2 == 0:
       total = total + next
   if total > 4000000:
       break
   i += 1

print total



#2
def fib(n):
    if n ==1:
        return 1
    if n == 2:
        return 2
    return fib(n-1)+fib(n-2)

a=[]
i=1
while(fib(i) < 4000000):
    if fib(i) % 2 == 0:
        a.append(fib(i))
    i += 1

print sum(a)


#3
x,y,n = 0,2, 4000000

while y < n:
    x,y = y, (4*y + x)

print (x + y -2) // 4
