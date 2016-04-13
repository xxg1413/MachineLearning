from urllib.request import  urlopen

from bs4 import  BeautifulSoup

import  re


html = urlopen("http://www.pythonscraping.com/pages/page3.html")

data = BeautifulSoup(html, "html.parser")

images = data.findAll("img", {"src": re.compile("\.\.\/img\/gifts/img.*\.jpg")})

for i in images:
    print(i["src"])

