#coding=utf-8
'''
from math import sqrt

def isPrimer(n):
    for i in range(2, int(sqrt(n)) + 1):
        if n%i == 0:
            return False
    return True

i=4
a=[2,3]
while(True):
    if isPrimer(i) == True:
        a.append(i)

    if len(a) == 10001:
        print a[10000]
        exit(0)

    i += 1
'''
##优化算法

a = range(10002)
sz = 2
a[0] = 2
a[1] = 3
i = 5

while sz < 10002:
    j = 0
    while a[j] * a[j] <= i:
        if i % a[j] == 0: break
        j += 1
    if a[j] * a[j] > i:
        a[sz] = i
        sz += 1
    i += 2

print a[10000]
