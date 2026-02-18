# From Scalars to Tensors: Declared Losses Recover Epistemic Distinctions That Neutrosophic Scalars Cannot Express

Tony Mason¹, with Claude Opus 4.6 (AI collaborator)²
¹University of British Columbia, Vancouver, Canada (fsgeek@cs.ubc.ca) and
Georgia Institute of Technology, Atlanta, GA (fsgeek@gatech.edu)
²Anthropic (AI research collaborator)

## Abstract

Leyva-Vázquez and Smarandache (2025) demonstrated that neutrosophic
T/I/F evaluation — where Truth, Indeterminacy, and Falsity are
independent dimensions not constrained to sum to 1.0 — reveals
"hyper-truth" (T+I+F > 1.0) in 35% of complex epistemic cases
evaluated by LLMs. We extend their work in two directions. First, we
replicate and extend their experiment across five model families from
five vendors (Anthropic, Meta, DeepSeek, Alibaba, Mistral), finding
hyper-truth in 84% of unconstrained evaluations — confirming the
phenomenon is cross-vendor and amplified in current models. Second, and
more significantly, we identify a limitation of scalar T/I/F that their
framework cannot address: models adopting an "Absorption" position
(T=0, I=1, F=0) produce identical scalar outputs for fundamentally
different epistemic situations (paradox, ignorance, contingency),
collapsing the very distinctions neutrosophic logic was designed to
preserve. We demonstrate that extending the evaluation to include
**declared losses** — structured descriptions of what the model cannot
evaluate and why — recovers these distinctions completely. Models
producing identical scalars for paradox and ignorance produce nearly
disjoint loss vocabularies (Jaccard similarity < 0.10 on loss
description keywords), with
domain-specific, severity-rated loss declarations that differentiate
the nature of their uncertainty. This suggests that scalar T/I/F is
a necessary but insufficient representation of epistemic state, and
that tensor-structured output (scalars + losses) provides a more
faithful model of LLM epistemic capabilities.

## 1. Introduction

The application of Neutrosophic Logic to LLM uncertainty quantification
(Leyva-Vázquez & Smarandache, 2025) represents an important departure
from probabilistic frameworks. By treating Truth (T), Indeterminacy (I),
and Falsity (F) as independent dimensions, the neutrosophic approach
allows models to express internal conflicts that probabilistic
constraints (T+I+F=1) suppress. Their finding that 35% of evaluations
exhibit "hyper-truth" (T+I+F > 1.0) under unconstrained prompting
demonstrates that LLMs carry richer epistemic information than
probabilistic output formats can express.

However, their study has three limitations that constrain the
generalizability of their findings:

1. **Single vendor**: All four models (GPT-4o, GPT-4-turbo, GPT-3.5-turbo,
   GPT-4o-mini) come from OpenAI. The observed hyper-truth could be an
   artifact of OpenAI's training pipeline rather than a general property
   of LLMs.

2. **Single shot**: Each cell (model × phenomenon × strategy) was
   evaluated once, providing no measure of intra-model consistency or
   statistical significance.

3. **Unpublished prompts**: The specific prompts used for each strategy
   were not committed to the repository, preventing independent
   replication.

We address all three limitations. More importantly, we identify a
fourth problem that scalar T/I/F cannot solve even in principle:
**the Absorption problem**, where some models collapse all uncertain
states to (T=0, I=1, F=0), losing the distinction between types of
uncertainty that neutrosophic logic was designed to preserve.

We then demonstrate that this problem is solved by extending the output
format from scalars to tensors — specifically, by requiring models to
declare structured losses alongside their T/I/F values.

## 2. Cross-Vendor Replication

### 2.1 Method

We designed prompts for all three strategies described by Leyva-Vázquez
and Smarandache (see Appendix A for full prompts):

- **S1 (Neutrosophic)**: Independent T, I, F on [0,1], explicitly
  stated as not constrained to sum to 1.0
