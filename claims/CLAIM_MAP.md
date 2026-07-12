# Claim map

This map separates analytic results, conditional inputs, and numerical diagnostics. Numbering refers to `paper/main.tex`.

| Result | Epistemic status | Reproducible check |
|---|---|---|
| Lemma 2.1, chiral diagonal splitting | Exact one-body spectral proof | Direct diagonalization checks both projector diagonals |
| Theorem 3.1, filled-SSH transfer identity | Exact many-body Slater/Fock-space identity | One-body and explicit Fock-space evaluations agree |
| Corollary 3.2, remote leakage floor | Exact consequence of the zero-mode profile | Leakage reaches `0.25` to numerical precision |
| Theorem 4.1, Davies line-continuum separation | Analytic conditional theorem under the stated two-sided bath envelope | Unweighted matrix elements are checked; the bath envelope remains an assumption |
| Corollary 4.2, coefficient exponent `min{4m,q}` | Exact asymptotic consequence of Theorem 4.1 | Phase-diagram figure evaluates the formula |
| Lemma 5.1, boundary free-energy loss | Analytic support-extension argument; entropy nonanalyticity attributed to Grace–Guha | No numerical test substitutes for the proof |
| Lemmas 5.2–5.3, uniform leakage and free-energy sandwich | Analytic semigroup and block-entropy estimates under explicit uniformity assumptions | Source invariants and limiting weights are checked |
| Theorem 5.4, power exponent `min{4m,q}` | Analytic conditional theorem under the fresh-target-cell ledger | Figure illustrates, but does not prove, the exponent law |
| Theorem 6.1, interacting occupation-leakage identity | Exact algebra for arbitrary number-conserving rails | Verified for attractive, free, and repulsive spinless SSH chains |
| Lemma 7.1, local spectral window | Exact spectral-moment/Chebyshev inequality | No level-counting or numerical premise is used |
| Theorem 7.2, interacting Davies floor | Analytic conditional theorem using a bath lower envelope on the certified window | Static weights are checked; the reservoir spectrum is not derived |
| Proposition 8.1, small-interaction persistence | Conditional analytic consequence of a symmetry-preserving uniformly gapped path and standard quasi-local spectral flow | ED is supporting evidence only, not a proof of a uniform gap |

## Explicit non-claims

- No uniform microscopic weak-coupling limit before the Davies generator.
- No derivation of the reservoir envelope from a specific bath.
- No exact interacting logical exponent throughout an arbitrary SPT phase.
- No autonomous work-only optimality theorem.
- No claim that finite-size exact diagonalization proves the thermodynamic interacting proposition.
- No Lean or other machine-checked formalization.
