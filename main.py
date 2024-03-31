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