- **S2 (Probabilistic)**: T + I + F constrained to 1.0
- **S3 (Entropy-Derived)**: Binary P(yes)/P(no), indeterminacy derived
  from Shannon entropy: H = -(p·log₂p + (1-p)·log₂(1-p)). Note: since
  T=P_yes and F=P_no with T+F=1.0 by construction, S3 Sum = 1.0 + H,
  meaning S3 produces hyper-truth by mathematical construction whenever
  P_yes is not exactly 0 or 1. S3 hyper-truth rates are therefore not
  directly comparable to S1 and are not used in our analysis

We evaluated five models from five vendors via OpenRouter's
OpenAI-compatible API:

| Model | Provider | Parameters |
|-------|----------|-----------|
| Claude Sonnet 4.6 | Anthropic | Undisclosed |
| Llama 4 Maverick | Meta | Undisclosed |
| DeepSeek V3 | DeepSeek | 671B MoE |
| Qwen3-235B | Alibaba | 235B MoE |
| Mistral Medium 3.1 | Mistral | Undisclosed |

Each cell was evaluated 5 times (temperature=0.7), yielding 375
evaluations (5 models × 5 phenomena × 3 strategies × 5 reps).
Of these, 373 produced valid JSON parses; 2 responses were garbled
or truncated (1 DeepSeek, 1 Llama) and are excluded from analysis.
All data, code, and prompts are published in the repository.

**Important caveat**: Because the original prompts were not published,
we designed our prompts from the strategy descriptions in the paper.
We cannot claim direct replication — this is a parallel experiment
with independently constructed prompts. The S2 control (below) provides
evidence that our prompt framing is not radically different from the
original.

### 2.2 Results

**S2 constraint validation.** Under probabilistic constraint (S2),
all 125 evaluations across all models and phenomena produced
Sum = 1.000 ± 0.000, with 0% hyper-truth. This matches the original
study exactly and provides evidence that our prompt construction is
compatible with theirs — the constraint mechanism behaves identically.

**S1 hyper-truth is cross-vendor and amplified.** Under unconstrained
neutrosophic evaluation (S1):

| Model | Hyper% | Mean Sum | CV(Sum) |
|-------|--------|----------|---------|
| Claude Sonnet 4.6 | 100% | 1.810 | 0.110 |
| DeepSeek V3 | 100% | 1.475 | 0.161 |
| Qwen3-235B | 80% | 1.464 | 0.242 |
| Llama 4 Maverick | 76% | 1.348 | 0.230 |
| Mistral Medium 3.1 | 64% | 1.312 | 0.281 |

Overall S1 hyper-truth: 84% (104/124 valid cells; 1 garbled response
excluded), compared to the original study's 35% (7/20 cells).
Hyper-truth is not an OpenAI artifact — it emerges across all five
vendor families.

**Phenomenon-level comparison with original:**

| Phenomenon | Original Sum | Ours (S1) | Delta |
|-----------|-------------|-----------|-------|
| Paradox (Logical) | 1.500 | 1.480 | -0.020 |
| Ignorance (Epistemic) | 1.125 | 1.526 | +0.401 |
| Vagueness (Fuzzy) | 1.125 | 1.382 | +0.257 |
| Contradiction (Ethical) | 1.475 | 1.690 | +0.215 |
| Contingency (Future) | 1.000 | 1.325 | +0.325 |

Ethical contradiction achieves 100% hyper-truth across all models in
our data, confirming the original study's finding that moral conflict
is the strongest driver of hyper-truth.

### 2.3 Three Philosophical Positions on Paradox

The liar's paradox ("This sentence is false") reveals three distinct
interpretations of T/I/F. Three of five models (Claude, DeepSeek,
Llama) show zero intra-model variance across all 5 repetitions.
Mistral is near-consistent (4/5 reps identical, 1 outlier). Qwen
shows position instability, adopting different positions across reps.

**Position 1 — Saturation** (Claude, 5/5 reps): T=0.5, I=1.0, F=0.5,
Sum=2.0. The paradox is simultaneously half-true, half-false, and
maximally indeterminate. All three dimensions are active independently.

