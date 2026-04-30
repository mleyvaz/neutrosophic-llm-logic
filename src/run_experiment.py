"""
Replication script for v2 of "Breaking the Chains of Probability".

Runs 5 repetitions per cell over the 4 OpenAI models, 5 phenomena,
and 3 prompting strategies. Cost: ~USD 5-10 across the four model
tiers. Reads OPENAI_API_KEY from the environment; never persists it.

Usage:
    OPENAI_API_KEY=... python -m src.run_experiment
Output:
    data/openai_neutrosophic_results_v2.csv
"""

from __future__ import annotations
import os
import sys
import json
import time
import math
import csv
from datetime import datetime

from openai import OpenAI

# --------------------------------------------------------------------
PHENOMENA = [
    ("Paradox (Logical)",
     "This sentence is false."),
    ("Ignorance (Epistemic)",
     "The number of stars in the universe is even."),
    ("Vagueness (Fuzzy)",
     "John is 1.75 meters tall, therefore John is tall."),
    ("Contradiction (Ethical)",
     "Lying to save an innocent life is morally right and wrong at "
     "the same time."),
    ("Contingency (Future)",
     "It will rain in New York tomorrow."),
]

MODELS = [
    "gpt-4o",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
    "gpt-4o-mini",
]

REPS = 5

# --------------------------------------------------------------------
SYS_S1 = (
    "You are an expert in Neutrosophic Logic. You evaluate statements "
    "using three INDEPENDENT dimensions: Truth (T), Indeterminacy (I), "
    "and Falsity (F), each on [0.0, 1.0]. These dimensions are NOT "
    "constrained to sum to 1.0. A statement can be simultaneously "
    "partially true AND partially false AND partially indeterminate. "
    "Respond with ONLY a JSON object, no other text."
)
USR_S1 = (
    "Evaluate this statement on three independent dimensions:\n\n"
    "Statement: \"{stmt}\"\n\n"
    "- Truth (T): To what degree is this statement true? [0.0 to 1.0]\n"
    "- Indeterminacy (I): To what degree is the truth value unknown, "
    "undetermined, or inherently uncertain? [0.0 to 1.0]\n"
    "- Falsity (F): To what degree is this statement false? [0.0 to 1.0]\n\n"
    "T, I, and F are independent. They need NOT sum to 1.0.\n\n"
    "Respond with ONLY: {{\"T\": , \"I\": , \"F\": }}"
)

SYS_S2 = (
    "You are a probabilistic classifier. You assign probabilities to "
    "three mutually exclusive categories that MUST sum to exactly 1.0. "
    "Respond with ONLY a JSON object, no other text."
)
USR_S2 = (
    "Classify this statement into three mutually exclusive categories "
    "whose probabilities sum to 1.0:\n\n"
    "Statement: \"{stmt}\"\n\n"
    "- T (True): Probability the statement is true\n"
    "- I (Uncertain): Probability the truth value is unknown or "
    "undetermined\n"
    "- F (False): Probability the statement is false\n\n"
    "CONSTRAINT: T + I + F must equal 1.0\n\n"
    "Respond with ONLY: {{\"T\": , \"I\": , \"F\": }}"
)

SYS_S3 = (
    "You are a binary truth estimator. You estimate the probability "
    "that a statement is true (YES) versus false (NO). The two "
    "probabilities must sum to 1.0. Respond with ONLY a JSON object, "
    "no other text."
)
USR_S3 = (
    "Estimate the probability that this statement is true versus "
    "false:\n\n"
    "Statement: \"{stmt}\"\n\n"
    "- P_yes: Probability the statement is true [0.0 to 1.0]\n"
    "- P_no: Probability the statement is false [0.0 to 1.0]\n\n"
    "CONSTRAINT: P_yes + P_no must equal 1.0\n\n"
    "Respond with ONLY: {{\"P_yes\": , \"P_no\": }}"
)


def parse_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.startswith("json"):
            text = text[4:]
        text = text.strip("`").strip()
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < 0:
        raise ValueError(f"no JSON braces found in: {text[:120]}")
    return json.loads(text[start:end + 1])


def call_model(client: OpenAI, model: str, system: str, user: str,
               temperature: float = 0.7, max_retries: int = 3) -> str:
    last_err = None
    for attempt in range(max_retries):
        try:
            r = client.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": user},
                ],
            )
            return r.choices[0].message.content
        except Exception as e:
            last_err = e
            time.sleep(2 ** attempt)
    raise RuntimeError(f"failed after {max_retries} retries: {last_err}")


