"""S5 Prompt Ablation Experiment: Free-form epistemic assessment without neutrosophic framing.

Hypothesis: If S4 results are just instruction-following, removing the structured
prompt should produce different (or no) epistemic observations. If S4 is surfacing
pre-existing assessment, the same epistemic themes should appear even without the framing.

Design:
- System prompt stripped of ALL neutrosophic vocabulary (no T/I/F, no severity, no JSON)
- Same 5 stimuli as S4
- 3 models: claude-sonnet-4.6, deepseek-v3, llama-4-maverick
- 3 reps per cell = 45 API calls
- Free-form natural language responses
"""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI

# --- Ablated prompt: NO neutrosophic framing ---

S5_SYSTEM = (
    "You are evaluating a statement. Identify any limitations, uncertainties, "
    "or difficulties in determining whether this statement is true or false. "
    "Be specific about what makes evaluation difficult and why. "
    "If the statement is straightforward to evaluate, say so."
)

S5_USER = 'Evaluate this statement: "{statement}"'

# --- Same 5 stimuli as original experiment ---

PHENOMENA = (
    {
        "type": "Paradox (Logical)",
        "phrase": "This sentence is false.",
        "short_name": "liar",
    },
    {
        "type": "Contingency (Future)",
        "phrase": "It will rain in New York City tomorrow.",
        "short_name": "rain",
    },
    {
        "type": "Ignorance (Epistemic)",
        "phrase": "The total number of stars in the observable universe is even.",
        "short_name": "stars",
    },
    {
        "type": "Vagueness (Fuzzy)",
        "phrase": "John is 1.75 meters tall. Therefore, John is tall.",
        "short_name": "tall",
    },
    {
        "type": "Contradiction (Ethical)",
        "phrase": "Lying to save an innocent life is morally justified.",
        "short_name": "moral",
    },
)

# --- 3 models matching tautology experiment ---

MODELS = {
    "anthropic/claude-sonnet-4.6": {
        "provider": "Anthropic",
        "short_name": "claude-sonnet-4.6",
    },
    "deepseek/deepseek-chat-v3-0324": {
        "provider": "DeepSeek",
        "short_name": "deepseek-v3",
    },
    "meta-llama/llama-4-maverick": {
        "provider": "Meta",
        "short_name": "llama-4-maverick",
    },
}

REPS = 3


def run_s5_experiment(output_path: str = "data/s5_ablation_results.json") -> Path:
    """Run the S5 ablation experiment."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: Set OPENROUTER_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://github.com/fsgeek/neutrosophic-llm-logic",
            "X-Title": "S5 Ablation: Free-form Epistemic Assessment",
        },
    )

    results = []
    total_calls = len(PHENOMENA) * len(MODELS) * REPS
    completed = 0

    for phenomenon in PHENOMENA:
        for model_id, model_info in MODELS.items():
            for rep in range(1, REPS + 1):
                completed += 1
                timestamp = datetime.now(timezone.utc).isoformat()

                print(
                    f"[{completed}/{total_calls}] "
                    f"{model_info['short_name']} "
                    f"'{phenomenon['short_name']}' rep={rep}",
                    flush=True,
                )

                user_msg = S5_USER.format(statement=phenomenon["phrase"])

                try:
                    response = client.chat.completions.create(
                        model=model_id,
                        messages=[
                            {"role": "system", "content": S5_SYSTEM},
                            {"role": "user", "content": user_msg},
                        ],
                        temperature=0.7,
                        max_tokens=1500,
                    )
                    raw = response.choices[0].message.content
                    status = "Success"
                    prompt_tokens = response.usage.prompt_tokens if response.usage else None
                    completion_tokens = response.usage.completion_tokens if response.usage else None
                    total_tokens = response.usage.total_tokens if response.usage else None
                except Exception as e:
                    raw = ""
                    status = f"Error: {e}"
                    prompt_tokens = None
                    completion_tokens = None
                    total_tokens = None

                results.append({
                    "timestamp": timestamp,
                    "phenomenon_type": phenomenon["type"],
                    "phenomenon_short": phenomenon["short_name"],
                    "phrase": phenomenon["phrase"],
                    "provider": model_info["provider"],
                    "model": model_info["short_name"],
                    "model_id": model_id,
                    "rep": rep,
                    "system_prompt": S5_SYSTEM,
                    "user_prompt": user_msg,
                    "raw_response": raw,
                    "status": status,
                    "prompt_tokens": prompt_tokens,
                    "completion_tokens": completion_tokens,
                    "total_tokens": total_tokens,
                })

                # Rate limiting
                time.sleep(0.5)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nDone. {completed} evaluations written to {out}")
    return out


if __name__ == "__main__":
    run_s5_experiment()
