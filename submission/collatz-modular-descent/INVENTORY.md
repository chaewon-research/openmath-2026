# Evidence inventory and inspection notes

Before preparing this packet, inspection covered the preserved `collatz-search/final-351d2794/` candidate, the byte-identical ablation file, the immutable AutoLab submission objects, the existing `submission/collatz-modular-descent/`, all local Collatz search sources/candidates/reports, the public hill evaluator/configuration/baselines/tests, and relevant locally retained AutoLab logs and reports. No optimization or new AutoLab evaluation was run.

## Exact originals

- `solution.json`: exact preserved bytes, checked against the immutable commit and both local frozen/ablation copies.
- `validation-report.json`: pre-existing packet report, checked byte-for-byte against the original AutoLab job report and run report.
- `evidence/commit.raw`, `evidence/tree.raw`: original raw Git object contents, with independently reproducible object hashes.
- `logs/autolab-output.txt`: entire original job output for 351d2794, including the signed report. Original absolute filesystem paths remain for provenance; they reveal workspace layout and public project/account names, but no target instances or secrets were found.
- `logs/env.txt`, `logs/evaluator.txt`: original run files, both zero bytes. They do not establish a complete official execution environment.
- `public-hill/`: unchanged local public `eval.py`, `README.md`, `pyproject.toml`, `uv.lock`. The source names private split files but contains no split contents. It is provided as local public-source evidence, not a complete independently reconstructed hill tree hash.
- `history/organizer-baseline.json`: unchanged public two-rule example.
- `history/local-22-rule-baseline.json`: unchanged earlier local candidate.
- `history/collatz-search/`: unchanged existing source files, V2/V3/V4/V5-A candidates, reports, diagnosis, frozen candidate, ablation and scan records. Hashes are in the manifest.

## Historical caveats

`history/collatz-search/coordinated-swap-scan.json` contains prose instructions followed by JSON, and is **not valid JSON as a whole**. It is retained unchanged as an imperfect historical record. Its figures are not newly validated results. The separate 3-for-3 scan file is valid JSON.

Historical Markdown contains statements such as “No AutoLab submission was made” describing an earlier stage. Such notes do not override the signed 351d2794 report. Some notes describe exact optimization; the staged-debug objective in `search_v4.py` and incomplete execution records mean this packet makes no independently established global-optimality claim.

Historical scripts expect the original repository paths and `.autolab/hills` checkout, and some overwrite candidates. They are archival evidence, not the offline replay entry point. **Do not run them to inspect the preserved result.** All search scripts were inspected; none were executed during packet preparation.

## New review material

`check.py`, `local-check.json`, environment/identity metadata, checksum manifest and review Markdown were added for inspection. The newly written `paper/main.tex` technical report and repository-only bibliography document the same preserved result; any generated PDF is typeset from that source and is not an original experiment-era paper. `local-check.json` is deterministically derived from the unchanged certificate. Its explicit public-universe residues were constructed mathematically from powers 8–12, not extracted from any held-out split.

## Exclusions and genuine gaps

Excluded: credentials, tokens, HMAC signing keys, private target data, split files/locks, node configuration, unrelated AutoLab logs, Busy Beaver material and Python caches. Full private-score reproduction, public HMAC authentication, a complete original evaluator environment, Lean formalization and final/test report remain unavailable. These gaps are explicit rather than replaced with invented artifacts.
