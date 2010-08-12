"""Provides the BasicTagger class which tags English language text"""
import logging
import sys
import csv

import nltk
from silcc.lib.util import CIList
from optparse import OptionParser # command-line option parser                                                                                                  
from paste.deploy import appconfig
from sqlalchemy import select, and_, create_engine, MetaData, Table
from pylons import app_globals
from silcc.config.environment import load_environment

from silcc.model import meta
from silcc.model.meta import metadata, Session
from silcc.lib.basictagger import BasicTagger
from silcc.lib.goog import ser

class TagParserException(Exception):
    pass


class TagParser(object):
    """ Load up a DB with tags """
    def __init__(self,engine):
        self.engine = engine
        self.tag_table = Table('tag', metadata, autoload=True, autoload_with=engine)
        self.tag_assoc_table = Table('tag_assoc', metadata, autoload=True, autoload_with=engine)

    def loaddb(self,tags):
        #Variables
        engine = self.engine
        tag_table = self.tag_table
        tag_assoc_table = self.tag_assoc_table
        conn = engine.connect()
        tag_list = []
        tup_list = []
        
        
        #Alphabetical sort and lowercase conversin
        tags = [s.lower() for s in tags]
        tags.sort()

        #Generating Tag pairs
        for i in (range(0, (len(tags))-1)):
            for j in range((i+1),len(tags)):
                tup_list = [tags[i],tags[j]]
                tag_list.append(tup_list)
        print "-----------------------"
        print tag_list
        print "-----------------------"
        
        #Loading Tags in the Database if not present, individually
        for t in tags:
            query_ = select([tag_table.c.tag], tag_table.c.tag == t)
            result = conn.execute(query_)
            j=0
            for row in result:
                j+=1
            if j == 0:
                #Call to Google Results
                #count = ser(t)
                count = 1;
                insert = tag_table.insert().values(tag = t, g_no = count)
                conn.execute(insert)
                #print t + " " + count
                
        #For each tag pair, query Tag_assoc
        for i in range(0, (len(tag_list))):
            query_ = select([tag_table], tag_table.c.tag == tag_list[i][0])
            result = conn.execute(query_)
            ans = result.fetchone()
            tag1_id = ans['id']
            
            query_ = select([tag_table], tag_table.c.tag == tag_list[i][1])
            result = conn.execute(query_)
            ans = result.fetchone()
            tag2_id = ans['id']
            
            query_ = select([tag_assoc_table],
                        and_(
                            tag_assoc_table.c.tag_one_id == tag1_id,
                            tag_assoc_table.c.tag_two_id == tag2_id)
                    )
            result = conn.execute(query_)
            

            j=0
            for row in result:
                new_score = row[tag_assoc_table.c.score] + 1
                assoc_id = row[tag_assoc_table.c.id]
                j+=1

##            print new_score
##            print assoc_id 
            
            if j == 0:
                insert_ = tag_assoc_table.insert().values(tag_one_id = tag1_id, tag_two_id = tag2_id, score = 1)
                conn.execute(insert_)
            else:
                update_ = tag_assoc_table.update().where(tag_assoc_table.c.id == assoc_id).values(score = new_score)
                conn.execute(update_)

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
    tp = TagParser(engine = engine)
    fcsv = open('data/training/muti_submissions.csv', "rb")
    reader = csv.reader(fcsv)
    for row in reader :
        print row[0]
        tags = basict.tag(row[1])
        tp.loaddb(tags)
    fcsv.close()


