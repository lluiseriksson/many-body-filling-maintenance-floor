"""Deterministic checks for the filled-SSH leakage floor and interacting diagnostics."""

from __future__ import annotations

import math

import numpy as np

from explore_interacting import diagnostics


def ssh_matrix(ell: int, t1: float, t2: float) -> np.ndarray:
    sites = 2 * ell + 1
    matrix = np.zeros((sites, sites))
    for j in range(ell):
        matrix[2 * j, 2 * j + 1] = matrix[2 * j + 1, 2 * j] = t1
        matrix[2 * j + 1, 2 * j + 2] = matrix[2 * j + 2, 2 * j + 1] = t2
    return matrix


def free_diagnostics(ell: int, t1: float, t2: float) -> dict[str, float]:
    matrix = ssh_matrix(ell, t1, t2)
    values, vectors = np.linalg.eigh(matrix)
    zero = int(np.argmin(abs(values)))
    site = 2 * ell
    w = float(abs(vectors[site, zero]) ** 2)
    negative = values < -1e-10
    positive = values > 1e-10
    pminus = float(np.sum(abs(vectors[site, negative]) ** 2))
    pplus = float(np.sum(abs(vectors[site, positive]) ** 2))
    total = (pminus + w) * (1 - pminus)
    logical = w**2
    leakage = total - logical
    zeta = t1 / t2
    exact_w = (1 - zeta**2) * zeta ** (2 * ell) / (1 - zeta ** (2 * ell + 2))
    exact_leakage = (1 + 2 * w - 3 * w**2) / 4
    dilute_leakage = w * (1 - w)
    return {
        "w_error": abs(w - exact_w),
        "chiral_error": max(abs(pminus - (1 - w) / 2), abs(pplus - (1 - w) / 2)),
        "leakage_error": abs(leakage - exact_leakage),
        "logical": logical,
        "leakage": leakage,
        "dilute_leakage": dilute_leakage,
        "w": w,
    }


def main() -> None:
    t1, t2 = 0.37, 1.0
    free_rows = [free_diagnostics(ell, t1, t2) for ell in range(2, 31)]
    worst_w = max(row["w_error"] for row in free_rows)
    worst_chiral = max(row["chiral_error"] for row in free_rows)
    worst_leakage = max(row["leakage_error"] for row in free_rows)
    filled_floor = free_rows[-1]["leakage"]

    ells = np.arange(2, 16)
    logical_slope = np.polyfit(ells, np.log([free_rows[k]["logical"] for k in range(14)]), 1)[0]
    dilute_slope = np.polyfit(ells, np.log([free_rows[k]["dilute_leakage"] for k in range(14)]), 1)[0]
    expected_logical = 4 * math.log(t1 / t2)
    expected_dilute = 2 * math.log(t1 / t2)

    interaction_rows: dict[float, list[dict[str, float]]] = {}
    for interaction in (-0.55, 0.0, 0.55):
        interaction_rows[interaction] = [diagnostics(ell, t1, t2, interaction) for ell in range(2, 7)]

    free_ed_error = max(
        abs(row["alpha2"] - free_diagnostics(int(row["ell"]), t1, t2)["w"])
        for row in interaction_rows[0.0]
    )
    ph_residual = max(
        row["particle_hole_residual"] for rows in interaction_rows.values() for row in rows
    )
    minimum_interacting_leakage = min(
        row["leakage"] for rows in interaction_rows.values() for row in rows
    )
    terminal_floors = {interaction: rows[-1]["leakage"] for interaction, rows in interaction_rows.items()}

    print(f"worst zero-mode weight residual       = {worst_w:.3e}")
    print(f"worst chiral-projector residual       = {worst_chiral:.3e}")
    print(f"worst filled sum-rule residual        = {worst_leakage:.3e}")
    print(f"filled leakage at ell=30              = {filled_floor:.12f}")
    print(f"logical slope residual                = {abs(logical_slope-expected_logical):.3e}")
    print(f"dilute leakage slope residual         = {abs(dilute_slope-expected_dilute):.3e}")
    print(f"free Fock/one-body weight residual    = {free_ed_error:.3e}")
    print(f"interacting particle-hole residual    = {ph_residual:.3e}")
    print(f"minimum interacting leakage           = {minimum_interacting_leakage:.12f}")
    for interaction, floor in terminal_floors.items():
        print(f"ell=6 leakage at V={interaction:+.2f}          = {floor:.12f}")

    assert worst_w < 1e-12
    assert worst_chiral < 1e-12
    assert worst_leakage < 1e-12
    assert abs(filled_floor - 0.25) < 1e-10
    assert abs(logical_slope - expected_logical) < 2e-3
    assert abs(dilute_slope - expected_dilute) < 2e-3
    assert free_ed_error < 1e-11
    assert ph_residual < 1e-9
    assert minimum_interacting_leakage > 0.24


if __name__ == "__main__":
    main()
