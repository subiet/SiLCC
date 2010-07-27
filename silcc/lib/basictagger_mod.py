"""Provides the BasicTagger class which tags English language text"""
"""Mod for adjective-noun association, would work for newspaper headlines & not tweets"""
import logging
import sys
import csv

import nltk

from optparse import OptionParser # command-line option parser                                                                                                  
from paste.deploy import appconfig
from sqlalchemy import select, and_, create_engine, MetaData, Table
from pylons import app_globals
from silcc.config.environment import load_environment

from silcc.lib.util import CIList, stop_words # , capitalization_type
from silcc.lib.basictokenizer import BasicTokenizer
from silcc.lib.singularizer import singularize
from silcc.lib.normalizer import Normalizer


log = logging.getLogger(__name__)

# nltk POS codes:
# NN - noun
# NNP - proper noun
# NNS - plural noun
# VBD - verb 

pos_include = ('NN', 'NNP', 'NNS')
pos_adj = ('JJ',  'JJR')

                 
class BasicTagger(object):
    """BasicTagger class for tagging English text"""

    def __init__(self, engine):
        self.engine = engine

    @classmethod
    def tag(cls, text):

        
        if not text:
            return []

        text = text.replace("'", "")
        bt = BasicTokenizer()
        
        #Call to Capitalization Normalizer.
        n = Normalizer(engine=engine)

        text = n.normalizer(text)
        tokens = bt.tokenize(text)
        pos = nltk.pos_tag(tokens)

        for word_ in pos:
            print word_
        
        # Only return those tokens whose pos is in the include list
        #tags = [t[0] for t in pos if t[1] in pos_include]
        
        tags = []
        
        for i, t in enumerate(pos):
            if (i>0 and (pos[i-1][1] in pos_adj) and (pos[i][1] in pos_include)  and (not(pos[i][0] in stop_words)) and (not(pos[i-1][0] in stop_words))):
                temp = pos[i-1][0] + " " + pos[i][0]
                tags.append(temp)
           #if(pos[i][1] in pos_include):  #uncomment for repeating individually also   
            elif(pos[i][1] in pos_include and (not(pos[i][0] in stop_words))):
                tags.append(pos[i][0])
    
        # Now exclude stopwords...
        tags = [t for t in tags if not t in stop_words]
        
        # Call Singularize
        tags = [singularize(t) for t in tags]
    
        # We want to preserve the order of tags purely for esthetic value
        # hence we will not use set()
        # We will also preserve uppercased tags if they are the first occurence
        #print tags
        tags_ = CIList()

        for t in tags:
            if t in tags_: 
                continue
            if len(t) < 2: 
                continue
            tags_.append(t)

        return tags_
        
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--ini',
                      help='INI file to use for application settings',
                      type='str',
                      default='development.ini')
    parser.add_option('--text',
                      help='Enter text to tag',
                      type='str',
                      default='This is a sample tagging text')
    (options, args) = parser.parse_args()
    
    conf = appconfig('config:' + options.ini, relative_to='.')
    load_environment(conf.global_conf, conf.local_conf)
    
    engine = create_engine(conf['sqlalchemy.url'], echo=False)
    text = options.text
    tags = BasicTagger.tag(text)
    print tags
