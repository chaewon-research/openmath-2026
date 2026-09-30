# Preserved accelerated-Collatz descent certificate

## Identity and status

- Human entrant: Chaewon Yoon.
- Target/hill: `alejandrozu/collatz-modular-descent`.
- AutoLab climb: `chaewon-research/collatz-modular-descent-v3-v4-evaluation`.
- Climb URL: https://app.autolab.ai/projects/chaewon-research/collatz-modular-descent-v3-v4-evaluation
- Experiment ID: `351d2794-d842-41a1-aa86-83e11fbca2fa` (short ID: `351d2794`).
- Immutable submission commit: `57c1ad7f2af78339260fcc4d8498a05dda4cfc77`.
- Evaluated hill tree hash: `7414e19511b2b99954a3898beed545401b79a571`.
- Evaluator report timestamp: `2026-09-29T22:09:07Z`.
- `solution.json` SHA-256: `1e533cbd5dbb17bb6ad52c7c80faa3a6abce587a32204ef5228de54da5b069e6`.

The existing official, passing report is a **validation** evaluation (`final=false`):

| Metric | Exact value | Direction |
| --- | ---: | --- |
| coverage_ppm | 1000000 | max |
| min_descent_ppm | 525390 | max |
| rule_count | 512 | min |

No final/test score is claimed. This packet has not been submitted or published.

## Mathematical artifact

The 512 rules certify strict descent for specified odd dyadic residue classes under accelerated Collatz steps, `C(n) = (3n + 1) / 2^v2(3n + 1)`. Each rule prescribes a stable valuation sequence for its entire residue class. The evaluator composes the resulting affine map and checks strict contraction and descent. Coverage and the weakest descent margin are measured against the hill's held-out validation targets. This finite collection of descent lemmas does not prove the Collatz conjecture.

`solution.json` is copied byte for byte from the preserved candidate and independently compared with the file stored in the immutable AutoLab commit. The JSON mathematics has not been edited.

## Reproduction and checking

From the repository root, check the packaged file checksum:

```sh
sha256sum submission/collatz-modular-descent/solution.json
```

The expected digest is the SHA-256 above. To inspect the existing evaluation without starting a run, use the linked AutoLab workspace:

```sh
cd collatz-modular-descent-v3-v4-evaluation
autolab logs 351d2794
```

`validation-report.json` preserves the existing report JSON and its HMAC signature without editing its fields. A signature is not an access token. Independent signature verification requires the signing node's verification context; this packet supplies no signing secret. The report's `submission_hash` is the evaluator's submission hash, distinct from the SHA-256 of the single solution file.

Authorized organizers or the hill owner, with the exact frozen hill version and its private evaluation data installed, can use the supported hills evaluator:

```sh
hills eval <solution-only-directory> -H collatz-modular-descent -o validation-report.json
hills eval <solution-only-directory> -H collatz-modular-descent --final -o final-report.json
```

Here `<solution-only-directory>` must contain exactly the supplied `solution.json`; use a separate temporary directory and keep reports outside it. The packet directory also contains documentation and report JSON, so it is not itself the evaluator input directory. The final command is for authorized organizer/owner use with the private test split; it has not been run. Non-owners with only public hill files cannot reproduce official private-split scoring locally. No verified platform-side final/test action is asserted here.