def evaluate_cell(client: OpenAI, model: str, stmt: str) -> dict:
    out = {"S1_Truth_T": None, "S1_Indet_I": None, "S1_Falsity_F": None,
           "S2_Truth_T": None, "S2_Indet_I": None, "S2_Falsity_F": None,
           "S3_Truth_T": None, "S3_Indet_I": None, "S3_Falsity_F": None,
           "Status": "Success"}

    try:
        raw = call_model(client, model, SYS_S1, USR_S1.format(stmt=stmt))
        d = parse_json(raw)
        out["S1_Truth_T"] = float(d.get("T", 0.0))
        out["S1_Indet_I"] = float(d.get("I", 0.0))
        out["S1_Falsity_F"] = float(d.get("F", 0.0))
    except Exception as e:
        out["Status"] = f"S1_error: {e}"

    try:
        raw = call_model(client, model, SYS_S2, USR_S2.format(stmt=stmt))
        d = parse_json(raw)
        out["S2_Truth_T"] = float(d.get("T", 0.0))
        out["S2_Indet_I"] = float(d.get("I", 0.0))
        out["S2_Falsity_F"] = float(d.get("F", 0.0))
    except Exception as e:
        if out["Status"] == "Success":
            out["Status"] = f"S2_error: {e}"

    try:
        raw = call_model(client, model, SYS_S3, USR_S3.format(stmt=stmt))
        d = parse_json(raw)
        p_yes = float(d.get("P_yes", 0.0))
        p_no = float(d.get("P_no", 0.0))
        if 0.0 < p_yes < 1.0:
            I_s3 = -(p_yes * math.log2(p_yes) +
                     (1 - p_yes) * math.log2(1 - p_yes))
        else:
            I_s3 = 0.0
        out["S3_Truth_T"] = p_yes
        out["S3_Indet_I"] = I_s3
        out["S3_Falsity_F"] = p_no
    except Exception as e:
        if out["Status"] == "Success":
            out["Status"] = f"S3_error: {e}"

    return out


def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set in environment", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)
    out_path = os.path.join("data", "openai_neutrosophic_results_v2.csv")

    columns = [
        "Timestamp", "Phenomenon_Type", "Phrase_English",
        "Provider", "Model", "Rep",
        "S1_Truth_T", "S1_Indet_I", "S1_Falsity_F",
        "S2_Truth_T", "S2_Indet_I", "S2_Falsity_F",
        "S3_Truth_T", "S3_Indet_I", "S3_Falsity_F",
        "Status", "S1_Sum_TIF",
    ]

    total = len(MODELS) * len(PHENOMENA) * REPS
    rows = []
    done = 0
    t0 = time.time()
    for model in MODELS:
        for phen, stmt in PHENOMENA:
            for rep in range(1, REPS + 1):
                done += 1
                ts = datetime.now().strftime("%Y-%m-%d %H:%M")
                print(f"  [{done:3d}/{total}] {model:14s} | "
                      f"{phen:24s} | rep {rep}", flush=True)
                cell = evaluate_cell(client, model, stmt)
                s1_sum = (
                    (cell["S1_Truth_T"] or 0) +
                    (cell["S1_Indet_I"] or 0) +
                    (cell["S1_Falsity_F"] or 0)
                ) if cell["Status"] == "Success" else None
                rows.append({
                    "Timestamp": ts,
                    "Phenomenon_Type": phen,
                    "Phrase_English": stmt,
                    "Provider": "OpenAI",
                    "Model": model,
                    "Rep": rep,
                    **cell,
                    "S1_Sum_TIF": s1_sum,
                })
                if done % 10 == 0 or done == total:
                    with open(out_path, "w", encoding="utf-8", newline="") as f:
                        w = csv.DictWriter(f, fieldnames=columns)
                        w.writeheader()
                        w.writerows(rows)

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed/60:.1f} min. Saved {len(rows)} rows to {out_path}")
    n_success = sum(1 for r in rows if r["Status"] == "Success")
    print(f"Success: {n_success}/{len(rows)}")
    n_hyper = sum(1 for r in rows
                  if r["Status"] == "Success" and r["S1_Sum_TIF"]
                  and r["S1_Sum_TIF"] > 1.001)
    print(f"Hyper-truth (S1_Sum > 1): {n_hyper}/{n_success} = "
          f"{100*n_hyper/max(n_success,1):.1f}%")


if __name__ == "__main__":
    main()
