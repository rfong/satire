import feature_opt

def main():
	feature_opt.prep("training")
#	feature_opt.calculate_vocab("slang-vocabulary", "slang-optimized-vocabulary", "training")
	feature_opt.stats("slang-optimized-vocabulary", "slang-class-training", "slang-probs-training", "training")

	feature_opt.prep("test")
	feature_opt.stats("slang-optimized-vocabulary", "slang-class-test", "slang-probs-test", "test")

main()
