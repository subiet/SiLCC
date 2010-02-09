import nltk
from nltk import pos_tag
from nltk import word_tokenize
from nltk import wordpunct_tokenize
import re
import feedparser  
import HTMLParser
import sqlite3
import json
import urllib2

"""
####################
#### Needs      ####
####################
* function to work with populating a table
* function should test whether part of the table has been tagged
* train corpus on handling non-english primitives

"""

class Stripper(HTMLParser.HTMLParser):
    def __init__(self):
        self.reset()
        self.fed=[]
    def handle_data(self,d):
        self.fed.append(d)
    def get_fed_data(self):
        return "".join(self.fed)

    # for links that have the format http://twitter.com/api/cnn
def discreteWord(link):
    s = link.split('/')
    return s[len(s)-1]

    ######################################################
"""This searches the twitter api for current feeds"""    
def replace(self,sw):
    f="http://search.twitter.com/search.atom?q=%s"%sw
    return f
######################################################

def link_to_user(text):
    t = text.split()
    for i in t:
        if i.startswith('@'):
            return "http://twitter.com/"+i
    
def feedObject(search_word):
    f = feedparser.parse("http://search.twitter.com/search.atom?q=%s"%search_word)
    descr = [i.description for i in f.entries]
    newdescr = []
    for j in descr:
        x = Stripper()
        x.feed(j)
        newdescr.append(x.get_fed_data())
    return newdescr
    # function that will extract the url to the user!
    
def searchword(link):
    x = wordpunct_tokenize(link)
    if x[len(x)-1] == 'com':
        return False
    else:
        return x.pop()
    #x = "http://search.twitter.com/vicmiclovich"

    # a function that cleans the string by removing punctuation symbols from name!
    
def linkify_tweet(tweet):
    tweet = re.sub(r'(\A|\s)@(\w+)',
                   r'\1@<a href="http://www.twitter.com/\2">\2</a>',
                   tweet)
    return re.sub(r'(\A|\s)#(\w+)',
                  r'\1#<a href="http://search.twitter.com/search?q=%23\2">\2</a>',
                  tweet)

    """
        def tokenize(text):
            pattern = r'''(?x)   # strip embedded whitespace
            \w+              # sequences of 'word' characters
            | \$?\d+(\.\d+)? # currency amounts e.g. $12.53
            | (A-Z]\.) +     # abbreviations like U.S.A.
            | [^\w\s]+       # sequences of punctuation
            | \@?\d+(\.\d+)?
            '''
        return nltk.tokenize.regexp_tokenize(text,pattern)
    """

# punctuation is regex compile statement; much faster.
punctuation = re.compile(r'[.,;:!]')

def twitterSearch(feed):
    """
    A twitter is an entity.. denoted by @<some name> e.g. @vicmiclovich, @cnn, etc.
    """
    feed_list = feed.split()
    x = []
    for i in feed_list:
        if i.startswith("@"):
            x.append(punctuation.sub("",i))
        else:
            x.append(None)
    """Implement the part that should strip off all None values to only keep fixed values"""
    y = []
    for i in x:
        if i != None:
            y.append(i)
    if not y:
        return None
    return y[0] # indexed at zero for testing purposes: How would you store a list of tags?
    # I will have this converted to json
    
def get_hash_tag(feed):
    """
    This is normally called the hashtag (# tag) by twitter
    """
    feed_list = feed.split()
    x = []
    for i in feed_list:
        if i.startswith("#"):
            x.append(punctuation.sub("",i))
        else:
            x.append(None)
    y = []
    for i in x:
        if i != None:
            y.append(i)
    if not y:
        return None
    return y[0] # indexed at zero for testing purposes; this list usually contents other tags... 
    
def urlsearch(feed):
    """
    A simple function that looks for urls
    """
    x = [i for i in feed.split() if i.startswith("http://")]
    return x
            
def createTag(xdict):
    """
    POS tag??? or should it be a brille tag... 
    This up for debate... with good reason btw!
    """
    tagged_corpus = []
    for text in xdict:
        tagged_corpus.append(pos_tag(word_tokenize(text['text'])))
    return tagged_corpus

# will use couchDB because of json support
def connectToDatabase(db):

    conn = sqlite3.connect(db)
    return conn

def askuser(tweet):
	# ask user to tag tweet as either Good or Noise
	# use g for good, and n for noise
	x = str(raw_input(tweet))
	return x
################################
askuser("hello!")
"""
tweets = ([(tweet,'good')
			for tweet in tweetbucket("good.json")]
			# the user will create a good.json file for good tweets
			+
		  [(tweet,'noise')
		  	for tweet in tweetbucket("noise.json")
		  	# the user will create a noise.json file for noisey tweets
import random
random.shuffle(tweets)
featuresets??? what should this contain?
"""

j = open('geotagged_tweets_from_haiti.json')

jsonobjects = [i for i in j]

l = [json.loads(j) for j in jsonobjects]
from pprint import pprint

x = [(i['id'],i['from_user'],i['text']) for i in l]

"""Are the ids unique enough to be Database ids???"""
ids = [i['id'] for i in l]
#pprint(sorted(ids))


#tagged_list = [nltk.pos_tag(nltk.word_tokenize(j)) for j in x ]

y = []
#for tweet in x:
#	y = nltk.word_tokenize(tweet)
#	y = [i for i in y if i != 'RT']

term_extractor = []  	
#predictive_tag = [] # keywords or more important terms in text
#symbols = ['@','#']
#predictive_tag = [list(set([word])) for word, tag in i if tag == 'NNP' and word not in symbols] 
#for i in tagged_list:
#	predictive_tag.append(
#		list(set([word for word,tag in i if tag == 'NNP' and word not in symbols]))
#		)
                     