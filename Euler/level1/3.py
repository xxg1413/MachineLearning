from math import sqrt

def isPrimer(n):
    a=[]
    for i in range(2, int(sqrt(n))):
        if n%i == 0:
            a.append(i)
            n=n/i

    print(max(a))


isPrimer(600851475143)
