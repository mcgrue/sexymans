#!/usr/bin/env python
# coding=utf-8

import re
import web
import MySQLdb, _mysql

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
        
        if len(args) >= 2 and is_numeric(args[1]):
            idx = int(args[1])
            return self.cmd_indexed(idx, args[2:])
        
        if len(args) > 1 and self.cmds.has_key(args[1].lower()):
            func = self.cmds[args[1].lower()]
            
            if func:
                return func(args[2:])
                
        return self.cmd_default(args[1:])
    
    def _quote_format(self, quote, idx=0):
        
        if idx > 0:
            quote = quote +  ('  (— http://pingpawn.com/q/%d )' % (idx) ) 
                
        quote = ' '.join(quote.splitlines())
                
        ret = []
        
        while len(quote) > 450:
            ret.append( quote[:450] )
            quote = quote[450:]
        
        ret.append( quote )
        
        return ret
    
    def cmd_default(self, args):
        
        if len(args) > 0:
            txt = ' '.join(args)
            txt = _mysql.escape_string(txt)
            
            sql = "SELECT quote, id FROM quotes WHERE quote LIKE '%"+txt+"%' ORDER BY RAND() LIMIT 1" 
        else:
            sql = "SELECT quote, id FROM quotes ORDER BY RAND() LIMIT 1"
            
        res = try_query(self.phenny, sql)
            
        return self._quote_format(res['quote'], res['id'])
    
    def cmd_indexed(self, idx, args):
        try:
            txt = ''
            if len(args) > 0:
                txt = ' '.join(args)
                txt = _mysql.escape_string(txt)
                txt = " WHERE quote LIKE '%"+txt+"%' "
                
            sql = "SELECT quote FROM quotes %s LIMIT %d,1" % (txt, idx)
                
            res, = self.phenny.query(sql)
        except ValueError:
            print sql
            res = {
                'quote': 'Invalid index, mofo.'
            }
        return self._quote_format(res['quote'], idx)
    
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
            
            print "............"
            print dir(res)
            print "............"
            
        except ValueError:
            res = {
                'my_cnt': 0,
                'quote': 'That was totally out of bounds.'
            }
        
        if count:
            return self._quote_format("Count: %d" % (res['my_cnt']))
        else:
            return self._quote_format(res['quote'], res['id'])
    
    def cmd_count(self, args):
        where = ''
        if len(args):
            esc = _mysql.escape_string(' '.join(args))
            where = "WHERE quote LIKE '%"+esc+"%'"
        
        sql = "SELECT count(*) as my_cnt FROM quotes " + where
        result_set = try_query(self.phenny, sql)
        return [ ('There are %d quotes in my sexy databanks.' % (result_set['my_cnt'])) ]
    
    def cmd_list(self, input):
        sql = "SELECT count(*) as total, p.name as prf_name FROM quotes q, prfs p WHERE p.id = q.prf_id GROUP BY p.id ORDER BY total DESC"
        
        result_set = self.phenny.query(sql)
        
        txt = ''
        
        for row in result_set:
            if txt:
                txt = txt + ', '
                
            print row
            
            txt = txt + row['prf_name'] + ('(%d)' % row['total'])
        
        return ['prf counts: ' + txt]
    
    def cmd_help(self, input):
        return ['quo, quo from <dude>, quo count <phrase>, quo list, quo <phrase>']
    
    def _search_query(self, args, kwargs):
        
        kwargs.setdefault('count', False)
        kwargs.setdefault('from', False)
        kwargs.setdefault('index', False)
            
        if len(args) > 0:
            txt = ' '.join(args)
            txt = _mysql.escape_string(txt)
            
            where = " WHERE quote LIKE '%"+txt+"%' " 
        else:
            where = " WHERE 1 "
            
        if kwargs['from']:
            _from = _mysql.escape_string(kwargs['from'])
            where = where + " AND prf_id = (SELECT id FROM prfs WHERE name = '"+_from+"' ) "
            
        if kwargs['count']:
            select = "SELECT COUNT(*) as my_cnt FROM quotes "
        else:
            select = "SELECT quote, id FROM quotes "
            
        if kwargs['index']:
            n = kwargs['index']
            limit = " LIMIT %d, 1 " % (n)  
        else:
            limit = " ORDER BY RAND() LIMIT 1 "
        
        sql = select + where + limit
        
        return sql

def is_numeric(str):
    try:
        int(str)
    except ValueError:
        return 0
    return 1

def try_query(phenny, sql):
    try:
        res, = phenny.query(sql)
    except ValueError:
        res = {'quote': 'That query was dumb.'}
        
    return res
    
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
