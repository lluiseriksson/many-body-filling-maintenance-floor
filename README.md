# Many-Body Filling Turns Soft Spectral Leakage into a Maintenance Floor

<!-- RESEARCH-UPDATE-2026-09-09 -->
> **Research update · 9 September 2026:** [verified source cards, limits and next experiments](research/updates/2026-09-09.md) · [machine-readable dossier](research/updates/2026-09-09.json).

Reproducibility package for

> **Many-Body Filling Turns Soft Spectral Leakage into a Maintenance Floor**
>
> *Exact Filled-SSH Sum Rules and an Interaction-Stable Obstruction*

Lluis Eriksson, 2026.

The paper proves an exact finite-density SSH identity. For zero-mode boundary weight `w`, the desired logical transfer has squared weight `w^2`, whereas the summed nonlogical particle-hole weight is

```text
(1 + 2w - 3w^2) / 4.
```

At the remote boundary the first term decays as `zeta^(4 ell)`, while the second tends to `1/4`. Under the stated Davies filter envelope this changes the bounded-latency maintenance exponent from the dilute law `min{4m,2m+q}` to `min{4m,q}`.

## Authoritative files

- `paper/main.tex` — authoritative manuscript and analytic proofs.
- `paper/main.pdf` — release PDF.
- `paper/many_body_filling_phase_diagram.png` — manuscript figure.
- `claims/CLAIM_MAP.md` — claim-by-claim proof and assumption map.
- `REVISION_NOTES.md` — audit trail for the strengthened second version.
- `verification/verify.py` — deterministic free and interacting checks.
- `verification/explore_interacting.py` — exact Fock-space construction and diagonalization.
- `verification/make_figure.py` — deterministic figure generator.

## Reproduce

```bash
python -m pip install -r requirements.txt
python verification/verify.py
python verification/make_figure.py
tectonic -X compile paper/main.tex --outdir paper --keep-logs
python verification/check_release.py
```

GitHub Actions runs the checks, regenerates the figure, builds the manuscript with Tectonic 0.16.9, validates source and PDF invariants, and rejects drift in the committed PDF.

## Epistemic separation

The analytic proofs are in the manuscript. The exact-diagonalization results are diagnostics, not proofs of the interaction-stability theorem. The exact exponent equality is proved for the free filled SSH family under an explicit invariance condition for the Davies block-diagonal algebra; spectral isolation alone is not used to infer that condition, and full commutation with block dephasing is not required. The interacting results prove a static identity, a local spectral-window theorem, and a conditional stability result under a symmetry-preserving uniformly gapped path. Exponent zero at `q=0` permits subexponential decay; a positive maintenance floor additionally requires `liminf epsilon_ell > 0`. No uniform pre-Davies weak-coupling limit, autonomous work-only optimum, or proof-assistant formalization is claimed.

The manuscript and supporting package were prepared with AI assistance and reviewed by the author, who is responsible for all claims.

## License

Code is MIT licensed. The paper, figure, claim map, and documentation are CC BY 4.0.
