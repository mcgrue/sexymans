#!/usr/bin/env python

import os, sys, urllib, random
cmd_folder = os.path.dirname(os.path.abspath(__file__))
cmd_folder = os.path.join(cmd_folder, "jm_names")
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

import names


def name(phenny, input): 
   origterm = input.groups()[1]
   if not origterm: 
      return phenny.say('usage: name <gender>')
   term = origterm.encode('utf-8')

   term = term.lower()
   if term not in ['male', 'female', 'random']:
      return phenny.say('gender must be male, female, or random. other genders not supported, pervert')
   
   if term == 'random':
      term = random.choice(['male, female'])
   if term == 'male':
      return phenny.say(names.get(True))
   return phenny.say(names.get(False))


name.commands = ['name']
name.priority = 'high'

if __name__ == '__main__': 
   print __doc__.strip()
