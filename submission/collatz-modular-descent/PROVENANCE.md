# Provenance and disclosures

## Author and exact identities

Author and human entrant: **Chaewon Yoon**.

- AutoLab experiment: `351d2794-d842-41a1-aa86-83e11fbca2fa` (short ID `351d2794`).
- Immutable submission commit: `57c1ad7f2af78339260fcc4d8498a05dda4cfc77`.
- Submission tree: `8997cd5553aa973ab11405ff8b2efa1ea2876c55`; solution Git blob: `6fb4698345a44ce6c1f79c24b84360b1971e7f0b`.
- Solution SHA-256: `1e533cbd5dbb17bb6ad52c7c80faa3a6abce587a32204ef5228de54da5b069e6`.
- Hill: `alejandrozu/collatz-modular-descent`.
- Project: `chaewon-research/collatz-modular-descent-v3-v4-evaluation` ([AutoLab project](https://app.autolab.ai/projects/chaewon-research/collatz-modular-descent-v3-v4-evaluation)).
- Report submission identity: `exp/openmath-codespace/351d2794@57c1ad7`.
- Evaluator submission hash: `sha256:35ffae42005041a099e5b742fb9a4996b3d3e7583621efd2fec4c822b43c1e28` (not the solution file hash).
- Evaluated hill tree hash: `7414e19511b2b99954a3898beed545401b79a571`.
- Report `commit` field: `ad2b555cf91d7d4250bbdb6f94b30fac07e3d512`; this is distinct from the immutable submission commit.

`identity.json` records these values in machine-readable form. No separate organizer submission/acceptance receipt or identifier was found; the AutoLab experiment alone does not establish competition acceptance.

## Evaluator report provenance

The original local AutoLab job report was retained at `tmp/job-logs/351d2794-d842-41a1-aa86-83e11fbca2fa/report.json` under the project on node `openmath-codespace`. The matching run report was under `hills-home/runs/collatz-modular-descent/20260929T220906Z-58f7856f/report.json`. The existing packaged `validation-report.json` was compared byte-for-byte with both originals. Its fields and HMAC signature are unchanged. The full original job output is `logs/autolab-output.txt`; original environment/evaluator logs were empty and are retained as empty files.

The signed report is timestamped `2026-09-29T22:09:07Z`, report version 1, hill specification version 2. It records hills tool version 0.11.0 and its tool hash, `passed=true`, `official=true`, `final=false`, and metrics 1000000 / 525390 / 512. An HMAC signature is not a credential, but authenticating it requires the organizer's signing verification context. No signing key is disclosed, and packet preparation did not independently authenticate the HMAC.

Original commit/tree bytes are included under `evidence/`; together with the exact solution blob they permit offline hash verification of the submission linkage. Parent history and a full evaluator bundle are not included. The copied public evaluator is the inspected local source; this packet does not reconstruct the complete evaluated hill tree.

## AI, model and compute disclosure

**Codex** assisted with search, code generation, candidate construction and review-packet preparation. **AutoLab** performed the recorded official evaluation. The earlier provenance record states that the entrant confirmed $4.69 in AutoLab model credits used and $0.00 in rented compute spend to date; these were account totals, not an audited cost of experiment 351d2794. Account balance is omitted from this public packet. Funding source and exact AutoLab model name/version are not established by the retained records. The exact model version and billed usage for earlier Codex assistance are also not established; none are inferred from the current preparation session.

Recorded compute was GitHub Codespaces, with AutoLab node `openmath-codespace`. The original run's full hardware allocation, duration and runtime image are not recorded in the signed report. `ENVIRONMENT.json` records the observed review-time environment, with CPython 3.14.2; it must not be mistaken for a complete original run environment.

## Construction versus review preparation

Historical files describe rule enumeration and selection under the 512-rule limit. The preserved revision changes one V4 rule from `(8,113,[2])` to `(5,17,[2])`. Existing sources/candidates/reports are archived under `history/` without rerunning them. Historical optimality and exhaustive-search claims remain local analysis; the packet does not elevate them into signed evaluator conclusions.

Review preparation compared exact artifact/report bytes, extracted original Git objects, archived public supporting records, ran a new **offline inspection of the fixed certificate**, and wrote review documentation and derived affine witnesses. This is not a new AutoLab evaluation or optimization experiment. It made no changes to the mathematical certificate or original signed report. `local-check.json` is explicitly local analysis. Official metrics come only from `validation-report.json`.

## Privacy and status

No credentials, tokens, signing secrets, private targets, held-out split files/locks, node configuration, unrelated logs or Busy Beaver work are included. The public report's aggregate metrics, hashes and HMAC signature are retained. Original logs expose public account/project names and local workspace paths. No private target instances were found in the included output. The requested author identity is intentionally public.

The newly written technical report under `paper/` documents the preserved result; it is not an original experiment-era manuscript. No final/test evaluation, full Collatz proof, Lean formalization, leaderboard publication, novelty determination, eligibility determination or competition acceptance is claimed. Repository preparation stops before commit/push pending the entrant's approval.

## Formalization and official submission status

No Lean formalization was produced for this submission. Verification is provided by the supplied exact checker/certificate pipeline and the signed AutoLab validation report.

AutoLab experiment 351d2794 and its signed validation report (`final=false`) are available. Competition final submission/acceptance receipt is not yet available. The GitHub packet does not constitute evidence of an official competition final submission.
