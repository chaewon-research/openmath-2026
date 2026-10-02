# OpenMath 2026 — Collatz review materials

Author: **Chaewon Yoon**. This repository presents the preserved accelerated-Collatz modular descent certificate associated with AutoLab experiment **351d2794** for judge review. It contains exact artifact bytes, the full signed evaluator report, immutable commit evidence, checker code, historical supporting files, and offline replay instructions.

**This is not a proof of the full Collatz conjecture.** The result is a finite collection of 512 exact descent rules for specified infinite odd residue classes. It does not establish convergence to 1 for all positive integers.

## Preserved result

The exact AutoLab experiment is `351d2794-d842-41a1-aa86-83e11fbca2fa`; its immutable submission commit is `57c1ad7f2af78339260fcc4d8498a05dda4cfc77`. The unchanged [solution.json](submission/collatz-modular-descent/solution.json) has SHA-256 `1e533cbd5dbb17bb6ad52c7c80faa3a6abce587a32204ef5228de54da5b069e6`.

The [original signed report](submission/collatz-modular-descent/validation-report.json), dated 2026-09-29T22:09:07Z, records a passing **official validation** evaluation (`official=true`, `final=false`):

| Metric | Official value | Direction |
| --- | ---: | --- |
| coverage_ppm | 1000000 | maximize |
| min_descent_ppm | 525390 | maximize |
| rule_count | 512 | minimize |

These are private-validation metrics: 639/639 covered weight across 20 targets. Minimum descent uses each target's strongest matching affine contraction margin. They do not represent coverage of every odd integer. No final/test score or competition acceptance is established by this report.

Independent offline inspection verifies all 512 rules, covering 3352/3968 public target classes at powers 8–12. The union is exactly 1765 odd residues modulo 4096, with no upper bound on integers in those classes. See [RESULT.md](submission/collatz-modular-descent/RESULT.md) for the precise theorem, explicit residue-list location, assumptions and baseline comparisons.

## Check without AutoLab access

Use CPython **3.14.2**; no third-party dependencies or private files are required. From the repository root:

```sh
cd submission/collatz-modular-descent
sha256sum -c SHA256SUMS
python3 check.py --output /tmp/collatz-local-check.json
cmp local-check.json /tmp/collatz-local-check.json
```

Expected: all checksums `OK`, all 512 rules pass, public coverage `3352/3968`, odd-residue union `1765/2048`, and `cmp` exits 0. [REPRODUCE.md](submission/collatz-modular-descent/REPRODUCE.md) gives full commands, expected output and original Git object verification. The offline checker verifies the certificate mathematics; reproducing the official weighted score requires organizer-held private data. The HMAC report signature requires organizer verification context to authenticate.

## Repository structure

The dedicated review directory is [submission/collatz-modular-descent/](submission/collatz-modular-descent/README.md):

- `RESULT.md`, `NOVELTY.md`, `REPRODUCE.md`, `PROVENANCE.md`: result, contribution, replay and disclosures.
- `solution.json`, `validation-report.json`, `identity.json`, `IMMUTABLE_COMMIT.txt`: exact artifact and official identity evidence.
- `check.py`, `local-check.json`, `ENVIRONMENT.json`, `.python-version`, `SHA256SUMS`: public offline inspection and environment pin.
- `evidence/`, `logs/`, `public-hill/`, `history/`: immutable Git objects, original run output, public evaluator source and preserved historical code/data.
- `INVENTORY.md`, `PAPER_STATUS.md`: source inventory, historical caveats and genuine missing materials.

Local `collatz-search/` and AutoLab workspace directories are working copies; the review packet contains the relevant archived files and does not depend on those working copies. Busy Beaver work remains separate and is not part of the Collatz review packet.

A newly written [technical report source](submission/collatz-modular-descent/paper/main.tex) documents the fixed result; a [five-page PDF](submission/collatz-modular-descent/paper/main.pdf) compiled successfully. See [paper build status](submission/collatz-modular-descent/PAPER_STATUS.md). No original experiment-era paper source was found. No Lean formalization was produced. No new optimization experiments or changes to the preserved mathematics were made while preparing this packet.

Competition final submission/acceptance receipt is **not yet available**. This GitHub packet is for judge review and does not establish an official competition final submission.
