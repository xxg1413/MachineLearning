from urllib.request import  urlopen
from io import  StringIO
import  csv


'''
Don't name your file csv.py.
When you do, Python will look in your file for the csv code instead of the standard library csv module.
'''

data = urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv").read().decode('ascii', 'ignore')

dataFile = StringIO(data)

'''
csvRead = csv.reader(dataFile)

for row in csvRead:
    print(row)
'''

dictReader = csv.DictReader(dataFile)

print(dictReader.fieldnames)

for row in dictReader:
    print(row)