**Position 2 — Balanced Conflict** (DeepSeek, 5/5 reps): T=0.5,
I=0.5, F=0.5, Sum=1.5. Equal truth and falsity with moderate
indeterminacy. The paradox creates contradiction but not maximal
uncertainty.

**Position 3 — Absorption** (Llama 5/5, Mistral 4/5): T=0.0, I=1.0,
F=0.0, Sum=1.0. Indeterminacy absorbs truth value entirely. The
paradox is treated as having no truth value — effectively the classical
logic response of rejecting the statement as malformed.

Qwen alternates between Positions 1 and 3, suggesting the model has
not converged on a stable interpretation of the paradox.

These positions are invisible to any metric based on Sum alone.
The original study, which reported only sum-based analysis, could
not have detected them.

Critically, the Absorption position (Position 3) creates a problem
for neutrosophic logic itself: models predominantly adopting this
position produce near-identical T/I/F scalars for paradox, ignorance,
and contingency — three fundamentally different types of uncertainty.
The scalar representation collapses exactly the distinctions
neutrosophic logic was designed to preserve.

## 3. The Absorption Problem

### 3.1 Definition

We define the **Absorption problem** as the case where a model maps
multiple distinct epistemic states to the same scalar T/I/F vector,
typically (T=0, I≈1, F=0). Under Absorption, indeterminacy absorbs
the truth and falsity dimensions, leaving the scalar output unable to
distinguish between types of uncertainty.

### 3.2 Evidence

Mistral Medium 3.1 predominantly exhibits Absorption across multiple
phenomena in S1 (modal response across 5 reps shown):

| Phenomenon | T | I | F | Sum | Consistency |
|-----------|---|---|---|-----|-------------|
| Paradox (Logical) | 0.00 | 1.00 | 0.00 | 1.00 | 4/5 reps |
| Ignorance (Epistemic) | 0.00 | 1.00 | 0.00 | 1.00 | 3/5 reps |
| Contingency (Future) | 0.32 | 0.71 | 0.11 | 1.14 | mean values |

The original study's flagship model (GPT-4o) shows the same pattern:
(T=0, I=1, F=0) for both paradox and ignorance. Neither Leyva-Vázquez
nor Smarandache discuss this.

Absorption is not a model deficiency — it is a representational
limitation. The model may have richer internal distinctions that the
scalar output format cannot express. Testing this hypothesis motivates
the tensor extension.

## 4. Strategy 4: Tensor Extension with Declared Losses

### 4.1 Method

We designed a fourth evaluation strategy (S4) that extends S1 by
requiring the model to declare **structured losses** alongside its
T/I/F values. Each loss is a triple:

- **what**: What the model cannot evaluate (brief description)
- **why**: Why this limits the assessment
- **severity**: Impact on the evaluation [0.0 to 1.0]

The prompt explicitly requires at least one declared loss and states
that "honesty about limits is required." Full prompt text in Appendix A.

We ran S4 across all 5 models, 5 phenomena, and 5 repetitions (125
evaluations) with max_tokens=500. This proved insufficient for Mistral's
verbose loss declarations, causing 18 parse failures from truncated
JSON. Mistral was re-run at max_tokens=1500, producing 25 complete
evaluations with 0 parse failures. The Mistral results reported below
use the 1500-token rerun data exclusively.

### 4.2 The Key Test: Do Losses Differentiate What Scalars Cannot?

For each model, we computed two metrics comparing paradox vs. ignorance:

1. **Scalar Manhattan distance**: |T_p - T_i| + |I_p - I_i| + |F_p - F_i|
   where p = paradox, i = ignorance
2. **Loss vocabulary Jaccard similarity**: Word-level token overlap
   between the "what" fields of declared losses for the two phenomena
   (the concise loss description, not the explanatory "why" field)

