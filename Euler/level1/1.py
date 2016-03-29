#1
'''
sum = 0
for i in range(1000):
    if ((i % 3 == 0) or (i % 5 == 0)):
       sum += i

print sum
'''

#2
print sum(i for i in xrange(1000) if i % 3 == 0 or i % 5 == 0)
