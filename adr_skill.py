"""
ADR Legal Reasoning Skill
=========================
A Claude-powered skill for Alternative Dispute Resolution legal reasoning,
designed for LLM students at world-leading law schools.

For each query the skill returns four deliverables:
  1. Structured legal argument with novel angle highlighted
  2. Full legal reasoning — both sides
  3. Novel argument spike (⚡ original idea, sensation-grade)
  4. Socratic challenge to an existing position

Usage
-----
As a library:
    from adr_skill import ADRSkill
    skill = ADRSkill()
    result = skill.reason("Is mandatory mediation compatible with access to justice?")
    print(result.text)

As a CLI:
    python adr_skill.py "Is mandatory mediation compatible with access to justice?"

Environment variables
---------------------
ANTHROPIC_API_KEY   Your Anthropic API key (required)
ADR_MODEL           Claude model to use (default: claude-opus-4-5)
"""

from __future__ import annotations

import os
import sys
import textwrap
from pathlib import Path
from dataclasses import dataclass

import anthropic


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_DEFAULT_MODEL = "claude-opus-4-5"
_PROMPTS_DIR = Path(__file__).parent / "prompts"
_SYSTEM_PROMPT_PATH = _PROMPTS_DIR / "adr_system_prompt.md"


def _load_system_prompt() -> str:
    """Load the ADR system prompt from the prompts directory."""
    if not _SYSTEM_PROMPT_PATH.exists():
        raise FileNotFoundError(
            f"System prompt not found at {_SYSTEM_PROMPT_PATH}. "
            "Ensure prompts/adr_system_prompt.md exists."
        )
    return _SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class ADRResponse:
    """Structured response from the ADR legal reasoning skill."""

    query: str
    text: str
    model: str
    input_tokens: int
    output_tokens: int

    def __str__(self) -> str:
        header = (
            f"{'=' * 72}\n"
            f"ADR LEGAL REASONING SKILL\n"
            f"Query: {self.query}\n"
            f"Model: {self.model}  |  "
            f"Tokens in: {self.input_tokens}  out: {self.output_tokens}\n"
            f"{'=' * 72}\n\n"
        )
        return header + self.text


# ---------------------------------------------------------------------------
# Skill class
# ---------------------------------------------------------------------------