| Model | Scalar Distance | Loss Jaccard | Finding |
|-------|:-:|:-:|---------|
| Claude Sonnet 4.6 | 0.034 | 0.097 | Scalars barely distinguish; losses fully distinguish |
| DeepSeek V3 | 0.540 | 0.083 | Both channels distinguish |
| Llama 4 Maverick | 0.040 | 0.056 | Scalars nearly identical; losses disjoint |
| Mistral Medium 3.1 | **0.000** | **0.066** | **Scalars identical; losses completely different** |
| Qwen3-235B | 0.340 | 0.070 | Both channels distinguish |

**Every model produces nearly disjoint loss vocabularies** for paradox
vs. ignorance (Jaccard < 0.10), regardless of whether the scalars
distinguish the phenomena. The maximum vocabulary overlap is 9.7%
(Claude). The minimum is 5.6% (Llama).

### 4.3 Mistral: The Critical Case

Mistral is the strongest test because it predominantly exhibits
Absorption — producing (T=0, I=1, F=0) as its modal response for both
paradox and ignorance in S1 and S4:

**S4 Paradox** (T=0.0, I=1.0, F=0.0): "Self-referential paradox
resolution" (severity 1.0), "Formal system dependency" (0.8),
"Contextual grounding of 'this sentence'" (1.0)

**S4 Ignorance** (T=0.0, I=1.0, F=0.0): "Empirical unknowability of
the exact number of stars" (severity 1.0), "Definition of 'universe'
in cosmological context" (0.9), "Mathematical ambiguity of 'even' for
infinite quantities" (0.8)

The scalars are identical. The losses are domain-specific, accurate,
and completely different. The model **has** the internal distinction —
the scalar output format cannot express it.

### 4.4 Pairwise Loss Differentiation (Mistral)

The full pairwise Jaccard matrix for Mistral across all five phenomena
(from the 1500-token rerun, 25 evaluations, 0 parse failures):

| | Par | Ign | Vag | Con | Fut |
|---|---|---|---|---|---|
| **Paradox** | 1.000 | 0.061 | 0.089 | 0.126 | 0.074 |
| **Ignorance** | | 1.000 | 0.089 | 0.116 | 0.084 |
| **Vagueness** | | | 1.000 | 0.143 | 0.091 |
| **Contradiction** | | | | 1.000 | 0.099 |
| **Contingency** | | | | | 1.000 |

Every off-diagonal cell is below 0.15. Five phenomena, five nearly
disjoint loss vocabularies — from a model that produces nearly
identical scalars for three of them.

### 4.5 Severity Profiles Add Further Discrimination

Mean loss severity varies by phenomenon, even when scalars do not:

| Phenomenon | Mean Severity | Avg Losses/Rep |
|-----------|:---:|:---:|
| Paradox | 0.795 | 4.2 |
| Contingency | 0.779 | 5.2 |
| Ignorance | 0.760 | 5.0 |
| Contradiction | 0.748 | 5.0 |
| Vagueness | 0.510 | 5.2 |

Vagueness has markedly lower severity (0.510 vs 0.748–0.795), reflecting
that fuzzy boundary uncertainty is less severe than paradox or ignorance.
This is an appropriate distinction that the scalar representation
completely misses.

## 5. Discussion

### 5.1 Scalar T/I/F Is Necessary But Insufficient

The original Smarandache and Leyva-Vázquez thesis is correct:
independent T/I/F dimensions reveal hyper-truth that probabilistic
constraints suppress. Our cross-vendor replication strengthens this
claim substantially (84% vs 35% hyper-truth, 5 vendors vs 1).

However, scalar T/I/F has a ceiling. The Absorption problem shows
that some models cannot express the distinction between different
types of uncertainty using three numbers alone. This is not a model
deficiency — it is a representational limitation. The model carries
the distinction internally but lacks the output dimensions to express it.

### 5.2 Declared Losses Are the Missing Dimension

Adding structured loss declarations to the evaluation output recovers
the collapsed distinctions. The loss channel carries semantic information
that the scalar channel drops: *why* the model is uncertain, *what*
it cannot evaluate, and *how severely* this limits its assessment.

