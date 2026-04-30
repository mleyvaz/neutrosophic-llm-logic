"""
Analysis pipeline for the v2 dataset (n=100).

Generates per-phenomenon and per-model summary tables (with std), the
hyper-truth rate, and the six replication figures (boxplots over the
five repetitions per cell). Output goes to results/v2/.
"""

from __future__ import annotations
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

CSV_PATH = "data/openai_neutrosophic_results_v2.csv"
OUT_DIR = "results/v2"
NAVY = "#1F4E79"
GOLD = "#B8860B"

os.makedirs(OUT_DIR, exist_ok=True)
sns.set_style("whitegrid")
plt.rcParams.update({
    "font.family": "DejaVu Serif",
    "font.size": 10,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
})


def load():
    df = pd.read_csv(CSV_PATH)
    return df[df["Status"] == "Success"].copy()


def report(df):
    print(f"=== n_total = {len(df)} ===\n")
    g1 = df.groupby("Phenomenon_Type").agg(
        T_mean=("S1_Truth_T", "mean"), T_std=("S1_Truth_T", "std"),
        I_mean=("S1_Indet_I", "mean"), I_std=("S1_Indet_I", "std"),
        F_mean=("S1_Falsity_F", "mean"), F_std=("S1_Falsity_F", "std"),
        Sum_mean=("S1_Sum_TIF", "mean"), Sum_std=("S1_Sum_TIF", "std"),
        n=("S1_Truth_T", "count"))
    print("TABLE 1 — by phenomenon")
    print(g1.round(3).to_string())
    g1.round(3).to_csv(os.path.join(OUT_DIR, "table1_phenomenon.csv"))

    g2 = df.groupby("Model").agg(
        T_mean=("S1_Truth_T", "mean"), T_std=("S1_Truth_T", "std"),
        I_mean=("S1_Indet_I", "mean"), I_std=("S1_Indet_I", "std"),
        F_mean=("S1_Falsity_F", "mean"), F_std=("S1_Falsity_F", "std"),
        Sum_mean=("S1_Sum_TIF", "mean"), Sum_std=("S1_Sum_TIF", "std"),
        n=("S1_Truth_T", "count"))
    print("\nTABLE 2 — by model")
    print(g2.round(3).to_string())
    g2.round(3).to_csv(os.path.join(OUT_DIR, "table2_model.csv"))

    df["hyper"] = df["S1_Sum_TIF"] > 1.001
    n_hyper, n_total = int(df["hyper"].sum()), len(df)
    print(f"\nHyper-truth: {n_hyper}/{n_total} = {100*n_hyper/n_total:.1f}%")
    by_phen = df.groupby("Phenomenon_Type")["hyper"].agg(["sum", "count", "mean"])
    by_phen.columns = ["n_hyper", "n_total", "rate"]
    by_phen["rate_pct"] = (by_phen["rate"] * 100).round(1)
    print(by_phen.to_string())
    by_phen.to_csv(os.path.join(OUT_DIR, "table_hypertruth_by_phen.csv"))


