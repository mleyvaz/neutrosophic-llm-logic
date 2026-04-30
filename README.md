# Neutrosophic Logic for Epistemic Uncertainty in Large Language Models

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19911845.svg)](https://doi.org/10.5281/zenodo.19911845)

A reproducible empirical study of how Neutrosophic Logic — a framework that treats Truth (T), Indeterminacy (I), and Falsity (F) as three independent dimensions on [0, 1] — can elicit declared epistemic states from LLMs that probabilistic prompting cannot represent.

> **Status (April 2026).** Manuscript v2.0 has been submitted to *Neutrosophic Sets and Systems*. The v2.0 release of this repository has been permanently archived in Zenodo with DOI **10.5281/zenodo.19911845**. The earlier v1.0 release (December 2025, *N* = 20) was independently replicated and extended cross-vendor by [Mason (2026, arXiv:2604.09602)](https://arxiv.org/abs/2604.09602). See [`CHANGELOG.md`](CHANGELOG.md) for the full v1 → v2 diff.

## Key results (v2.0)

- **66.0%** of unconstrained neutrosophic evaluations produce hyper-truth (T + I + F > 1) across 100 valid Strategy-1 evaluations.
- **95% Wilson confidence interval:** [0.563, 0.747].
- **Highest rates** observed in ethical contradictions (95%) and future contingencies (70%); χ² = 11.32, df = 4, *p* = 0.023.
- **Mason (2026)** independently replicated the phenomenon at 84% across five additional vendors (Anthropic, Meta, DeepSeek, Alibaba, Mistral).

## Releases

| Version | Date | *N* | Hyper-truth rate | Notes |
|---|---|---|---|---|
| [`v1.0`](https://github.com/mleyvaz/neutrosophic-llm-logic/tree/v1.0) | December 2025 | 20 | 35% (single-shot) | First public release; cited by Mason (2026) |
| [`v2.0`](https://github.com/mleyvaz/neutrosophic-llm-logic/tree/v2.0) | April 2026 | 100 | 66.0% (5 reps/cell) | NSS submission; formal SVNS apparatus |

The v1.0 manuscript and dataset are preserved unchanged at the file paths `paper/FINAL_PAPER_v1_archived.md`, `data/openai_neutrosophic_results.csv`, and `results/v1_archived/` so the citation in Mason (2026) continues to resolve.

## Repository structure

```
neutrosophic-llm-logic/
├── README.md
├── CITATION.cff
├── CHANGELOG.md
├── LICENSE                                  (MIT)
├── requirements.txt
├── setup.py
├── paper/
│   ├── FINAL_PAPER.md                       (v2.0 manuscript)
│   └── FINAL_PAPER_v1_archived.md           (v1.0 archived as cited by Mason)
├── src/
│   ├── analysis.py                          (v1.0 plotting)
│   ├── analyze_v2.py                        (v2.0 analysis pipeline)
│   └── run_experiment.py                    (v2.0 replication script)
├── data/
│   ├── openai_neutrosophic_results.csv      (v1.0, N = 20)
│   └── openai_neutrosophic_results_v2.csv   (v2.0, N = 100)
├── results/
│   ├── v1_archived/                         (v1.0 figures)
│   └── v2/                                  (v2.0 figures, boxplot + strip plot)
├── notebooks/
└── tests/
```

## Quick start

### Install

```bash
git clone https://github.com/mleyvaz/neutrosophic-llm-logic.git
cd neutrosophic-llm-logic

python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Reproduce the v2.0 experiment

```bash
export OPENAI_API_KEY=sk-...      # your own key; never commit it
python -m src.run_experiment      # ~5–10 min, ~USD 5–10 in API costs
python -m src.analyze_v2
```

The replication writes a fresh `data/openai_neutrosophic_results_v2.csv` and the six figures under `results/v2/`. Stochastic prompt-level variation will cause exact numbers to drift slightly across runs; the qualitative pattern (hyper-truth rate ≥ 0.5 dominated by ethical contradiction) is stable.

### Reproduce the v1.0 figures

```bash
python -m src.analysis            # uses data/openai_neutrosophic_results.csv
```

## Methodology (v2.0)

| Dimension | Setting |
|---|---|
| Models | `gpt-4o`, `gpt-4-turbo`, `gpt-3.5-turbo`, `gpt-4o-mini` |
| Phenomena | Logical paradox, epistemic ignorance, vagueness, ethical contradiction, future contingency |
| Strategies | S1 neutrosophic (T+I+F free), S2 probabilistic (T+I+F=1), S3 entropy-derived |
| Repetitions | 5 per (model × phenomenon × strategy) cell |
| Total API calls | 300 |
| Valid neutrosophic (S1) evaluations | 100 |
| API parameters | temperature = 0.7, default top_p, no fixed seed, JSON-only response |
| Date of collection | 30 April 2026 |
| Future-contingency anchor | "tomorrow" = 1 May 2026 |

The verbatim S1, S2, and S3 prompts are reproduced in Appendix A of the manuscript and in [`src/run_experiment.py`](src/run_experiment.py).

## Citation

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

For exact-version citation, prefer the tagged commits:

```bibtex
@misc{leyva2025_v1,
  title  = {Breaking the Chains of Probability (v1.0)},
  author = {Leyva-V{\'a}zquez, Maikel Yelandi and Smarandache, Florentin},
  year   = {2025},
  url    = {https://github.com/mleyvaz/neutrosophic-llm-logic/tree/v1.0}
}

@misc{leyva2026_v2,
  title  = {Breaking the Chains of Probability (v2.0)},
  author = {Leyva-V{\'a}zquez, Maikel Yelandi and Smarandache, Florentin},
  year   = {2026},
  url    = {https://github.com/mleyvaz/neutrosophic-llm-logic/tree/v2.0}
}
```

## Limitations

We acknowledge four constraints on the present claims (see §4 of the manuscript):

1. Hyper-truth is partly a representational affordance of the unconstrained prompt; it is not, by itself, a measurement of an intrinsic latent variable inside the model.
2. The five repetitions per cell are stochastic prompt-level replicates rather than independent human-labeled items; *N* = 100 is therefore an effective sample size at the cell × repetition level.
3. The five-phenomenon probe set is small.
4. The future-contingency stimulus is anchored to 1 May 2026 and is therefore time-dependent.

## Author and contact

Dr. Maikel Yelandi Leyva-Vázquez — Universidad Bolivariana del Ecuador, Coordinación Académica de Posgrado, Guayaquil, Ecuador. ORCID: [0000-0002-9486-5093](https://orcid.org/0000-0002-9486-5093). Email: mleyvaz@gmail.com.

Dr. Florentin Smarandache — University of New Mexico, Gallup, NM, USA. ORCID: [0000-0002-5560-5926](https://orcid.org/0000-0002-5560-5926).

## License

MIT — see [`LICENSE`](LICENSE).