class ADRSkill:
    """
    Claude-powered Alternative Dispute Resolution legal reasoning skill.

    Synthesises 15 landmark ADR papers (Mnookin & Kornhauser 1979; Genn 2010/2012;
    Galanter 1983; Felstiner, Abel & Sarat 1980; Nader 1984; Sander 1976; Fiss 1984;
    Fisher & Ury 1981; Mnookin, Peppet & Tulumello 2000; Hoffman 2004; Sander &
    Goldberg 1994; Luban 1995; Resnik 2015) into a unified, doctoral-grade reasoning
    engine.

    Parameters
    ----------
    api_key:
        Anthropic API key. If omitted, read from the ANTHROPIC_API_KEY
        environment variable.
    model:
        Claude model identifier. Defaults to ADR_MODEL env var or
        ``claude-opus-4-5``.
    max_tokens:
        Maximum tokens in the response (default 8192).
    """

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        max_tokens: int = 8192,
    ) -> None:
        resolved_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not resolved_key:
            raise ValueError(
                "An Anthropic API key is required. Pass api_key= or set the "
                "ANTHROPIC_API_KEY environment variable."
            )
        self._client = anthropic.Anthropic(api_key=resolved_key)
        self.model = model or os.environ.get("ADR_MODEL", _DEFAULT_MODEL)
        self.max_tokens = max_tokens
        self._system_prompt = _load_system_prompt()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def reason(self, query: str) -> ADRResponse:
        """
        Run the full ADR legal reasoning skill on *query*.

        Returns an :class:`ADRResponse` containing all four deliverables:
        1. Structured legal argument (novel angle highlighted)
        2. Full legal reasoning — both sides
        3. Novel argument spike ⚡
        4. Socratic challenge

        Parameters
        ----------
        query:
            The legal question, scenario, or topic to analyse.
        """
        if not query.strip():
            raise ValueError("Query must not be empty.")

        message = self._client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self._system_prompt,
            messages=[{"role": "user", "content": query}],
        )

        response_text = "".join(
            block.text for block in message.content if hasattr(block, "text")
        )

        return ADRResponse(
            query=query,
            text=response_text,
            model=self.model,
            input_tokens=message.usage.input_tokens,
            output_tokens=message.usage.output_tokens,
        )

    def structured_argument(self, query: str) -> str:
        """
        Return only Deliverable 1 — Structured Legal Argument with Novel Angle.

        This issues a focused instruction appended to the query so the model
        returns only that single section.
        """
        focused_query = (
            f"{query}\n\n"
            "[Instruction: Provide ONLY Deliverable 1 — Structured Legal Argument "
            "with Novel Angle. Do not include the other deliverables.]"
        )
        resp = self.reason(focused_query)
        return resp.text

    def both_sides(self, query: str) -> str:
        """Return only Deliverable 2 — Full Legal Reasoning, Both Sides."""
        focused_query = (
            f"{query}\n\n"
            "[Instruction: Provide ONLY Deliverable 2 — Full Legal Reasoning, "
            "Both Sides. Do not include the other deliverables.]"
        )
        return self.reason(focused_query).text

    def novel_spike(self, query: str) -> str:
        """Return only Deliverable 3 — Novel Argument Spike ⚡."""
        focused_query = (
            f"{query}\n\n"
            "[Instruction: Provide ONLY Deliverable 3 — Novel Argument Spike. "
            "Do not include the other deliverables.]"
        )
        return self.reason(focused_query).text

    def socratic_challenge(self, query: str) -> str:
        """Return only Deliverable 4 — Socratic Challenge."""
        focused_query = (
            f"{query}\n\n"
            "[Instruction: Provide ONLY Deliverable 4 — Socratic Challenge. "
            "Do not include the other deliverables.]"
        )
        return self.reason(focused_query).text


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def _cli_main() -> None:  # pragma: no cover
    """Command-line interface for the ADR legal reasoning skill."""
    if len(sys.argv) < 2:
        print(
            textwrap.dedent(
                """\
                ADR Legal Reasoning Skill
                -------------------------
                Usage:
                    python adr_skill.py "<your legal question>"

                Options:
                    --argument          Return only Deliverable 1 (structured argument)
                    --both-sides        Return only Deliverable 2 (both sides)
                    --novel             Return only Deliverable 3 (novel spike)
                    --socratic          Return only Deliverable 4 (Socratic challenge)

                Environment variables:
                    ANTHROPIC_API_KEY   Required. Your Anthropic API key.
                    ADR_MODEL           Optional. Claude model (default: claude-opus-4-5)

                Example:
                    ANTHROPIC_API_KEY=sk-... python adr_skill.py \\
                        "Is mandatory mediation compatible with access to justice?"
                """
            )
        )
        sys.exit(0)

    flags = {"--argument", "--both-sides", "--novel", "--socratic"}
    mode_flags = [a for a in sys.argv[1:] if a in flags]
    query_parts = [a for a in sys.argv[1:] if a not in flags]
    query = " ".join(query_parts).strip()

    if not query:
        print("Error: no query provided.", file=sys.stderr)
        sys.exit(1)

    skill = ADRSkill()

    if "--argument" in mode_flags:
        print(skill.structured_argument(query))
    elif "--both-sides" in mode_flags:
        print(skill.both_sides(query))
    elif "--novel" in mode_flags:
        print(skill.novel_spike(query))
    elif "--socratic" in mode_flags:
        print(skill.socratic_challenge(query))
    else:
        response = skill.reason(query)
        print(response)


if __name__ == "__main__":
    _cli_main()
