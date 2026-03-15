"""
Command-line interface for the ADR Legal Reasoning extractor.

Usage
-----
    python -m adr_legal_reasoning.cli --file paper.txt
    python -m adr_legal_reasoning.cli --stdin < paper.txt

The extracted analysis is printed to stdout.  An OpenAI API key must be
available via the ``OPENAI_API_KEY`` environment variable (or passed with
``--api-key``).
"""

from __future__ import annotations

import argparse
import sys

from .extractor import extract_theoretical_dna


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="adr-legal-reasoning",
        description=(
            "Extract the theoretical DNA of a legal academic paper "
            "and print a structured analysis to stdout."
        ),
    )

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "--file",
        metavar="PATH",
        help="Path to a plain-text file containing the paper.",
    )
    source.add_argument(
        "--stdin",
        action="store_true",
        help="Read the paper text from stdin.",
    )

    parser.add_argument(
        "--model",
        default="gpt-4o",
        metavar="MODEL",
        help="OpenAI model to use (default: gpt-4o).",
    )
    parser.add_argument(
        "--api-key",
        metavar="KEY",
        help="OpenAI API key (overrides OPENAI_API_KEY env var).",
    )
    parser.add_argument(
        "--base-url",
        metavar="URL",
        help="Optional base URL for OpenAI-compatible APIs.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Entry-point for the CLI.  Returns an exit code."""
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.stdin:
        paper_text = sys.stdin.read()
    else:
        try:
            with open(args.file, encoding="utf-8") as fh:
                paper_text = fh.read()
        except OSError as exc:
            print(f"Error reading file: {exc}", file=sys.stderr)
            return 1

    if not paper_text.strip():
        print("Error: paper text is empty.", file=sys.stderr)
        return 1

    result = extract_theoretical_dna(
        paper_text,
        model=args.model,
        api_key=args.api_key,
        base_url=args.base_url,
    )
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
