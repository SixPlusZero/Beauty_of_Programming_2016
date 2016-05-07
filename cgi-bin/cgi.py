#!/usr/bin/python
import sys
from sys import argv

if len(argv)!=3:
        print 'Error: Illegal argument number!'
        print argv
        sys.exit(0)

try:
        id1 = int(argv[1])
        id2 = int(argv[2])
except ValueError:
        print 'Error: Illegal arguments!'
        sys.exit(0)

print '[[%d, %d]]' % (id1, id2)

