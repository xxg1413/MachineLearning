def isPalidromic(n):
    flag = True
    s=str(n)
    for i in range(len(s)/2):
        if s[i] != s[len(s)-i-1]:
            flag = False
            break

    return flag

def largestPalidromic():
    a=[]
    for i in range(100,1000)[::-1]:
        for j in range(100,1000)[::-1]:
            if  isPalidromic(i*j) == True:
                a.append(i*j)

    print max(a)

largestPalidromic()

