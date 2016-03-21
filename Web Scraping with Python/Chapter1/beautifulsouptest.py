from urllib.request import urlopen
from bs4 import  BeautifulSoup


html = urlopen("http://www.pythonscraping.com/pages/page1.html")

'''
To get rid of this warning, change this:

 BeautifulSoup([your markup])

to this:

 BeautifulSoup([your markup], "html.parser")

  markup_type=markup_type))
'''
#data = BeautifulSoup(html.read())

data = BeautifulSoup(html.read(), "html.parser")


print(data.title)
