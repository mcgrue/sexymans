#!/usr/bin/env python
# coding=utf-8

# This file is awful but functional.  
# There should be an easier way to build a query from component parts.
# Need to think about it...

import re
import web
import MySQLdb, _mysql

def is_numeric(str):
	try:
		int(str)
	except ValueError:
		return 0
	
	return 1

class Quote():
	def __init__(self, phenny):
		self.phenny = phenny
		self.cmds = {}
		self.cmds['from'] = self.cmd_from 
		self.cmds['count'] = self.cmd_count 
		self.cmds['list'] = self.cmd_list 
		self.cmds['help'] = self.cmd_help
	
	def do(self, input):
		args = input.split(' ')
		
		if len(args) == 2 and is_numeric(args[1]):
			return self.cmd_indexed(int(args[1]))
		
		if len(args) > 1 and self.cmds.has_key(args[1].lower()):
			func = self.cmds[args[1].lower()]
			
			if func:
				return func(args[2:])
				
		return self.cmd_default(args[1:])
	
	def _quote_format(self, quote):
		
		ret = []
		
		while len(quote) > 450:
			ret.append( quote[:450] )
			quote = quote[450:]
		
		ret.append( quote )
		
		return ret
	
	def cmd_from(self, args):
		
		count = 0
		
		if len(args) < 1:
			return ['From whom?']
		
		dictargs = {
			'from' : args[0]
		}
		
		if len(args) >= 2 and args[1].lower() == 'count':
			count = dictargs['count'] = 1
			
		elif len(args) >= 2 and is_numeric(args[1]):
			index = int(args[1])
			if index < 0:
				index = -index
			dictargs['index'] = index
			
		try:
			args  = args[1:]
					
			sql = self._search_query(args, dictargs)
		
			res, = self.phenny.query(sql)
		except ValueError:
			res = {
				'my_cnt': 0,
				'quote': 'That was totally out of bounds.'
			}
		
		if count:
			return self._quote_format("Count: %d" % (res['my_cnt']))
		else:
			return self._quote_format(res['quote'])
	
	def cmd_count(self, args):
		where = ''
		if len(args):
			esc = _mysql.escape_string(' '.join(args))
			where = "WHERE quote LIKE '%"+esc+"%'"
		
		sql = "SELECT count(*) as my_cnt FROM quote " + where
		result_set, = self.phenny.query(sql)
		return [ ('There are %d quotes in my sexy databanks.' % (result_set['my_cnt'])) ]
		
	def cmd_list(self, input):
		sql = "SELECT count(*) as total, prf_name FROM quote GROUP BY prf_name ORDER BY total DESC"
		result_set = self.phenny.query(sql)
		
		txt = ''
		
		for row in result_set:
			if txt:
				txt = txt + ', '
				
			txt = txt + row['prf_name'] + ('(%s)' % row['total'])
			
		return ['prf counts: ' + txt]

	def cmd_help(self, input):
		return ['quo, quo from <dude>, quo count <phrase>, quo list, quo <phrase>']
		
	def _search_query(self, args, kwargs):
		
		kwargs.setdefault('count', False)
		kwargs.setdefault('from', False)
		kwargs.setdefault('index', False)
			
		if len(args) > 1:
			args = args[1:]
			txt = ' '.join(args)
			txt = _mysql.escape_string(txt)
			
			where = " WHERE quote LIKE '%"+txt+"%' " 
		else:
			where = " WHERE 1 "
			
		if kwargs['from']:
			_from = _mysql.escape_string(kwargs['from'])
			where = where + " AND prf_name = '"+_from+"' "
			
		if kwargs['count']:
			select = "SELECT COUNT(*) as my_cnt FROM quote "
		else:
			select = "SELECT quote FROM quote "
			
		if kwargs['index']:
			n = kwargs['index']
			limit = " LIMIT %d, 1 " % (n)  
		else:
			limit = " ORDER BY RAND() LIMIT 1 "
		
		sql = select + where + limit
		
		#print sql
		
		return sql
		
	def cmd_default(self, args):
		
		if len(args) > 0:
			txt = ' '.join(args)
			txt = _mysql.escape_string(txt)
			
			print "escaped: (%s)" % (txt)
			
			sql = "SELECT quote FROM quote WHERE quote LIKE '%"+txt+"%' ORDER BY RAND() LIMIT 1" 
		else:
			sql = "SELECT quote FROM quote ORDER BY RAND() LIMIT 1"
			
		res, = self.phenny.query(sql)
			
		return self._quote_format(res['quote'])
		
	def cmd_indexed(self, idx):
		try:
			sql = "SELECT quote FROM quote LIMIT %d,1" % (idx)
				
			res, = self.phenny.query(sql)
		except ValueError:
			print sql
			res = {
				'quote': 'Invalid index, mofo.'
			}
		return self._quote_format(('Quote #%d: ' % (idx) ) + res['quote'])

def quo(phenny, input):
	
	q = Quote(phenny)
	
	res = q.do(input)
	
	if res:
		for line in res:
			phenny.say(line)
	else:
		phenny.say('What is this I don\'t even :(')

quo.commands = ['quo']

if __name__ == '__main__': 
    print __doc__.strip()
