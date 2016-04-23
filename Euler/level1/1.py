#1

total= 0
for i in range(1000):
    if ((i % 3 == 0) or (i % 5 == 0)):
       total += i

print total



#2
print sum(i for i in xrange(1000) if i % 3 == 0 or i % 5 == 0)




#3

print 3* (999//3) *(999//3 + 1) // 2  + 5 * (999//5) *( (999//5) +1) // 2   -  (3*5) * (999//(3*5)) * (999//(3*5) + 1) // 2

def sumNum(n,d):
    return d * (n//d) *((n//d)+1) // 2

n,d1,d2 = 1000-1, 3, 5

print sumNum(n,d1) +  sumNum(n,d2) - sumNum(n, d1*d2)

