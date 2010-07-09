"""Provides the BasicTagger class which tags English language text"""
import logging
import sys
import csv

import nltk

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

    @classmethod
    def tag(cls, text):
        """Class method that returns tags given some text"""
        if not text:
            return []

        text = text.replace("'", "")
        bt = BasicTokenizer()
        
        #Call to Capitalization Normalizer.
        n = Normalizer()
        text = n.normalizer(text)
        
        tokens = bt.tokenize(text)
        pos = nltk.pos_tag(tokens)
        for a in pos:
            print a  
        
        
        # Only return those tokens whose pos is in the include list
        #tags = [t[0] for t in pos if t[1] in pos_include]
        
        tags = []
        
        for i, t in enumerate(pos):
            if ((pos[i-1][1] in pos_adj) and (pos[i][1] in pos_include)):
                temp = pos[i-1][0] + " " + pos[i][0]
                tags.append(temp)
            elif(pos[i][1] in pos_include):
                tags.append(pos[i][0])
    
        print pos[i][0] + " " + pos[i][1]
            

        # Now exclude stopwords...
        tags = [t for t in tags if not t in stop_words]
        
        # Call Singularize
        tags = [singularize(t) for t in tags]
    
        # We want to preserve the order of tags purely for esthetic value
        # hence we will not use set()
        # We will also preserve uppercased tags if they are the first occurence

        tags_ = CIList()
        print tags
        for t in tags:
            if t in tags_: 
                continue
            if len(t) < 2: 
                continue
            tags_.append(t)

        return tags_
        
if __name__ == '__main__':
    text = sys.argv[1]
    tags = BasicTagger.tag(text)
    print tags
