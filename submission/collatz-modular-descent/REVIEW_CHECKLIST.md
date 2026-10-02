# Pre-commit review checklist

This packet is prepared locally and awaits approval before commit/push. No optimization experiment, new official evaluation or change to the preserved solution was performed.

## Requested organizer materials

| Requested item | Status |
| --- | --- |
| Strong top-level README: project, exact result, official metrics, scope, replay, structure | Supplied |
| Dedicated Collatz directory with exact artifact, immutable commit, signed report and IDs | Supplied; solution/report original bytes verified |
| Checker and certificates | Supplied: unchanged 512-rule JSON; offline checker; derived affine witnesses |
| Lean files if genuine | No Lean formalization produced; exact checker/certificate pipeline supplied |
| Exact public replay, pinned dependencies/environment, logs/data | Supplied for offline mathematical inspection; original official runtime incompletely recorded |
| RESULT.md: covered classes, theorem, assumptions, baseline additions, limitations | Supplied with explicit machine-readable residue lists |
| NOVELTY.md: motivation, contribution, prior context and event work | Supplied; literature priority/novelty not established |
| REPRODUCE.md: versions, commands, expected outputs, hashes, no-private-data check | Supplied |
| PROVENANCE.md: author, experiment, commit, report, AI/model/compute, official/local distinction | Supplied; original model versions and exact per-run resource usage unavailable |
| Paper / technical report | Supplied: newly written `paper/main.tex`, verified repository-only `references.bib`, successfully compiled five-page `main.pdf`, build record/instructions |

## Genuinely missing or limited

- Lean formalization (explicitly not produced).
- Final/test signed result and separate organizer competition submission/acceptance receipt.
- Complete original evaluator runtime/container/hardware record, tool binary and exact earlier AI model versions/per-run billed usage.
- Public authentication of the HMAC report and regeneration of the private weighted score: requires organizer verification context/private split; excluded intentionally.
- Completed literature review or independent novelty/optimality determination.

## Privacy/security review

The retained output contains workspace filesystem paths and public account/project names. Author identity is public as requested. The report contains aggregate evaluation counts/weights and an HMAC signature, but no private target instances. No likely credentials were found in a credential-pattern scan of the proposed packet and top-level changes; included original sources/logs were also inspected. No private split files, signing keys, tokens, node configurations or Busy Beaver files are included. Local AutoLab state and agent configuration are ignored. The manifest is a checksum list, not an authenticity signature.

## Validation performed

- Byte equality: solution versus preserved candidate, ablation file, immutable commit and tracked original packet.
- Byte equality: signed report versus original AutoLab job/run reports and tracked packet.
- Original commit, tree and blob Git hashes reproduced.
- All 512 fixed rules checked with independent affine arithmetic and cross-checked with public verifier.
- Derived public class/baseline data regenerated and compared exactly.
- Five checker rejection tests passed.
- SHA-256 manifest verified; relative Markdown links and whitespace checked.

No commit or push has been made during preparation. Only explicit Collatz packet paths and top-level README/.gitignore changes should be staged after approval; unrelated untracked working directories must remain separate.

## Lean/formalization status

No Lean formalization was produced for this submission. Verification is provided by the supplied exact checker/certificate pipeline and the signed AutoLab validation report.

## Official submission status

- AutoLab experiment: `351d2794-d842-41a1-aa86-83e11fbca2fa`.
- Original signed report: official validation, `final=false`.
- Competition final submission/acceptance receipt: not yet available.

This GitHub packet is prepared for judge review; it does not constitute evidence of official competition final submission or acceptance.

## Technical report verification

The new report was written solely from preserved artifacts and existing review material. Archived organizer/local V2/V3/V4/V5-A candidates were checked as fixed inputs for its comparison table; no optimization ran. All bibliography entries identify existing repository materials. The PDF compiled successfully with Tectonic 0.15.0, all three citations resolved, and final LaTeX/BibTeX logs had no warnings. Five rendered pages and extracted text/metadata were inspected. No original artifact, checker, derived certificate data or historical file was rewritten.

## Post-report sanity and privacy recheck

All local Markdown links in the packet and top-level README resolve. No Busy Beaver files, private split files/targets, node configuration, credentials or symlinks are included in the intended publication files. Credential-pattern scans of source/text/binary files and extracted PDF text found no likely credentials; the PDF has no embedded attachments. The original output is labelled in `logs/README.md` as containing workspace paths/public infrastructure names and signed report aggregates. The prose-plus-JSON historical record remains unchanged and is documented.

The exact solution and signed report again match the immutable/local originals and tracked packet byte-for-byte. Preserved history, public hill source, Git object evidence, original logs, checker and derived certificate data match the previous checkpoint hashes. Fixed-certificate replay regenerates identical `local-check.json`; all five rejection tests pass; commit/tree/blob hashes match; the revised SHA-256 manifest passes completely. A literal NUL in the earlier documented tree-inspection command was corrected to the textual Python escape `\0` and the corrected command was executed successfully. No research code or result was changed.
