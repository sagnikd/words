"""Modules from extracting words from Membean"""

from xml.dom import minidom
from urllib import urlopen
import nltk

class WordDatabase():
    
    def __init__(self):
        self.membeanWordsUrl = 'http://membean.com/products/GRE/plans/Voyage/\
                           words.xml'
        self.wordDict = {}
        self.createWordDict()

    def createWordDict(self):    
        site = urlopen(self.membeanWordsUrl)
        dom = minidom.parse(site)               
        words_tag = dom.getElementsByTagName('words')[0]
        letters = words_tag.getElementsByTagName('letter')
        for letter in letters:
            letter_key = str(letter._attrs['id'].value)
            #self.wordDict[letter_key]={}
            levels = letter.getElementsByTagName('level')
            for level in levels:
                level_key = str(level._attrs['difficulty'].value)
                #self.wordDict[letter_key][level_key]={}
                words = level.getElementsByTagName('word')
                #self.wordDict[letter_key][level_key]=[]
                for word in words:
                    word_key = str(word.attributes.values()[0].value)
                    #self.wordDict[letter_key][level_key].append(word_key) 
                    self.wordDict[word_key]=(letter_key,level_key)
        return self.wordDict

class urlProcessor():
    """Input url and returns a string of textual material"""
    def __init__(self, url):    
        self.wordDict = self.WordDatabase()
        self.url = url
        self.raw = self.makeUrlReady(self.url)

    def makeUrlReady(self, url):
        html = urlopen(url).read()
        raw = nltk.clean_html(html)
        return raw

class wordEngine(urlProcessor)    
    """input is the raw material and returns sentences using words"""
    def __init__(self, raw):
        if not self.raw:
            self.raw = raw       

    def get_Words(self):
        wordsFound = []
        for word in self.wordDict.keys():
            if word in self.raw.split(" "):
                wordsFound.append(word)
        print wordsFound
        return wordsFound

    def get_sentences_from_word(self, word):
        return re.findall(r'(.+%s.+)\.'%word, self.raw)[0].strip()



        
        
