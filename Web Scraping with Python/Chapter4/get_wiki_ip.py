from urllib.request import  urlopen
from bs4 import  BeautifulSoup
import  datetime
import  random
import  re
import  json


random.seed(datetime.datetime.now())

class IPv4_Address_Info:
    def __init__(self, d):
        self.__dict__ = d

def getIPv4Info(ipv4Address):
    response = urlopen("http://ip.taobao.com/service/getIpInfo.php?ip="+ipv4Address).read().decode('utf-8')

    responseJson = json.loads(response, object_hook=IPv4_Address_Info)

    print(responseJson.data.country)


def getIPv6Info(ipv6Address):
    html  = urlopen("http://geoip.neu.edu.cn/?ip=" + ipv6Address)
    data = BeautifulSoup(html, "html.parser")

    city = data.findAll("p", {"class": "text-info lead"})

    print(city[2].get_text())


def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org" + articleUrl)
    data = BeautifulSoup(html, "html.parser")

    return  data.find("div", {"id":"bodyContent"}).findAll("a",
                        href=re.compile("^(/wiki/)((?!:).)*$"))


def getHistoryIPs(pageUrl):
    pageUrl = pageUrl.replace("/wiki/","")
    historyUrl = "http://en.wikipedia.org/w/index.php?title=" + pageUrl + "&action=history"

    print("history url is:" + historyUrl)

    html = urlopen(historyUrl)

    data = BeautifulSoup(html, "html.parser")

    ipAddress = data.findAll("a", {"class": "mw-anonuserlink"})
    addressList = set()

    for ip in ipAddress:
        addressList.add(ip.get_text())

    return  addressList


def main():
    links = getLinks("/wiki/Python_(programming_language)")
    while(len(links) > 0 ):
        for link in links:
            historyIPs = getHistoryIPs(link.attrs["href"])
            for historyIP in historyIPs:
                print("IP:",historyIP," city:", getIPv4Info(historyIP))

    newLink = links[random.randint(0,len(links)-1)].attrs["href"]
    links = getLinks(newLink)


if __name__ == "__main__":
    main()
