#!/usr/bin/env python3

# https://stackoverflow.com/questions/3103178/how-to-get-the-system-info-with-python
#Shamelessly combined from google and other stackoverflow like sites to form a single function

import platform,socket,re,uuid,json,psutil,logging
import multiprocessing as mp

def getSystemInfo():
	try:
		info={}
		info['platform']=platform.system()
		info['platform-release']=platform.release()
		info['platform-version']=platform.version()
		info['architecture']=platform.machine()
		info['hostname']=socket.gethostname()
		info['ip-address']=socket.gethostbyname(socket.gethostname())
		info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
		info['processor']=platform.processor()
		info['cpu count (vCPUs):']=mp.cpu_count()
		info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
		
#		info_as_str = {str(key): str(value) for key, value in info.items()}
		
		return json.dumps({str(key): str(value) for key, value in info.items()}, indent=2)
	except Exception as e:
		logging.exception(e)
		
# json.loads(getSystemInfo())

## Output sample:
#	{
#	'platform': 'Linux',
#	'platform-release': '5.3.0-29-generic',
#	'platform-version': '#31-Ubuntu SMP Fri Jan 17 17:27:26 UTC 2020',
#	'architecture': 'x86_64',
#	'hostname': 'naret-vm',
#	'ip-address': '127.0.1.1',
#	'mac-address': 'bb:cc:dd:ee:bc:ff',
#	'processor': 'x86_64',
#	'ram': '4 GB'
#	}
		
		
## BELOW IS A COPY OF MEMORYTOOLS IN PATTERNGEN BECAUSE THIS PROJECT IS MESSY LOL (TODO)

from os import getpid
from resource import getrusage, RUSAGE_SELF
import sys
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
	OS_MEMORY_UNIT_COEFFICIENT = 1024 if not sys.platform.startswith('darwin') else 1
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
