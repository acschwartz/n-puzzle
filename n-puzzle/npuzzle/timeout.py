#!/usr/bin/env python3

# SOURCE: https://code-maven.com/python-timeout

import signal
import time

class TimeOutException(Exception):
	print('>> TimeOutException raised')
	pass
	
def alarm_handler(signum, frame):
#	print("ALARM signal received")
	raise TimeOutException()
	
def loop(n):
	for sec in range(n):
		print("sec {}".format(sec))
		time.sleep(1)
		
signal.signal(signal.SIGALRM, alarm_handler)

def setAlarm(seconds):
	signal.alarm(seconds)

def turnOffAlarm():
	signal.alarm(0)
	
# e.g...
#signal.alarm(8)
#
#try:
#	loop(6)
#except TimeOutException as ex:
#	print(ex)
#signal.alarm(0)
#
#loop(6)