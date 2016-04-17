from urllib.request import  urlopen
from bs4 import  BeautifulSoup

import  re
import  datetime
import  random

pages = set()
random.seed(datetime.datetime.now())

def getInternalLinks(data, includeUrl):

    inLinks = []

    for link in data.findAll("a", href=re.compile("^(/|.*" + includeUrl+")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in inLinks:
                inLinks.append(link.attrs['href'])

    return  inLinks


def getExLinks(data, excludeUrl):

    exLinks = []

    for link in data.findAll("a", href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
        if link.attrs['href']  is not None:
            if link.attrs['href'] not in exLinks:
                exLinks.append(link.attrs['href'])

    return exLinks


def splitAddress(address):
    addressParts = address.replace("http://", "").split("/")

    return addressParts

def getRandomExtLink(startPage):
    html = urlopen(startPage)
    data = BeautifulSoup(html, "html.parser")
    exLinks = getExLinks(data, splitAddress(startPage)[0])

    if len(exLinks) == 0:
        inLinks = getInternalLinks(startPage)
        return getNext



