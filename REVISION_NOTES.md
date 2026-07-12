# Revision notes

This revision responds to independent technical criticism of the first public version.

## Corrections

1. **Subexponential tails.** The manuscript no longer equates `q=0` with a positive maintenance floor. The exponent is zero whenever `epsilon_ell = exp[o(ell)]`; a positive width-independent floor additionally requires `liminf epsilon_ell > 0`.
2. **Spectral isolation.** The fixed-latency section now requires the logical projector to be a sum of complete isolated spectral projections. This is the condition that makes the secular `P ⊕ Q` decomposition exact in the presence of degeneracies.
3. **Crossing maps.** Outgoing and incoming completely positive crossing maps are defined explicitly. Their `1→1` norms are bounded by `O(epsilon_ell)` using positivity and energy pinching, without counting Bohr modes.
4. **Finite-time leakage.** The leakage proof now starts from an exact `P↔Q` balance equation and controls outgoing variation and incoming return separately by Gronwall estimates.
5. **Free-energy sandwich.** The logical terms carry their required factor of `tau`; Duhamel control, logical faithfulness, bounded energy flux, and the leakage-sector entropy bound are shown explicitly.
6. **Interacting persistence.** The former proof sketch is replaced by a conditional theorem with four named inputs: an isolated band, a number-preserving quasi-local spectral flow, a model-specific free-endpoint edge estimate, and a summable flow generator. The truncation radius, occupation response, two-rail reduction, and commutator bound are explicit.
7. **Priority boundary.** Prior work on operational entanglement of half-filled SSH edge states is now cited. Novelty is restricted to the leakage sum rule and its spectral-filter consequences.
8. **Block compatibility.** Spectral isolation is no longer claimed to imply exact `P ⊕ Q` invariance. The manuscript separately assumes invariance of the block-diagonal algebra, gives a sufficient source-to-one-target criterion, and does not claim that this weaker criterion implies full commutation with block dephasing.
9. **Exact-filter generator.** The reference evolution is defined by deleting complete Lindblad dissipators, including their anticommutator terms. It is therefore normalized and trace preserving.

The exact free identity and numerical outputs are unchanged.
