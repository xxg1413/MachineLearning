sum1=0
sum2=0

for i in range(1,101):
    sum1 = sum1 + i
    sum2 = sum2 + pow(i,2)


print pow(sum1,2) - sum2
