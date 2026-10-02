Find exact accelerated-Collatz descent rules that cover as much unseen odd residue mass as possible.

## Task

The parent question is the Collatz conjecture. This hill does not ask for a solution of it. It asks for finite, exact certificates that a whole congruence class of positive odd integers strictly decreases after a prescribed number of accelerated odd Collatz steps.

For odd `n`, one accelerated step is

```
C(n) = (3n + 1) / 2^v2(3n + 1).
```

A certificate rule fixes an odd residue class `n ≡ residue (mod 2^modulus_power)` and gives the exact 2-adic valuations encountered by repeated applications of `C`. The evaluator proves that the valuation pattern is stable for every member of the class and that the resulting affine map is strictly decreasing on that entire class.

Your goal is to cover as many secret target residue classes as possible. A target class is covered when it is a subclass of one of your certified rules. Broad rules matter more because they cover more targets. The evaluator checks only submitted data; it never runs submission code.

## Submission format

Submit a directory containing exactly one UTF-8 JSON file:

```json
{
  "rules": [
    {"modulus_power": 4, "residue": 9, "exponents": [2]},
    {"modulus_power": 4, "residue": 13, "exponents": [3]}
  ]
}
```

Every rule has:

- `modulus_power`: an integer `k` from 2 through 32;
- `residue`: an odd integer `r` with `0 < r < 2^k`;
- `exponents`: a nonempty list `[e1, ..., es]`, where `ei` is the exact value of `v2(3x+1)` at accelerated step `i`.

At most 512 rules, 24 accelerated steps per rule, and valuation exponents at most 32 are accepted. Duplicate rules are rejected.

The evaluator requires `k >= 1 + e1 + ... + es`. This makes the full valuation pattern stable across the residue class. It then proves both

```
3^s < 2^(e1 + ... + es)
C^s(n) < n for every positive n in the class.
```

The two example rules are valid: for `n ≡ 9 (mod 16)`, `C(n) = (3n+1)/4 < n`; for `n ≡ 13 (mod 16)`, `C(n) = (3n+1)/8 < n`.

## Metrics

| metric | direction | meaning |
| --- | --- | --- |
| `coverage_ppm` | max | Fraction of hidden target residue classes covered, scaled by 1,000,000. |
| `min_descent_ppm` | max | Weakest affine contraction among rules that actually cover a hidden target, scaled by 1,000,000. |
| `rule_count` | min | Number of submitted rules. |

Reports are ranked lexicographically. A `coverage_ppm` of 250000 means 25% of the hidden target classes were covered.

## Held-out split

Validation and final scoring use different private target collections. Both use odd residue classes at powers of two between 8 and 12, but their choices and weights are held out. The final score is the test-split score.

## What counts as progress

This is a compact, machine-checkable component of a modular descent program. A high score is not a proof of the Collatz conjecture. It is an exact collection of descent lemmas that a researcher can independently inspect, combine, or strengthen.
