#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
#   Author  :   wh
#   E-mail  :   wh_linux@126.com
#   Date    :   12/12/19 17:19:03
#   Desc    :   Readline Access Buffer
#
import readline

class BufferAwareCompleter(object):
    def __init__(self, options):
        self.options = options
        self.current_candidates = []

        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # 首次输入文本,建立匹配项
            origline = readline.get_line_buffer()
            begin = readline.get_begidx()
            end = readline.get_endidx()
            being_completed = origline[begin:end]
            words = origline.split()

            if not words:
                self.current_candidates = sorted(self.options.keys())
            else:
                try:
                    if begin == 0:
                        candidates = self.options.keys()
                    else:
                        first = words[0]
                        candidates = self.options[first]

                    if being_completed:
                        self.current_candidates = [
                            w for w in candidates
                            if w.startswith(being_completed)
                        ]
                    else:
                        self.current_candidates = candidates
                except (KeyError, IndexError), err:
                    self.current_candidates = []

            try:
                response = self.current_candidates[state]
            except IndexError:
                response = None
            return response

def input_loop():
    line = ''
    while line != 'stop':
        line = raw_input('Prompt ("stop" to quit): ')
        print 'Dispatch', line

readline.set_completer(BufferAwareCompleter(
    {'list':['files', 'directories'],
     'print':['byname', 'bysize'],
     'stop':[],}).complete)

readline.parse_and_bind('tab: complete')
input_loop()

