#!/usr/bin/env python3
#coding=utf-8

from urllib.request import  urlopen
from bs4 import  BeautifulSoup
import  re

html = urlopen("http://en.wikipedia.org/wiki/Kevin_Bacon")

data = BeautifulSoup(html, "html.parser")

'''
for link in data.findAll("a"):
    if 'href'  in link.attrs:
        print(link.attrs['href'])
'''

for link in data.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
    if 'href' in link.attrs:
        print(link.attrs['href'])
