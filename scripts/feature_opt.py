import util
import time
import operator
import json

counts = {}			# docids to dictionary of word counts
classifiers = {}# docids to "true", "satire"
doclens = {}		# docids to doc lengths
scores = {}			# docids to doc scores for last iteration
docids = {}			# docid ranges for "training" and "test"

separator = 0

r_n = 0			# recall denominator = # of results that should have been returned

def prep(type):
	global counts
	global classifiers
	global doclens
	global scores
	global docids

	global p_n
	global r_n

	counts = {}
	classifiers = {}

	# read classifiers
	for line in open(util.projdir + "/corpus/"+type+"-class", "r"):
		c = line.split(' ')
		classifiers[c[0].split('-')[1]] = c[1].split('\n')[0]
	for docid,c in classifiers.iteritems():
		if c=="satire":
			r_n += 1
	
	# read word counts
	docids = {
		"test": [util.format(i) for i in range(1,1595+1)],
		"training": [util.format(i) for i in range(1,2638+1)]
	}
	for docid in docids[type]:
		tmpcounts = util.read_counts_nopos("/data/bag/"+type+"/"+type+"-"+docid)
		counts[docid] = {}
		for w,c in tmpcounts.iteritems():
			counts[docid][w.lower()] = c
		# these are floats because we need to divide something by them later
		doclens[docid] = float(sum([c for c in counts[docid].values()]))


def stats(vocab_file, class_out, probs_out, type):
	# read vocab
	fout = open(class_out, "w")
	vocab = open(vocab_file, "r").read().split('\n')

	# calculate new scores
	in_vocab = {}
	for v in vocab:
		in_vocab[v.lower()] = True
	ss = {}
	for docid,c in classifiers.iteritems():	
		ss[docid] = slang_slow(in_vocab, docid)
	new_scores = sorted(ss.iteritems(), key=operator.itemgetter(1), reverse=True)
	
	if type=="training":
		# k now find the linear separator
		global separator
		max_F = 0.0	# F-score
		satire_count = 0.0		# satire count so far
		satire_correct = 0.0	# correctly identified so far
		separator = 0.0
		for (docid,score) in new_scores:
			satire_count += 1.0
			if classifiers[docid]=="satire":
				satire_correct += 1.0
			F = 2 * satire_correct / (r_n + satire_count)
			if F > max_F:
				max_F = F
				separator = score
#	else:
	classify = {}
	for (docid,s) in new_scores:
		if s>=separator:
			classify[docid] = "satire"
		else:
			classify[docid] = "true"
	for (docid,c) in sorted(classify.iteritems(), key=operator.itemgetter(0)):
		fout.write(type+"-"+docid+" " + c +"\n")

	# print probabilities
	probs_out = open(probs_out, "w")
	pts = []
	for (docid,s) in new_scores:
		if classifiers[docid]=="satire":
			pts.append([s,1])
		else:
			pts.append([s,-1])
	probs_out.write(json.dumps(pts))
	probs_out.write("separator="+str(separator))
#		f.write(type+"-"+docid + " %f\n"%s)
	


# maximize accuracy over vocabulary subset.
#we only need to do this over the training set.
def calculate_vocab(vocab_file, output_file, type):
	fout = open(output_file, "w")
	vocab = [v.lower() for v in open(vocab_file, "r").read().split('\n')]

	for docid in docids[type]:
		scores[docid] = 0.0
	rem_vocab = {}		# vocab words not in curr_vocab
	for v in vocab:
		rem_vocab[v] = True
	max = -1.0			# overall max accuracy
	curr_vocab = []		# vocabulary yielding max accuracy

	# over all subset sizes
	for i in range(1, len(vocab)):
		checkpoint = time.time()
		curr_max = -1.0		# max accuracy for this iteration
		best_word = ''		# best new word of remaining usable words

		# over all usable words
		for w,val in rem_vocab.iteritems():
			if val == False:
				continue
			acc = accuracy(w)

			# this word is the best out of this set
			if acc>curr_max:
				curr_max = acc
#				print "w:"+w+", acc="+str(acc)
				best_word = w
		print str(i)+": max="+str(curr_max)+", w="+w+", %f ms"%(1000.0*(time.time() - checkpoint))

		# if the new word yielded negative improvements, quit
		if curr_max <= max:
			break

		# otherwise, the new word becomes part of the vocab
		else:
			curr_vocab.append(best_word)
			rem_vocab[best_word] = False
			max = curr_max

			# update all the scores
			for docid in docids[type]:
				scores[docid] = slang(best_word, docid)

#			print best_word + " " + str(max)

	# record final vocabulary
	for w in curr_vocab:
		fout.write(w+"\n")


# RETURN float in range [0.0, 1.0]
#  w: a new word
#  docid: format(int)
def slang(w, docid):
	# add score from new word to score from last iteration
	return scores[docid] + (counts[docid].get(w, 0) / doclens[docid])

# evaluate without prior knowledge
# RETURN float in range [0.0, 1.0]
#  in_vocab: words to True
def slang_slow(in_vocab, docid):
	score = 0.0
	# doc is bigger than vocabulary
	if len(in_vocab) > len(counts[docid]):
		score = sum( counts[docid].get(w,0) for w in in_vocab.keys() )
	# vocabulary is bigger than doc
	else:
		score = sum( c*in_vocab.get(w,False) for w,c in counts[docid].iteritems() )
	return score / doclens[docid]

# measures scoring accuracy
# RETURN float in range [0.0, 1.0]
#  w: a new word
def accuracy(w): 
#	in_vocab = {}
#	for v in vocab:
#		in_vocab[v] = True

	ss = {}	# new scores
	for docid,c in classifiers.iteritems():	
		ss[docid] = slang(w, docid)
	new_scores =  sorted(ss.iteritems(), key=operator.itemgetter(1), reverse=True)

#	sep = separability(new_scores)
#	if sep > 0:
#	return sep

#	score_satire = 0.0
#	num_satire = 0
#	score_true = 0.0
#	num_true = 0
#	for docid,c in classifiers.iteritems():	
#		score_true += (new_scores[docid] * (c=="true"))**2
#		num_true += (c=="true")
#		score_satire += (new_scores[docid] * (c=="satire"))**2
#		num_satire += (c=="satire")
#	return ((score_satire / num_satire) + (1 - (score_true / num_true)))/2

	# F-score based
	max_F = 0.0	# F-score
	satire_count = 0.0	# satire count so far
	satire_correct = 0.0# correctly identified so far
	for (docid,score) in new_scores:
		satire_count += 1.0
		if classifiers[docid]=="satire":
			satire_correct += 1.0
		F = 2 * satire_correct / (r_n + satire_count)
		if F > max_F:
			max_F = F
	return max_F


# calculate the clusteredness of the scores
def separability(new_scores):
	# maximized separator
	separator = sum(new_scores.values()) / len(new_scores)
	if separator>0: separator -= 10**(-11)
	# ok now linear regression
	score = 0.0
	for docid,c in classifiers.iteritems():
		if c=="satire":
			score += (new_scores[docid] - separator)**2
		elif c=="true":
			score -= (new_scores[docid] - separator)**2
#	print "separator:"+str(separator)+" score:"+str(score/len(classifiers))
	return score #/ len(classifiers) # whatever, it's already small enough

