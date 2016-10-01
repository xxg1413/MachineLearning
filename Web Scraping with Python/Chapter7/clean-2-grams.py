#!/usr/bin/env python3
#!encoding=utf-8

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
from collections import OrderedDict


def cleanInput(input):
    '''
    移除转义字符，过滤Unicode字符
    '''
    input = re.sub('\n+', " ", input) #替换换行符
    input = re.sub('\[[0-9]*\]', "", input)#除去数字
    input = re.sub(' +', " ", input) #除去多余的空格
    input = bytes(input, "UTF-8") #更改编码
    input = input.decode("ascii", "ignore")

    cleanInput = []
    input = input.split(' ')

    for item in input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput


def getNgrams(input, n):
    input = cleanInput(input)
    output = dict()
    for i in range(len(input)-n+1):
        newNGram = " ".join(input[i:i+n])
        if newNGram in output:
            output[newNGram] += 1
        else:
            output[newNGram] = 1
    return output



html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html,"html.parser")
content = bsObj.find("div", {"id":"mw-content-text"}).get_text()


ngrams = getNgrams(content, 2)

#使用OrderedDict 去重
ngrams = OrderedDict(sorted(ngrams.items(), key=lambda t: t[1], reverse=True))


print(ngrams)