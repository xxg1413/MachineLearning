#coding=utf-8

from urllib.request import  urlopen
from bs4 import BeautifulSoup

#html = urlopen("http://www.baidu.com")
html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")

data = BeautifulSoup(html.read(), "html.parser")

'''
name_list = data.findAll("span", {"class":"green"})

for name in name_list:
    print(name.get_text())

'''

prince_list = data.findAll(text="the prince")
print(len(prince_list))
