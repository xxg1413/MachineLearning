#!/usr/bin/env python3
#coding=utf-8

from urllib.request  import urlopen
from urllib.error import HTTPError
from bs4 import  BeautifulSoup

def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        data = BeautifulSoup(html.read(),"html.parser")  ##需要加上"html.parser"
        title = data.head.title
    except AttributeError as e:
        return None

    return title


def main():
    title = getTitle("http://www.baidu.com")
    if title == None:
        print("title not found")
    else:
        print(title)

if __name__ == "__main__":
    main()