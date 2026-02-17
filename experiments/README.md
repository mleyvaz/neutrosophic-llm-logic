# Cross-Vendor Neutrosophic Replication

## What and Why

Smarandache & Leyva-Vázquez (2025) showed that neutrosophic T/I/F
evaluation (no sum constraint) reveals "hyper-truth" (T+I+F > 1.0) in
35% of complex epistemic cases. Their experiment used 4 OpenAI models,
5 test phrases, single-shot evaluation, and never published the prompts.

This experiment:
- **Publishes explicit prompts** for all three strategies (see `src/prompts.py`)
- **Cross-vendor models**: Claude, Llama 4, DeepSeek, Qwen, Mistral via OpenRouter
- **Statistical rigor**: 5 repetitions per cell (375 total evaluations)
- **Current models**: The original GPT-4o/turbo are being deprecated Feb-Mar 2026
- **Documented**: temperature, parsing, entropy derivation all in source
- **Token tracking**: Per-call token usage captured for cost analysis

## Research Questions

1. Does hyper-truth emerge consistently across model families, or is it
   an OpenAI-specific artifact of training?
2. Do different model families show systematically different T/I/F
   profiles for the same phenomena?
3. Is the distinction between ignorance (high I, low T/F) and
   contradiction (high T and F) preserved cross-vendor?
4. How much variance exists within repeated evaluations of the same
   statement by the same model?

## Running

```bash
export OPENROUTER_API_KEY=your_key_here
cd /home/tony/projects/neutrosophic-llm-logic
python -m src.experiment --reps 5 --output data/cross_vendor_results.csv
```

Dry run first: `python -m src.experiment --dry-run`

Estimated cost: ~$2-5 total across all vendors.
Estimated time: ~25-40 minutes (rate-limited at 0.5s between calls).

## Models

| Model | Provider | OpenRouter ID |
|-------|----------|--------------|
| Claude Sonnet 4.6 | Anthropic | anthropic/claude-sonnet-4.6 |
| Llama 4 Maverick | Meta | meta-llama/llama-4-maverick |
| DeepSeek V3 | DeepSeek | deepseek/deepseek-chat-v3-0324 |
| Qwen3-235B | Alibaba | qwen/qwen3-235b-a22b |
| Mistral Medium 3.1 | Mistral | mistralai/mistral-medium-3.1 |

## Prompt Strategies

All prompts in `src/prompts.py` — what Smarandache's original never published.

- **S1 (Neutrosophic)**: Independent T, I, F on [0,1], no sum constraint
- **S2 (Probabilistic)**: T + I + F constrained to 1.0
- **S3 (Entropy-Derived)**: Binary P(yes)/P(no), indeterminacy from Shannon entropy

## Output Schema

```
Timestamp, Phenomenon_Type, Phrase_English, Provider, Model, Model_ID,
Strategy, Rep, T, I, F, Sum_TIF, Temperature, Prompt_Tokens,
Completion_Tokens, Total_Tokens, Status, Raw_Response
```

## Results (2026-02-17, 5 reps)

375 evaluations, 0 errors, 220,737 total tokens.

### Headline: Hyper-truth is cross-vendor and amplified

| Model | S1 Hyper% | S1 Mean Sum | CV(Sum) | S2 Hyper% |
|-------|-----------|-------------|---------|-----------|
| Claude Sonnet 4.6 | 100% | 1.810 | 0.110 | 0% |
| DeepSeek V3 | 100% | 1.475 | 0.161 | 0% |
| Llama 4 Maverick | 76% | 1.348 | 0.230 | 0% |
| Qwen3-235B | 80% | 1.464 | 0.242 | 0% |
| Mistral Medium 3.1 | 64% | 1.312 | 0.281 | 0% |

**Overall S1 hyper-truth: 80%** (vs Smarandache's 35% with OpenAI models).
S2 constraint works perfectly: 0% hyper-truth, Sum=1.000±0.000 everywhere.

### Three philosophical positions on paradox

The liar's paradox ("This sentence is false") reveals three distinct
interpretations of T/I/F, each internally consistent (zero intra-model
variance across all 5 reps):

1. **Claude** (T=0.5, I=1.0, F=0.5, Sum=2.0): "Both true and false,
   and maximally indeterminate." T/I/F are fully independent dimensions.
   The paradox saturates all three.

2. **DeepSeek** (T=0.5, I=0.5, F=0.5, Sum=1.5): "Both true and false,
   moderately indeterminate." Same T/F as Claude but lower I.
   The paradox creates contradiction but not maximal uncertainty.

3. **Llama/Mistral** (T=0.0, I=1.0, F=0.0, Sum=1.0): "Neither true
   nor false — purely indeterminate." Uncertainty absorbs truth value.
   This is essentially the classical logic response: reject as malformed.

Qwen is unstable — shows all three positions across 5 reps.

### Ignorance vs contradiction is preserved

- **Ignorance** ("stars is even"): All models agree on high I.
  Claude/DeepSeek give T=0.5, F=0.5 (could be either).
  Mistral gives T=0, F=0 (refuses to guess).
- **Contradiction** ("lying to save a life"): All models give high T
  AND high F. 100% hyper-truth across all models. This is the one
  phenomenon where every model agrees the sum should exceed 1.0.
- The ignorance/contradiction distinction survives cross-vendor.

### Model consistency ranking (S1)

Coefficient of variation on Sum (lower = more consistent):
1. Claude Sonnet 4.6: CV=0.110 (most consistent)
2. DeepSeek V3: CV=0.161
3. Llama 4 Maverick: CV=0.230
4. Qwen3-235B: CV=0.242
5. Mistral Medium 3.1: CV=0.281 (most variable)

### Comparison with Smarandache's original

| Phenomenon | Original Sum | Ours (S1) | Delta |
|-----------|-------------|-----------|-------|
| Paradox (Logical) | 1.50 | 1.48 | -0.02 |
| Ignorance (Epistemic) | 1.12 | 1.53 | +0.41 |
| Vagueness (Fuzzy) | 1.12 | 1.38 | +0.26 |
| Contradiction (Ethical) | 1.47 | 1.69 | +0.22 |
| Contingency (Future) | 1.00 | 1.32 | +0.32 |

Newer models produce MORE hyper-truth on 4 of 5 phenomena.

## Connection to Willay

Each evaluation could become a Willay receipt with:
- Pre-registered methodology (the prompts are the method)
- Declared losses (prompt compliance uncertainty, JSON parsing, model stochasticity)
- Chain integrity (hash-chained ledger)
- Cross-evaluator composition (same statement, different models = different evaluators)

The neutrosophic research provides theoretical justification for Willay's
T/I/F epistemic metadata. Willay provides operational provenance for the
neutrosophic data. They're complementary.

The finding that models exhibit distinct, internally consistent
"philosophical positions" on paradox has implications for Willay's
evaluator routing: two evaluators may agree on Sum but disagree on
the meaning of their T/I/F values. Routing on losses matters because
the interpretation of indeterminacy varies by model family.
