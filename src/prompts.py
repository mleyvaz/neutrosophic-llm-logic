"""Prompt strategies for neutrosophic evaluation of LLM uncertainty.

These are the prompts that Smarandache's paper describes but never published.
Three strategies, each extracting T/I/F through a different lens:
  S1 (Neutrosophic): Independent dimensions, no sum constraint
  S2 (Probabilistic): Constrained to sum = 1.0
  S3 (Entropy-Derived): Binary probability, I derived from Shannon entropy
"""

# --- Strategy 1: Neutrosophic (independent dimensions) ---

S1_SYSTEM = (
    "You are an expert in Neutrosophic Logic. "
    "You evaluate statements using three INDEPENDENT dimensions: "
    "Truth (T), Indeterminacy (I), and Falsity (F), each on [0.0, 1.0]. "
    "These dimensions are NOT constrained to sum to 1.0. "
    "A statement can be simultaneously partially true AND partially false "
    "AND partially indeterminate. "
    "Respond with ONLY a JSON object, no other text."
)

S1_USER = (
    "Evaluate this statement on three independent dimensions:\n\n"
    "Statement: \"{statement}\"\n\n"
    "- Truth (T): To what degree is this statement true? [0.0 to 1.0]\n"
    "- Indeterminacy (I): To what degree is the truth value unknown, "
    "undetermined, or inherently uncertain? [0.0 to 1.0]\n"
    "- Falsity (F): To what degree is this statement false? [0.0 to 1.0]\n\n"
    "T, I, and F are independent. They need NOT sum to 1.0.\n\n"
    'Respond with ONLY: {{"T": <float>, "I": <float>, "F": <float>}}'
)

# --- Strategy 2: Probabilistic (constrained sum = 1.0) ---

S2_SYSTEM = (
    "You are a probabilistic classifier. "
    "You assign probabilities to three mutually exclusive categories "
    "that MUST sum to exactly 1.0. "
    "Respond with ONLY a JSON object, no other text."
)

S2_USER = (
    "Classify this statement into three mutually exclusive categories "
    "whose probabilities sum to 1.0:\n\n"
    "Statement: \"{statement}\"\n\n"
    "- T (True): Probability the statement is true\n"
    "- I (Uncertain): Probability the truth value is unknown or undetermined\n"
    "- F (False): Probability the statement is false\n\n"
    "CONSTRAINT: T + I + F must equal 1.0\n\n"
    'Respond with ONLY: {{"T": <float>, "I": <float>, "F": <float>}}'
)

# --- Strategy 3: Entropy-Derived ---

S3_SYSTEM = (
    "You are a binary truth estimator. "
    "You estimate the probability that a statement is true (YES) versus "
    "false (NO). The two probabilities must sum to 1.0. "
    "Respond with ONLY a JSON object, no other text."
)

S3_USER = (
    "Estimate the probability that this statement is true versus false:\n\n"
    "Statement: \"{statement}\"\n\n"
    "- P_yes: Probability the statement is true [0.0 to 1.0]\n"
    "- P_no: Probability the statement is false [0.0 to 1.0]\n\n"
    "CONSTRAINT: P_yes + P_no must equal 1.0\n\n"
    'Respond with ONLY: {{"P_yes": <float>, "P_no": <float>}}'
)


# --- Test stimuli (from Smarandache's original 5) ---

PHENOMENA = (
    {
        "type": "Paradox (Logical)",
        "phrase": "This sentence is false.",
    },
    {
        "type": "Ignorance (Epistemic)",
        "phrase": "The number of stars in the universe is even.",
    },
    {
        "type": "Vagueness (Fuzzy)",
        "phrase": "John is 1.75 meters tall, therefore John is tall.",
    },
    {
        "type": "Contradiction (Ethical)",
        "phrase": "Lying to save an innocent life is morally right and wrong at the same time.",
    },
    {
        "type": "Contingency (Future)",
        "phrase": "It will rain in New York tomorrow.",
    },
)


def format_prompt(strategy: int, statement: str) -> tuple[str, str]:
    """Return (system_message, user_message) for a given strategy and statement.

    Args:
        strategy: 1, 2, or 3
        statement: The text to evaluate

    Returns:
        (system_prompt, user_prompt) tuple
    """
    if strategy == 1:
        return S1_SYSTEM, S1_USER.format(statement=statement)
    elif strategy == 2:
        return S2_SYSTEM, S2_USER.format(statement=statement)
    elif strategy == 3:
        return S3_SYSTEM, S3_USER.format(statement=statement)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")
