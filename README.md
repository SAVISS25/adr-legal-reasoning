# adr-legal-reasoning

A Python tool that extracts the **theoretical DNA** of legal academic papers
(ADR, mediation, arbitration, negotiation, ODR) using an LLM.

## What it does

Given the full text of a legal academic paper the tool returns a structured
analysis covering:

| Section | Contents |
|---|---|
| **Paper Metadata** | Full citation, academic tradition, core ADR field |
| **Central Thesis** | The paper's exact claim in one paragraph |
| **Theoretical Framework** | Conceptual apparatus and intellectual lineage |
| **Key Arguments** | 3–6 numbered arguments with claim, logical structure, and evidence |
| **Scholarly Positioning** | Agreement, challenges, and place in the debate |
| **Key Quotes** | 3–5 verbatim, page-numbered theoretically-loaded sentences |
| **Methodology** | Doctrinal / normative / comparative / empirical breakdown |
| **Acknowledged Gaps** | What the author admits is unresolved |
| **Unresolved Tensions** | Internal contradictions not acknowledged by the author |
| **Contribution to the Field** | What the paper adds to the discipline |

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command-line

```bash
# From a file
python -m adr_legal_reasoning.cli --file paper.txt

# From stdin
cat paper.txt | python -m adr_legal_reasoning.cli --stdin

# Custom model or API-compatible endpoint
python -m adr_legal_reasoning.cli --file paper.txt \
    --model gpt-4-turbo \
    --api-key sk-... \
    --base-url https://api.example.com/v1
```

An OpenAI API key must be available via the `OPENAI_API_KEY` environment
variable or the `--api-key` flag.

### Python API

```python
from adr_legal_reasoning.extractor import extract_theoretical_dna

with open("paper.txt") as f:
    paper_text = f.read()

analysis = extract_theoretical_dna(paper_text, model="gpt-4o")
print(analysis)
```

## Development

```bash
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

