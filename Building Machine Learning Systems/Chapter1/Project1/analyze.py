#!/usr/bin/env python
#coding:utf-8

import os
import  scipy as sp
import  matplotlib.pyplot as plt

data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data")

#print(data_dir)

data_path = os.path.join(data_dir, "web_traffic.tsv")

if os.path.exists(data_path):
    data = sp.genfromtxt(data_path, delimiter="\t")#必须是Tab
    #print(data[:2])
else:
    print("data not exist!")
    exit(0)


print(data[:2])


