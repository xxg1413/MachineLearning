import httplib
from xml.dom.minidom import parse, parseString, Node

devKey = 'YOUR DEV KEY'
appKey = 'YOUR APP KEY'
certKey = 'YOUR CERT KEY'
serverUrl = 'api.ebay.com'
userToken = 'YOUR TOKEN'

def getHeaders(apicall,siteID="0",compatabilityLevel = "433"):
  headers = {"X-EBAY-API-COMPATIBILITY-LEVEL": compatabilityLevel,	
             "X-EBAY-API-DEV-NAME": devKey,
             "X-EBAY-API-APP-NAME": appKey,
             "X-EBAY-API-CERT-NAME": certKey,
             "X-EBAY-API-CALL-NAME": apicall,
             "X-EBAY-API-SITEID": siteID,
             "Content-Type": "text/xml"}
  return headers

def sendRequest(apicall,xmlparameters):
  connection = httplib.HTTPSConnection(serverUrl)
  connection.request("POST", '/ws/api.dll', xmlparameters, getHeaders(apicall))
  response = connection.getresponse()
  if response.status != 200:
    print "Error sending request:" + response.reason
  else: 
    data = response.read()
    connection.close()
  return data

def getSingleValue(node,tag):
  nl=node.getElementsByTagName(tag)
  if len(nl)>0:
    tagNode=nl[0]
    if tagNode.hasChildNodes():
      return tagNode.firstChild.nodeValue
  return '-1'


def doSearch(query,categoryID=None,page=1):
  xml = "<?xml version='1.0' encoding='utf-8'?>"+\
        "<GetSearchResultsRequest xmlns=\"urn:ebay:apis:eBLBaseComponents\">"+\
        "<RequesterCredentials><eBayAuthToken>" +\
        userToken +\
        "</eBayAuthToken></RequesterCredentials>" + \
        "<Pagination>"+\
          "<EntriesPerPage>200</EntriesPerPage>"+\
          "<PageNumber>"+str(page)+"</PageNumber>"+\
        "</Pagination>"+\
        "<Query>" + query + "</Query>"
  if categoryID!=None:
    xml+="<CategoryID>"+str(categoryID)+"</CategoryID>"
  xml+="</GetSearchResultsRequest>"
  
  data=sendRequest('GetSearchResults',xml)
  response = parseString(data)
  itemNodes = response.getElementsByTagName('Item');
  results = []
  for item in itemNodes:
    itemId=getSingleValue(item,'ItemID')
    itemTitle=getSingleValue(item,'Title')
    itemPrice=getSingleValue(item,'CurrentPrice')
    itemEnds=getSingleValue(item,'EndTime')
    results.append((itemId,itemTitle,itemPrice,itemEnds))
  return results


def getCategory(query='',parentID=None,siteID='0'):
  lquery=query.lower()
  xml = "<?xml version='1.0' encoding='utf-8'?>"+\
        "<GetCategoriesRequest xmlns=\"urn:ebay:apis:eBLBaseComponents\">"+\
        "<RequesterCredentials><eBayAuthToken>" +\
        userToken +\
        "</eBayAuthToken></RequesterCredentials>"+\
        "<DetailLevel>ReturnAll</DetailLevel>"+\
        "<ViewAllNodes>true</ViewAllNodes>"+\
        "<CategorySiteID>"+siteID+"</CategorySiteID>"
  if parentID==None:
    xml+="<LevelLimit>1</LevelLimit>"
  else:
    xml+="<CategoryParent>"+str(parentID)+"</CategoryParent>"
  xml += "</GetCategoriesRequest>"
  data=sendRequest('GetCategories',xml)
  categoryList=parseString(data)
  catNodes=categoryList.getElementsByTagName('Category')
  for node in catNodes:
    catid=getSingleValue(node,'CategoryID')
    name=getSingleValue(node,'CategoryName')
    if name.lower().find(lquery)!=-1:
      print catid,name

def getItem(itemID):
  xml = "<?xml version='1.0' encoding='utf-8'?>"+\
        "<GetItemRequest xmlns=\"urn:ebay:apis:eBLBaseComponents\">"+\
        "<RequesterCredentials><eBayAuthToken>" +\
        userToken +\
        "</eBayAuthToken></RequesterCredentials>" + \
        "<ItemID>" + str(itemID) + "</ItemID>"+\
        "<DetailLevel>ItemReturnAttributes</DetailLevel>"+\
        "</GetItemRequest>"
  data=sendRequest('GetItem',xml)
  result={}
  response=parseString(data)
  result['title']=getSingleValue(response,'Title')
  sellingStatusNode = response.getElementsByTagName('SellingStatus')[0];
  result['price']=getSingleValue(sellingStatusNode,'CurrentPrice')
  result['bids']=getSingleValue(sellingStatusNode,'BidCount')
  seller = response.getElementsByTagName('Seller')
  result['feedback'] = getSingleValue(seller[0],'FeedbackScore')

  attributeSet=response.getElementsByTagName('Attribute');
  attributes={}
  for att in attributeSet:
    attID=att.attributes.getNamedItem('attributeID').nodeValue
    attValue=getSingleValue(att,'ValueLiteral')
    attributes[attID]=attValue
  result['attributes']=attributes
  return result


def makeLaptopDataset():
  searchResults=doSearch('laptop',categoryID=51148)
  result=[]
  for r in searchResults:
    item=getItem(r[0])
    att=item['attributes']
    try:
      data=(float(att['12']),float(att['26444']),
            float(att['26446']),float(att['25710']),
            float(item['feedback'])
           )
      entry={'input':data,'result':float(item['price'])}
      result.append(entry)
    except:
      print item['title']+' failed'
  return result
