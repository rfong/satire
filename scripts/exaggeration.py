import feature_opt

def main():
	# prep data
	feature_opt.prep("training")
	# optimize vocabulary
#	feature_opt.calculate_vocab("exaggeration-vocabulary", "exaggeration-optimized-vocabulary", "training")
	# record optimal linear separator
	feature_opt.stats("exaggeration-optimized-vocabulary", "exaggeration-classification-training", "exaggeration-probs-training", "training")

# NOW EVALUATE TEST DATA
	# prep data
	feature_opt.prep("test")
	# finally produce classifications!
	feature_opt.stats("exaggeration-optimized-vocabulary", "exaggeration-classification-test", "exaggeration-probs-test", "test")
	

main()
