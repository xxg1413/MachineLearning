import random
import math
from math import sqrt
from PIL import Image,ImageDraw,ImageFont

# Returns the Pearson correlation coefficient for p1 and p2
def pearson(v1,v2):
  # Simple sums
  sum1=sum(v1)
  sum2=sum(v2)
  
  # Sums of the squares
  sum1Sq=sum([pow(v,2) for v in v1])
  sum2Sq=sum([pow(v,2) for v in v2])	
  
  # Sum of the products
  pSum=sum([v1[i]*v2[i] for i in range(len(v1))])
  
  # Calculate r (Pearson score)
  num=pSum-(sum1*sum2/len(v1))
  den=sqrt((sum1Sq-pow(sum1,2)/len(v1))*(sum2Sq-pow(sum2,2)/len(v1)))
  if den==0: return 0

  return 1.0-(num/den)


class bicluster:
  def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
    self.left=left
    self.right=right
    self.vec=vec
    self.id=id
    self.distance=distance

def euclidean(v1,v2):
  sqsum=sum([math.pow(v1[i]-v2[i],2) for i in range(len(v1))])
  return math.sqrt(sqsum)

def printclust(clust,labels=None,n=0):
  for i in range(n): print ' ',
  if clust.id<0:
    print '-'
  else:
    if labels==None: print clust.id
    else: print labels[clust.id]
  if clust.left!=None: printclust(clust.left,labels=labels,n=n+1)
  if clust.right!=None: printclust(clust.right,labels=labels,n=n+1)

def hcluster(vecs,distance=pearson):
  distances={}
  currentclustid=-1
  clust=[bicluster(vecs[i],id=i) for i in range(len(vecs))]

  while len(clust)>1:
    lowestpair=(0,1)
    closest=distance(clust[0].vec,clust[1].vec)
    for i in range(len(clust)):
      for j in range(i+1,len(clust)):
        if (clust[i].id,clust[j].id) not in distances: 
          distances[(clust[i].id,clust[j].id)]=distance(clust[i].vec,clust[j].vec)
        d=distances[(clust[i].id,clust[j].id)]

        if d<closest:
          closest=d
          lowestpair=(i,j)

    mergevec=[(clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0 for i in range(len(clust[0].vec))]
    error=closest
    newcluster=bicluster(mergevec,left=clust[lowestpair[0]],right=clust[lowestpair[1]],distance=error,id=currentclustid)
    
    currentclustid-=1
    del clust[lowestpair[1]]
    del clust[lowestpair[0]]
    clust.append(newcluster)

  return clust[0]
  
  
def kcluster(vecs,distance=pearson,k=4):
  ranges=[(min([vec[i] for vec in vecs]),max([vec[i] for vec in vecs])) for i in range(len(vecs[0]))]
  clusters=[[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] for i in range(len(vecs[0]))] for j in range(k)]
  
  lastmatches=None
  for t in range(100):
    print 'Iteration %d' % t
    bestmatches=[[] for i in range(k)]
    
    for j in range(len(vecs)):
      vec=vecs[j]
      bestmatch=0
      for i in range(k):
        d=distance(clusters[i],vec)
        if d<distance(clusters[bestmatch],vec): bestmatch=i
      bestmatches[bestmatch].append(j)

    if bestmatches==lastmatches: break
    lastmatches=bestmatches
    
    for i in range(k):
      avgs=[0.0]*len(vecs[0])
      if len(bestmatches[i])>0:
        for vecid in bestmatches[i]:
          for m in range(len(vecs[vecid])):
            avgs[m]+=vecs[vecid][m]
        for j in range(len(avgs)):
          avgs[j]/=len(bestmatches[i])
        clusters[i]=avgs
      
  return bestmatches

def readfile(filename):
  lines=[line for line in file(filename)]
  colnames=lines[0].strip().split('\t')[1:]
  rownames=[]
  data=[]
  for line in lines[1:]:
    p=line.strip().split('\t')
    rownames.append(p[0])
    data.append([float(x) for x in p[1:]])
  return rownames,colnames,data

