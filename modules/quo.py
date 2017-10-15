#!/usr/bin/env python
# coding=utf-8

import simplejson as json
import sys
import re
import web
import MySQLdb, _mysql

class Quote():
    def __init__(self, phenny):
        self.phenny = phenny
        self.cmds = {}
        self.cmds['from'] = self.cmd_from 
        self.cmds['count'] = self.cmd_count 
        self.cmds['help'] = self.cmd_help
    
    def do(self, input):
        
        args = input.split(' ')
        
        if len(args) >= 2 and is_numeric(args[1]):
            idx = int(args[1])
            return self.cmd_indexed(idx, args[2:])
        
        if len(args) > 1 and self.cmds.has_key(args[1].lower()):
            func = self.cmds[args[1].lower()]
            
            if func:
                return func(args[2:])
                
        return self.cmd_default(args[1:])
    
    def _do_quote(self, url):
        
        d = json.loads(web.get(url))
        
        if d.has_key('Error'):
            return ['Something done fucked up.']
        elif d.has_key('quotes'):
            q = d['quotes'];
        elif d.has_key('q'):
            q = d['q'];
        else:
            return ['Is website down?']
        
        ### make it so it never splits the link.
        quote = q['quote'] +  (u'  (- http://pingpawn.com/q/%s )' % (q['id']) ) 
                
        quote = u' '.join(quote.splitlines())
                
        ret = []
        
        while len(quote) > 450:
            ret.append( quote[:450] )
            quote = quote[450:]
        
        ret.append( quote )
        
        return ret
    
    def cmd_default(self, args):
        
        if len(args) > 0:
            txt = '+'.join(args)
            url = 'http://api.pingpawn.com/search?size_limit=800&q=%s' % txt
            return self._do_quote(url)
        else:
            return self._do_quote('http://api.pingpawn.com/rand?size_limit=800')
    
    def cmd_indexed(self, idx, args):
        return ['Indexed.']
    
    def cmd_from(self, args):
        _from = args[0]
        args = args[1:]

        if len(args) > 0:
            txt = '+'.join(args)
            url = 'http://api.pingpawn.com/search/%s?q=%s' % (_from, txt)
            return self._do_quote(url)
        else:
            return self._do_quote('http://api.pingpawn.com/rand/%s' % _from)
    
    def cmd_count(self, args):
        return ['-1']
    
    def cmd_help(self, input):
        return ['quo, quo from <quotefile>, quo # from <quotefile>, quo count <phrase>, quo <phrase>, quo # <phrase>']
    
def is_numeric(s):
    try:
        i = float(s)
    except ValueError:
        return False # not numeric
    else:
        return True# numeric

def quo(phenny, input):    
    try:
        q = Quote(phenny)
        res = q.do(input)
        for line in res:
            phenny.say(line)
    except:
        print "Unexpected error:", sys.exc_info()[0], sys.exc_info()[1]
        phenny.say('No.')

quo.commands = ['quo']

if __name__ == '__main__': 
    print __doc__.strip()
