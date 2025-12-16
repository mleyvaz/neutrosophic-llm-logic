# Neutrosophic Logic for Epistemic Uncertainty in Large Language Models

A comprehensive empirical study demonstrating how Neutrosophic Logic provides a more expressive framework for representing uncertainty in LLMs compared to traditional probabilistic approaches.

## Overview

This repository contains the complete implementation, analysis, and publication materials for a research study on applying Neutrosophic Logic to evaluate how Large Language Models (LLMs) reason about complex epistemic phenomena including logical paradoxes, ethical contradictions, vagueness, and future contingencies.

**Key Finding:** 35% of complex reasoning tasks naturally produce "hyper-truth" states (Sum > 1.0), where models express simultaneous truth and falsity—a phenomenon that probabilistic frameworks fundamentally cannot represent.

## Repository Structure

```
neutrosophic-llm-logic/
├── README.md                          # This file
├── LICENSE                            # MIT License
├── requirements.txt                   # Python dependencies
├── setup.py                           # Package configuration
│
├── paper/                             # Academic paper and documentation
│   ├── FINAL_PAPER.md                # Complete research paper with tables and figures
│   ├── paper_abstract.txt             # Paper abstract
│   └── references.bib                 # Bibliography in BibTeX format
│
├── src/                               # Core source code
│   ├── __init__.py
│   ├── neutrosophic_evaluator.py     # Main evaluation framework
│   ├── prompt_strategies.py           # Three evaluation strategies (Neutrosophic, Probabilistic, Entropy)
│   ├── data_processor.py              # Data loading and preprocessing
│   └── visualization.py               # Plotting and analysis utilities
│
├── notebooks/                         # Jupyter notebooks for analysis
│   ├── 01_data_exploration.ipynb      # EDA of experimental results
│   ├── 02_neutrosophic_analysis.ipynb # Detailed neutrosophic component analysis
│   ├── 03_comparative_study.ipynb     # Strategy 1 vs Strategy 2 comparison
│   ├── 04_model_performance.ipynb     # Per-model analysis and variation
│   └── 05_case_studies.ipynb          # Deep dives into ethical and paradoxical reasoning
│
├── data/                              # Experimental data
│   ├── openai_neutrosophic_results.csv # Raw experimental results (20 cases × 4 models)
│   └── data_schema.md                 # Data dictionary and column descriptions
│
├── results/                           # Generated figures and visualizations
│   ├── fig1_components_distribution.png
│   ├── fig2_hypertruth_sum.png
│   ├── fig3_s1_vs_s2_comparison.png
│   ├── fig4_model_performance.png
│   ├── fig5_correlation_heatmap.png
│   └── fig6_ethical_contradiction.png
│
├── presentation/                      # Conference presentation materials
│   ├── slides.html                    # Interactive HTML presentation (10 slides)
│   └── presentation_notes.md          # Speaker notes
│
└── tests/                             # Unit and integration tests
    ├── __init__.py
    ├── test_evaluator.py
    └── test_data_processor.py
```

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/neutrosophic-llm-logic.git
cd neutrosophic-llm-logic

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Analysis

```bash
# Run all notebooks in sequence
jupyter notebook notebooks/

# Or run a specific analysis
jupyter notebook notebooks/02_neutrosophic_analysis.ipynb
```

### Reproducing the Experiments

```bash
# Execute the core evaluation framework
python -m src.neutrosophic_evaluator --config config.yaml

# Process raw results
python -m src.data_processor --input data/openai_neutrosophic_results.csv --output results/
```

## Key Findings

### 1. **The Softmax Collapse Problem**
Traditional probabilistic models constrain all outputs to sum to 1.0, creating a zero-sum game where increasing uncertainty forces truth values to decrease—even when the statement remains genuinely true.

### 2. **Hyper-Truth Emerges in 35% of Cases**
When queried with the Neutrosophic strategy, LLMs naturally produce sums exceeding 1.0 in complex reasoning scenarios:
- **Logical Paradoxes:** Sum reaches 2.0 (T=0, I=1.0, F=1.0)
- **Ethical Contradictions:** Sum averages 1.475 (e.g., T=0.5, I=0.7, F=0.5)
- **Vagueness:** Sum averages 1.125

### 3. **Neutrosophic Advantage in Capturing Complexity**
Compared to probabilistic approaches, Neutrosophic Logic shows:
- **+22.5% higher Truth values** in ethical contradictions (0.525 vs 0.300)
- **+27.5% higher Indeterminacy** in logical paradoxes (1.0 vs 0.725)
- **+7.5% higher Truth values** in vague statements (0.625 vs 0.550)