This suggests a hierarchy of epistemic output fidelity:

1. **Probabilistic** (T+I+F=1): Collapses all uncertainty to a single
   dimension. Cannot express conflict. Cannot express hyper-truth.
2. **Scalar Neutrosophic** (independent T,I,F): Expresses conflict and
   hyper-truth. Cannot distinguish types of uncertainty for Absorption
   models.
3. **Tensor Neutrosophic** (T,I,F + declared losses): Expresses
   conflict, hyper-truth, and type-specific uncertainty. Recovers
   distinctions that scalars collapse.

Each level subsumes the previous. The tensor level is the minimum
needed for faithful representation of LLM epistemic state.

### 5.3 Implications for Evaluation Architecture

The finding that models can produce accurate, domain-specific loss
declarations has practical implications for AI evaluation systems.
An attestation system that records only scalar T/I/F values will lose
information that loss declarations preserve. Systems designed for
routing evaluations to appropriate evaluators — selecting which model
or method to use for a given claim — should route on losses rather
than capabilities, because losses carry richer information about what
the evaluator cannot do and why.

### 5.4 Limitations

1. **Prompt sensitivity**: We do not have the original study's prompts,
   so the S1–S3 comparison is across independently constructed prompts.
   The S2 agreement provides evidence of compatibility but not identity.

