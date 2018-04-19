#!/usr/bin/env python
# coding=utf-8

import simplejson as json
import sys
import re
import web
import MySQLdb, _mysql
import os

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
        print(url)        
        d = json.loads(web.get(url))

	ret = []
	
        try:        
	    if d.has_key('Error'):
	        return ['Bzzt: %s' % d['Error'] ]
	    elif d.has_key('quotes'):
	        q = d['quotes'];
	    elif d.has_key('q'):
	        q = d['q'];
	    elif d.has_key('quote'):
	        q = d['quote'];
	    else:
	        return ['Is website down?']
	
	    ### make it so it never splits the link
            quote = q
	    quote = quote + (u'  (- http://pingpawn.com/q/%s )' % (str(d['id'])) ) 
			
	    quote = u' '.join(quote.splitlines())
	    print('after split: %s' % (quote))		
		
	    while len(quote) > 450:
                ret.append( quote[:450] )
                quote = quote[450:]
        
            ret.append( quote )
	except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print(e.message)
       
        return ret
    
    def cmd_default(self, args):
        print args        
        if len(args) > 0 or (len(args) == 1 and args[0] == ''):
            txt = '+'.join(args)
            url = 'http://api.pingpawn.com/search?size_limit=800&q=%s' % txt
            return self._do_quote(url)
        else:
            return self._do_quote('http://api.pingpawn.com/rand?size_limit=800')

    
    def cmd_indexed(self, idx, args):

	if len(args) >= 2 and (args[0] == 'from' or args[0] == 'FROM'):
		_from = args[1]
		txt = '+'.join(args[2:])
	else:
		txt =  '+'.join(args)
		_from = '~~~NOBODY~~~'

	url = 'http://api.pingpawn.com/search/%s/%s/?q=%s' % (_from, idx, txt)
	return self._do_quote(url)
	
        #return ['indexed: ' + txt]
	#return ['Indexed #%s %s "%s" - %s' % (idx, _from, txt, url)]
    

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
	if len(args) >= 2 and (args[0] == 'from' or args[0] == 'FROM'):
		_from = args[1]
		txt = '+'.join(args[2:])
	else:
		txt =  '+'.join(args)
		_from = ''

	url = 'http://api.pingpawn.com/count/%s?q=%s' % (_from, txt)

	d = json.loads(web.get(url))

        return ['count: %s' % d['my_count']]
    
    def cmd_help(self, input):
        return ['quo, quo from <quotefile>, quo # from <quotefile>, quo count <phrase>, quo count from <quotefile> <phrase>, quo <phrase>, quo # <phrase>']
    
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
