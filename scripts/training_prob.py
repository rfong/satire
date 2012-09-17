# grooms training data and produces initial probabilities
# keep this file in $proj

# document x^i for i=1,...,m is a sequence of words x_1^i,...,x_n^i
# y^i for i=1,...,m is a hidden boolean. y=true --> x^i is classified as satire
	
import util 

types = ["all", "satire", "true"]

counts = {}	# word counts
sum = {}	# total word count
prob = {}	# P(y)

for type in types:
	counts[type] = util.read_counts(projdir + "/data/bag/training/count-"+type)
#	for w,c in counts[type].iteritems():
#		fout_word.write(w+' %f'%(c/sum[type])+'\n')

# P(y) forall y
#fin_type = open(projdir + "/data/bag/training/prob-type", "r")			# P(y) -- overall probability of satire categorization
#for line in fin_type:
#	sp = line.split(' ')
#	prob[sp[0]] = float(sp[1])
#for type in ["satire", "true", "all"]:
#	prob[type] = prob[type] / prob["all"]

# calculate P(y|x) forall words x in vocabulary
for type in ["satire", "true"]: # for y=true,false
	fout_doc = open(projdir + "/data/bag/training/prob-doc-"+type, "w")	# P(y|x) -- probability of satire categorization given word 
#	const = sum[type] * prob[type] / sum["all"]
#	print "const("+type+")="+str(const)
	for w,c in counts[type].iteritems():
#		print "\nc_"+type+"("+w+")=%d"%(c)
#		print "c_all("+w+")=%d"%(counts["all"][w])
#		print "c_"+type+" / c_all = %f"%(c/counts["all"][w])
		fout_doc.write(w+' %f'%( ( c / counts["all"][w] ) ) + '\n')
