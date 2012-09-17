import feature_opt

def main():
	# prep data
	feature_opt.prep("training")
	# optimize vocabulary
#	feature_opt.calculate_vocab("vocabularies/exaggeration", "vocabularies/exaggeration-optimized", "training")
	# record optimal linear separator
	feature_opt.stats("vocabularies/exaggeration-optimized", "classifications/exaggeration-training", "probabilities/exaggeration-training", "training")

# NOW EVALUATE TEST DATA
	# prep data
	feature_opt.prep("test")
	# finally produce classifications!
	feature_opt.stats("vocabularies/exaggeration-optimized", "classifications/exaggeration-test", "probabilities/exaggeration-test", "test")
	

main()
