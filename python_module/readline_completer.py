#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   wh
#   E-mail  :   wh_linux@126.com
#   Date    :   12/12/19 17:13:09
#   Desc    :   Test
#
import readline
import logging

class SimpleCompleter(object):
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            if text:
                self.matches = [s for s in self.options
                                if s and s.startswith(text)]
            else:
                self.matches = self.options[:]

        try:
            response = self.matches[state]
        except IndexError:
            response = None

        return response

def input_loop():
    line = ''
    while line != 'stop':
        line = raw_input("Prompt ('stop' to quit): ")
        print 'Dispatch %s' % line

OPTIONS = ['start', 'stop', 'list', 'print']
readline.set_completer(SimpleCompleter(OPTIONS).complete)
readline.parse_and_bind('tab: complete')
input_loop()

