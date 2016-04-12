import urllib,md5,webbrowser,time
from xml.dom.minidom import parseString

apikey="47e953c8ea9ed30db904af453125c759"
secret="ea703e4721e8c7bf88b92110a46a9b06"
FacebookURL = "https://api.facebook.com/restserver.php"

def getsinglevalue(node,tag):
  nl=node.getElementsByTagName(tag)
  if len(nl)>0:
    tagNode=nl[0]
    if tagNode.hasChildNodes():
      return tagNode.firstChild.nodeValue
  return ''

def callid(): 
  return str(int(time.time()*10))

class fbsession:
  def __init__(self):
    self.session_secret=None
    self.session_key=None
    self.createtoken()
    webbrowser.open(self.getlogin())
    print "Press enter after logging in:",
    raw_input()
    self.getsession()
  def sendrequest(self, args):
    args['api_key'] = apikey
    args['sig'] = self.makehash(args)
    post_data = urllib.urlencode(args)
    url = FacebookURL + "?" + post_data
    data=urllib.urlopen(url).read()
    print data
    return parseString(data)
  def makehash(self,args):
    hasher = md5.new(''.join([x + '=' + args[x] for x in sorted(args.keys())]))
    if self.session_secret: hasher.update(self.session_secret)
    else: hasher.update(secret)
    return hasher.hexdigest()
  def createtoken(self):
    res = self.sendrequest({'method':"facebook.auth.createToken"})
    self.token = getsinglevalue(res,'token')
  def getlogin(self):
    return "http://api.facebook.com/login.php?api_key="+apikey+\
           "&auth_token=" + self.token
  def getsession(self):
    doc=self.sendrequest({'method':'facebook.auth.getSession',
                               'auth_token':self.token})
    self.session_key=getsinglevalue(doc,'session_key')
    self.session_secret=getsinglevalue(doc,'secret')
  def getfriends(self):
    doc=self.sendrequest({'method':'facebook.friends.get',
                          'session_key':self.session_key,'call_id':callid()})
    results=[]
    for n in doc.getElementsByTagName('result_elt'):
      results.append(n.firstChild.nodeValue)
    return results

  def getinfo(self,users):
    ulist=','.join(users)
    
    fields='gender,current_location,relationship_status,'+\
           'affiliations,hometown_location'
    
    doc=self.sendrequest({'method':'facebook.users.getInfo',
    'session_key':self.session_key,'call_id':callid(),
    'users':ulist,'fields':fields})

    results={}
    for n,id in zip(doc.getElementsByTagName('result_elt'),users):
      # Get the location
      locnode=n.getElementsByTagName('hometown_location')[0]
      loc=getsinglevalue(locnode,'city')+', '+getsinglevalue(locnode,'state')
      
      # Get school
      college=''
      gradyear='0'
      affiliations=n.getElementsByTagName('affiliations_elt')
      for aff in affiliations:
        # Type 1 is college
        if getsinglevalue(aff,'type')=='1': 
          college=getsinglevalue(aff,'name')
          gradyear=getsinglevalue(aff,'year')
      
      results[id]={'gender':getsinglevalue(n,'gender'),
                   'status':getsinglevalue(n,'relationship_status'),
                   'location':loc,'college':college,'year':gradyear}
    return results

  def arefriends(self,idlist1,idlist2):
    id1=','.join(idlist1)
    id2=','.join(idlist2)
    doc=self.sendrequest({'method':'facebook.friends.areFriends',
                          'session_key':self.session_key,'call_id':callid(),
                          'id1':id1,'id2':id2})
    results=[]
    for n in doc.getElementsByTagName('result_elt'):
      results.append(int(n.firstChild.nodeValue))
    return results
  
  

  def makedataset(self):
    from advancedclassify import milesdistance
    # Get all the info for all my friends
    friends=self.getfriends()
    info=self.getinfo(friends)
    ids1,ids2=[],[]
    rows=[]

    # Nested loop to look at every pair of friends
    for i in range(len(friends)):
      f1=friends[i]
      data1=info[f1]
      
      # Start at i+1 so we don't double up
      for j in range(i+1,len(friends)):
        f2=friends[j]
        data2=info[f2]
        ids1.append(f1)
        ids2.append(f2)

        # Generate some numbers from the data
        if data1['college']==data2['college']: sameschool=1
        else: sameschool=0
        male1=(data1['gender']=='Male') and 1 or 0
        male2=(data2['gender']=='Male') and 1 or 0        
        
        row=[male1,int(data1['year']),male2,int(data2['year']),sameschool]
        rows.append(row)
    # Call arefriends in blocks for every pair of people
    arefriends=[]
    for i in range(0,len(ids1),30):
      j=min(i+30,len(ids1))
      pa=self.arefriends(ids1[i:j],ids2[i:j])
      arefriends+=pa
    return arefriends,rows
  
