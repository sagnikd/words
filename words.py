#!/usr/bin/env python
"""Modules from extracting words from Membean"""
from xml.dom import minidom
from urllib import urlopen
import nltk, re
from argparse import ArgumentParser

def urlProcessor(options):
    """Input url and returns a string of textual material"""
    url = options.url
    html = urlopen(url).read()
    raw = nltk.clean_html(html)
    return raw

class wordEngine(): 
    """input is the raw material and returns sentences using words"""
    def __init__(self, wordDict, raw):
        self.raw = raw       
        self.wordDict = wordDict
        for word in self.get_Words():
            print "%s : %s\n\n" % (word, self.get_sentences_from_word(word))
         
    def get_Words(self):
        wordsFound = []
        for word in self.wordDict.keys():
            if word in self.raw.split(" "):
                wordsFound.append(word)
        return wordsFound

    def get_sentences_from_word(self, word):
        return re.findall(r'([^\.]+%s[^\.]+)'%word, self.raw)[0].strip()

class wordDatabase(object):
    def __init__(self, wordDict):
        if not wordDict:
            self.membeanWordsUrl = \
                'http://membean.com/products/GRE/plans/Voyage/words.xml'
            self.wordDict = {}
            self.wordDict = self.createWordDict()
        else:
            self.wordDict = wordDict

    def createWordDict(self):
        self.site = urlopen(self.membeanWordsUrl)
        self.dom = minidom.parse(self.site)
        self.words_tag = self.dom.getElementsByTagName('words')[0]
        letters = self.words_tag.getElementsByTagName('letter')
        for letter in letters:
            letter_key = str(letter._attrs['id'].value)
            levels = letter.getElementsByTagName('level')
            for level in levels:
                level_key = str(level._attrs['difficulty'].value)
                words = level.getElementsByTagName('word')
                for word in words:
                    word_key = str(word.attributes.values()[0].value)
                    self.wordDict[word_key]=(letter_key,level_key)
        return self.wordDict

def main():
    """Entry Point"""
    argParser = ArgumentParser()
    argParser.add_argument("-u", "--url", dest="url", required=True,
                            help="Enter url where you want to search words")
    cmdargs = argParser.parse_args() 
    wordDict = wordDatabase(None).wordDict # None implies to use Membean Database itself
    raw = urlProcessor(cmdargs)
    wordEngine(wordDict, raw)

if __name__ == "__main__":
    main()
