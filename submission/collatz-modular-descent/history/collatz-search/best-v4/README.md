# Collatz modular descent, generation 4

V4 keeps all 3,352 coverable target classes and uses 512 rules. It never lowers a V3 per-target margin. All individual optima require at least 649 rules, so they cannot fit within the 512-rule limit.

The exact robust optimization gives a worst regret of 45/1024 (43945 ppm), with 3084 targets at their individual optimum. The selection uses an exact tree dynamic program that lexicographically minimizes the sorted regret vector, then removes only rules that preserve every target margin.

The 616 uncoverable classes are unchanged from V3 and are exhaustively documented in `../best-v3/search-report.json`. No hill files were modified and no AutoLab submission was made.
