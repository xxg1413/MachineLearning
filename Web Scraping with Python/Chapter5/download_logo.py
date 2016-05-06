from urllib.request import urlopen, urlretrieve
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com")
data = BeautifulSoup(html, "html.parser")

logo_location = data.find("a",{"id": "logo"}).find("img")["src"]
urlretrieve(logo_location, "logo.jpg")
