#!/usr/bin/env python3

# SOURCE: https://code-maven.com/python-timeout

import signal
import time

class TimeOutException(Exception):
    pass
    
def alarm_handler(signum, frame):
#    print("ALARM signal received")
    raise TimeOutException()
    
def loop(n):
    for sec in range(n):
        print("sec {}".format(sec))
        time.sleep(1)

# Sets handler
signal.signal(signal.SIGALRM, alarm_handler)

def setAlarm(seconds):
    signal.alarm(seconds)

def turnOffAlarm():
    signal.alarm(0)
    
# e.g...
#signal.alarm(8)
#
#try:
#    loop(6)
#except TimeOutException as ex:
#    print(ex)
#signal.alarm(0)
#
#loop(6)
    
    
def prettyTime(seconds, shorter=True):
    h=seconds//3600
    m=(seconds%3600)//60
    s=(seconds%3600)%60
    if shorter:
        return f'{h} h {m} m {s:.2f} s'
    else:
        return f'{h} hours {m} mins {s:.2f} sec'