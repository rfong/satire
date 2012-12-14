# estimates probability that the test docs are satire
import util, json
import time
import operator
from scipy.stats import norm

probs = {}
classifiers = {}
doclens = {}
presence = {}
scores = {}

truedocs = []

separator = 0

r_n = 0			# recall denominator = # of results that should have been returned

def main():
	prep("training")
	train()
	score("probabilities/topicality-training", "training")
	stats("classifications/topicality-training", "topicality-plot-training", "training")
	prep("test")
	score("probabilities/topicality-test", "test")
	stats("classifications/topicality-test", "topicality-plot-test", "test")

def prep(type):
	global probs
	global classifiers
	global doclens
	global truedocs

	global r_n

	probs = {}
	classifiers = {}

	# read classifiers
	for line in open(util.projdir + "/corpus/"+type+"-class", "r"):
		c = line.split(' ')
		classifiers[c[0].split('-')[1]] = c[1].split('\n')[0]

	in_doc = {}
	r_n = 0
	# read counts
	tmp_probs = {}
	for docid,c in classifiers.iteritems():
		probs[docid] ={}
		if c=="satire":
			r_n += 1
		if c=="true" or type=="test":
			truedocs.append(docid)
		tmp_probs[docid] = util.read_counts("/data/bag/"+type+"/"+type+"-"+docid)
		doclens[docid] = float(sum([c for c in tmp_probs[docid].values()]))
		for w in tmp_probs[docid].keys():
			probs[docid][w.lower()] = probs[docid].get(w,0.0)/doclens[docid] 
		in_doc[docid] = {}
		for w in probs[docid].keys():
			in_doc[docid][w] = True

def train():
	# initialize counters
	global presence
	presence = {}
	for docid in truedocs:
#		if docid in probs: 
		for w1 in probs[docid].keys():
			presence[w1] = {}

	# sum feature values
	print "summing feature values..."
	for docid in truedocs:
		for w1 in probs[docid].keys():
			for w2 in probs[docid].keys():
				presence[w1][w2] = presence[w1].get(w2,0.0) + 1.0

	# normalize
	print "normalizing..."
	for w1 in presence.keys(): 
		for w2 in presence[w1].keys():
			presence[w1][w2] /= len(doclens)

def score(output_file, type):
	fout = open(output_file, "w")

	global scores;
	scores = {}

	# calculate probs!
	print "calculating document irrelevance..."
	for docid in classifiers.keys():
		irr = 1
		for w1 in probs[docid].keys():
			if w1 in presence:
				for w2 in probs[docid].keys():
					if w2 in presence[w1]:
						irr *= (1.0-presence[w1][w2])
		irr = 1-(irr**0.1)
		scores[docid] = irr
		fout.write(type+"-"+docid + " " +str(irr) + "\n")
		#scores[docid] = irr
	#fout.write(json.dumps(scores))


# what the hell is this and why did i name it so generically
def stats(class_out, plot_out, type):
	# read probs
	fout = open(class_out, "w")
	plot = open(plot_out, "w")

	ss = sorted(scores.iteritems(), key=operator.itemgetter(0), reverse=True)

	if type=="training":
		global separator
		max_F = 0.0
		satire_count = 0.0
		satire_correct = 0.0
		separator = 0.0
		for (docid,score) in ss:
			#print docid + " " + str(score) + " " + classifiers[docid]
			satire_count += 1.0
			if classifiers[docid]=="satire":
				satire_correct += 1.0
			F = 2 * satire_correct / (r_n + satire_count)
			if F > max_F:
				max_F = F
				separator = score
		print "separator: " + str(separator)
	
	else:
		classify = {}
		data = []
		for (docid,s) in ss:
			if s>=separator:
				classify[docid] = "satire"
				data.append([s,1])
			else:
				classify[docid] = "true"
				data.append([s,-1])
		plot.write(json.dumps(data) + '\n')
		for (docid,c) in sorted(classify.iteritems(), key=operator.itemgetter(0)):
			fout.write(type+"-"+docid+" " + c + "\n")


main()
