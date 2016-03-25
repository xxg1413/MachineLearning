#!/usr/bin/env python
#coding=utf-8


from numpy import *
import operator  ##运算符模块


def create_data_set():
    group = array([[1.0,1.1], [1.0,1.0], [0,0], [0,0.1]]) ##创建数据集
    labels = ['A','A','B','B'] ##创建标签
    return group, labels



def kNN0(in_X, data_set, labels, k):
    data_set_size = data_set.shape[0]
    diff_mat = tile(in_X, (data_set_size,1)) - data_set
    sq_diff_mat= diff_mat ** 2
    sq_distances = sq_diff_mat.sum(axis=1)
    distances = sq_distances ** 0.5

    sorted_dist_indicies = distances.argsort()
    class_count={}

    for i in range(k):
        vote_i_label= labels[sorted_dist_indicies[i]]
        class_count[vote_i_label] = class_count.get(vote_i_label,0) + 1

    sorted_class_count = sorted(class_count.iteritems(),key=operator.itemgetter(1),reverse=True) ##排序

    return sorted_class_count[0][0]



def main():
    group,labels = create_data_set()
    result=kNN0([1,1],group,labels,3)
    print result


if __name__ == "__main__":
    main()



##result
'''
>>> import kNN
>>> group,labels = kNN.create_data_set()
>>> group
array([[ 1. ,  1.1],
       [ 1. ,  1. ],
       [ 0. ,  0. ],
       [ 0. ,  0.1]])
>>> labels
['A', 'A', 'B', 'B']
>>> kNN.kNN0([0,0],group,labels,3)
'B'
>>> kNN.kNN0([1,2],group,labels,3)
'A'
>>>

'''
