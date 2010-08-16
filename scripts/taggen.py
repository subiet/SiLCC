"""Generates more tags given existing tags for reports"""
import logging
import sys
import csv

import nltk
from silcc.lib.util import CIList
# command-line option parser  
from optparse import OptionParser                                                                                                 
from paste.deploy import appconfig
from sqlalchemy import select, and_, create_engine, MetaData, Table
from pylons import app_globals
from silcc.config.environment import load_environment

from silcc.model import meta
from silcc.model.meta import metadata, Session
#from silcc.lib.basictagger import BasicTagger
from silcc.lib.basictagger_mod import BasicTagger
from silcc.lib.goog import ser, sery
from silcc.lib.tagreturn import TagReturn

class TagGenException(Exception):
    pass


class TagGen(object):
    """ Load up a DB with tags """
    def __init__(self, engine):
        self.engine = engine
        self.tag_table = Table('tag', metadata, autoload=True,
                                            autoload_with=engine)
        self.tag_assoc_table = Table('tag_assoc', metadata, autoload=True,
                                            autoload_with=engine)

    def gen(self, tags):
        #Variables
        engine = self.engine
        tag_table = self.tag_table
        tag_assoc_table = self.tag_assoc_table
        conn = engine.connect()
        tr_ = TagReturn(engine = engine)
        
        #Alphabetical sort and lowercase conversin
        tags = [s.lower() for s in tags]
        tags.sort()  
          
        #Generate More tags based on the above 
        
        #if score crosses this add directly as a tag
        itt = 80
        #if score corsses this add as a potential tag
        ictt = 30
        #if combined score of potential tag crosses this add it as a new_tag
        ctt = (len(tags)*3)+20   
        #Combined number of search result
        csr = 30000     
        
        new_tags = []
        new_tags_tag = []
        pot_tags = {"tag":0}
        t_score = 0
        for t in tags:
            tag_id = tr_.ret_id(t)                       
            query_ = select([tag_assoc_table],
                    and_(
                        tag_assoc_table.c.tag_one_id == tag1_id,
                        tag_assoc_table.c.score > ictt)
                        )
            result = conn.execut(query_)
            for row in result:
                if (row['score'] > itt and row['s_no'] > csr):
                    new_tags.append(row['tag_two_id'])
                    #Adding in pot_tags
                    t_score = row['score']
                    if row['tag_two_id'] in pot_tags.keys():
                        t_score += pot_tags[row['tag_two_id']]
                    pot_tags[row['tag_two_id']] = t_score           
                elif (row['score'] > ictt and row['s_no'] > csr):
                    t_score = row['score']
                    if row['tag_two_id'] in pot_tags.keys():
                        t_score += pot_tags[row['tag_two_id']]
                    pot_tags[row['tag_two_id']] = t_score
                else:
                    pass
            
        #add selected pot_tags to new_tags
        for a_,b_ in pot_tags.items():
            if b > ctt:
                new_tags.append(a)
        
        #convert tag_ids to tags
        for t_ in new_tags:
            new_tags_tag.append(tr_.ret_tag(t_))
        
        #remove duplicates in new_tags
        new_tags_tag = list(set(new_tags_tag))
        
        return new_tags_tag

        
        

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--ini',
                      help='INI file to use for application settings',
                      type='str',
                      default='development.ini')

    (options, args) = parser.parse_args()
    conf = appconfig('config:' + options.ini, relative_to='.')
    load_environment(conf.global_conf, conf.local_conf)
    engine = create_engine(conf['sqlalchemy.url'], echo=False)
    basict = BasicTagger(engine = engine)
    tg = TagGen(engine = engine)
    fcsv = open('data/training/trial.csv', "rb")
    fcsv = open('data/training/muti_submissions.csv', "rb")
    reader = csv.reader(fcsv)
    for row in reader :
        print row[0]
        tags = basict.tag(row[1])
        new_tag = tg.TagGen(tags)
        print tags
        print new_tags
        print "---------------------------"
  
    fcsv.close()


