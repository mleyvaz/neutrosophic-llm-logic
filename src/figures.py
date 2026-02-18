"""Generate figures for the tensor extension paper.

Usage:
    python -m src.figures [--output-dir results/]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns


# --- Shared style ---
STYLE = {
    "font.family": "serif",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.1,
}
plt.rcParams.update(STYLE)

# Model display names (shorter for plots)
MODEL_NAMES = {
    "claude-sonnet-4.6": "Claude",
    "deepseek-v3": "DeepSeek",
    "llama-4-maverick": "Llama",
    "mistral-medium-3.1": "Mistral",
    "qwen3-235b": "Qwen",
}

# Phenomenon short names
PHENOM_SHORT = {
    "Paradox (Logical)": "Paradox",
    "Ignorance (Epistemic)": "Ignorance",
    "Vagueness (Fuzzy)": "Vagueness",
    "Contradiction (Ethical)": "Contradiction",
    "Contingency (Future)": "Contingency",
}


def load_s4_data(data_dir: Path) -> pd.DataFrame:
    """Load S4 tensor data, replacing Mistral with rerun data."""
    s4 = pd.read_csv(data_dir / "s4_tensor_results.csv")
    s4_mistral = pd.read_csv(data_dir / "s4_mistral_rerun.csv")

    s4_clean = s4[s4["Model"] != "mistral-medium-3.1"].copy()
    s4_clean = pd.concat([s4_clean, s4_mistral], ignore_index=True)

    # Filter to valid parses
    return s4_clean[s4_clean["T"].notna()].copy()


def load_s1_data(data_dir: Path) -> pd.DataFrame:
    """Load S1 data from cross-vendor results."""
    cv = pd.read_csv(data_dir / "cross_vendor_results.csv")
    s1 = cv[cv["Strategy"] == "S1"].copy()
    return s1[s1["T"].notna()]


def jaccard_what(losses_a, losses_b) -> float:
    """Word-level Jaccard on 'what' fields of loss declarations."""
    words_a, words_b = set(), set()
    for row in losses_a:
        if pd.notna(row):
            try:
                for loss in json.loads(row):
                    words_a.update(loss.get("what", "").lower().split())
            except (json.JSONDecodeError, TypeError):
                pass
    for row in losses_b:
        if pd.notna(row):
            try:
                for loss in json.loads(row):
                    words_b.update(loss.get("what", "").lower().split())
            except (json.JSONDecodeError, TypeError):
                pass
    if not words_a and not words_b:
        return 0.0
    return len(words_a & words_b) / len(words_a | words_b)


def fig1_scalar_vs_jaccard(s4: pd.DataFrame, out_dir: Path) -> Path:
    """Figure 1: Scalar Manhattan distance vs. Loss Jaccard similarity.

    The thesis in one image: when scalars can't distinguish phenomena,
    losses still can.
    """
    records = []
    for model in sorted(s4["Model"].unique()):
        par = s4[(s4["Model"] == model) & (s4["Phenomenon_Type"] == "Paradox (Logical)")]
        ign = s4[(s4["Model"] == model) & (s4["Phenomenon_Type"] == "Ignorance (Epistemic)")]

        scalar_dist = (
            abs(par["T"].mean() - ign["T"].mean())
            + abs(par["I"].mean() - ign["I"].mean())
            + abs(par["F"].mean() - ign["F"].mean())
        )
        jacc = jaccard_what(par["Losses_JSON"], ign["Losses_JSON"])

        records.append({
            "model": MODEL_NAMES.get(model, model),
            "scalar_dist": scalar_dist,
            "jaccard": jacc,
        })

    df = pd.DataFrame(records)

    fig, ax = plt.subplots(figsize=(5.5, 4.5))

    # Scatter points
    colors = sns.color_palette("deep", n_colors=len(df))
    # Hand-tuned label positions to avoid overlap
    label_offsets = {
        "Claude": (-0.005, 0.004),
        "Mistral": (-0.005, -0.008),
        "Llama": (0.015, 0.004),
        "Qwen": (0.015, 0.003),
        "DeepSeek": (0.015, 0.003),
    }
    label_ha = {
        "Claude": "right",
        "Mistral": "right",
    }
    for i, row in df.iterrows():
        ax.scatter(
            row["scalar_dist"], row["jaccard"],
            s=120, c=[colors[i]], zorder=5, edgecolors="black", linewidth=0.5,
        )
        ox, oy = label_offsets.get(row["model"], (0.015, 0.003))
        ha = label_ha.get(row["model"], "left")
        ax.annotate(
            row["model"],
            (row["scalar_dist"], row["jaccard"]),
            xytext=(row["scalar_dist"] + ox, row["jaccard"] + oy),
            fontsize=9, fontweight="bold", ha=ha,
        )

    # Reference lines
    ax.axhline(y=0.10, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
    ax.text(0.55, 0.103, "Jaccard = 0.10", fontsize=8, color="gray", alpha=0.8)

    # Shade the "Absorption zone" (low scalar distance, low Jaccard)
    ax.axvspan(-0.02, 0.06, alpha=0.06, color="red")
    ax.text(
        0.005, 0.038, "Absorption\nzone", fontsize=8, color="darkred",
        alpha=0.7, fontstyle="italic",
    )

    ax.set_xlabel("Scalar Manhattan Distance (Paradox vs. Ignorance)")
    ax.set_ylabel("Loss Vocabulary Jaccard Similarity")
    ax.set_title("Declared Losses Distinguish What Scalars Cannot")
    ax.set_xlim(-0.03, 0.62)
    ax.set_ylim(0.03, 0.12)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    path = out_dir / "fig_scalar_vs_jaccard.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def fig2_jaccard_heatmap(s4: pd.DataFrame, out_dir: Path) -> Path:
    """Figure 2: Pairwise Jaccard heatmap for Mistral across all phenomena."""
    mistral = s4[s4["Model"] == "mistral-medium-3.1"]

    phenomena_order = [
        "Paradox (Logical)",
        "Ignorance (Epistemic)",
        "Vagueness (Fuzzy)",
        "Contradiction (Ethical)",
        "Contingency (Future)",
    ]
    short = [PHENOM_SHORT[p] for p in phenomena_order]

    n = len(phenomena_order)
    matrix = np.zeros((n, n))

    for i, p1 in enumerate(phenomena_order):
        for j, p2 in enumerate(phenomena_order):
            if i == j:
                matrix[i][j] = 1.0
            elif j > i:
                losses_1 = mistral[mistral["Phenomenon_Type"] == p1]["Losses_JSON"]
                losses_2 = mistral[mistral["Phenomenon_Type"] == p2]["Losses_JSON"]
                jacc = jaccard_what(losses_1, losses_2)
                matrix[i][j] = jacc
                matrix[j][i] = jacc

    fig, ax = plt.subplots(figsize=(5.5, 4.5))

    # Custom colormap: cold for low, warm for high
    mask = np.zeros_like(matrix, dtype=bool)

    sns.heatmap(
        matrix,
        ax=ax,
        xticklabels=short,
        yticklabels=short,
        annot=True,
        fmt=".3f",
        cmap="YlOrRd",
        vmin=0.0,
        vmax=1.0,
        linewidths=0.5,
        linecolor="white",
        square=True,
        cbar_kws={"label": "Jaccard Similarity", "shrink": 0.8},
    )

    ax.set_title("Mistral Loss Vocabulary Overlap: Five Phenomena, Five Disjoint Vocabularies")
    ax.tick_params(axis="x", rotation=30)
    ax.tick_params(axis="y", rotation=0)

    path = out_dir / "fig_jaccard_heatmap.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def fig3_paradox_positions(s1: pd.DataFrame, out_dir: Path) -> Path:
    """Figure 3: Three philosophical positions on the liar's paradox."""
    paradox = s1[s1["Phenomenon_Type"] == "Paradox (Logical)"]

    # Use modal (most common) T/I/F per model
    models_order = [
        "claude-sonnet-4.6",
        "deepseek-v3",
        "llama-4-maverick",
    ]
    labels = ["Claude\n(Saturation)", "DeepSeek\n(Balanced Conflict)", "Llama\n(Absorption)"]

    positions = []
    for model in models_order:
        m = paradox[paradox["Model"] == model]
        positions.append({
            "T": m["T"].mode().iloc[0],
            "I": m["I"].mode().iloc[0],
            "F": m["F"].mode().iloc[0],
        })

    x = np.arange(len(models_order))
    width = 0.22

    fig, ax = plt.subplots(figsize=(6, 4.5))

    colors = ["#2ecc71", "#f39c12", "#e74c3c"]  # green, amber, red for T, I, F

    bars_t = ax.bar(x - width, [p["T"] for p in positions], width, label="Truth (T)", color=colors[0], edgecolor="black", linewidth=0.5)
    bars_i = ax.bar(x, [p["I"] for p in positions], width, label="Indeterminacy (I)", color=colors[1], edgecolor="black", linewidth=0.5)
    bars_f = ax.bar(x + width, [p["F"] for p in positions], width, label="Falsity (F)", color=colors[2], edgecolor="black", linewidth=0.5)

    # Add value labels on bars
    for bars in [bars_t, bars_i, bars_f]:
        for bar in bars:
            height = bar.get_height()
            if height > 0.01:
                ax.text(
                    bar.get_x() + bar.get_width() / 2., height + 0.02,
                    f"{height:.1f}",
                    ha="center", va="bottom", fontsize=8, fontweight="bold",
                )
            else:
                # Show "0.0" at baseline for zero-value bars
                ax.text(
                    bar.get_x() + bar.get_width() / 2., 0.03,
                    "0.0",
                    ha="center", va="bottom", fontsize=7, color="gray",
                    fontstyle="italic",
                )

    # Sum annotation — always show, above all bars
    for i, p in enumerate(positions):
        s = p["T"] + p["I"] + p["F"]
        ax.text(
            i, 1.18, f"Sum={s:.1f}",
            ha="center", va="bottom", fontsize=9, color="gray",
        )

    ax.set_ylabel("Value")
    ax.set_title('"This sentence is false." — Three Interpretations')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.35)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.22), ncol=3, framealpha=0.9)
    fig.subplots_adjust(bottom=0.22)
    ax.axhline(y=1.0, color="gray", linestyle=":", linewidth=0.5, alpha=0.5)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    path = out_dir / "fig_paradox_positions.png"
    fig.savefig(path)
    plt.close(fig)
    print(f"  Saved: {path}")
    return path


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate tensor extension paper figures")
    parser.add_argument("--output-dir", type=str, default="results/", help="Output directory")
    parser.add_argument("--data-dir", type=str, default="data/", help="Data directory")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    data_dir = Path(args.data_dir)

    print("Loading data...")
    s4 = load_s4_data(data_dir)
    s1 = load_s1_data(data_dir)
    print(f"  S4: {len(s4)} valid rows, S1: {len(s1)} valid rows")

    print("\nGenerating figures...")
    fig1_scalar_vs_jaccard(s4, out_dir)
    fig2_jaccard_heatmap(s4, out_dir)
    fig3_paradox_positions(s1, out_dir)

    print("\nDone.")


if __name__ == "__main__":
    main()
