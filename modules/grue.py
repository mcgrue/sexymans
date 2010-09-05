#!/usr/bin/env python
# coding=utf-8

import re
import web
import MySQLdb

def grue(phenny, input): 
    q = phenny.query( "SELECT * FROM quote LIMIT 1;" )
    phenny.say('wtf do you want? %s' % (q))

grue.commands = ['grue']

if __name__ == '__main__': 
    print __doc__.strip()
