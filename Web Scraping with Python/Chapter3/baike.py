#!/usr/bin/env python3
#coding=utf-8

from urllib.request import  urlopen
from bs4 import  BeautifulSoup
import  re

html = urlopen("http://baike.baidu.com/calendar/")

data = BeautifulSoup(html, "html.parser")

for event  in data.findAll("dl", {"class": "events"}):
    print(event)




