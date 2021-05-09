#!/usr/bin/env python3

from resource import getrusage, RUSAGE_SELF
from sys import platform

MAXRSS_UNIT_COEFFICIENT = 1024 if not platform.startswith('darwin') else 1

def getMaxRSS():
	return getrusage(RUSAGE_SELF).ru_maxrss


def rawMaxRSStoPrettyString(raw_maxrss):
	# get_maxrss returns bytes on macOS and kB on linux. this handles that for you.
	return bytes_to_human_readable_string(raw_maxrss * MAXRSS_UNIT_COEFFICIENT)


def bytes_to_human_readable_string(size,precision=2):
# SOURCE: https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python/14822210
# http://code.activestate.com/recipes/578019-bytes-to-human-human-to-bytes-converter/
	suffixes=['B','KB','MB','GB','TB']
	suffixIndex = 0
	while size > 1024 and suffixIndex < 4:
		suffixIndex += 1 #increment the index of the suffix
		size = size/1024.0 #apply the division
	return "%.*f%s"%(precision,size,suffixes[suffixIndex])