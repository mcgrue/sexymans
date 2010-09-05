#!/usr/bin/env python
# coding=utf-8

import re
import web
import MySQLdb

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
		
		if len(args) > 1 and self.cmds.has_key(args[1].lower()):
			func = self.cmds[args[1].lower()]
			
			if func:
				return func(input)
			
		return self.cmd_default(input)
	
	def cmd_from(self, input):
		return ['from!']
	
	def cmd_count(self, input):
		return ['count!']
		
	def cmd_list(self, input):
		return ['list!']

	def cmd_help(self, input):
		return ['help!']
	
	def cmd_default(self, input):
		return ['default!']


def quo(phenny, input):
 
    q = Quote(phenny)
    
    res = q.do(input)
    
    for line in res:
	phenny.say(line)

quo.commands = ['quo']

if __name__ == '__main__': 
    print __doc__.strip()
