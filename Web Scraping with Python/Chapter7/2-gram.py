from urllib.request import  urlopen
from bs4 import  BeautifulSoup


def ngrams(indata, n):
    indata = indata.split(' ')
    outodata=[]

    for i in range(len(indata)-n+1):
        outodata.append(indata[i:i+n])

    return outodata


html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
data = BeautifulSoup(html, "html.parser")

content = data.find("div",{"id": "mw-content-text"}).get_text()

ngram = ngrams(content, 2)

print(ngram)
print("2-ngrams count is:" + str(len( ngram)))



