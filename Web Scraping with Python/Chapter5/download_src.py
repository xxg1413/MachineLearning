import  os

from urllib.request import  urlopen, urlretrieve
from bs4 import  BeautifulSoup

download_dir = "downloaded"

baseUrl = "http://pythonscraping.com"

def getURI(url, source):
    if source.startswith("http://www."):
        url = "http://"+ source[11:]
    elif source.startswith("http://"):
        url = source
    elif  source.startswith("www."):
        url = "http://" + source[4:]
    else:
        url = baseUrl +"/" + source

    if baseUrl not in url:
        return None

    return url


def getDownloadPath(baseUrl, url, download_dir):
    path = url.replace("www.", "")
    path = path.replace(baseUrl, "")
    path = download_dir + path

    dir = os.path.dirname(path)

    if not os.path.exists(dir):
        os.makedirs(dir)

    return path


def main():

    html = urlopen(baseUrl)
    data = BeautifulSoup(html, "html.parser")
    download_list = data.findAll(src=True)

    for download in download_list:
        fileUrl = getURI(baseUrl, download["src"])
        if fileUrl is not None:
            print(fileUrl)

        urlretrieve(fileUrl, getDownloadPath(baseUrl, fileUrl, download_dir))



if __name__ == "__main__":
    main()





