#!/usr/bin/env python3


# RANDOM NOTE: a lot of the food emojis (fruit, veg, etc) would be real cute popping up wrandomly
# on my terminal.. cherries or avocado.. (:
# NOTE: iemoji.com  almost always has the correct python character NAMES, compared to rest


minimemoji = '\U0001F469\U0001F3FB\u200D\U0001F4BB'
myskin = '\U0001f3fb'


emoji = [
    '\N{PUSHPIN}',                    # "pinned" settings to wrapper instance
    '\u2699\uFE0F',      #GEAR     # settings obv        P.S. just {GEAR} prints like a tiny font
    '\N{SHOPPING TROLLEY}',            # shopping cart: args?
    '\N{INPUT SYMBOL FOR NUMBERS}',     # this is like an 8-puzzle omg !!!!
    '\N{ABACUS}',
    '\N{OPEN MAILBOX WITH RAISED FLAG}',  #ARGS?
    '\N{CLOSED MAILBOX WITH RAISED FLAG}',  #ARGS in run header?
    '\N{POSTBOX}',                    # ARGS?
    '\u2709\uFE0F', # ENVELOPE        # ARGS?
    '\N{BASKET}',        # ARGS?
    '\N{PACKAGE}',                    # ... DATA? ARGS?
    '\N{WRAPPED PRESENT}',            # if box = args before calling solver, wrapped box = after
    '\N{OCTAGONAL SIGN}',
    '\N{CONSTRUCTION SIGN}',        # SETUP/ ARGS?
    '\N{BUILDING CONSTRUCTION}',    # SETUP / ARGS?
    '\N{LUGGAGE}',  #args?? lol
    '\U0001F3F4\u200D\u2620\uFE0F',  # Pirate flag - ARRRRRGS? (:  
    '\N{OIL DRUM}',                    # DATABASE
    '\N{HANDSHAKE}',                # DB CONNECTION
    '\N{LINK SYMBOL}',                # DB CONNECTION
    '\N{WRENCH}',
    '\N{HAMMER AND WRENCH}',        # SETTINGS OBVS
    '\U0001f92c',                    # CURSING FACE - FOR EXCEPTION LOL
    '\U0001F60E',                    # SOLUTION FOUND LOL (smiley face with glasses)
    '\U0001f575\uFE0F',                # 'SEARCH AGENT'
    '\u270F\uFE0F',                    # PENCIL    # WRITE TO FILE..
    '\N{ALARM CLOCK}',
    '\N{STOPWATCH}',    # doesn't look great in terminal
    '\N{WATCH}',        # looks a bit nicer i think    
    '\u23F3',# HOURGLASS - IN PROOGRESS
    '\u231B',# HOURGLASS DONE
    '\N{SPIRAL NOTE PAD}',        # logfile..?
    '\N{DIRECT HIT}',          # BULLSEYE   / OPTIMAL SOLUTION
    '\N{CARD FILE BOX}',         # DB ?
    '\u2696\uFE0F',      #SCALES        # TIME VS SPACE COMPLEXITY / TRADEOFF
    '\N{HEAVY PLUS SIGN}',
    '\N{HEAVY MINUS SIGN}',
    '\u2716\uFE0F', # "HEAVY MULTIPLICATION SIGN" - prints in dingbat font otherwise
    '\N{SQUARED ID}', # ID  # this code was hard to find: here: http://www.iemoji.com/view/emoji/350/symbols/id-button
    '\N{WORLD MAP}',      # path
    '\N{SKULL}',   # killed search early / timeour
    '\N{BOMB}', '\N{FIRECRACKER}' ,  #... signify timeout setting?? lol
    '\u2620\uFE0F', # "SKULL AND CROSSBONES"
    '\N{OPEN LOCK}',
    '\N{LOCK}',
    '\N{BROOM}',   # cleaning up after Keyboard interrupt ayyy? / cleanu after exiting in general
    '\N{BROOM}\N{DOOR}',
    '\N{Door}\N{Broom}',
    '\N{Door}\N{Runner}',
    '\u2328\uFE0F',  # - KEYBOARD.   Keyboard interrupt  or 'manual input'
    '\u2611\uFE0F', # "BALLOT BOX WITH CHECK" (CHECKMARK IN BOX)
    '\u2714\uFE0F', # HEAVY BLACK CHECK  (otherwise dingbat)
    '\N{CLAPPER BOARD}',  # "Action!" 
    '\N{file cabinet}',   #db
    '\N{bar chart}',   # 'results'
    '\N{HUNDRED POINTS SYMBOL}',  #100!
    "\u270D\uFE0F",  # "WRITING HAND" ... like writing file.. ✍️'
    '\N{RECEIPT}',   # log... vs results bar chart? ayyy? 
    '\N{LABEL}',   # for runID / base file nickname?
    '\N{CRYSTAL BALL}',   # SEARCHING FOR ANSWERS? AYY?
    '\N{test tube}',   #args lol
    '\N{RIBBON}',
    '\N{HEART WITH RIBBON}',
    '\N{GLOWING STAR}',
    '\N{white medium STAR}',   # ⭐ IT'S A REGULAR FUCKING STAR LOL 
    '\U0001f92b',  # "SHUSHING FACE"     # DELETE FILES AFTER FAILED RUN?
    '\N{PILE OF POO}', 
    '\N{WASTEBASKET}',     
    '\N{Put Litter In Its Place Symbol}',  # "Bye garbage!"
    '\N{PANCAKES}', # STACK!! that's really clever 
    '\U0001F9F6',  # Ball of yarn, for traceback??
    '\N{Spaghetti}',  # (tracebak?? lol?)
    '\N{Steaming bowl}',  # RAMEN
    '\N{Pretzel}',    # same tho
    '\N{POUTING CAT FACE}',
    '\N{Derelict House Building}',
    '\U0001F643',  # upside down smiley (:
    '\N{oil drum}\N{fire}',
    '\N{PILE OF POO}\N{Fire}', 
    '\N{FIRE}\N{PILE OF POO}', 
    '\N{Wastebasket}\N{Fire}', 
    '\N{Link Symbol}\u200d\N{Cross mark}',
    '\N{PILE OF POO}\u2668\uFE0F', 
    '\N{Derelict House Building}\N{FIRE}',
	'\N{Personal Computer}',
	'\N{Fire}\N{Personal Computer}',
	'\N{Personal Computer}\N{Fire}',
	'\N{Personal Computer}\N{SPAGHETTI}',
	'\N{Personal Computer}\N{STEAMING BOWL}',
	'\N{Personal Computer}\N{Pile of Poo}',
	'\u2328\uFE0F\N{Pile of Poo}',
	'\u2328\uFE0F\N{Fire}',
	'\N{Reversed Hand with Middle Finger Extended}', # MIDDLE FINGER lol
	'\N{Personal Computer}\N{Reversed Hand with Middle Finger Extended}',
    '\u2328\uFE0F\u26A0\uFE0F', #keyboard + warning
    '\u2328\uFE0F\U0001F447', # keyboard + finger press
    '\u2328\uFE0F\u203C\uFE0F', # keyboard + !!
    '\u2328\uFE0F\u2757\uFE0F', # keyboard + !
    '\u2328\uFE0F\U0001F6D1', # keyboard + stop sign
#	'\N{}',
#	'\N{}',
#	'\N{}',
#	'\N{}',
#	'\N{}',
#	'\N{}',
]