def test2():
  rownames,colnames,data=readfile('datafile.txt')
  return hcluster(data)
  #for i in range(len(rownames)):
  #  print i,rownames[i]

def distance(v1,v2):
  c1,c2,shr=0,0,0
  
  for i in range(len(v1)):
    if v1[i]!=0: c1+=1
    if v2[i]!=0: c2+=1
    if v1[i]!=0 and v2[i]!=0: shr+=1
  
  return float(shr)/(c1+c2-shr)


#test2()

def getheight(clust):
  if clust.left==None and clust.right==None: return 1
  return getheight(clust.left)+getheight(clust.right)

def getdepth(clust):
  if clust.left==None and clust.right==None: return 0
  return max(getdepth(clust.left),getdepth(clust.right))+clust.distance

def drawdendrogram(clust,labels,jpeg='clusters.jpg'):
  h=getheight(clust)*20
  depth=getdepth(clust)
  w=1200
  scaling=float(w-150)/depth
  img=Image.new('RGB',(w,h),(255,255,255))
  draw=ImageDraw.Draw(img)

  draw.line((0,h/2,10,h/2),fill=(255,0,0))    

  drawnode(draw,clust,10,(h/2),scaling,labels)
  img.save(jpeg,'JPEG')

def drawnode(draw,clust,x,y,scaling,labels):
  if clust.id<0:
    h1=getheight(clust.left)*20
    h2=getheight(clust.right)*20
    top=y-(h1+h2)/2
    bottom=y+(h1+h2)/2
    
    ll=clust.distance*scaling
    
    draw.line((x,top+h1/2,x,bottom-h2/2),fill=(255,0,0))    

    draw.line((x,top+h1/2,x+ll,top+h1/2),fill=(255,0,0))    
    draw.line((x,bottom-h2/2,x+ll,bottom-h2/2),fill=(255,0,0))        
    
    drawnode(draw,clust.left,x+ll,top+h1/2,scaling,labels)
    drawnode(draw,clust.right,x+ll,bottom-h2/2,scaling,labels)
  else:   
    draw.text((x+5,y-7),labels[clust.id].encode('utf8'),(0,0,0))

def rotatematrix(data):
  newdata=[]
  for i in range(len(data[0])):
    newrow=[data[j][i] for j in range(len(data))]
    newdata.append(newrow)
  return newdata

def scaledown(data,distance=pearson,rate=0.01):
  n=len(data)
  realdist=[[distance(data[i],data[j]) for j in range(n)] for i in range(0,n)]

  outersum=0.0
  
  loc=[[random.random(),random.random()] for i in range(n)] 
  fakedist=[[0.0 for j in range(n)] for i in range(n)]
  
  lasterror=None
  for m in range(0,1000):
    # Find projected distances
    for i in range(n):
      for j in range(n):
        fakedist[i][j]=sqrt(sum([pow(loc[i][x]-loc[j][x],2) 
                                 for x in range(len(loc[i]))]))
  
    # Move points
    grad=[[0.0,0.0] for i in range(n)]
    
    totalerror=0
    for k in range(n):
      for j in range(n):
        if j==k: continue
        errorterm=(fakedist[j][k]-realdist[j][k])/realdist[j][k]
        grad[k][0]+=((loc[k][0]-loc[j][0])/fakedist[j][k])*errorterm
        grad[k][1]+=((loc[k][1]-loc[j][1])/fakedist[j][k])*errorterm    
        totalerror+=abs(errorterm)
    print totalerror
    if lasterror and lasterror<totalerror: break
    lasterror=totalerror
    
    for k in range(n):
      loc[k][0]-=rate*grad[k][0]
      loc[k][1]-=rate*grad[k][1]

  return loc

def draw2d(data,labels,jpg='mds2d.jpg'):
  img=Image.new('RGB',(2000,2000),(255,255,255))
  draw=ImageDraw.Draw(img)
  for i in range(len(data)):
    x=(data[i][0]+0.5)*1000
    y=(data[i][1]+0.5)*1000
    draw.text((x,y),labels[i],(0,0,0))
  img.save(jpg,'JPEG')  
  img.show()
