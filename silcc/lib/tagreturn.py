"""returns tag or tag_id given the other one from tag table in silcc"""

from optparse import OptionParser #command-line option parser                                                                                                  
from paste.deploy import appconfig
from sqlalchemy import select, and_, create_engine, MetaData, Table
from pylons import app_globals
from silcc.config.environment import load_environment

from silcc.model import meta
from silcc.model.meta import metadata, Session

class TagReturnException(Exception):
    pass


class TagReturn(object):
    """ Load up a DB with tags """
    def __init__(self,engine):
        self.engine = engine
        self.tag_table = Table('tag', metadata, autoload=True, autoload_with=engine)
        self.tag_assoc_table = Table('tag_assoc', metadata, autoload=True, autoload_with=engine)

    def ret_tag(self,tag_id):
        engine = self.engine
        tag_table = self.tag_table
        tag_assoc_table = self.tag_assoc_table
        conn = engine.connect()
        
        query_ = select([tag_table], tag_table.c.tag_one_id == tag_id)
        result = conn.execute(query_)
        ans = result.fetchone()
        tag = ans['tag']
        return tag
    
    def ret_id(self,tag):
        engine = self.engine
        tag_table = self.tag_table
        tag_assoc_table = self.tag_assoc_table
        conn = engine.connect()
        
        query_ = select([tag_table], tag_table.c.tag == tag)
        result = conn.execute(query_)
        ans = result.fetchone()
        tag_id = ans['id']
        return tag_id