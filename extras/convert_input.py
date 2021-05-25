import pickle

f_in = open("input/100_random_8puzzles.txt", "r")
lines = f_in.readlines()
f_in.close()
puzzles = [tuple([int(n) for n in line.split()]) for line in lines]
print(puzzles)

picklefile = "input/100_random_8puzzles_listoftuples.p"
f_out = open(picklefile, "wb")
pickle.dump(puzzles, f_out, protocol=0)  #human-readable protocol
f_out.close()

f_in = open(picklefile, "rb")
unpickled_puzzles = pickle.load(f_in)
print(unpickled_puzzles)