#!/usr/bin/env python3

from os import getpid
from resource import getrusage, RUSAGE_SELF
from sys import platform
import subprocess

def getCurrentRSS(pid=None):
	return getRSS(pid)

def getRSS(pid=None):
	if not pid:
		pid = getpid()
	cmd_get_current_rss = f'ps -o rss= {pid}'
	output = subprocess.check_output(cmd_get_current_rss, shell=True)
	return int(output)

def getMaxRSS():
	return getrusage(RUSAGE_SELF).ru_maxrss

def prettyMemory(raw_val_returned_by_os):
	# os memory functions returns bytes on macOS and kB on linux
	# this takes in the raw value given by the os and converts it automatically
	OS_MEMORY_UNIT_COEFFICIENT = 1024 if not platform.startswith('darwin') else 1
	return bytes_to_human_readable_string(raw_val_returned_by_os * OS_MEMORY_UNIT_COEFFICIENT)

def bytes_to_human_readable_string(size,precision=2):
# SOURCE: https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python/14822210
# http://code.activestate.com/recipes/578019-bytes-to-human-human-to-bytes-converter/
	suffixes=['B','KB','MB','GB','TB']
	suffixIndex = 0
	while size > 1024 and suffixIndex < 4:
		suffixIndex += 1 #increment the index of the suffix
		size = size/1024.0 #apply the division
	return "%.*f%s"%(precision,size,suffixes[suffixIndex])