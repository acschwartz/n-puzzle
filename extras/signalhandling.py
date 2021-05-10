#!/usr/bin/env python3

# Not using now, might need later

# Source: https://stackoverflow.com/questions/24426451/how-to-terminate-loop-gracefully-when-ctrlc-was-pressed-in-python

import signal, sys, time
terminate = False

def signal_handling(signum,frame):           
	global terminate                         
	terminate = True                         
	
signal.signal(signal.SIGINT,signal_handling) 
x=1                                          
while True:                                  
	print("Processing file #",x,"started...")
	time.sleep(1)                            
	x+=1                                     
	if terminate:                            
		print("I'll be back")                 
		break                                
print("bye")                                  
print(x)