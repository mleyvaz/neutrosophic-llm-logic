"""Cross-vendor neutrosophic evaluation experiment.

Reproduces and extends Smarandache's experiments using current models
from multiple vendors via OpenRouter's OpenAI-compatible API.

What this fixes vs the original:
- Published prompts (the original committed no prompts)
- Cross-vendor models (the original used only OpenAI)
- Multiple runs per cell (the original was single-shot)
- Current models (the original's models are being deprecated)

Usage:
    export OPENROUTER_API_KEY=your_key_here
    python -m src.experiment [--reps 10] [--output data/cross_vendor_results.csv]
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from openai import OpenAI

from src.prompts import PHENOMENA, format_prompt

# --- Model configuration ---
# OpenRouter model IDs for cross-vendor comparison
MODELS = {
    "anthropic/claude-sonnet-4.6": {
        "provider": "Anthropic",
        "short_name": "claude-sonnet-4.6",
    },
    "meta-llama/llama-4-maverick": {
        "provider": "Meta",
        "short_name": "llama-4-maverick",
    },
    "deepseek/deepseek-chat-v3-0324": {
        "provider": "DeepSeek",
        "short_name": "deepseek-v3",
    },
    "qwen/qwen3-235b-a22b": {
        "provider": "Alibaba",
        "short_name": "qwen3-235b",
    },
    "mistralai/mistral-medium-3.1": {
        "provider": "Mistral",
        "short_name": "mistral-medium-3.1",
    },
}

# Strategies (default includes all; use --strategies to select)
STRATEGIES = (1, 2, 3, 4)


def _parse_tif(raw: str, strategy: int) -> dict:
    """Parse model response into T/I/F values.

    For S1 and S2: expects {"T": float, "I": float, "F": float}
    For S3: expects {"P_yes": float, "P_no": float}, derives T/I/F
    """
    # Strip markdown code fences if present
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last lines (``` markers)
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Try to find JSON in the response
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            data = json.loads(text[start:end])
        else:
            return {"T": None, "I": None, "F": None, "parse_error": raw[:200]}

    if strategy in (1, 2):
        return {
            "T": float(data.get("T", data.get("t", 0))),
            "I": float(data.get("I", data.get("i", 0))),
            "F": float(data.get("F", data.get("f", 0))),
        }
    elif strategy == 4:
        losses = data.get("losses", [])
        # Normalize losses to list of dicts
        loss_list = []
        for loss in losses:
            if isinstance(loss, dict):
                loss_list.append({
                    "what": str(loss.get("what", "")),
                    "why": str(loss.get("why", "")),
                    "severity": float(loss.get("severity", 0.5)),
                })
        return {
            "T": float(data.get("T", data.get("t", 0))),
            "I": float(data.get("I", data.get("i", 0))),
            "F": float(data.get("F", data.get("f", 0))),
            "losses": json.dumps(loss_list),
            "num_losses": len(loss_list),
            "mean_severity": (
                round(sum(l["severity"] for l in loss_list) / len(loss_list), 4)
                if loss_list else 0.0
            ),
        }
    elif strategy == 3:
        p_yes = float(data.get("P_yes", data.get("p_yes", 0.5)))
        p_no = float(data.get("P_no", data.get("p_no", 0.5)))
        # Derive indeterminacy from Shannon entropy (normalized to [0,1])
        # H = -p*log2(p) - (1-p)*log2(1-p), max = 1.0 at p=0.5
        eps = 1e-10
        p = max(eps, min(1 - eps, p_yes))
        entropy = -(p * math.log2(p) + (1 - p) * math.log2(1 - p))
        return {
            "T": p_yes,
            "I": round(entropy, 4),
            "F": p_no,
        }
    return {"T": None, "I": None, "F": None}


def run_single(
    client: OpenAI,
    model_id: str,
    strategy: int,
    statement: str,
    temperature: float = 0.7,
) -> dict:
    """Run a single evaluation: one model, one strategy, one statement."""
    system_msg, user_msg = format_prompt(strategy, statement)

    # S4 (tensor) needs more tokens for loss declarations
    max_tok = 1500 if strategy == 4 else 150

    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            temperature=temperature,
            max_tokens=max_tok,
        )
        raw = response.choices[0].message.content
        result = _parse_tif(raw, strategy)
        result["raw_response"] = raw
        result["status"] = "Success"

        # Capture token usage for cost tracking
        if response.usage:
            result["prompt_tokens"] = response.usage.prompt_tokens
            result["completion_tokens"] = response.usage.completion_tokens
            result["total_tokens"] = response.usage.total_tokens
    except Exception as e:
        result = {
            "T": None,
            "I": None,
            "F": None,
            "raw_response": "",
            "status": f"Error: {e}",
        }

    return result


def run_experiment(
    reps: int = 10,
    output_path: str = "data/cross_vendor_results.csv",
    models: dict | None = None,
    temperature: float = 0.7,
    strategies: tuple | None = None,
) -> Path:
    """Run the full cross-vendor experiment.

    Args:
        reps: Number of repetitions per cell
        output_path: Where to write results CSV
        models: Model dict (defaults to MODELS)
        temperature: Sampling temperature

    Returns:
        Path to output CSV
    """
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: Set OPENROUTER_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
        default_headers={
            "HTTP-Referer": "https://github.com/fsgeek/neutrosophic-llm-logic",
            "X-Title": "Neutrosophic Cross-Vendor Replication",
        },
    )

    if models is None:
        models = MODELS
    if strategies is None:
        strategies = STRATEGIES

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "Timestamp",
        "Phenomenon_Type",
        "Phrase_English",
        "Provider",
        "Model",
        "Model_ID",
        "Strategy",
        "Rep",
        "T",
        "I",
        "F",
        "Sum_TIF",
        "Num_Losses",
        "Mean_Severity",
        "Losses_JSON",
        "Temperature",
        "Prompt_Tokens",
        "Completion_Tokens",
        "Total_Tokens",
        "Status",
        "Raw_Response",
    ]

    total_calls = len(PHENOMENA) * len(models) * len(strategies) * reps
    completed = 0

    with out.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for phenomenon in PHENOMENA:
            for model_id, model_info in models.items():
                for strategy in strategies:
                    for rep in range(1, reps + 1):
                        completed += 1
                        timestamp = datetime.now(timezone.utc).isoformat()

                        print(
                            f"[{completed}/{total_calls}] "
                            f"{model_info['short_name']} S{strategy} "
                            f"'{phenomenon['phrase'][:30]}...' rep={rep}",
                            flush=True,
                        )

                        result = run_single(
                            client,
                            model_id,
                            strategy,
                            phenomenon["phrase"],
                            temperature=temperature,
                        )

                        t_val = result["T"]
                        i_val = result["I"]
                        f_val = result["F"]
                        sum_tif = None
                        if t_val is not None and i_val is not None and f_val is not None:
                            sum_tif = round(t_val + i_val + f_val, 4)

                        writer.writerow({
                            "Timestamp": timestamp,
                            "Phenomenon_Type": phenomenon["type"],
                            "Phrase_English": phenomenon["phrase"],
                            "Provider": model_info["provider"],
                            "Model": model_info["short_name"],
                            "Model_ID": model_id,
                            "Strategy": f"S{strategy}",
                            "Rep": rep,
                            "T": t_val,
                            "I": i_val,
                            "F": f_val,
                            "Sum_TIF": sum_tif,
                            "Num_Losses": result.get("num_losses", ""),
                            "Mean_Severity": result.get("mean_severity", ""),
                            "Losses_JSON": result.get("losses", ""),
                            "Temperature": temperature,
                            "Prompt_Tokens": result.get("prompt_tokens", ""),
                            "Completion_Tokens": result.get("completion_tokens", ""),
                            "Total_Tokens": result.get("total_tokens", ""),
                            "Status": result["status"],
                            "Raw_Response": result.get("raw_response", ""),
                        })
                        csvfile.flush()

                        # Rate limiting — be polite to the API
                        time.sleep(0.5)

    print(f"\nDone. {completed} evaluations written to {out}")
    return out


def main():
    parser = argparse.ArgumentParser(
        description="Cross-vendor neutrosophic evaluation experiment"
    )
    parser.add_argument(
        "--reps", type=int, default=10,
        help="Repetitions per cell (default: 10)",
    )
    parser.add_argument(
        "--output", type=str, default="data/cross_vendor_results.csv",
        help="Output CSV path",
    )
    parser.add_argument(
        "--temperature", type=float, default=0.7,
        help="Sampling temperature (default: 0.7)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print what would be run without making API calls",
    )
    parser.add_argument(
        "--models", type=str, nargs="*", default=None,
        help="Run only specific models (by short name, e.g., claude-sonnet-4.6)",
    )
    parser.add_argument(
        "--strategies", type=int, nargs="*", default=None,
        help="Run only specific strategies (e.g., 4 for tensor-only)",
    )
    args = parser.parse_args()

    strats = tuple(args.strategies) if args.strategies else None

    if args.dry_run:
        selected = MODELS
        if args.models:
            selected = {
                k: v for k, v in MODELS.items()
                if v["short_name"] in args.models
            }
        run_strats = strats or STRATEGIES
        total = len(PHENOMENA) * len(selected) * len(run_strats) * args.reps
        print(f"DRY RUN: {total} API calls")
        print(f"  {len(PHENOMENA)} phenomena x {len(selected)} models x "
              f"{len(run_strats)} strategies x {args.reps} reps")
        print(f"  Models: {', '.join(v['short_name'] for v in selected.values())}")
        print(f"  Strategies: {', '.join(f'S{s}' for s in run_strats)}")
        print(f"  Temperature: {args.temperature}")
        print(f"  Output: {args.output}")
        print(f"  Estimated cost: ~${total * 0.008:.2f} (rough)")
        sys.exit(0)

    selected = MODELS
    if args.models:
        selected = {
            k: v for k, v in MODELS.items()
            if v["short_name"] in args.models
        }
        if not selected:
            print(f"ERROR: No models matched {args.models}", file=sys.stderr)
            print(f"Available: {', '.join(v['short_name'] for v in MODELS.values())}")
            sys.exit(1)

    run_experiment(
        reps=args.reps,
        output_path=args.output,
        models=selected,
        temperature=args.temperature,
        strategies=strats,
    )


if __name__ == "__main__":
    main()
