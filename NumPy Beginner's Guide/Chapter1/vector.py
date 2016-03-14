#!/usr/bin/env python
#coding:utf-8

import sys
import  datetime

import  numpy as np

def numpy_sum(n):
    a  = np.arange(n) ** 2 ##numpy在操作数组上的效率优于纯python的数组
    b  = np.arange(n) ** 3

    c = a + b

    return c


def python_sum(n):
    a = range(n)
    b = range(n)
    c = []

    for i in range(len(a)):
        a[i] = i ** 2
        b[i] = i ** 3
        c.append(a[i] + b[i])

    return c

def run(num):
    start = datetime.datetime.now()
    c = python_sum(num)
    delta = datetime.datetime.now()-start
    print "The last 2 elements of the sum", c[-2:]
    print "Python elapsed time in microseconds", delta.microseconds

    start = datetime.datetime.now()
    c = numpy_sum(num)
    delta = datetime.datetime.now()-start
    print "The last 2 elements of the sum", c[-2:]
    print "Numpy elapsed time in microseconds", delta.microseconds


def main():
    num = int(sys.argv[1])
    run(num)


if __name__ == "__main__":
    main()
