## THOUGHTS DUMP ON ENCODING & IMPLEMENTATION OF FRINGE PATTERN


BIG PICTURE INPUT: "a normal 15 puzzle" is given to solver
solver calls heuristic. heuristic queries db based on the state's PATTERN

we want to store the 15-puzzle state as bytes in the DB - p easy to encode/decode and saves room

So......
input to solver: state(0,1,2,3,4,5....,15)  (where each index is a location and each number/value is a tile)
but here in PDB land we only care about the PATTERN 

(state representation) ---CONVERT----> (pattern representation) ----ENCODE----> (encoded DB key)

our pattern info:
	PATTERN_INFO = {
		'15puzzle_fringe': {
			# 0  -  -  3
			# -  -  -  7
			# -  -  -  11
			# 12 13 14 15
			
					'dim': 4,	# 15-puzzle is 4x4
					'pattern tiles': (3, 7, 11, 12, 13, 14, 15),
					'goal state': (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15),
					'empty tile': 0,
	#				'encode': encode15puzzle_fringe_DummyTile,
	#				'decode': decode15puzzle_fringe_DummyTile,
					},

we only care about the locations of 8 tiles  (technically just 7 but we also need to store the 0/empty tile somehow)
since bytes hold an even number of hex digits, we will store the position of the empty tile within the pattern, 
unlike our implementation of the 8-puzzle. this means the generator will have different logic.
for example, we must think about the way that states are stored in the frontier, explored set, etc.
if no pattern tiles move (i.e. the cost doesn't change'), but the zero tile moves, that is still a distinct state that 
must be tracked properly or it will completely mess up the pathfinding of the search agent.

also we were handling the 8-puzzle nodes in a 'creative way' because the empty tile was not represented within the
pattern's encoding or database key... but in this pattern, we have room for it, and in fact those 2 bits would be used
whether we store a meaningful value or  a throwaways one.
So we will store the zero - this has implications for the size of the in-memory explored set.

From test runs, we've found that the database is too slow to be used as an explored set for that many nodes, being constantly queried.
It was E X T R E M E L Y slow. Slower than any of my other poor implementations, including the one that ran for 7 hours and produced
incorrect estimates :)

So we will use the database as a data store, but will have to keep an in-memory explored set as well. I believe it only needs
to contain the PATTERN representation (not node - node contains additional info, etc), as long as it meaningfully distinguishes it from 
states that share the same placement of numbered pattern tiles. This should work well with the chosen pattern representation & encoding
which includes the empty tile. 

In my previous attempt to implement the fringe PDB, I tried to plug-and-play into the framework I already built for the 8-puzzle.
The intent was to have the framework be generalizable with the addition of pattern-specific functions. This seemed like a good idea
because the high-level logic of pattern generation is the same - a "backwards" BFS from the goal state.
However, making the logic more generalizable? abstractable? abstract? ... lol.. is a performance tradeoff.
A major issue was the actual representations of the nodes - since the 8-puzzle "pattern" had an even number of squares, it fit
perfectly into bytes, and there was no room to represent the empty tile, nor did it make sense to do so - in fact, it saved
space not to do so because the empty tile's location as implicit from the organization of the database- i.e. it was split into
tables 0-8, with each table containing states where the empty tile is at that index. We did not need to keep an in-memory explored set,
and could differentiate states with the same pattern tile locations (which is meaningful information and must be retained during
the search). This was a great implementation for the 8puzzle, but even then I found myself making extreme optimization like using
bitwise rather than mathematical operators, and using some non-pythonic code style (e.g. C-style for loops rather than enumerate(iterable))).
This added up to shaving second(s) off my timeit benchmarks (per 10,000 calls) -- which is significant when dealing with hundreds of
millions of records.

Trying to plug-and-play the 15-puzzle into the 8-puzzle's framework simply didn't work, especially when the 15-puzzle code needs
as many optimizations as possible to make it reasonable in runtime in memory use. (I'm sure this would be easier if I used a more
compact language like C... but I chose to use Python so here we are....)
But I digress...


So......
input to solver: state(0,1,2,3,4,5....,15)  (where each index is a location and each number/value is a tile)
but here in PDB land we only care about the PATTERN 

(state representation) ---CONVERT----> (pattern representation) ----ENCODE----> (encoded DB key)



puzzle state:						  state representation:
   4   1   2   3       ------->     ( 4, 1, 2, 3, 5, 9, 7, 0, 8, 13, 6, 10, 12, 14, 15, 11)
   5   9   7   0				     in state representation,
   8   13  6   10					  index/'key' = location of tile in puzzle board        = k?, L for loc?, p for place? pip = place in puzle?
   12  14  15  11					        value = the numbered tile					    = n (for its number tile?)  


