"""Modules from extracting words from Membean"""

from xml.dom import minidom
import urllib

class MembeanResource(object):
    
    def __init__(self):
        membeanWordsUrl = 'http://membean.com/products/GRE/plans/Voyage/\
                           words.xml'
        wordDict = {}
    def createWordDict(self):    
        site = urllib.urlopen(self.membeanWordsUrl)
        dom = minidom.parse(site)                i
        words_tag = dom.getElementsByTagName('words')[0]
        letters = words_tag.getElementsByTagName('letter')
        for letter in letters:
            letter_key = str(letter._attrs['id'].value)
            #wordDict[letter_key]={}
            levels = letter.getElementsByTagName('level')
            for level in levels:
                level_key = str(level._attrs['difficulty'].value)
                #wordDict[letter_key][level_key]={}
                words = level.getElementsByTagName('word')
                #wordDict[letter_key][level_key]=[]
                for word in words:
                    word_key = str(word.attributes.values()[0].value)
                    #wordDict[letter_key][level_key].append(word_key) 
                    wordDict[word_key]=(letter_key,level_key)
         return wordDict
    
    def createWordDict(self):
             
    def mapLevelsToWords(self):
        
