"""Tests for adr_legal_reasoning.cli."""

import sys
from io import StringIO
from unittest.mock import MagicMock, patch

import pytest

from adr_legal_reasoning.cli import _build_parser, main


SAMPLE_ANALYSIS = "PAPER METADATA\n- Full citation: Author, Title, Journal, 2023"
SAMPLE_PAPER = "Full text of the legal paper goes here."


# ---------------------------------------------------------------------------
# Argument parser tests
# ---------------------------------------------------------------------------

class TestBuildParser:
    def test_file_argument(self, tmp_path):
        p = tmp_path / "paper.txt"
        p.write_text(SAMPLE_PAPER)
        args = _build_parser().parse_args(["--file", str(p)])
        assert args.file == str(p)
        assert not args.stdin

    def test_stdin_argument(self):
        args = _build_parser().parse_args(["--stdin"])
        assert args.stdin
        assert args.file is None

    def test_file_and_stdin_mutually_exclusive(self, tmp_path):
        p = tmp_path / "paper.txt"
        p.write_text(SAMPLE_PAPER)
        with pytest.raises(SystemExit):
            _build_parser().parse_args(["--file", str(p), "--stdin"])

    def test_neither_file_nor_stdin_raises(self):
        with pytest.raises(SystemExit):
            _build_parser().parse_args([])

    def test_default_model(self):
        args = _build_parser().parse_args(["--stdin"])
        assert args.model == "gpt-4o"

    def test_custom_model(self):
        args = _build_parser().parse_args(["--stdin", "--model", "gpt-4-turbo"])
        assert args.model == "gpt-4-turbo"

    def test_api_key_argument(self):
        args = _build_parser().parse_args(["--stdin", "--api-key", "sk-test"])
        assert args.api_key == "sk-test"

    def test_base_url_argument(self):
        args = _build_parser().parse_args(["--stdin", "--base-url", "http://localhost"])
        assert args.base_url == "http://localhost"


# ---------------------------------------------------------------------------
# main() integration tests (extractor is mocked)
# ---------------------------------------------------------------------------

class TestMain:
    @patch("adr_legal_reasoning.cli.extract_theoretical_dna", return_value=SAMPLE_ANALYSIS)
    def test_reads_from_file(self, mock_extract, tmp_path, capsys):
        p = tmp_path / "paper.txt"
        p.write_text(SAMPLE_PAPER)
        exit_code = main(["--file", str(p)])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert SAMPLE_ANALYSIS in captured.out
        mock_extract.assert_called_once()

    @patch("adr_legal_reasoning.cli.extract_theoretical_dna", return_value=SAMPLE_ANALYSIS)
    def test_reads_from_stdin(self, mock_extract, capsys, monkeypatch):
        monkeypatch.setattr("sys.stdin", StringIO(SAMPLE_PAPER))
        exit_code = main(["--stdin"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert SAMPLE_ANALYSIS in captured.out
        mock_extract.assert_called_once()

    @patch("adr_legal_reasoning.cli.extract_theoretical_dna", return_value=SAMPLE_ANALYSIS)
    def test_passes_model_to_extractor(self, mock_extract, tmp_path):
        p = tmp_path / "paper.txt"
        p.write_text(SAMPLE_PAPER)
        main(["--file", str(p), "--model", "gpt-4-turbo"])
        _, kwargs = mock_extract.call_args
        assert kwargs.get("model") == "gpt-4-turbo"

    @patch("adr_legal_reasoning.cli.extract_theoretical_dna", return_value=SAMPLE_ANALYSIS)
    def test_passes_api_key_to_extractor(self, mock_extract, tmp_path):
        p = tmp_path / "paper.txt"
        p.write_text(SAMPLE_PAPER)
        main(["--file", str(p), "--api-key", "sk-test"])
        _, kwargs = mock_extract.call_args
        assert kwargs.get("api_key") == "sk-test"

    def test_missing_file_returns_error(self, capsys):
        exit_code = main(["--file", "/nonexistent/path/paper.txt"])
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Error" in captured.err

    @patch("adr_legal_reasoning.cli.extract_theoretical_dna", return_value=SAMPLE_ANALYSIS)
    def test_empty_stdin_returns_error(self, mock_extract, capsys, monkeypatch):
        monkeypatch.setattr("sys.stdin", StringIO(""))
        exit_code = main(["--stdin"])
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "empty" in captured.err
        mock_extract.assert_not_called()

    @patch("adr_legal_reasoning.cli.extract_theoretical_dna", return_value=SAMPLE_ANALYSIS)
    def test_whitespace_only_stdin_returns_error(self, mock_extract, capsys, monkeypatch):
        monkeypatch.setattr("sys.stdin", StringIO("   \n\t  "))
        exit_code = main(["--stdin"])
        assert exit_code == 1
        mock_extract.assert_not_called()
