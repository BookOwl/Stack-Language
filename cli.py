from __future__ import with_statement
from __future__ import absolute_import
import sys
from stack import interpeter
from io import open
print u'***Stack 2.0 Program Runner***'
print u"Running on Python", sys.version.split()[0]
while True:
    filename = raw_input(u'Enter file name (nothing to exit): ')
    if not filename: break
    try:
        with open(filename) as f:
            prog = f.read()
        print u'\n***STARTING PROGRAM***'
        try:
            interpeter.interpet(prog)
        except SystemExit:
            pass
        print u'***ENDING PROGRAM***'
    except IOError:
        print u'The file %s does not exist!' % filename
