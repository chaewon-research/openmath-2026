# Collatz judge review packet — experiment 351d2794

Author: **Chaewon Yoon**. This packet preserves a finite accelerated-Collatz residue descent certificate. **It is not a proof of the full Collatz conjecture.**

The exact submitted `solution.json` contains 512 rules. AutoLab experiment `351d2794-d842-41a1-aa86-83e11fbca2fa` evaluated immutable submission commit `57c1ad7f2af78339260fcc4d8498a05dda4cfc77` on 2026-09-29. The full original signed report is [validation-report.json](validation-report.json).

| Official validation metric | Value | Direction |
| --- | ---: | --- |
| coverage_ppm | 1000000 | maximize |
| min_descent_ppm | 525390 | maximize |
| rule_count | 512 | minimize |

The report records `passed=true`, `official=true`, **`final=false`**. Coverage is weighted private-validation coverage, with 639/639 weight across 20 targets. Minimum descent is the minimum, across covered targets, of the best matching rule's affine contraction margin, floored to ppm. Neither number is a claim about every odd integer. No final/test result or competition acceptance is established.

## Inspect and replay

From the repository root:

```sh
cd submission/collatz-modular-descent
sha256sum -c SHA256SUMS
python3 check.py --output /tmp/collatz-local-check.json
cmp local-check.json /tmp/collatz-local-check.json
```

Use CPython 3.14.2 for the pinned replay. No third-party packages, network, credentials, AutoLab client, or private split are required. See [REPRODUCE.md](REPRODUCE.md) for expected outputs and Git object verification.

## Contents

- [RESULT.md](RESULT.md): exact theorem, assumptions, covered set, baseline comparison, limitations.
- [NOVELTY.md](NOVELTY.md): contribution and conservative novelty statement.
- [PROVENANCE.md](PROVENANCE.md), [identity.json](identity.json), `IMMUTABLE_COMMIT.txt`: identities and disclosures.
- `solution.json`: unchanged certificate; `check.py`: offline checker; `local-check.json`: exact derived affine witnesses and residue lists.
- `evidence/commit.raw`, `evidence/tree.raw`: original Git objects linking the immutable commit to the solution blob.
- `validation-report.json`, `logs/`: signed report and original AutoLab output; two original run logs are empty. [Log privacy label](logs/README.md) identifies the retained paths/public project names and report aggregates.
- `public-hill/`: original public evaluator, task description, project configuration and lockfile; no private targets.
- `history/`: existing search sources, candidates, reports, and both baseline certificates. These are historical evidence, not instructions to run optimization. See [INVENTORY.md](INVENTORY.md) for caveats.
- `ENVIRONMENT.json`, `.python-version`, `SHA256SUMS`: replay pin and checksums.

The newly written [technical report](paper/README.md) supplies editable [LaTeX source](paper/main.tex) and a repository-only [bibliography](paper/references.bib). The [five-page PDF](paper/main.pdf) compiled successfully; see [PAPER_STATUS.md](PAPER_STATUS.md) for build details. No original experiment-era paper or Lean files were found. Busy Beaver material is outside this packet.

No Lean formalization was produced for this submission. Verification is provided by the supplied exact checker/certificate pipeline and the signed AutoLab validation report.

Competition final submission/acceptance receipt is **not yet available**. This GitHub packet is for judge review and does not constitute evidence of official competition final submission.
