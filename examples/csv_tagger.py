import re
import sys
import csv

from silcc.lib.basictagger import BasicTagger

#current tagging
reader = csv.reader(open('data/training/muti_submissions.csv')) #assuming you are in parent directory
btag = BasicTagger()
for line in reader:
    print btag.tag(line[1])  #starting from zero, substitite 1 for your desired coloumn number
