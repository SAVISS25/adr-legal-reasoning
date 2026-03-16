"""
Core extraction logic.

``extract_theoretical_dna`` sends the paper text to an OpenAI-compatible
chat-completions endpoint and returns the model's structured analysis.
"""

from __future__ import annotations

import os
from typing import Optional

try:
    import openai
except ImportError:  # pragma: no cover
    openai = None  # type: ignore[assignment]

from .prompts import SYSTEM_PROMPT, build_user_prompt


def extract_theoretical_dna(
    paper_text: str,
    *,
    model: str = "gpt-4o",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> str:
    """Extract the theoretical DNA of a legal academic paper.

    Parameters
    ----------
    paper_text:
        The full text of the academic paper to analyse.
    model:
        OpenAI model name (default ``"gpt-4o"``).
    api_key:
        OpenAI API key.  Falls back to the ``OPENAI_API_KEY`` environment
        variable when not supplied explicitly.
    base_url:
        Optional alternative base URL for OpenAI-compatible APIs.

    Returns
    -------
    str
        The model's structured analysis of the paper.

    Raises
    ------
    ValueError
        If ``paper_text`` is empty.
    ImportError
        If the ``openai`` package is not installed.
    """
    if openai is None:  # pragma: no cover
        raise ImportError(
            "The 'openai' package is required.  Install it with: pip install openai"
        )

    resolved_key = api_key or os.environ.get("OPENAI_API_KEY")

    client_kwargs: dict = {}
    if resolved_key:
        client_kwargs["api_key"] = resolved_key
    if base_url:
        client_kwargs["base_url"] = base_url

    client = openai.OpenAI(**client_kwargs)

    user_message = build_user_prompt(paper_text)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
    )

    return response.choices[0].message.content or ""
