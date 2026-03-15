"""Tests for adr_legal_reasoning.prompts."""

import pytest

from adr_legal_reasoning.prompts import (
    SYSTEM_PROMPT,
    USER_PROMPT_TEMPLATE,
    build_user_prompt,
)


# ---------------------------------------------------------------------------
# SYSTEM_PROMPT content checks
# ---------------------------------------------------------------------------

class TestSystemPrompt:
    """The system prompt must contain every required extraction section."""

    REQUIRED_SECTIONS = [
        "PAPER METADATA",
        "CENTRAL THESIS",
        "THEORETICAL FRAMEWORK",
        "KEY ARGUMENTS",
        "SCHOLARLY POSITIONING",
        "KEY QUOTES",
        "METHODOLOGY",
        "ACKNOWLEDGED GAPS",
        "UNRESOLVED TENSIONS",
        "CONTRIBUTION TO THE FIELD",
    ]

    def test_is_non_empty_string(self):
        assert isinstance(SYSTEM_PROMPT, str)
        assert len(SYSTEM_PROMPT.strip()) > 0

    @pytest.mark.parametrize("section", REQUIRED_SECTIONS)
    def test_contains_required_section(self, section):
        assert section in SYSTEM_PROMPT, (
            f"SYSTEM_PROMPT is missing required section: {section!r}"
        )

    def test_instructs_legal_assistant_role(self):
        assert "legal academic assistant" in SYSTEM_PROMPT

    def test_preserves_author_language_instruction(self):
        assert "author's exact language" in SYSTEM_PROMPT

    def test_key_arguments_range(self):
        """Prompt must request between 3 and 6 key arguments."""
        assert "3" in SYSTEM_PROMPT
        assert "6" in SYSTEM_PROMPT

    def test_key_quotes_verbatim_instruction(self):
        assert "verbatim" in SYSTEM_PROMPT

    def test_paper_text_placeholder_present(self):
        assert "Paper text follows" in SYSTEM_PROMPT

    def test_core_field_options_present(self):
        for field in ["mediation", "negotiation", "arbitration", "ODR"]:
            assert field in SYSTEM_PROMPT, (
                f"Core field option {field!r} missing from SYSTEM_PROMPT"
            )

    def test_methodology_options_present(self):
        assert "Doctrinal analysis" in SYSTEM_PROMPT
        assert "Normative theory" in SYSTEM_PROMPT
        assert "Comparative" in SYSTEM_PROMPT
        assert "Empirical" in SYSTEM_PROMPT

    def test_logical_structure_options_present(self):
        for structure in ["deductive", "analogical", "normative", "empirical"]:
            assert structure in SYSTEM_PROMPT, (
                f"Logical structure option {structure!r} missing from SYSTEM_PROMPT"
            )


# ---------------------------------------------------------------------------
# build_user_prompt
# ---------------------------------------------------------------------------

class TestBuildUserPrompt:
    """build_user_prompt wraps raw paper text into the user-turn message."""

    SAMPLE_PAPER = "This is the full text of a legal academic paper on mediation."

    def test_returns_string(self):
        result = build_user_prompt(self.SAMPLE_PAPER)
        assert isinstance(result, str)

    def test_contains_paper_text(self):
        result = build_user_prompt(self.SAMPLE_PAPER)
        assert self.SAMPLE_PAPER in result

    def test_strips_leading_trailing_whitespace_from_paper(self):
        padded = f"\n\n  {self.SAMPLE_PAPER}  \n\n"
        result = build_user_prompt(padded)
        assert self.SAMPLE_PAPER in result

    def test_empty_string_raises_value_error(self):
        with pytest.raises(ValueError):
            build_user_prompt("")

    def test_whitespace_only_raises_value_error(self):
        with pytest.raises(ValueError):
            build_user_prompt("   \n\t  ")

    def test_multiline_paper_preserved(self):
        multiline = "Line one.\nLine two.\nLine three."
        result = build_user_prompt(multiline)
        assert "Line one." in result
        assert "Line two." in result
        assert "Line three." in result

    def test_template_format_consistency(self):
        """USER_PROMPT_TEMPLATE must contain the {paper_text} placeholder."""
        assert "{paper_text}" in USER_PROMPT_TEMPLATE
