"""Exact-diagonalization probe of the finite-density SSH leakage identity."""

from __future__ import annotations

import argparse
import itertools
import math

import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh


def basis_states(sites: int, particles: int) -> list[int]:
    return [sum(1 << j for j in occupied) for occupied in itertools.combinations(range(sites), particles)]


def fermion_sign(state: int, site: int) -> int:
    return -1 if (state & ((1 << site) - 1)).bit_count() % 2 else 1


def rail_hamiltonian(ell: int, particles: int, t1: float, t2: float, interaction: float):
    sites = 2 * ell + 1
    basis = basis_states(sites, particles)
    index = {state: k for k, state in enumerate(basis)}
    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []

    # Site ordering A_0,B_0,A_1,B_1,...,B_{ell-1},A_ell.
    bonds = []
    for j in range(ell):
        bonds.append((2 * j, 2 * j + 1, t1))
        bonds.append((2 * j + 1, 2 * j + 2, t2))

    for col, state in enumerate(basis):
        diagonal = 0.0
        for left in range(sites - 1):
            nl = (state >> left) & 1
            nr = (state >> (left + 1)) & 1
            diagonal += interaction * (nl - 0.5) * (nr - 0.5)
        rows.append(col)
        cols.append(col)
        data.append(diagonal)

        for left, right, hopping in bonds:
            for source, target in ((left, right), (right, left)):
                if ((state >> source) & 1) and not ((state >> target) & 1):
                    after_annihilation = state ^ (1 << source)
                    sign = fermion_sign(state, source) * fermion_sign(after_annihilation, target)
                    moved = after_annihilation | (1 << target)
                    rows.append(index[moved])
                    cols.append(col)
                    data.append(hopping * sign)

    matrix = coo_matrix((data, (rows, cols)), shape=(len(basis), len(basis))).tocsr()
    return matrix, basis


def annihilation_matrix(sites: int, source_basis: list[int], target_basis: list[int], site: int):
    target_index = {state: k for k, state in enumerate(target_basis)}
    rows: list[int] = []
    cols: list[int] = []
    data: list[float] = []
    for col, state in enumerate(source_basis):
        if (state >> site) & 1:
            lowered = state ^ (1 << site)
            rows.append(target_index[lowered])
            cols.append(col)
            data.append(float(fermion_sign(state, site)))
    return coo_matrix((data, (rows, cols)), shape=(len(target_basis), len(source_basis))).tocsr()


def ground_state(matrix):
    if matrix.shape[0] == 1:
        return float(matrix[0, 0]), np.ones(1)
    vals, vecs = eigsh(matrix, k=1, which="SA", tol=1e-12)
    return float(vals[0]), vecs[:, 0]


def diagnostics(ell: int, t1: float, t2: float, interaction: float) -> dict[str, float]:
    sites = 2 * ell + 1
    nlow = ell
    h_low, basis_low = rail_hamiltonian(ell, nlow, t1, t2, interaction)
    h_high, basis_high = rail_hamiltonian(ell, nlow + 1, t1, t2, interaction)
    e_low, psi_low = ground_state(h_low)
    e_high, psi_high = ground_state(h_high)
    site = sites - 1
    annihilation = annihilation_matrix(sites, basis_high, basis_low, site)
    alpha = np.vdot(psi_low, annihilation @ psi_high)
    number_high = float(np.linalg.norm(annihilation @ psi_high) ** 2)
    creation_low = annihilation.conj().T @ psi_low
    vacancy_low = float(np.linalg.norm(creation_low) ** 2)
    logical = float(abs(alpha) ** 4)
    total = number_high * vacancy_low
    return {
        "ell": float(ell),
        "gap_charge": e_high - e_low,
        "alpha2": float(abs(alpha) ** 2),
        "number_high": number_high,
        "vacancy_low": vacancy_low,
        "total": total,
        "logical": logical,
        "leakage": total - logical,
        "particle_hole_residual": abs(number_high - vacancy_low),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-ell", type=int, default=6)
    parser.add_argument("--t1", type=float, default=0.37)
    parser.add_argument("--t2", type=float, default=1.0)
    parser.add_argument("--interaction", type=float, default=0.55)
    args = parser.parse_args()

    rows = [diagnostics(ell, args.t1, args.t2, args.interaction) for ell in range(2, args.max_ell + 1)]
    print("ell    |alpha|^2       total weight    leakage         ph residual")
    for row in rows:
        print(
            f"{int(row['ell']):3d}  {row['alpha2']:13.6e}  {row['total']:13.6e}  "
            f"{row['leakage']:13.6e}  {row['particle_hole_residual']:10.2e}"
        )
    slopes = np.polyfit([row["ell"] for row in rows], np.log([row["alpha2"] for row in rows]), 1)
    print(f"fitted log-slope of |alpha|^2 = {slopes[0]:.8f}")
    print(f"free expected slope           = {2 * math.log(args.t1 / args.t2):.8f}")
    print(f"last leakage floor            = {rows[-1]['leakage']:.10f}")
    assert max(row["particle_hole_residual"] for row in rows) < 1e-9
    assert min(row["leakage"] for row in rows) > 0.15


if __name__ == "__main__":
    main()
