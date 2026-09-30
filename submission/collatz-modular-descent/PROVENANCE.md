# Provenance and disclosures

- Human entrant: **Chaewon Yoon**. This identifies the entrant; it does not infer entrant class, roster approval, or publication authorization.
- AI/tool use: **Codex** assisted with search, code generation, candidate construction, and packet preparation. **AutoLab** performed the recorded machine evaluation. The existing report identifies hills evaluator tool version `0.11.0`.
- Execution environment: **GitHub Codespaces**. The recorded AutoLab run used the connected Codespaces compute node `openmath-codespace`.
- AutoLab credits/model usage: Resource usage confirmed by the entrant: **$4.69** in AutoLab model credits spent so far; **$0.00** in AutoLab rented compute spend; **$95.31** AutoLab credit balance shown. These are account usage figures to date, not a cost attribution solely to this experiment. The funding/credit source and AutoLab model name/version are not established by the preserved artifact or signed evaluator report. Codex usage was separate from AutoLab evaluation; the available artifact records do not establish its exact model version or billed usage.

## Construction and verification

The mathematical artifact was iteratively generated with code and machine-checked. Search enumerated candidate accelerated-Collatz residue rules and selected a collection within the hill's 512-rule limit. The preserved candidate was the controlled one-rule revision of V4: replace `(modulus_power=8, residue=113, exponents=[2])` with `(modulus_power=5, residue=17, exponents=[2])`. This history describes the already preserved mathematics; packet preparation performed no search, optimization, or new evaluation.

AutoLab experiment `351d2794-d842-41a1-aa86-83e11fbca2fa` evaluated immutable commit `57c1ad7f2af78339260fcc4d8498a05dda4cfc77`. Its existing signed report records an official passing validation evaluation with `coverage_ppm=1000000`, `min_descent_ppm=525390`, and `rule_count=512`. Packet preparation compared the solution bytes with both the preserved artifact and the immutable commit and checked the SHA-256; it did not independently rerun the mathematical evaluator.

## Scope and final/test status

`validation-report.json` is a validation report, not a final/test report. These metrics are validation results, not final/test results. The report explicitly records `final=false`. No final/test evaluation is claimed unless organizers perform it and supply a corresponding report. No competition acceptance, semantic review, novelty determination, proof of the full Collatz conjecture, or leaderboard publication is claimed.

This packet contains the certificate, documentation, and the existing signed evaluator report. The report contains evaluator-produced aggregate scoring details, but no private target instances, private split files, or private hill bundle. Credentials, access tokens, signing secrets, unrelated logs, and private data files are excluded. The recorded public hill hash, submission hash, aggregate metrics, and HMAC report signature are retained for provenance.
