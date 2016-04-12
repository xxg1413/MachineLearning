from BeautifulSoup import BeautifulSoup
import urllib2
import re
chare=re.compile(r'[!-\.&]')
itemowners={}

# Words to remove
dropwords=['a','new','some','more','my','own','the','many','other','another']

currentuser=0
for i in range(1,51):
  # URL for the want search page
  c=urllib2.urlopen(
  'http://member.zebo.com/Main?event_key=USERSEARCH&wiowiw=wiw&keyword=car&page=%d'
  % (i))
  soup=BeautifulSoup(c.read())
  for td in soup('td'):
    # Find table cells of bgverdanasmall class
    if ('class' in dict(td.attrs) and td['class']=='bgverdanasmall'):
      items=[re.sub(chare,'',str(a.contents[0]).lower()).strip() for a in td('a')]
      for item in items:
        # Remove extra words
        txt=' '.join([t for t in item.split(' ') if t not in dropwords])
        if len(txt)<2: continue
        itemowners.setdefault(txt,{})
        itemowners[txt][currentuser]=1
      currentuser+=1
      
out=file('zebo.txt','w')
out.write('Item')
for user in range(0,currentuser): out.write('\tU%d' % user)
out.write('\n')
for item,owners in itemowners.items():
  if len(owners)>10:
    out.write(item)
    for user in range(0,currentuser):
      if user in owners: out.write('\t1')
      else: out.write('\t0')
    out.write('\n')