def figures(df):
    short = {
        "Paradox (Logical)": "Paradox",
        "Ignorance (Epistemic)": "Ignorance",
        "Vagueness (Fuzzy)": "Vagueness",
        "Contradiction (Ethical)": "Contradiction",
        "Contingency (Future)": "Contingency",
    }
    df["Phen"] = df["Phenomenon_Type"].map(short)
    order = ["Paradox", "Ignorance", "Vagueness", "Contradiction", "Contingency"]

    fig, axes = plt.subplots(1, 3, figsize=(13, 4.5), sharey=True)
    for ax, comp, lbl in zip(
        axes,
        ["S1_Truth_T", "S1_Indet_I", "S1_Falsity_F"],
        ["Truth (T)", "Indeterminacy (I)", "Falsity (F)"]):
        sns.boxplot(data=df, x="Phen", y=comp, order=order, ax=ax,
                    color=NAVY, width=0.6, fliersize=2)
        sns.stripplot(data=df, x="Phen", y=comp, order=order, ax=ax,
                      color=GOLD, alpha=0.4, size=2.5, jitter=0.25)
        ax.set_title(lbl)
        ax.set_xlabel("")
        ax.tick_params(axis="x", rotation=20)
        ax.set_ylim(-0.05, 1.1)
    plt.suptitle("Figure 1. Distribution of neutrosophic components by phenomenon (S1, n=20 per box)", y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig1_components_distribution.png"))
    plt.close()

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.boxplot(data=df, x="Phen", y="S1_Sum_TIF", order=order,
                ax=ax, color=NAVY, width=0.6)
    sns.stripplot(data=df, x="Phen", y="S1_Sum_TIF", order=order,
                  ax=ax, color=GOLD, alpha=0.5, size=4, jitter=0.25)
    ax.axhline(1.0, color="red", linestyle="--", alpha=0.7,
               label="Probabilistic limit")
    ax.set_title("Figure 2. Hyper-truth by phenomenon (T+I+F under S1)")
    ax.set_ylabel("Sum (T + I + F)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig2_hypertruth_sum.png"))
    plt.close()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))
    means_t = pd.DataFrame({
        "S1": df.groupby("Phen")["S1_Truth_T"].mean(),
        "S2": df.groupby("Phen")["S2_Truth_T"].mean(),
    }).reindex(order)
    means_i = pd.DataFrame({
        "S1": df.groupby("Phen")["S1_Indet_I"].mean(),
        "S2": df.groupby("Phen")["S2_Indet_I"].mean(),
    }).reindex(order)
    means_t.plot.bar(ax=ax1, color=[NAVY, GOLD], width=0.7)
    ax1.set_title("Truth: S1 vs S2"); ax1.tick_params(axis="x", rotation=20)
    means_i.plot.bar(ax=ax2, color=[NAVY, GOLD], width=0.7)
    ax2.set_title("Indeterminacy: S1 vs S2"); ax2.tick_params(axis="x", rotation=20)
    plt.suptitle("Figure 3. Comparison of neutrosophic vs. probabilistic strategies", y=1.03)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig3_s1_vs_s2_comparison.png"))
    plt.close()

    fig, ax = plt.subplots(figsize=(9, 5))
    sns.violinplot(data=df, x="Model", y="S1_Sum_TIF", ax=ax,
                   color=NAVY, inner="quartile", cut=0)
    ax.axhline(1.0, color="red", linestyle="--", alpha=0.7)
    ax.set_title("Figure 4. Per-model T+I+F distribution (S1)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig4_model_performance.png"))
    plt.close()

    cols = ["S1_Truth_T", "S1_Indet_I", "S1_Falsity_F", "S1_Sum_TIF",
            "S2_Truth_T", "S2_Indet_I", "S2_Falsity_F"]
    corr = df[cols].corr()
    fig, ax = plt.subplots(figsize=(7.5, 6.5))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r",
                center=0, vmin=-1, vmax=1, square=True, ax=ax,
                cbar_kws={"shrink": 0.7})
    ax.set_title("Figure 5. Correlation matrix")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig5_correlation_heatmap.png"))
    plt.close()

    eth = df[df["Phenomenon_Type"] == "Contradiction (Ethical)"].copy()
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    palette = sns.color_palette("colorblind", n_colors=eth["Model"].nunique())
    sns.scatterplot(data=eth, x="S1_Truth_T", y="S1_Falsity_F",
                    hue="Model", size="S1_Indet_I",
                    sizes=(60, 350), palette=palette, alpha=0.75, ax=ax)
    ax.set_xlim(-0.05, 1.1); ax.set_ylim(-0.05, 1.1)
    ax.set_title("Figure 6. Ethical contradiction (S1)")
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "fig6_ethical_contradiction.png"))
    plt.close()
    print(f"\nGenerated 6 figures in {OUT_DIR}/")


if __name__ == "__main__":
    df = load()
    report(df)
    figures(df)
