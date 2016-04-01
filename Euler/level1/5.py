import numpy

ints = numpy.array(range(1,21))
primes = [2,3,5,7,11,13,17,19]

facts =[]

for i in primes:
    counter=0
    nums = ints
    while any(nums % i == 0):
        nums = nums / float(i)
        counter += 1
    facts.append(counter)

facts = numpy.array(facts)
mults = primes ** facts
res = 1

for j in mults:
    res = j * res

print res
