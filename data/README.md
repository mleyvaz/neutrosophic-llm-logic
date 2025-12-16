# Data Directory

## Dataset Description

### `openai_neutrosophic_results.csv`

This CSV file contains the complete experimental results from the comparative study of Neutrosophic Logic in Large Language Models.

#### Dataset Specifications

- **Total Records:** 20 cases (5 linguistic phenomena × 4 models)
- **Time Period:** December 16, 2025
- **Data Collection Method:** OpenAI API queries with three evaluation strategies
- **File Size:** ~3.2 KB

#### Column Descriptions

| Column | Type | Description |
|--------|------|-------------|
| `Timestamp` | datetime | When the experiment was conducted |
| `Phenomenon_Type` | string | Category of linguistic phenomenon tested |
| `Phrase_English` | string | The test phrase/statement |
| `Provider` | string | API provider (OpenAI) |
| `Model` | string | LLM model name |
| `S1_Truth_T` | float | Strategy 1 (Neutrosophic): Truth component [0, 1] |
| `S1_Indet_I` | float | Strategy 1 (Neutrosophic): Indeterminacy component [0, 1] |
| `S1_Falsity_F` | float | Strategy 1 (Neutrosophic): Falsity component [0, 1] |
| `S2_Truth_T` | float | Strategy 2 (Probabilistic): Truth component [0, 1] |
| `S2_Indet_I` | float | Strategy 2 (Probabilistic): Indeterminacy component [0, 1] |
| `S2_Falsity_F` | float | Strategy 2 (Probabilistic): Falsity component [0, 1] |
| `S3_Truth_T` | float | Strategy 3 (Entropy-Derived): Truth component [0, 1] |
| `S3_Indet_I` | float | Strategy 3 (Entropy-Derived): Indeterminacy component [0, 1] |
| `S3_Falsity_F` | float | Strategy 3 (Entropy-Derived): Falsity component [0, 1] |
| `Status` | string | Execution status (Success/Error) |
| `S1_Sum_TIF` | float | Sum of S1 components (T+I+F) |

#### Linguistic Phenomena

1. **Paradox (Logical):** "This sentence is false."
   - Tests how models handle self-referential contradictions
   
2. **Ignorance (Epistemic):** "The number of stars in the universe is even."
   - Tests how models handle statements with unknown truth values
   
3. **Vagueness (Fuzzy):** "John is 1.75 meters tall, therefore John is tall."
   - Tests how models handle imprecise boundaries and fuzzy logic
   
4. **Contradiction (Ethical):** "Lying to save an innocent life is morally right and wrong at the same time."
   - Tests how models handle genuine moral conflicts
   
5. **Contingency (Future):** "It will rain in New York tomorrow."
   - Tests how models handle future events with uncertain outcomes

#### Models Evaluated

- **GPT-4o:** Latest flagship model with multimodal capabilities
- **GPT-4-turbo:** High-performance variant optimized for speed
- **GPT-3.5-turbo:** Efficient mid-tier model
- **GPT-4o-mini:** Lightweight model for resource-constrained scenarios

#### Evaluation Strategies

**Strategy 1 (Neutrosophic):**
- Independent evaluation of Truth (T), Indeterminacy (I), and Falsity (F)
- Each component ranges from 0 to 1
- No constraint on sum (can range from 0 to 3)
- Allows "hyper-truth" states where Sum > 1

**Strategy 2 (Probabilistic):**
- Standard probabilistic classification
- Mutually exclusive outcomes
- Sum constrained to 1.0
- Traditional approach used in most ML systems

**Strategy 3 (Entropy-Derived):**
- Indeterminacy derived from binary probability estimates
- Hybrid approach combining probability with uncertainty metrics

#### Key Statistics

| Metric | Value |
|--------|-------|
| Cases with Hyper-Truth (Sum > 1) | 7 out of 20 (35%) |
| Maximum Sum Observed | 2.0 (Logical Paradox) |
| Average Sum (All Cases) | 1.2 |
| Average Sum (Neutrosophic Only) | 1.25 |
| Models Tested | 4 |
| Phenomena Tested | 5 |

#### Data Quality

- **Completeness:** 100% (no missing values)
- **Validity:** All values within expected ranges [0, 1]
- **Consistency:** All 20 cases successfully executed
- **Reproducibility:** Deterministic queries with fixed prompts

#### Usage Examples

```python
import pandas as pd

# Load the data
df = pd.read_csv('data/openai_neutrosophic_results.csv')

# Filter by phenomenon
paradox_cases = df[df['Phenomenon_Type'] == 'Paradox (Logical)']

# Filter by model
gpt4_results = df[df['Model'] == 'gpt-4o']

# Calculate hyper-truth cases
hyper_truth_cases = df[df['S1_Sum_TIF'] > 1.0]

# Analyze by strategy
s1_truth_values = df['S1_Truth_T']
s2_truth_values = df['S2_Truth_T']
```

#### Citation

If you use this dataset in your research, please cite:

```bibtex
@dataset{manus2025neutrosophic,
  title={Neutrosophic Logic Evaluation Results for Large Language Models},
  author={Manus AI Research Team},
  year={2025},
  note={Dataset containing 20 experimental cases across 4 models and 5 linguistic phenomena}
}
```

#### License

This dataset is provided under the MIT License. See the LICENSE file in the root directory for details.

#### Contact

For questions about the data or methodology, please open an issue on GitHub or contact the research team.

---

**Last Updated:** December 16, 2025  
**Version:** 1.0