ExceptionEmojis = [ 
	'\N{NO ENTRY SIGN}',
	'\u26A0\uFE0F',  # {WARNING}/caution (which prints as dingbat)
#	'\U0001f92c',  # CUSSIN' MAD FACE
#	'\u2049\uFE0F', #'u\N{EXCLAMATION QUESTION MARK}', (o/w dingbat)
	'\N{SOS}',  
	'\N{Fire}' ,  
	'\N{Fire Extinguisher}' , 
	'\N{COLLISION SYMBOL}',  # Bang!
	'\N{CROSS MARK}', # BIG RED X
	'\U0001F921',  #  CLOWN FACE LOL
	'\U0001f974',  # 'WOOZY' / SCRUNCHED UP FACE
	'\U0001f644',  #  EYE ROLLING FACE
	'\N{PILE OF POO}',
	'\N{THUMBS DOWN SIGN}',
	'\N{Derelict House Building}',	# lol
	'\U0001F9D0',  # FACE W/ MONOCLE
	'\U0001F928',  # FACE W/ RAISED EYEBROW
	'\N{Grimacing Face}',  # CRINGE
	'\N{Popcorn}', #lol
	'\N{POUTING CAT FACE}',
	'\N{SKULL}',
    '\N{oil drum}\N{fire}',
    '\N{Spaghetti}',  # (tracebak?? lol?)
    '\N{Steaming bowl}',  # RAMEN
    '\N{Pretzel}',    # same tho
    '\N{Derelict House Building}\N{FIRE}',
	'\N{Personal Computer}\N{STEAMING BOWL}',
	'\N{Personal Computer}\N{Pile of Poo}',
    f'{minimemoji}\N{Fire}',
]



ArgsEmojis = [
    '\N{SPEECH BALLOON}', 
    '\N{ABACUS}',
    '\N{HEAVY PLUS SIGN}', 
    '\N{WRAPPED PRESENT}', 
    '\N{HEAVY PLUS SIGN}'
]

solverEmojiSet = [
    '\N{ROBOT FACE}', 
    '\N{BRAIN}', 
    '\N{RAT}',  
    '\N{ABACUS}',  
    '\U0001F50D',
    '\U0001F50E',
    '\N{DIRECT HIT}',
    '\N{JIGSAW PUZZLE PIECE}'
]




if __name__ == '__main__':
    #printGridlike(num_cols, rowSepStr, ):
    printable = ''
    for i, em in enumerate(emoji):
        if i % 5 == 0:
            printable = ''.join([printable, '\n\n\n'])
        printable = ''.join([printable, f'\t {em}'])
    printable = printable+'\n'
    print(printable)