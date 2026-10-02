# Paper and formalization status

## Technical report supplied

A concise technical report has now been newly written from the verified preserved result and existing review materials, at the entrant's request:

- [Editable LaTeX source](paper/main.tex), author **Chaewon Yoon**.
- [Verified bibliography](paper/references.bib), containing only three existing repository sources.
- [Generated PDF](paper/main.pdf), successfully compiled: **five pages**.
- [Build record](paper/BUILD.json) and [build instructions](paper/README.md).

The PDF was generated faithfully using portable Tectonic 0.15.0; all pages were rendered and inspected. The final LaTeX/BibTeX logs have no warnings or unresolved citations. Toolchain/cache/intermediate files stayed under `/tmp`. The PDF is review-time documentation, not an original experiment-era paper or a new mathematical result. No original paper source was found in the earlier local work, and the immutable submission tree still contains only the unchanged `solution.json`.

## Lean/formalization status

No Lean formalization was produced for this submission. Verification is provided by the supplied exact checker/certificate pipeline and the signed AutoLab validation report.

No Lean files or kernel-checked proof have been invented. The report explains the already supported affine descent statement and its assumptions; it does not prove the full Collatz conjecture.

## Official submission status

AutoLab experiment 351d2794 and the original signed validation report (`final=false`) are available. Competition final submission/acceptance receipt is **not yet available**. The GitHub packet and newly written report do not constitute evidence of an official final submission or acceptance.
