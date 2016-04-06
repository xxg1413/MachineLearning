from urllib.request import  urlopen
from bs4 import  BeautifulSoup

html = urlopen("http://www.pythonscraping.com/pages/page3.html")

data = BeautifulSoup(html, "html.parser")

for child in data.find("table",{"id":"giftList"}).children:
    print(child)



