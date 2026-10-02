# Technical report for judge review

- [main.tex](main.tex): editable source, author **Chaewon Yoon**.
- [references.bib](references.bib): three verified repository sources only: the public task/evaluator, signed 351d2794 report, and offline checker/inspection data. No external literature citations or bibliographic authors were invented.
- [main.pdf](main.pdf): successfully compiled five-page report, faithfully generated from these sources.
- [BUILD.json](BUILD.json): compiler version, source/PDF hashes, resource-bundle identity and inspection status.

This report was newly written during review preparation from the verified packet. It is not an original experiment-era manuscript, a new experiment, or a proof of the full Collatz conjecture. The certificate and original signed report were not changed.

## PDF build

The existing environment had no LaTeX compiler. A portable **Tectonic 0.15.0** Linux musl binary was obtained from the [official release](https://github.com/tectonic-typesetting/tectonic/releases/tag/tectonic%400.15.0). Its standard resource bundle and temporary build/cache files stayed under `/tmp`. No toolchain binary or cache is included in the repository. The release archive/binary checksums and bundle identity are recorded in `BUILD.json`; the compiler is not part of the certificate verification environment.

From the packet directory, with `tectonic` 0.15.0 available:

```sh
mkdir -p /tmp/reviewer-collatz-paper
cp paper/main.tex paper/references.bib /tmp/reviewer-collatz-paper/
cd /tmp/reviewer-collatz-paper
tectonic --untrusted --reruns 2 --keep-logs --keep-intermediates main.tex
```

For an already populated resource cache, add `--only-cached`. A fresh Tectonic cache may require network access for standard TeX resources. `BUILD.json` identifies the resource bundle used here. Two explicit reruns resolved the bibliography and references. The final LaTeX/BibTeX logs had no warnings, unresolved citations or overfull boxes. All five pages were rendered and inspected; PDF text and metadata were also checked.

Expected output is a five-page `main.pdf` with title and author matching the source, three resolved repository references, and the precise preserved result. Different engines/resources or PDF timestamps can change PDF bytes; bitwise-identical rebuilding is not claimed. The packet checksum manifest verifies the supplied PDF bytes. Ordinary certificate replay needs neither LaTeX nor the PDF inspection library.

## Formalization and official status

No Lean formalization was produced for this submission. Verification is provided by the supplied exact checker/certificate pipeline and the signed AutoLab validation report.

AutoLab experiment 351d2794 and its signed validation report with `final=false` are available. Competition final submission/acceptance receipt is not yet available. This GitHub review packet is not evidence of an official competition final submission.
