#!/usr/bin/env python3

from math import floor, ceil
from formatting.txt_elements import *

def center_by_padding(
    text, 
    maxlinelength=MAX_LINE_LENGTH, 
    padding_char=' '):
    """
    Pad text on both sides to 'center-align' it within a fixed line.
    
    Beware of unexpected behavior if there are special hidden characters
    like color codes, unicode, or even whitespace chars (\t, \n, ...)
    the colors appended to the string,
    """
    if len(text) > maxlinelength:
        raise ValueError('len(text) > maxlinelength')
    elif len(text) == maxlinelength:
        return text
    else:
        empty_space = maxlinelength-len(text)
        leftpadding = int(floor(empty_space/2))
        rightpadding = int(ceil(empty_space/2))
        
        return ''.join([ 
                        leftpadding * padding_char, 
                        text, 
                        rightpadding * padding_char 
                    ])


def get_base_file_name(filepath):
    """'/with/or_without/path/filename.ext --> 'filename'"""
    f = filepath.split('/')
    f = f[-1]
    f = f.split('.')
    f = f[0]
    return f