"""Given short snippet of text converts it into REGULAR capitilization"""

import sys
import math
import pickle
from optparse import OptionParser # command-line option parser                                                                                                  

from silcc.lib.sentencetokenizer import SentenceTokenizer

from paste.deploy import appconfig
from sqlalchemy import select, and_, create_engine, MetaData, Table

from silcc.model.meta import metadata, Session
from silcc.config.environment import load_environment

unpickle = pickle.load(open('data/weights/capnorm_weights.pickle'))
C = unpickle[0]
V = unpickle[1]
prior = unpickle[2]
condprob = unpickle[3]



def apply_multinomial_NB(C, V, prior, condprob, dt_):
    W = dt_['tokens']
    score = {}
    for c in C:
        score[c] = math.log(prior[c])
        for t in W:
            # if the word has never been seen use 0.4?
            score[c] += math.log(condprob.get((t, c), 0.4)) 
    max_score = score[C[0]]
    max_cat = C[0]
    for k, v in score.iteritems():
        if v > max_score:
            max_score = v
            max_cat = k
    return max_cat, max_score


def regular(text, ya_,  geo_table, acro_table, engine):
    '''Convert from Regular to Regular'''
    return text
    
def german(text, ya_, geo_table, acro_table, engine):
    '''Convert from German to German'''
    return text
    
def allcaps(text, ya_, geo_table, acro_table, engine):
    '''Convert from AllCaps to Regular'''
    ab_ = []
    for i, xb_ in enumerate(ya_):
        ab_.append(xb_[1])
        #Add Cap Type Specific Rules
        if (xb_[0] == 'CAPITALIZED_STOPWORD' or 
            xb_[0] == 'CAPITALIZED' or xb_[0] == 'FIRST_CAPITALIZED_STOPWORD' 
            or xb_[0] == 'FIRST_CAPITALIZED'or xb_[1] == 'A'):
            
            ab_[i] = ab_[i].lower()
        #End of Rules
    text = ' '.join(ab_)
    return text
    
def shout(text, ya_, geo_table, acro_table, engine):
    '''Convert from shout to Regular'''
    conn = engine.connect()
    text = text.lower()
    ab_ = []
    for i, xb_ in enumerate(ya_):
        ab_.append(xb_[1])
        #Add Cap Type Specific Rules
        if (xb_[0] != 'ACRONYM'):
            ab_[i] = ab_[i].lower()
        if (xb_[0] == 'FIRST_SHOUT_STOPWORD' or xb_[0] == 'FIRST_SHOUT'):
            ab_[i] = ab_[i].capitalize()

        
        #Query Places Database, if present then convert to Capitalize
        sel = select([geo_table.c.name],  geo_table.c.name == xb_[1])    
        result = conn.execute(sel)
        j=0
        for row in result:
            j+=1
        if j > 0:
            ab_[i] = ab_[i].capitalize()
                
        
        #Query Acronmys Database, if present then convert to shout
        sel = select([acro_table.c.name],  acro_table.c.name== xb_[1])   
        result = conn.execute(sel)
        j=0
        for row in result:
           j+=1
        if j > 0:
            ab_[i] = ab_[i].upper()
        
        #End of Rules
        
    text = ' '.join(ab_)
    return text
    
def lower(text, ya_, geo_table, acro_table, engine):
    '''Convert from lower to Regular'''
    conn = engine.connect()
    ab_ = []
    for i, xb_ in enumerate(ya_):
        ab_.append(xb_[1])
        #Add Cap Type Specific Rules
        if (xb_[0] == 'FIRST_LOWER_STOPWORD' or xb_[0] == 'FIRST_LOWER'):
            ab_[i] = ab_[i].capitalize()
        if (xb_[0] == 'ACRONYM'):
            ab_[i] = ab_[i].upper()

        #Query Places Database, if present then convert to Capitalize
        sel = select([geo_table.c.name],  geo_table.c.name == xb_[1])    
        result = conn.execute(sel)
        j=0
        for row in result:
            j+=1
        if j > 0:
            ab_[i] = ab_[i].capitalize()
                
        
        #Query Acronmys Database, if present then convert to shout
        sel = select([acro_table.c.name],  acro_table.c.name== xb_[1])   
        result = conn.execute(sel)
        j=0
        for row in result:
           j+=1
        if j > 0:
            ab_[i] = ab_[i].upper()
        
        #End of Rules
        
        #End of Rules
    text = ' '.join(ab_)
    return text

def other(text, ya_, geo_table, acro_table, engine):
    '''Leave as it is'''
    return text


class NormalizerException(Exception):
    pass 
    
class Normalizer(object):
    """Normalizer class for which instance should be created"""

    def __init__(self, engine):
        self.engine = engine
        self.geo_table = Table('countries', metadata, autoload=True, autoload_with=engine)
        self.acro_table = Table('acronyms', metadata, autoload=True, autoload_with=engine)
        
    
    
    def normalizer(self, text):
        """To be called with the text string and returns normalized version"""
        
        dt_ = dict(text=text)
        ya_ = SentenceTokenizer.tokenize(dt_['text'])
        dt_['tokens'] = [xb_[0] for xb_ in ya_]
        result = apply_multinomial_NB(C, V, prior, condprob, dt_)[0]
        
        geo_table = self.geo_table
        acro_table = self.acro_table
        engine = self.engine

        # example of reading from the db
#        country_table = self.country_table
#        query = select([country_table.c.name], from_obj=[country_table])
#        for country_row in Session.execute(query):
#            print country_row

        #print result
        
        switch_normalizer = {
        'REGULAR' : regular, 
        'GERMAN' : german, 
        'ALLCAPS' : allcaps, 
        'SHOUT' : shout, 
        'LOWER' : lower }
        text = switch_normalizer.get(result, other)(text, ya_, geo_table, acro_table, engine)
        return text.replace(' .', '.')
    

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
    N = Normalizer(engine=engine)
    print N.normalizer(text)


  
    
