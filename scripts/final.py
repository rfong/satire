import util
from scipy.stats import norm

features = ["exaggeration", "slang", "topicality"]
classifiers = util.read_class("corpus/test-class")
weight = {}
cl = {}

for f in features:
	cl[f] = util.read_class("scripts/classifications/"+f+"-test")
	tpr = 0.0
	fpr = 0.0
	pos_class = 0
	neg_class = 0
	for docid,c in cl[f].iteritems():
		if c=="satire":
			pos_class += 1
			if classifiers[docid]=="satire":
				tpr += 1
		else:
			neg_class += 1
			if classifiers[docid]=="satire":
				fpr += 1
	tpr /= pos_class
	fpr /= neg_class
	weight[f] = abs(norm.ppf(norm.cdf(tpr)) - norm.ppf(norm.cdf(fpr)))
	print weight[f]

fout = open("classifications/final", "w")
for docid in classifiers.keys():
	score = 0.0
	for f in features:
		if cl[f][docid]=="satire":
			score += weight[f]
		else:
			score -= weight[f]
	fout.write(docid + " ")
	if score>=0:
		fout.write("satire\n")
	else:
		fout.write("true\n")
