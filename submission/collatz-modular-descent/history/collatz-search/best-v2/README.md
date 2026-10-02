# Collatz modular descent search, generation 2

`solution.json` is the strongest full-universe result found by the exhaustive
search in `../search.py`. It contains 107 rules and covers 3,352 of the 3,968
possible target classes. The selected minimum contraction margin is 13/256,
whose evaluator metric floor is 50,781 ppm.

The search enumerated 10,641 valid rule instances for every odd residue at
modulus powers 2 through 12 and every allowed prefix through 24 steps. It
reduced these to 3,423 strongest same-support rules, then to 649 rules after
removing only ancestor rules that had a superset of targets and at least as
large a margin. The final 107-rule set is a minimum-cardinality cover at the
best margin threshold and stays below the 512-rule limit.

Full exact uncovered target classes, grouped by target modulus power and with
the exhaustive non-coverability reason attached to each class, are in
`search-report.json`.

Compared with the 22-rule candidate: coverage increases by 469 classes
(2,883 to 3,352), rule count increases by 85, and the weakest margin decreases
from 5/32 (156,250 ppm) to 13/256 (50,781 ppm). One hundred percent coverage
is impossible under this evaluator: 616 target classes have no valid stable
contractive rule at any modulus power no greater than the target's power.

Every enumerated and selected rule was checked both by an independent verifier
and by the evaluator's `_verify_rule` implementation. No AutoLab submission was
made.
