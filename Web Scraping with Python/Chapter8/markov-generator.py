#!encoding=utf-8

from urllib.request import urlopen
from random import randint

def wordListSum(wordList):
    sum = 0
    for word, value in wordList.items():
        sum += value
    return sum

def retrieveRandomWord(wordList):

    randIndex = randint(1, wordListSum(wordList))
    for word, value in wordList.items():
        randIndex -= value
        if randIndex <= 0:
            return word


def buildWordDict(text):
    '''
    数据清洗
    '''
    #替换换行符，除去引号
    text = text.replace("\n", " ")
    text = text.replace("\"", "")



    punctuation = [',','.',';',':']

    for symbol in punctuation:
        text = text.replace(symbol, " "+symbol+" ") #在标点符号前后加空格


    words = text.split(" ")
    #Filter out empty words
    words = [word for word in words if word != ""] #除去空单词

    wordDict = {}
    for i in range(1, len(words)):
        if words[i-1] not in wordDict:
            #Create a new dictionary for this word
            wordDict[words[i-1]] = {}
        if words[i] not in wordDict[words[i-1]]:
            wordDict[words[i-1]][words[i]] = 0
        wordDict[words[i-1]][words[i]] += 1

    return wordDict

text = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(), 'utf-8')
wordDict = buildWordDict(text)

#生成长度为100的马尔可夫链

#单词数组的格式： {word_a : {word_b : 2, word_c : 1, word_d : 1}}
#               表示：word_a 出现4次 有两次是跟在word_b,一次word_c，一次word_d
#那么“word_a”可能就有带 50% 概率的箭头指向 “word_b”(四次中的两次),带 25% 概率的箭头指向“word_c”,还有带 25% 概率的箭头指向“word_d”

#最后一个单词的考虑： 因为可能一个单词的后面没有单词

length = 100
chain = ""
currentWord = "I"
for i in range(0, length):
    chain += currentWord+" "
    #print(wordDict[currentWord])
    currentWord = retrieveRandomWord(wordDict[currentWord])

print(chain)