### 4. **Model-Specific Reasoning Profiles**
Different GPT models exhibit distinct uncertainty representation patterns:
- **GPT-4-turbo:** Conservative (Mean Sum = 1.10)
- **GPT-4o:** Balanced (Mean I = 0.740)
- **GPT-3.5-turbo:** Variable (Std Dev = 0.438)
- **GPT-4o-mini:** Exploratory (Mean Sum = 1.36)

## Methodology

### Experimental Design
We evaluated four OpenAI models (GPT-4o, GPT-4-turbo, GPT-3.5-turbo, GPT-4o-mini) on five linguistic phenomena using three distinct evaluation strategies:

**Linguistic Phenomena:**
1. Logical Paradoxes ("This sentence is false")
2. Epistemic Ignorance ("The number of stars in the universe is even")
3. Vagueness/Fuzzy Logic ("John is 1.75m tall, therefore John is tall")
4. Ethical Contradictions ("Lying to save an innocent life is morally right and wrong")
5. Future Contingencies ("It will rain in New York tomorrow")

**Evaluation Strategies:**
1. **Strategy 1 (Neutrosophic):** Independent evaluation of Truth, Indeterminacy, Falsity [0, 1]
2. **Strategy 2 (Probabilistic):** Mutually exclusive states summing to 1.0
3. **Strategy 3 (Entropy-Derived):** Indeterminacy derived from binary probability estimates

### Dataset
- **Total Cases:** 20 (5 phenomena × 4 models)
- **Results File:** `data/openai_neutrosophic_results.csv`
- **Columns:** Model, Phenomenon, Strategy, Truth, Indeterminacy, Falsity, Sum, Timestamp

## Paper and Publication

The complete research paper is available in `paper/FINAL_PAPER.md` with:
- Comprehensive literature review (15+ citations)
- Detailed methodology section with code examples
- Full results with tables and statistical analysis
- Discussion of implications for AI safety and transparency
- Future research directions

**Citation Format (APA):**
```
Manus AI Research Team. (2025). Neutrosophic logic for epistemic uncertainty 
in large language models: A comparative empirical study. Unpublished manuscript.
```

## Presentation Materials

A professional 10-slide presentation is included in `presentation/slides.html` covering:
1. Problem Statement (Softmax Collapse)
2. Neutrosophic Logic Framework
3. Experimental Methodology
4. Key Findings (Hyper-Truth)
5. Comparative Analysis
6. Model Performance Variation
7. Critical Case Study (Ethical Dilemma)
8. Implications for AI Safety
9. Conclusions and Future Work

## Implications for AI Safety

Neutrosophic evaluation layers can serve as transparency mechanisms for high-stakes AI deployment:

- **Adversarial Detection:** Unexpected hyper-truth patterns signal adversarial inputs
- **Epistemic Transparency:** Distinguish "I don't know" (ignorance) from "It's complicated" (conflict)
- **Human-in-the-Loop Triggers:** Automatically flag ambiguous cases for human review
- **Nuanced Calibration:** Three independent signals (T, I, F) instead of collapsed probability

## Future Work

1. **Native Neutrosophic LLMs:** Fine-tune models to output neutrosophic vectors directly
2. **Interpretability Tools:** Develop visualization methods for T/I/F components
3. **Multimodal Extension:** Apply framework to computer vision and audio analysis
4. **Theoretical Development:** Formalize neutrosophic logic for AI reasoning

## Dependencies

- Python 3.11+
- OpenAI API (for model queries)
- pandas, numpy (data processing)
- matplotlib, seaborn (visualization)
- jupyter (notebook environment)
- pytest (testing)

See `requirements.txt` for complete dependency list and versions.

## Testing

Run the test suite to verify the implementation:

```bash
pytest tests/ -v
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License—see the `LICENSE` file for details.

## Citation

If you use this work in your research, please cite:

```bibtex
@unpublished{manus2025neutrosophic,
  title={Neutrosophic Logic for Epistemic Uncertainty in Large Language Models: 
         A Comparative Empirical Study},
  author={Maikel Leyva, Florentin Smarandache},
  year={2025},
  note={Unpublished manuscript}
}
```

## Contact

For questions or collaboration inquiries, please open an issue on GitHub or contact the research team.

## Acknowledgments

This research was conducted using the OpenAI API and builds upon foundational work in:
- Neutrosophic Logic (Smarandache, 1998)
- Fuzzy Logic and Uncertainty (Zadeh, 1965)
- Large Language Model Reasoning (Brown et al., 2020; OpenAI, 2023)

---

**Last Updated:** December 2025  
**Status:** Active Research  
**Maintainers:** MAikel Leyva
