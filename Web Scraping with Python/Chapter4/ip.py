#coding=utf-8

import json
from urllib.request import urlopen
from pprint import  pprint



class IP_Address_Info:
    def __init__(self, d):
        self.__dict__ = d



def parse(ipAddress):
    response = urlopen("http://ip.taobao.com/service/getIpInfo.php?ip="+ipAddress).read().decode('utf-8')

    responseJson = json.loads(response, object_hook=IP_Address_Info)

    print(responseJson.data.city)


def getCountry(ipAddress):

    response = urlopen("http://ip.taobao.com/service/getIpInfo.php?ip="+ipAddress).read().decode('utf-8')
    
    responseJson = json.loads(response)

    pprint(responseJson)

    return responseJson.get("data").get("country")


#print(getCountry("180.167.10.98"))

print(parse("180.167.10.98"))
