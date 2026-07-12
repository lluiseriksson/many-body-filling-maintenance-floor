"""Generate the three-panel phase diagram for the many-body filling paper."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from explore_interacting import diagnostics


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "paper" / "many_body_filling_phase_diagram.png"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    t1, t2 = 0.37, 1.0
    zeta = t1 / t2
    m = -np.log(zeta)
    ells = np.arange(2, 31)
    w = (1 - zeta**2) * zeta ** (2 * ells) / (1 - zeta ** (2 * ells + 2))
    logical = w**2
    dilute = w * (1 - w)
    filled = (1 + 2 * w - 3 * w**2) / 4

    interactions = (-0.55, 0.0, 0.55)
    ed = {
        interaction: [diagnostics(ell, t1, t2, interaction) for ell in range(2, 7)]
        for interaction in interactions
    }

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5})
    fig, axes = plt.subplots(1, 3, figsize=(10.9, 3.45), constrained_layout=True)

    ax = axes[0]
    ax.semilogy(ells, logical, "o-", ms=3, lw=1.4, label=r"logical $w_{far}^2$")
    ax.semilogy(ells, dilute, "s-", ms=3, lw=1.4, label=r"dilute leakage $w(1-w)$")
    ax.semilogy(ells, filled, "^-", ms=3, lw=1.4, label="filled leakage")
    ax.axhline(0.25, color="black", ls="--", lw=1, alpha=0.6, label=r"floor $1/4$")
    ax.set_xlabel(r"width $\ell$")
    ax.set_ylabel("exact squared weight")
    ax.set_title("(a) Filling changes the asymptotic class")
    ax.grid(True, which="both", alpha=0.22)
    ax.legend(frameon=False, fontsize=7.2)

    ax = axes[1]
    q = np.linspace(0, 5.2 * m, 300)
    ax.plot(q / m, np.minimum(4 * m, q) / m, lw=2, label=r"filled: $\min\{4m,q\}$")
    ax.plot(q / m, np.minimum(4 * m, 2 * m + q) / m, lw=2, label=r"dilute: $\min\{4m,2m+q\}$")
    ax.axhline(4, color="black", ls="--", lw=1, alpha=0.5)
    ax.set_xlabel(r"filter exponent $q/m$")
    ax.set_ylabel("maintenance exponent / m")
    ax.set_xlim(0, 5.2)
    ax.set_ylim(-0.05, 4.25)
    ax.set_title("(b) Exponent collapse")
    ax.grid(True, alpha=0.22)
    ax.legend(frameon=False, fontsize=7.3, loc="lower right")

    ax = axes[2]
    colors = {-0.55: "#2A6FBB", 0.0: "#444444", 0.55: "#D1495B"}
    for interaction in interactions:
        rows = ed[interaction]
        x = [int(row["ell"]) for row in rows]
        color = colors[interaction]
        ax.semilogy(
            x,
            [row["alpha2"] for row in rows],
            "o--",
            color=color,
            ms=3,
            lw=1.2,
            label=rf"$|\alpha|^2$, $V={interaction:+.2f}$",
        )
        ax.semilogy(
            x,
            [row["leakage"] for row in rows],
            "s-",
            color=color,
            ms=3,
            lw=1.4,
        )
    ax.axhline(0.25, color="black", ls=":", lw=1.1, label=r"leakage floor $1/4$")
    ax.set_xlabel(r"width $\ell$")
    ax.set_ylabel("ED weight")
    ax.set_title("(c) Interaction changes the tail, not the floor")
    ax.grid(True, which="both", alpha=0.22)
    ax.legend(frameon=False, fontsize=6.6, ncol=1)

    fig.suptitle("Finite filling converts remote soft-filter leakage into a many-body floor", fontsize=10.5)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=230, bbox_inches="tight", facecolor="white")
    print(args.output)


if __name__ == "__main__":
    main()
