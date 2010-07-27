import sys
import feedparser

from optparse import OptionParser # command-line option parser                                                                                                  
from paste.deploy import appconfig
from sqlalchemy import select, and_, create_engine, MetaData, Table

from silcc.model.meta import metadata, Session
from silcc.config.environment import load_environment
from silcc.lib.basictagger import BasicTagger

class FeedParser(object):
    """Normalizer class for which instance should be created"""

    def __init__(self, engine):
        self.engine = engine

    
    
    def feedinfo(self,  url):
        engine = self.engine
        T = BasicTagger(engine=engine)

#        feed_data = feedparser.parse(url)
#        items = feed_data.entries
#        print >> output, "Feed items:"
#        for item in items:
#            print item.title
        
        T.tag('Test Tag')


if __name__ == '__main__':
    
    parser = OptionParser()
    parser.add_option('--ini',
                      help='INI file to use for application settings',
                      type='str',
                      default='development_dump.ini')
    (options, args) = parser.parse_args()
    
    conf = appconfig('config:' + options.ini, relative_to='.')
    load_environment(conf.global_conf, conf.local_conf)
    engine = create_engine(conf['sqlalchemy.url'], echo=False)
    
    F = FeedParser(engine=engine)
    
    fh = open('data/feedlist.txt')
    line = fh.readline()
    while line:
        line = line.strip('\n')
        F.feedinfo(line)
    fh.close()


    