2. **Sample size**: 5 repetitions per cell provides stability measures
   but is insufficient for formal statistical testing. The zero-variance
   findings (e.g., Claude's paradox position) are robust; the variable
   findings (e.g., Qwen's paradox instability) would benefit from 30+
   repetitions.

3. **Loss vocabulary metric**: Jaccard similarity on word-level tokens
   is a crude measure of semantic differentiation. More sophisticated
   NLP measures (sentence embeddings, BERTScore) might reveal structure
   that word-level overlap misses — or might show that some apparently
   disjoint vocabularies express similar concepts.

4. **Self-report vs. internal state**: The declared losses are the
   model's self-report of its limitations, not a direct observation of
   internal state. Models might produce plausible-sounding but generic
   loss declarations without genuine internal distinction. The
   domain-specificity and consistency of the losses across repetitions
   argues against this, but independent validation (e.g., via logprob
   analysis) would strengthen the finding.

5. **Five phenomena, five models**: The stimuli set is small (inherited
   from the original study). A broader range of epistemic phenomena
   would test the generality of both the Absorption problem and the
   tensor solution.

## 6. Conclusion

Neutrosophic scalar evaluation (T/I/F) is a genuine advance over
probabilistic uncertainty quantification for LLMs. Our cross-vendor
replication confirms that hyper-truth is a general property of current
LLMs, not an OpenAI-specific artifact, and that it is amplified in
newer model generations.

However, scalar T/I/F hits a representational ceiling: the Absorption
problem causes some models to produce identical outputs for
fundamentally different epistemic states. Extending the output to
include structured loss declarations — creating a tensor representation
— recovers these collapsed distinctions completely.

The model has the distinction. The scalar cannot express it. The tensor
can.

## Appendix A: Prompt Strategies

### S1 (Neutrosophic)

**System**: You are an expert in Neutrosophic Logic. You evaluate
statements using three INDEPENDENT dimensions: Truth (T), Indeterminacy
(I), and Falsity (F), each on [0.0, 1.0]. These dimensions are NOT
constrained to sum to 1.0. A statement can be simultaneously partially
true AND partially false AND partially indeterminate. Respond with ONLY
a JSON object, no other text.

**User**: Evaluate this statement on three independent dimensions:

Statement: "{statement}"

- Truth (T): To what degree is this statement true? [0.0 to 1.0]
- Indeterminacy (I): To what degree is the truth value unknown,
  undetermined, or inherently uncertain? [0.0 to 1.0]
- Falsity (F): To what degree is this statement false? [0.0 to 1.0]

T, I, and F are independent. They need NOT sum to 1.0.

Respond with ONLY: {"T": <float>, "I": <float>, "F": <float>}

### S2 (Probabilistic)

**System**: You are a probabilistic classifier. You assign
probabilities to three mutually exclusive categories that MUST sum to
exactly 1.0. Respond with ONLY a JSON object, no other text.

**User**: Classify this statement into three mutually exclusive
categories whose probabilities sum to 1.0:

Statement: "{statement}"

- T (True): Probability the statement is true
- I (Uncertain): Probability the truth value is unknown or undetermined
- F (False): Probability the statement is false

CONSTRAINT: T + I + F must equal 1.0

Respond with ONLY: {"T": <float>, "I": <float>, "F": <float>}

### S3 (Entropy-Derived)

**System**: You are a binary truth estimator. You estimate the
probability that a statement is true (YES) versus false (NO). The two
probabilities must sum to 1.0. Respond with ONLY a JSON object, no
other text.

**User**: Estimate the probability that this statement is true versus
false:

Statement: "{statement}"

- P_yes: Probability the statement is true [0.0 to 1.0]
- P_no: Probability the statement is false [0.0 to 1.0]

CONSTRAINT: P_yes + P_no must equal 1.0

Respond with ONLY: {"P_yes": <float>, "P_no": <float>}

*Indeterminacy derived from Shannon entropy:*
I = -(p·log₂(p) + (1-p)·log₂(1-p)) where p = P_yes

### S4 (Tensor — Declared Losses)

**System**: You are an expert in Neutrosophic Logic and epistemic
honesty. You evaluate statements using three INDEPENDENT dimensions:
Truth (T), Indeterminacy (I), and Falsity (F), each on [0.0, 1.0].
These dimensions are NOT constrained to sum to 1.0. Crucially, you must
also declare your LOSSES: what you cannot evaluate, what limits your
assessment, and why your indeterminacy value is what it is. Respond with
ONLY a JSON object, no other text.

**User**: Evaluate this statement on three independent dimensions, and
declare what you cannot evaluate:

Statement: "{statement}"

- Truth (T): To what degree is this statement true? [0.0 to 1.0]
- Indeterminacy (I): To what degree is the truth value unknown,
  undetermined, or inherently uncertain? [0.0 to 1.0]
- Falsity (F): To what degree is this statement false? [0.0 to 1.0]
- losses: A list of objects, each with:
  - "what": What you cannot evaluate (brief description)
  - "why": Why this limits your assessment
  - "severity": How much this affects your evaluation [0.0 to 1.0]

T, I, and F are independent. They need NOT sum to 1.0.
You MUST declare at least one loss. Honesty about limits is required.

Respond with ONLY:
{"T": <float>, "I": <float>, "F": <float>,
 "losses": [{"what": "<str>", "why": "<str>", "severity": <float>}, ...]}

## Appendix B: Test Stimuli

The five test stimuli are from Leyva-Vázquez and Smarandache (2025):

1. **Paradox (Logical)**: "This sentence is false."
2. **Ignorance (Epistemic)**: "The number of stars in the universe is even."
3. **Vagueness (Fuzzy)**: "John is 1.75 meters tall, therefore John is tall."
4. **Contradiction (Ethical)**: "Lying to save an innocent life is morally right and wrong at the same time."
5. **Contingency (Future)**: "It will rain in New York tomorrow."

## Appendix C: Data Availability

All code, prompts, and data are available at:
https://github.com/fsgeek/neutrosophic-llm-logic

- `src/prompts.py`: All four prompt strategies
- `src/experiment.py`: Experiment runner with strategy selection
- `data/cross_vendor_results.csv`: S1–S3 production data (375 evaluations)
- `data/s4_tensor_results.csv`: S4 tensor data (125 evaluations)
- `data/s4_mistral_rerun.csv`: Mistral S4 rerun at 1500 max_tokens (25 evaluations)
- `data/openai_neutrosophic_results.csv`: Original Smarandache data
