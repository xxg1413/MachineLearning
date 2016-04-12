import time
import urllib2
import xml.dom.minidom

kayakkey='YOUR KEY HERE'

def getkayaksession():
  # Construct the URL to start a session
  url='http://www.kayak.com/k/ident/apisession?token=%s&version=1' % kayakkey
  
  # Parse the resulting XML
  doc=xml.dom.minidom.parseString(urllib2.urlopen(url).read())
  
  # Find <sid>xxxxxxxx</sid>
  sid=doc.getElementsByTagName('sid')[0].firstChild.data
  return sid

def flightsearch(sid,origin,destination,depart_date):
  
  # Construct search URL
  url='http://www.kayak.com/s/apisearch?basicmode=true&oneway=y&origin=%s' % origin
  url+='&destination=%s&depart_date=%s' % (destination,depart_date)
  url+='&return_date=none&depart_time=a&return_time=a'
  url+='&travelers=1&cabin=e&action=doFlights&apimode=1'
  url+='&_sid_=%s&version=1' % (sid)

  # Get the XML
  doc=xml.dom.minidom.parseString(urllib2.urlopen(url).read())

  # Extract the search ID
  searchid=doc.getElementsByTagName('searchid')[0].firstChild.data

  return searchid

def flightsearchresults(sid,searchid):
  def parseprice(p): 
    return float(p[1:].replace(',',''))

  # Polling loop
  while 1:
    time.sleep(2)

    # Construct URL for polling
    url='http://www.kayak.com/s/basic/flight?'
    url+='searchid=%s&c=5&apimode=1&_sid_=%s&version=1' % (searchid,sid)
    doc=xml.dom.minidom.parseString(urllib2.urlopen(url).read())

    # Look for morepending tag, and wait until it is no longer true
    morepending=doc.getElementsByTagName('morepending')[0].firstChild
    if morepending==None or morepending.data=='false': break

  # Now download the complete list
  url='http://www.kayak.com/s/basic/flight?'
  url+='searchid=%s&c=999&apimode=1&_sid_=%s&version=1' % (searchid,sid)
  doc=xml.dom.minidom.parseString(urllib2.urlopen(url).read())

  # Get the various elements as lists
  prices=doc.getElementsByTagName('price')
  departures=doc.getElementsByTagName('depart')
  arrivals=doc.getElementsByTagName('arrive')  

  # Zip them together
  return zip([p.firstChild.data.split(' ')[1] for p in departures],
             [p.firstChild.data.split(' ')[1] for p in arrivals],
             [parseprice(p.firstChild.data) for p in prices])


def createschedule(people,dest,dep,ret):
  # Get a session id for these searches
  sid=getkayaksession()
  flights={}
  
  for p in people:
    name,origin=p
    # Outbound flight
    searchid=flightsearch(sid,origin,dest,dep)
    flights[(origin,dest)]=flightsearchresults(sid,searchid)
    
    # Return flight
    searchid=flightsearch(sid,dest,origin,ret)
    flights[(dest,origin)]=flightsearchresults(sid,searchid)
    
  return flights
