# Changelog

## v2.0 — 2026-04-30

**Submitted to Neutrosophic Sets and Systems.**

### Added
- 5-repetition replication: `data/openai_neutrosophic_results_v2.csv` (n=100 instead of n=20)
- New replication script: `src/run_experiment.py`
- New analysis pipeline: `src/analyze_v2.py`
- Boxplot-style figures with raw points (n=20 per box): `results/v2/`
- Acknowledgment of Mason (2026) cross-vendor replication
- `CITATION.cff` for proper attribution
- Formal definition of neutrosophic logic in §2.1
- Appendix A with verbatim S1, S2, S3 prompts
- References to Kuhn 2023, SelfCheckGPT, Atanassov, Smarandache 2018

### Changed
- Hyper-truth rate: from 35% (7/20, v1) to **66% (66/100, v2)**
- Author metadata: ORCID corrected to 0000-0002-9486-5093, email to mleyvaz@gmail.com, affiliation to UBE Guayaquil (Coordinación Académica de Posgrado)
- Abstract: tightened to ≤250 words
- Tables 1–4: now include standard deviations
- §1: added explicit hypothesis statement
- §4 Discussion: comparison against Kuhn 2023 (Semantic Entropy), SelfCheckGPT, conformal abstention; removed speculative claims; added pointer to plithogenic companion note

### Preserved
- v1.0 manuscript at `paper/FINAL_PAPER_v1_archived.md`
- v1.0 dataset at `data/openai_neutrosophic_results.csv`
- v1.0 figures at `results/v1_archived/`
- Mason's citation URL still works (points to repo, not specific commit)

## v1.0 — 2025-12-16

Initial release. Cited by Mason (2026, arXiv:2604.09602).

- 20 evaluations: 4 OpenAI models × 5 phenomena × single shot per cell
- 35% hyper-truth rate reported
- Single-vendor design
