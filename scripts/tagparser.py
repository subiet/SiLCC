"""Provides the BasicTagger class which tags English language text"""
import logging
import sys
import csv

import nltk

from optparse import OptionParser # command-line option parser                                                                                                  
from paste.deploy import appconfig
from sqlalchemy import select, and_, create_engine, MetaData, Table
from pylons import app_globals
from silcc.config.environment import load_environment

from silcc.model import meta
from silcc.lib.basictagger import BasicTagger

        
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
    bt = BasicTagger(engine = engine)
    fcsv = open('data/training/trial.csv', "rb")
    reader = csv.reader(fcsv)
    for row in reader :
        tags = bt.tag(row[1])
        print tags
    fcsv.close()


