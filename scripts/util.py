projdir="/mit/rfong/Private/6.864/proj/"

# counts a bag of words
def read_counts(filename):
	fin = open(projdir+filename, "r")
	counts = {}	# word counts
	
	for line in fin:
		i=0 # need to parse through whitespace, check if we've hit the data yet...
		for w in line.split(' '):
			if w != '':
				if i==0:
					i+=1
					count = float(w)
				else:
					word = w[0:-1]	# there's a newline hanging off the end of w
		counts[word] = count
	return counts

# counts bag of words without parts of speech
def read_counts_nopos(filename):
	fin = open(projdir+filename, "r")
	counts = {} # word counts

	for line in fin:
		i=0
		for w in line.split(' '):
			if w != '':
				if i==0:
					i+=1
					count = float(w)
				else:
					word = w.split('/')[0]
		counts[word] = count
	return counts

# parses probabilities (<word> <prob>)
def read_probs(filename):
	fin = open(projdir+filename, "r")
	probs = {}

	for line in fin:
		probs[line.split(' ')[0]] = float(line.split(' ')[1])
	return probs	

# read classifiers...
def read_class(filename):
	fin = open(projdir+filename, "r")
	c = {}
	for line in fin:
		line = line.split('\n')[0]
		c[line.split(' ')[0]] = line.split(' ')[1]
	return c

# just return the lines.
def read_bag(filename):
	fin = open(projdir+filename, "r")
	bag = []
	for line in fin:
		bag.append(line)
	return bag

# pads an int to a string with length 4
def format(i):
	i = str(i)
	if len(i)>4:
		return i[-4:-1]
	while len(i)<4:
		i = '0'+i
	return i
