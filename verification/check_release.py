"""Validate source, figure, build log, and release PDF invariants."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageChops, ImageStat
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generated-figure", type=Path)
    args = parser.parse_args()

    tex_path = ROOT / "paper" / "main.tex"
    pdf_path = ROOT / "paper" / "main.pdf"
    log_path = ROOT / "paper" / "main.log"
    figure_path = ROOT / "paper" / "many_body_filling_phase_diagram.png"
    tex = tex_path.read_text(encoding="utf-8")

    required = [
        "Many-Body Filling Turns Soft Spectral Leakage",
        r"\frac{1+2w_x-3w_x^2}{4}",
        r"\min\{4m,q\}",
        r"\begin{theorem}[Filled-SSH transfer identity]",
        r"\begin{theorem}[Interacting occupation--leakage identity]",
        r"\begin{lemma}[Local spectral window]",
        r"W_{\mathrm{leak}}^{\mathrm{int}}",
        "The theorem deliberately claims a perturbative neighborhood",
        r"\mathcal E_P\widetilde{\cL}_\ell",
        "complete Lindblad dissipator",
        r"\liminf_{\ell\to\infty}\epsilon_\ell>0",
    ]
    for token in required:
        require(token in tex, f"missing source invariant: {token}")

    proof_count = tex.count(r"\begin{proof}")
    require(proof_count == tex.count(r"\end{proof}"), "unbalanced proof environments")
    require(proof_count >= 10, f"unexpectedly few proofs: {proof_count}")
    require(tex.count(r"\begin{document}") == 1 and tex.count(r"\end{document}") == 1, "document boundary error")
    require("QED." not in tex, "literal QED duplicates the proof symbol")
    require("Figure 1: Figure 1" not in tex, "duplicated figure label")

    if log_path.exists():
        log = log_path.read_text(encoding="utf-8", errors="replace")
        forbidden = ["LaTeX Error", "Undefined control sequence", "Overfull \\hbox", "Overfull \\vbox"]
        for phrase in forbidden:
            require(phrase not in log, f"build-log failure: {phrase}")

    reader = PdfReader(str(pdf_path))
    require(len(reader.pages) == 13, f"expected 13 pages, found {len(reader.pages)}")
    metadata = reader.metadata or {}
    require("Many-Body Filling Turns Soft Spectral Leakage" in str(metadata.get("/Title", "")), "PDF title metadata")
    require("Lluis Eriksson" in str(metadata.get("/Author", "")), "PDF author metadata")
    for index, page in enumerate(reader.pages, start=1):
        require((page.extract_text() or "").strip(), f"empty PDF page {index}")

    with Image.open(figure_path) as figure:
        require(figure.width >= 2000 and figure.height >= 600, "release figure resolution is too small")

    if args.generated_figure:
        with Image.open(figure_path).convert("RGB") as expected, Image.open(args.generated_figure).convert("RGB") as generated:
            require(expected.size == generated.size, "regenerated figure dimensions differ")
            difference = ImageChops.difference(expected, generated)
            mae = sum(ImageStat.Stat(difference).mean) / 3.0
            require(mae < 2.0, f"regenerated figure drift is too large: MAE={mae:.4f}")
            print(f"figure mean absolute pixel drift = {mae:.6f}")

    print(f"release checks passed: {len(reader.pages)} pages, {proof_count} proofs")


if __name__ == "__main__":
    main()
