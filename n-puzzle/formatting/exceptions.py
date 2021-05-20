#!/usr/bin/env python3

import inspect
import os
import traceback
from random import randint

from formatting.colors import color
from formatting.emoji import ExceptionEmojis as emojis
from formatting.txt_elements import *
from formatting.stringtools import center_by_padding

emoji_KInt = '\u2328\uFE0F\u203C\uFE0F' # keyboard + !!

# P.S. / TODO: all these lovely formatting and tool functions like (prettyTime, prettyMemory), shoud be stored
# nicely on their own and then imported into every file in the project.
# e.g. have a file for formatting variables like the separators i've made for wrapper (where I split this code from
# because surprise... I needed my exception "handler" across the project lol
# TODO  TODO  TODO  TODO  TODO :)


def random_emoji():
    try:
        i = randint(0, len(emojis)-1)
        return emojis[i]
    except:
        return 'X'


def lineno():
    """Returns the current line number in the program."""
    return inspect.currentframe().f_back.f_lineno


def printException(exc, lineNo, verbose=True):
    print('\n\n')
    
    exc_name = type(exc).__name__
    remark = f'\nexception caught by {os.path.basename(__file__)} '\
            f'line {lineNo}'
    print(color( 'black', remark ))
    
    separator = color('red2', 
                      center_by_padding('X', MAX_LINE_LENGTH, 'X'))
    
    deco = '\u26A0\uFE0F' # caution sign emoji
    title = color('red2', 
                    center_by_padding(
                        f'  {deco}   E X C E P T I O N  {deco}   ', 
                        MAX_LINE_LENGTH+1, 
                        padding_char='*'))
    
    # print header
    print(f'{separator}\n', color('red2', title), f'\n{separator}')
    
    # next, subtitle of sorts: a succinct description
    deco_left = emoji_KInt if isinstance(exc, KeyboardInterrupt) \
                else random_emoji()
    deco_right = ''   # nothing right now
    
    print(color('red2', f' \n  {deco_left}   {exc_name} : '), 
          color('yellow2', f'{str(exc)} {deco_right}'))
    
    if verbose:
        # print traceback
        deco_tb = '\U0001F9F6'  # ball of yarn.. ha ha get it..?
        print(color(
                'white', 
                f'\n{deco_tb} {traceback.format_exc()}'))
        
        # print stack
        deco_stk = '\N{PANCAKES}'
        print(f'\n{deco_stk} Stack:')
        traceback.print_stack()
    
    print(f'\n{separator}\n')
    
    if isinstance(exc, SystemExit):
        pass 