Let's define some nomenclature..    
			values are (n)umbered tiles:    n: ( 4, 1, 2, 3, 5, 9, 7, 0, 8, 13, 6, 10, 12, 14, 15, 11 )
			indices are place in puzzle:   pip:  0  1  2  3  4  5  6  7  8  9  10  11  12  13  14  15



 pattern:						 pattern tiles:  (3, 7, 11, 12, 13, 14, 15) + "0"
.   .   .   3       ------->     we ONLY care about the locations of these tiles.
.   .   7   0				     using the whole 16-length array to represent the board now doesn't make sense
.   13  .   .					 since our pattern tiles are "set in stone" (as far as what, not where, they are)
.   14  15  11					 we can save room....

the unchanging "reference list" of pattern tiles (pTiles):
							     values are    n:   (0, 3, 7, 11, 12, 13, 14, 15) 
list indices are "id" of n in reference list:  ref:  0  1  2   3   4   5   6   7
 
If we map  n to ref  (e.g. most obviously in sorted order), we don't even need to store  n  in a pattern representation
When dealing with patterns, we don't actually care what the values of the pTiles are, we only care about their 'essence'
and location relative to where they belong. The only meaningful thing about "n" is that it represents the tile's goal
pip - but here we are STARTING at the goal and just... wandering in a systematic breadth-first manner, so it doesn't matter.

So we can simply map  pip  to  ref.  In the rare case that we need  n, we can look it up by ref in the pTiles list 
Since we ONLY care about the pattern tiles, the locations that aren't occupied by them don't need storing

So we have:
    n:   .   .   .   3   .   .   7   0   .  13    .    .   12   14   15   11 
  ref:   .   .   .   1   .   .   2   0   .   5    .    .    4    6    7    3
  pip:   .   .   .   3   .   .   6   7   .   9    .    .   12   13   14   15


pattern:						  pattern representation:
.   .   .   3       ------->      pip: ( 7  3  6  15  12  9  13  14 )
.   .   7   0				      ref:   0  1  2  3   4   5   6   7
.   13  .   .
.   14  15  11



Just to break it down as if you don't get this already
        state[pip]  ==   n
	state.index(n)  ==  pip
   pTiles.index(n)  ==  ref
	   pTiles[ref]  ==   n
      pattern[ref]  ==  pip
pattern.index(pip)  ==  ref

Yeah, you get the idea......



Now let's compress our pattern repr by encoding it.
The best way I could figure out to do it in Python was in bytes.
I wish I had thought to use C, whose easy bit manipulations would really help... alas.
Live and learn.


Since this is a 15-puzzle,  both pip and n are bounded by (0, 15]
...which just so happens to be perfectly representable in hexadecimal digits


Ss  pattern:  "7 , 3 , 6 , 15 , 12 , 9 , 13 , 14"
	becomes:   736fc9de
	
I can't think of a more efficient way to represent this information off the top of my head,
while still being able to work with it reasonably, although I'm sure one exists.
I recall in the paper that introduced the Fringe PDB, each of their database entries was only one byte? how??
(Culberson and Schaeffer '92 ? -
"Iterative-deepening A* for the 15-Puzzle was implemented using the Manhattan distance heuristic estimate (MD), fringe pattern database (FR), and corner pattern database (CO). The fringe and corner databases were built using retrograde analysis and each contains 16 × 15 × 14 × 13 × 12 × 11 × 10 × 9 = 518,918,400 positions, one byte each.6 The programs were written in C and run on a BBN TC2000 at Lawrence Livermore National Laboratory. Each database took less than one hour of real time to compute. The TC2000 has 128 processors and 1 GB of RAM. The program would load the databases into shared memory and search each test position in parallel. An experiment consisted of running the 100 test positions given by Korf (1985)."
(position = puzzle state?)


Anyway, Python doesn't let you efficiently work with other numerical bases
There's a lot of converting back-and-forth between base10.

Buy Python bytes seem to work okay for our purposes...
they're immutable like strings but also like strings, are indexed.
and they use much fewer resources than other options, predictably.


Each byte in python is treated as a "unit", so:
b =  b'x\73x\6f\xc9\xde' is made up of 4 subunits 
b[0] = '\x73' etc ..
As one "unit" it cannot really be split or indexed further unless you convert it to another type like string or int
		-which is relatively expensive when it comes to generating >500mil nodes
				(Edit: omg I just double-checked and the default # of timeit() iterations is 1,000,000 ..... I thought it was 10,000. FML.
				I double checked because the math of saving a second of execution over 10,000 ops didn't didn't seem right)
				Anyway apparently the timing isn't as big a deal as I thought (I think it was my higher-level programming that was bag- like completely
				misunderstanding the actions the search should be taking on the game board... man I am not having a good track record with this project
				but at least I'm learning a lot...)

In the byte '\x73' (\x is just the escape char in the output), the "left digit" 
73 in hex == 115 so we will need to extract each digit separately - which is just math
and I already have the formulas for. So... let's get to this
