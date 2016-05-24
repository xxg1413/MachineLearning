#!/usr/bin/env python
#coding:utf-8

import os
import  scipy as sp
import  matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),"data")

#print(data_dir)

data_path = os.path.join(data_dir, "web_traffic.tsv")

if os.path.exists(data_path):
    data = sp.genfromtxt(data_path, delimiter="\t")#必须是Tab
    #print(data[:2])
else:
    print("data not exist!")
    exit(0)

#print(data.shape)

#把数据(x,y)分为两个向量来处理

x = data[:,0]
y = data[:,1]

#因为有值为nan的情况，
#print sp.sum(sp.isnan(y))
#print len(x), len(y)

days = len(y)/24 + 1

#数据清洗，删除为nan的项
x = x[~sp.isnan(y)]
y = y[~sp.isnan(y)]


#print len(x), len(y)
#print sp.sum(sp.isnan(y))


#散点图
plt.scatter(x,y)
plt.title(u"上一月的网络流量图")
plt.xlabel(u"日期")
plt.ylabel(u"访问量")

#plt.xticks([w*7*24 for w in range(10)], ['week %i' %w for w in range(10)])

#按日期分割
plt.xticks([w*24  for w in range(1,days+1)], ['%i' %w for w in range(1,days+1)])

plt.autoscale(tight=True)
plt.grid()
plt.show()




