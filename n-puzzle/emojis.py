#!/usr/bin/env python3

from pprint import pp

emoji = [
	'\N{PUSHPIN}',					# "pinned" settings to wrapper instance
	'\u2699\uFE0F',	  #GEAR 	# settings obv		P.S. just {GEAR} prints like a tiny font
	'\N{SHOPPING TROLLEY}',			# shopping cart: args?
	'\N{INPUT SYMBOL FOR NUMBERS}',	 # this is like an 8-puzzle omg !!!!
	'\N{OPEN MAILBOX WITH RAISED FLAG}',  #ARGS?
	'\N{POSTBOX}',					# ARGS?
	'\N{BASKET}',		# ARGS?
	'\N{PACKAGE}',					# ... DATA? ARGS?
	'\N{WRAPPED PRESENT}',			# if box = args before calling solver, wrapped box = after
	'\N{OCTAGONAL SIGN}',
	'\N{CONSTRUCTION SIGN}',		# SETUP/ ARGS?
	'\N{BUILDING CONSTRUCTION}',	# SETUP / ARGS?
	'\N{LUGGAGE}',  #args?? lol
	'\N{OIL DRUM}',					# DATABASE
	'\N{HANDSHAKE}',				# DB CONNECTION
	'\N{LINK SYMBOL}',				# DB CONNECTION
	'\N{WRENCH}',
	'\N{HAMMER AND WRENCH}',		# SETTINGS OBVS
	'\U0001f92c',					# CURSING FACE - FOR EXCEPTION LOL
	'\U0001F60E',					# SOLUTION FOUND LOL (smiley face with glasses)
	'\U0001f575\uFE0F',				# 'SEARCH AGENT'
	'\u270F\uFE0F', #PENCIL			# WRITE TO FILE..
	'\N{ALARM CLOCK}',
	'\N{STOPWATCH}',	# doesn't look great in terminal
	'\N{WATCH}',		# looks a bit nicer i think	
	'\u23F3',	#"HOURGLASS NOT DONE"
	'\u231B',	#"HOURGLASS DONE'
	'\N{SPIRAL NOTE PAD}',		# logfile..?
	'\N{DIRECT HIT}',  			# bullseye  / OPTIMAL SOLUTION
	'\N{CARD FILE BOX}',     	# DB ?
	'\u2696\uFE0F', #scales		# TIME VS SPACE COMPLEXITY / TRADEOFF
	'\N{HEAVY PLUS SIGN}',
	'\N{HEAVY MINUS SIGN}',
	'\U000FEB53', # "HEAVY MULTIPLICATION SIGN" - prints in dingbat font otherwise
	'\N{SQUARED ID}', # ID  # this code was hard to find: here: http://www.iemoji.com/view/emoji/350/symbols/id-button
	'\N{WORLD MAP}',  	# path
	'\N{SKULL}',   # killed search early / timeour
	'\N{BOMB}', '\N{FIRECRACKER}' ,  #... signify timeout setting?? lol
	'\u2620\uFE0F', # "SKULL AND CROSSBONES"
	'\N{OPEN LOCK}',
	'\N{LOCK}',
	'\N{BROOM}',   # cleaning up after Keyboard interrupt ayyy?
	'\u2328\uFE0F',  #  Keyboard interrupt  or 'manual input'
	'\N{BALLOT BOX WITH CHECK}', 
	'\N{CLAPPER BOARD}',  # "Action!" 
	'\N{file cabinet}',   #db
	'\N{bar chart}',   # 'results'
	'\N{HUNDRED POINTS SYMBOL}',  #100!
	"\u270D\uFE0F",  # "WRITING HAND" ... like writing file.. ✍️'
	'\N{RECEIPT}',   # log... vs results bar chart? ayyy? 
	'\N{LABEL}',   # for runID / base file nickname?
	'\N{CRYSTAL BALL}',   # SEARCHING FOR ANSWERS? AYY?
	'\N{test tube}',   #args lol
	'\N{RIBBON}'
]


printable = ''
for i, em in enumerate(emoji):
	if i % 5 == 0:
		printable = ''.join([printable, '\n\n'])
	printable = ''.join([printable, f'\t {em}'])
printable = printable+'\n'
print(printable)