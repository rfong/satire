import feature_opt

def main():
	feature_opt.prep("training")
#	feature_opt.calculate_vocab("vocabularies/slang", "vocabularies/slang-optimized", "training")
	feature_opt.stats("vocabularies/slang-optimized-vocabulary", "classifications/slang-training", "probabilities/slang-training", "training")

	feature_opt.prep("test")
	feature_opt.stats("vocabularies/slang-optimized-vocabulary", "classifications/slang-test", "probabilities/slang-test", "test")

main()
