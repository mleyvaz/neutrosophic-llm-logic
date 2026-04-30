# v2.0 — Neutrosophic LLM Logic Study, *N* = 100

This release contains the code, prompts, raw data, and figures associated with the manuscript:

> **Breaking the Chains of Probability: Neutrosophic Logic as a New Framework for Epistemic Uncertainty in Large Language Models**
> Maikel Yelandi Leyva-Vázquez, Florentin Smarandache.
> Submitted to *Neutrosophic Sets and Systems*, April 2026.

This v2.0 release includes **100 valid Strategy-1 neutrosophic evaluations** and **300 total API calls** across four OpenAI models (GPT-4o, GPT-4-turbo, GPT-3.5-turbo, GPT-4o-mini), five linguistic phenomena (logical paradox, epistemic ignorance, vagueness, ethical contradiction, future contingency), and three prompting strategies (S1 neutrosophic, S2 probabilistic, S3 entropy-derived), with five repetitions per cell.

## Headline results

- Hyper-truth (T + I + F > 1) emerges in **66.0%** of unconstrained neutrosophic evaluations.
- 95% Wilson confidence interval: **[0.563, 0.747]**.
- Highest rates in **ethical contradiction (95%)** and **future contingency (70%)**.
- Pearson χ² = 11.32, df = 4, *p* = 0.023; Fisher one-vs-rest identifies ethical contradiction as the only phenomenon individually significant (OR = 13.34, *p* = 0.0014).
- Externally replicated by Mason (2026, arXiv:2604.09602) at 84% across five additional vendors.

## What's new in v2.0

- 5 repetitions per cell (vs. single-shot in v1.0): *N* increased from 20 to 100.
- Formal SVNS apparatus: 6 numbered Definitions and 2 Propositions with proofs.
- Wilson 95% confidence interval for the hyper-truth rate.
- χ² and Fisher tests for phenomenon × hyper-truth association.
- New scripts: `src/run_experiment.py` (replication), `src/analyze_v2.py` (analysis pipeline).
- New figures (boxplot + strip plot, *n* = 20 per box) under `results/v2/`.
- Acknowledgment of Mason (2026) cross-vendor replication.
- Plithogenic extension hook (5-tuple structure (P, v, V, d, c)) toward companion note.
- Author metadata corrected (ORCID, email, affiliation).
- Reproducibility statement on the first page of the manuscript.

## Preserved from v1.0

- The exact v1.0 manuscript at [`paper/FINAL_PAPER_v1_archived.md`](paper/FINAL_PAPER_v1_archived.md).
- The v1.0 dataset (*N* = 20) at [`data/openai_neutrosophic_results.csv`](data/openai_neutrosophic_results.csv).
- The v1.0 figures at [`results/v1_archived/`](results/v1_archived).
- The v1.0 commit accessible via tag [`v1.0`](https://github.com/mleyvaz/neutrosophic-llm-logic/tree/v1.0), so the citation in Mason (2026) continues to resolve.

## How to cite

```bibtex
@article{leyva2026breaking,
  title  = {Breaking the Chains of Probability: Neutrosophic Logic as a New
            Framework for Epistemic Uncertainty in Large Language Models},
  author = {Leyva-V{\'a}zquez, Maikel Yelandi and Smarandache, Florentin},
  year   = {2026},
  journal = {Neutrosophic Sets and Systems},
  note   = {Submitted; preprint v2.0 at github.com/mleyvaz/neutrosophic-llm-logic}
}
```

## License

MIT — see [`LICENSE`](LICENSE).
