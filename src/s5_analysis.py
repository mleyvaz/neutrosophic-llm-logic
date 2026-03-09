"""S5 Ablation Analysis: Extract epistemic themes from free-form responses
and compare to S4 cross-model convergence results.

S4 reference themes (8 universally-shared across models):
  Liar:  self-reference/paradox, definitional-ambiguity
  Moral: cultural-relativity, situational-context
  Rain:  temporal/future, empirical-data-access
  Stars: scope/quantification, measurement-precision
  Tall:  reference-class/population, cultural-relativity
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

from src.s5_ablation import S5_SYSTEM, PHENOMENA, MODELS, REPS

# --- S4 reference themes: canonical names + keyword patterns ---
# Each theme has keyword/phrase patterns to detect it in free-form text.

S4_REFERENCE = {
    "liar": {
        "self-reference/paradox": [
            r"self.?refer", r"paradox", r"circular", r"refers?\s+to\s+itself",
            r"liar.?s?\s+paradox", r"self.?application", r"recursive",
            r"truth.*itself", r"applies to itself",
        ],
        "definitional-ambiguity": [
            r"definitional", r"what\s+.*(true|false)\s+means",
            r"meaning\s+of", r"truth\s+value", r"neither\s+true\s+nor\s+false",
            r"no\s+(stable|consistent)\s+truth", r"cannot\s+be\s+(consistently\s+)?assigned",
            r"ill.?defined", r"not\s+well.?defined", r"truth.*undefined",
            r"defies\s+(classical|standard|binary)\s+logic",
            r"bivalent", r"truth\s+gap", r"(two|2).?valued\s+logic",
            r"classical\s+logic\s+(cannot|fails|breaks)",
        ],
    },
    "rain": {
        "temporal/future": [
            r"future", r"hasn.?t\s+happened", r"temporal", r"tomorrow",
            r"prediction", r"not\s+yet\s+occurred", r"hasn.?t\s+occur",
            r"forecast", r"probabilistic", r"probability",
            r"uncertain.*future", r"contingent",
        ],
        "empirical-data-access": [
            r"empirical", r"data", r"weather\s+data", r"meteorolog",
            r"observe", r"measure", r"evidence", r"information",
            r"current\s+conditions", r"satellite", r"sensor",
            r"access\s+to", r"real.?time", r"atmospheric",
            r"model(?:s|ing)?\b(?!.*language)", r"forecast\s+model",
        ],
    },
    "stars": {
        "scope/quantification": [
            r"scope", r"quantif", r"observable\s+universe",
            r"count(?:ing)?", r"total\s+number", r"enumerat",
            r"immense", r"vast", r"scale", r"magnitude",
            r"how\s+many", r"number\s+of\s+stars",
            r"finite\s+but", r"changing", r"defined.*boundary",
        ],
        "measurement-precision": [
            r"measur(?:e|ing|ement)", r"precision", r"estimate",
            r"approximat", r"uncertain", r"cannot\s+be\s+(precisely\s+)?determined",
            r"imprecis", r"current\s+estimates", r"error\s+(margin|bar)",
            r"exact\s+(number|count)", r"beyond.*capacity",
            r"unknowable", r"inaccessible", r"epistem",
        ],
    },
    "tall": {
        "reference-class/population": [
            r"reference", r"population", r"average", r"mean\s+height",
            r"compared\s+to", r"relative\s+to", r"context.?dependent",
            r"who\s+.*(compar|group)", r"demographics?",
            r"country", r"region", r"culture", r"norm",
        ],
        "cultural-relativity": [
            r"cultur(?:al|e)", r"subjective", r"relative",
            r"vague(?:ness)?", r"sorites", r"heap\s+paradox",
            r"fuzzy", r"gradual", r"boundary", r"threshold",
            r"no\s+clear\s+(cut.?off|dividing|line|boundary)",
            r"arbitrary\s+(cut.?off|threshold|boundary|line)",
            r"definition\s+of\s+.?tall", r"what\s+counts\s+as\s+.?tall",
        ],
    },
    "moral": {
        "cultural-relativity": [
            r"cultur(?:al|e)", r"tradition", r"societ(?:y|al|ies)",
            r"relative", r"subjective", r"framework",
            r"ethical\s+(framework|system|tradition|theory)",
            r"moral\s+(framework|system|philosophy|relativism)",
            r"deontol", r"utilitarian", r"consequential",
            r"kantian", r"virtue\s+ethics",
        ],
        "situational-context": [
            r"situational", r"context", r"depend(?:s|ent|ing)\s+on",
            r"circumstance", r"specific\s+case", r"scenario",
            r"what\s+if", r"varies", r"case.?by.?case",
            r"innocent\s+life", r"stakes", r"severity",
            r"consequen(?:ce|tial)", r"outcome",
        ],
    },
}


def detect_themes(text: str, phenomenon: str) -> dict[str, bool]:
    """Detect S4 reference themes in a free-form response."""
    text_lower = text.lower()
    ref = S4_REFERENCE.get(phenomenon, {})
    found = {}
    for theme_name, patterns in ref.items():
        found[theme_name] = any(re.search(p, text_lower) for p in patterns)
    return found


def detect_novel_themes(text: str, phenomenon: str) -> list[str]:
    """Identify potential novel themes NOT in S4 reference set.

    Uses broad heuristic patterns for common epistemic limitation categories.
    """
    text_lower = text.lower()
    novel = []

    # Universal novel-theme candidates
    candidates = {
        "language-ambiguity": [r"ambig(?:uous|uity)", r"interpret(?:ation|ed)", r"polysem"],
        "logical-framework-choice": [r"(multi|many).?valued\s+logic", r"paraconsistent",
                                     r"dialethe", r"non.?classical", r"fuzzy\s+logic",
                                     r"three.?valued", r"intuitionist"],
        "observer-dependence": [r"observer", r"perspective", r"standpoint", r"viewpoint",
                                r"point\s+of\s+view"],
        "temporal-change": [r"chang(?:e|es|ing)\s+over\s+time", r"dynamic", r"flux",
                            r"evolv(?:e|ing)", r"not\s+static"],
        "meta-level-confusion": [r"meta.?level", r"level\s+confusion", r"object.?language",
                                 r"use.?mention"],
        "incompleteness": [r"incomplet(?:e|eness)", r"godel", r"undecid(?:able|ability)"],
        "pragmatic-truth": [r"pragmatic", r"useful(?:ness)?.*truth", r"practical"],
    }

    # Only flag if NOT already captured by S4 themes for this phenomenon
    s4_patterns = S4_REFERENCE.get(phenomenon, {})
    s4_all_patterns = [p for pats in s4_patterns.values() for p in pats]

    for cand_name, patterns in candidates.items():
        if any(re.search(p, text_lower) for p in patterns):
            # Check this isn't already covered by S4 pattern matching
            if cand_name not in s4_patterns:
                novel.append(cand_name)

    return novel


def analyze_s5(input_path: str = "data/s5_ablation_results.json") -> dict:
    """Full S5 analysis: theme detection, overlap scoring, novel theme extraction."""

    with open(input_path) as f:
        data = json.load(f)

    # Handle both raw list and nested analysis format
    if isinstance(data, list):
        results = data
    elif isinstance(data, dict) and "raw_results" in data:
        results = data["raw_results"]
    else:
        raise ValueError(f"Unexpected format in {input_path}")

    # --- Per-response theme detection ---
    for r in results:
        phenom = r["phenomenon_short"]
        text = r["raw_response"]
        r["detected_themes"] = detect_themes(text, phenom)
        r["novel_themes"] = detect_novel_themes(text, phenom)

    # --- Aggregate: by model x phenomenon ---
    # For each (model, phenomenon), compute what fraction of reps detect each theme

    agg = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for r in results:
        model = r["model"]
        phenom = r["phenomenon_short"]
        for theme, found in r["detected_themes"].items():
            agg[phenom][model][theme].append(found)

    # --- Theme overlap table ---
    theme_table = {}
    for phenom, models_data in agg.items():
        theme_table[phenom] = {}
        for model, themes in models_data.items():
            theme_table[phenom][model] = {}
            for theme, vals in themes.items():
                hit_rate = sum(vals) / len(vals)
                theme_table[phenom][model][theme] = {
                    "hits": sum(vals),
                    "reps": len(vals),
                    "rate": hit_rate,
                }

    # --- Cross-model convergence: theme present in at least 2/3 reps for ALL models ---
    cross_model = {}
    for phenom, models_data in theme_table.items():
        cross_model[phenom] = {}
        models = list(models_data.keys())
        themes = list(next(iter(models_data.values())).keys())
        for theme in themes:
            rates = [models_data[m][theme]["rate"] for m in models]
            # "Present" = at least 2/3 reps detected it
            all_present = all(r >= 0.67 for r in rates)
            any_present = any(r >= 0.67 for r in rates)
            cross_model[phenom][theme] = {
                "universal": all_present,
                "any_model": any_present,
                "rates": {m: models_data[m][theme]["rate"] for m in models},
            }

    # --- Overall S4 theme overlap score ---
    total_s4_themes = sum(len(themes) for themes in S4_REFERENCE.values())
    s5_universal = sum(
        1 for phenom_data in cross_model.values()
        for theme_data in phenom_data.values()
        if theme_data["universal"]
    )
    s5_any = sum(
        1 for phenom_data in cross_model.values()
        for theme_data in phenom_data.values()
        if theme_data["any_model"]
    )

    overlap = {
        "total_s4_themes": total_s4_themes,
        "s5_universal_match": s5_universal,
        "s5_any_model_match": s5_any,
        "universal_overlap_pct": round(100 * s5_universal / total_s4_themes, 1),
        "any_model_overlap_pct": round(100 * s5_any / total_s4_themes, 1),
    }

    # --- Novel themes ---
    novel_agg = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    for r in results:
        for nt in r["novel_themes"]:
            novel_agg[r["phenomenon_short"]][r["model"]][nt] += 1

    # --- Per-model per-phenomenon detection rates (for the report) ---
    per_model_per_phenom = defaultdict(lambda: defaultdict(dict))
    for r in results:
        model = r["model"]
        phenom = r["phenomenon_short"]
        for theme, found in r["detected_themes"].items():
            if theme not in per_model_per_phenom[phenom][model]:
                per_model_per_phenom[phenom][model][theme] = []
            per_model_per_phenom[phenom][model][theme].append(found)

    # --- Build final output ---
    output = {
        "experiment": "S5 Prompt Ablation",
        "hypothesis": (
            "If S4 results are instruction-following, removing the structured prompt "
            "should eliminate epistemic observations. If pre-existing, same themes appear."
        ),
        "design": {
            "system_prompt": S5_SYSTEM,
            "models": list(MODELS.keys()),
            "stimuli": [p["phrase"] for p in PHENOMENA],
            "reps_per_cell": REPS,
            "total_calls": len(results),
        },
        "theme_detection_summary": {},
        "cross_model_convergence": cross_model,
        "overlap_with_s4": overlap,
        "novel_themes_found": {
            phenom: {
                model: dict(themes)
                for model, themes in models.items()
            }
            for phenom, models in novel_agg.items()
        },
        "raw_results": results,
    }

    # Build theme detection summary (readable)
    for phenom in [p["short_name"] for p in PHENOMENA]:
        output["theme_detection_summary"][phenom] = {}
        ref_themes = S4_REFERENCE.get(phenom, {})
        for theme in ref_themes:
            per_model = {}
            for r in results:
                if r["phenomenon_short"] == phenom:
                    model = r["model"]
                    if model not in per_model:
                        per_model[model] = []
                    per_model[model].append(r["detected_themes"].get(theme, False))
            output["theme_detection_summary"][phenom][theme] = {
                m: f"{sum(v)}/{len(v)}"
                for m, v in per_model.items()
            }

    return output


def print_report(analysis: dict) -> None:
    """Print human-readable S5 analysis report."""

    print("=" * 72)
    print("S5 PROMPT ABLATION EXPERIMENT — RESULTS")
    print("=" * 72)
    print()
    print(f"Total API calls: {analysis['design']['total_calls']}")
    print(f"Models: {', '.join(analysis['design']['models'])}")
    print()

    # Theme detection table
    print("-" * 72)
    print("THEME DETECTION BY PHENOMENON (S4 reference themes)")
    print("-" * 72)

    for phenom, themes in analysis["theme_detection_summary"].items():
        print(f"\n  [{phenom.upper()}]")
        for theme, model_rates in themes.items():
            rates_str = "  ".join(f"{m[:8]:>8}={v}" for m, v in model_rates.items())
            print(f"    {theme:<30} {rates_str}")

    # Cross-model convergence
    print()
    print("-" * 72)
    print("CROSS-MODEL CONVERGENCE (theme detected in >=2/3 reps)")
    print("-" * 72)

    for phenom, themes in analysis["cross_model_convergence"].items():
        print(f"\n  [{phenom.upper()}]")
        for theme, data in themes.items():
            u = "UNIVERSAL" if data["universal"] else ("PARTIAL" if data["any_model"] else "ABSENT")
            rates_str = ", ".join(f"{m[:8]}={r:.0%}" for m, r in data["rates"].items())
            print(f"    {theme:<30} {u:>10}  ({rates_str})")

    # Overlap score
    print()
    print("-" * 72)
    print("S4 THEME OVERLAP SUMMARY")
    print("-" * 72)
    ov = analysis["overlap_with_s4"]
    print(f"  S4 reference themes:      {ov['total_s4_themes']}")
    print(f"  S5 universal matches:     {ov['s5_universal_match']} ({ov['universal_overlap_pct']}%)")
    print(f"  S5 any-model matches:     {ov['s5_any_model_match']} ({ov['any_model_overlap_pct']}%)")

    # Novel themes
    print()
    print("-" * 72)
    print("NOVEL THEMES (detected in S5 but NOT in S4 reference set)")
    print("-" * 72)
    novel = analysis["novel_themes_found"]
    if not novel:
        print("  None detected.")
    else:
        for phenom, models in novel.items():
            print(f"\n  [{phenom.upper()}]")
            for model, themes in models.items():
                for theme, count in themes.items():
                    print(f"    {model[:12]:>12}: {theme} (x{count})")

    # Interpretation
    print()
    print("-" * 72)
    print("INTERPRETATION")
    print("-" * 72)
    u_pct = ov["universal_overlap_pct"]
    any_pct = ov["any_model_overlap_pct"]
    if u_pct >= 80:
        verdict = (
            "STRONG PRE-EXISTING ASSESSMENT: The S4 neutrosophic framing did NOT create\n"
            "  the epistemic observations. Models surface the same themes in free-form text.\n"
            "  S4's contribution is STRUCTURING existing assessment, not creating it."
        )
    elif u_pct >= 50:
        verdict = (
            "MODERATE PRE-EXISTING ASSESSMENT: Most S4 themes appear without the framing,\n"
            "  but some themes may have been elicited by the structured prompt.\n"
            "  S4 partially structures and partially creates."
        )
    else:
        verdict = (
            "WEAK PRE-EXISTING ASSESSMENT: S4 themes do NOT reliably appear without\n"
            "  the neutrosophic framing. The structured prompt may be creating rather\n"
            "  than surfacing epistemic observations."
        )

    print(f"  Universal overlap: {u_pct}%  |  Any-model overlap: {any_pct}%")
    print(f"  {verdict}")
    print()


if __name__ == "__main__":
    analysis = analyze_s5()

    # Save enriched results back to file
    with open("data/s5_ablation_results.json", "w") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    print_report(analysis)
