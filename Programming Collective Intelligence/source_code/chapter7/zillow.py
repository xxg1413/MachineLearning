import xml.dom.minidom
import urllib2

zwskey="YOUR API KEY"

def getaddressdata(address,city):
  escad=address.replace(' ','+')
  url='http://www.zillow.com/webservice/GetDeepSearchResults.htm?'
  url+='zws-id=%s&address=%s&citystatezip=%s' % (zwskey,escad,city)
  doc=xml.dom.minidom.parseString(urllib2.urlopen(url).read())
  code=doc.getElementsByTagName('code')[0].firstChild.data
  if code!='0': return None
  if 1:
    zipcode=doc.getElementsByTagName('zipcode')[0].firstChild.data
    use=doc.getElementsByTagName('useCode')[0].firstChild.data
    year=doc.getElementsByTagName('yearBuilt')[0].firstChild.data
    sqft=doc.getElementsByTagName('finishedSqFt')[0].firstChild.data
    bath=doc.getElementsByTagName('bathrooms')[0].firstChild.data
    bed=doc.getElementsByTagName('bedrooms')[0].firstChild.data
    rooms=1 #doc.getElementsByTagName('totalRooms')[0].firstChild.data
    price=doc.getElementsByTagName('amount')[0].firstChild.data
  else:
    return None
       
  return (zipcode,use,int(year),float(bath),int(bed),int(rooms),price)

def getpricelist():
  l1=[]
  for line in file('addresslist.txt'):
    data=getaddressdata(line.strip(),'Cambridge,MA')
    l1.append(data)
  return l1
