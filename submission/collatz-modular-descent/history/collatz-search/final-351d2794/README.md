# Frozen final candidate: AutoLab experiment 351d2794

This directory preserves the exact 512-rule solution used by AutoLab experiment `351d2794-d842-41a1-aa86-83e11fbca2fa`, commit `57c1ad7f2af78339260fcc4d8498a05dda4cfc77`.

The candidate officially scored:

- `coverage_ppm`: 1,000,000
- `min_descent_ppm`: 525,390
- `rule_count`: 512

`solution.json` is byte-for-byte identical to `../ablation1-v4-8-113-to-5-17.json`; the SHA-256 digest is recorded in `SHA256SUMS`.

## Construction

Each rule is an exact accelerated-Collatz certificate for an odd dyadic residue class. For a prescribed valuation sequence, the evaluator checks valuation stability on the full residue class, composes the affine accelerated map, and requires strict contraction (`3^s < 2^(sum exponents)`) plus strict descent at the least representative.

The search enumerated 10,641 valid rules, independently cross-checked every generated rule against the evaluator logic, and selected at most 512 rules by public-universe coverage and per-target margin. V3 established the 3,352/3,968 mathematically coverable public classes. V4 optimized the per-target regret vector under the 512-rule limit. The frozen candidate is the controlled one-rule ablation of exact V4: replace `(8,113,[2])` with `(5,17,[2])`.

## Experiments and stopping decision

V3 officially scored `1,000,000 / 250,000 / 107`; exact V4 scored `1,000,000 / 525,300 / 512`. V5-A retained coverage but collapsed to `250,000` minimum margin. The controlled one-rule ablation, experiment `351d2794`, scored `1,000,000 / 525,390 / 512`, a 90 ppm improvement over V4. The exhaustive one-rule scan found no other promising replacement. Coordinated 2-for-2, 2-for-3, and focused 3-for-3 scans found no swap that improved any public target without worsening another. Further validation tuning was therefore stopped and this candidate was frozen.

No final/test evaluation or leaderboard publication has been triggered.
