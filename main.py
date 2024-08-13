"""Generate text variations and score externally supplied output consistency."""
import argparse
import json
from pathlib import Path
import re
import sys

VARIANTS = ("casefold", "whitespace", "typographic_quotes")


def generate(cases):
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a nonempty list")
    suite, seen = [], set()
    for case in cases:
        identity, text = case["id"], case["text"]
        if not isinstance(identity, str) or not identity or identity in seen:
            raise ValueError("case IDs must be unique nonempty strings")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("case text must be a nonempty string")
        seen.add(identity)
        suite.append({"id": identity, "original": text, "variants": {
            "casefold": text.casefold(),
            "whitespace": "\n  " + re.sub(r"\s+", "   ", text.strip()) + "  \n",
            "typographic_quotes": text.translate(str.maketrans({'"': "\u201d", "'": "\u2019"})),
        }})
    return suite


def score(suite, responses):
    if not isinstance(responses, list):
        raise ValueError("responses must be a list")
    cases = {case["id"]: case for case in suite}
    observed = {}
    for response in responses:
        identity = response["id"]
        if identity not in cases or identity in observed:
            raise ValueError("response IDs must be known and unique")
        if not isinstance(response["baseline_output"], str):
            raise ValueError("baseline_output must be a string")
        variants = response["variants"]
        if not isinstance(variants, dict) or not set(variants).issubset(VARIANTS):
            raise ValueError("response variants must use generated variant names")
        if any(not isinstance(value, str) for value in variants.values()):
            raise ValueError("variant outputs must be strings")
        observed[identity] = response
    tested, stable, missing, details = 0, 0, 0, []
    for case in suite:
        response = observed.get(case["id"])
        for variant in VARIANTS:
            if response is None or variant not in response["variants"]:
                missing += 1
                details.append({"id": case["id"], "variant": variant, "status": "missing"})
                continue
            matches = response["baseline_output"].strip() == response["variants"][variant].strip()
            tested += 1
            stable += matches
            details.append({"id": case["id"], "variant": variant, "status": "stable" if matches else "changed"})
    total = len(suite) * len(VARIANTS)
    return {"tested": tested, "missing": missing, "stable": stable, "coverage": tested / total,
            "exact_output_stability": stable / tested if tested else None, "details": details}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--mode", choices=("generate", "score"), default="score")
    args = parser.parse_args()
    try:
        input_path = Path(args.input)
        if not input_path.is_absolute():
            input_path = Path(__file__).resolve().parent / input_path
        with input_path.open(encoding="utf-8") as handle:
            data = json.load(handle)
        suite = generate(data["cases"])
        result = {"suite": suite} if args.mode == "generate" else score(suite, data["responses"])
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
        return 0
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f"Invalid robustness evaluation: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
