# Collatz modular descent, generation 3

V3 preserves the complete 3,352-class cover and optimizes the second metric exactly.

It uses 107 rules and covers 3,352/3,968 target classes. The achieved minimum margin is 13/256 (50781 ppm), equal to the theoretical per-target upper bound.

The other 616 classes are uncoverable: for each one, exhaustive enumeration found no valid stable contractive rule at any allowed modulus power no greater than its target power. The exact list and bottleneck targets are in `search-report.json`.

Rule selection retained narrower higher-margin rules; it only merged identical supports by keeping their strongest rule. The selected dyadic supports are inclusion-maximal at the optimal threshold, which proves minimum rule count at that threshold. Every generated and written rule was independently checked against the evaluator logic. No AutoLab submission was made.
