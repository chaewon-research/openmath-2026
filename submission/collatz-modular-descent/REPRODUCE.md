# Offline reproduction of the preserved result

## Environment

Pinned replay: **CPython 3.14.2**, standard library only; no pip dependencies. `.python-version` records the pin and `ENVIRONMENT.json` records the observed Linux runtime. The public hill project is version 0.1.0 and requires Python >=3.11. Its copied `uv.lock` records the existing optional development pins: pytest 9.1.1, iniconfig 2.3.0, packaging 26.3, pluggy 1.6.0, pygments 2.21.0, and Windows-only colorama 0.4.6. These packages are not needed by the offline checker.

The signed official report records hills **0.11.0**, tool SHA-256 `970e4a3fcb74c27e0c56b62efd22b4fab82a755229a8aef8f90bbc00a9cfe275`. This identifies the official tool; the complete original evaluator container, Python build, and tool binary are not archived. The replay environment pin is a review-time pin, not an assertion about the original run's full environment.

## Exact commands and outputs

From the repository root, using Python 3.14.2:

```sh
cd submission/collatz-modular-descent
python3 --version
sha256sum -c SHA256SUMS
python3 check.py --output /tmp/collatz-local-check.json
cmp local-check.json /tmp/collatz-local-check.json
```

Version output: `Python 3.14.2`. Every manifest entry should say `OK`. `cmp` exits 0 without output. Checker output:

```text
PASS: preserved SHA-256; 512 exact descent rules; public verifier agrees
Public classes: 3352/3968 (powers 8..12)
Union at power 12: 1765/2048 odd residues
{"local-22-rule-baseline": {"added_public_classes": 469, "lost_public_classes": 0, "public_covered": 2883, "rule_count": 22}, "organizer-baseline": {"added_public_classes": 2360, "lost_public_classes": 0, "public_covered": 992, "rule_count": 2}}
```

`check.py` enforces the preserved solution SHA-256, loads its strict schema with the original public loader, independently composes integer affine maps, verifies every valuation/stability/descent condition, and cross-checks all margins with the public rule verifier. It evaluates fixed inputs only. It does not call the private scoring function, use hidden targets, run historical search scripts, or generate candidate certificates.

## Checker regression checks

```sh
python3 test_check.py
```

Expected: five tests pass (`Ran 5 tests`, `OK`). These reject an incorrect valuation, insufficient modulus stability, a noncontractive map, contraction without strict descent at 1, and duplicate JSON keys. They do not run private scoring or historical optimization.

## Immutable Git object checks

No AutoLab checkout or Git write is needed:

```sh
git hash-object -t commit evidence/commit.raw
git hash-object -t tree evidence/tree.raw
git hash-object solution.json
cat evidence/commit.raw
```

Expected respective object IDs:

```text
57c1ad7f2af78339260fcc4d8498a05dda4cfc77
8997cd5553aa973ab11405ff8b2efa1ea2876c55
6fb4698345a44ce6c1f79c24b84360b1971e7f0b
```

The raw commit's `tree` field must equal the second ID. Inspect the binary tree without private data:

```sh
python3 -c 'from pathlib import Path; b=Path("evidence/tree.raw").read_bytes(); h,v=b.split(b"\0",1); print(h.decode(),v.hex())'
```

Expected: `100644 solution.json 6fb4698345a44ce6c1f79c24b84360b1971e7f0b`. These three objects establish the exact commit-to-file linkage. Parent commit history is not included in this minimal evidence set. Git SHA-1 object IDs and SHA-256 file checksums are distinct.

`solution.json` SHA-256 must be `1e533cbd5dbb17bb6ad52c7c80faa3a6abce587a32204ef5228de54da5b069e6`. The report's `submission_hash` identifies the evaluator submission bundle, not this single-file digest. The manifest detects changes relative to this packet; it is not a digital signature.

## Official evidence and limits

Read `validation-report.json` and `logs/autolab-output.txt` to inspect the recorded official score. Both are original bytes copied from the local AutoLab run; no platform access is necessary to read them. The report uses an HMAC-SHA256 signature, which cannot be independently authenticated from public data without the organizer's signing verification context. No signing secret is included. The offline check verifies the mathematics, not report authorship or private metrics.

Reproducing the official weighted score requires the original private validation targets and frozen evaluator context; they are intentionally not included. Final/test evaluation is a separate action and was not performed. No AutoLab commands or historical optimization scripts need to be run for judge inspection.

## Technical report source/PDF

The new [technical report source](paper/main.tex), [repository-only bibliography](paper/references.bib), and [five-page PDF](paper/main.pdf) are included in `SHA256SUMS`. [paper/README.md](paper/README.md) gives exact compilation instructions; [paper/BUILD.json](paper/BUILD.json) pins the compiler/resource identity and records hashes. The report compiled with Tectonic 0.15.0. LaTeX is optional and separate from the CPython-only certificate replay. PDF byte identity across builds is not promised because timestamps/resources can vary.
