# ADR Legal Reasoning Skill

A **Claude-powered legal reasoning skill** for Alternative Dispute Resolution, built for LLM students at world-leading law schools.

The skill synthesises **15 landmark ADR papers** into a unified doctoral-grade reasoning engine that produces four distinct intellectual outputs on any ADR question:

| # | Deliverable | What it does |
|---|-------------|--------------|
| 1 | **Structured Legal Argument** | Thesis-driven argument with the novel angle highlighted; publishable as a law review note core |
| 2 | **Full Legal Reasoning — Both Sides** | The strongest case for and against the proposition, with a synthesis verdict |
| 3 | **⚡ Novel Argument Spike** | A genuinely original argument — never articulated before in the literature — developed to publishable standard |
| 4 | **Socratic Challenge** | Identifies the hidden premise in the most prestigious existing position and systematically destabilises it |

---

## Knowledge Base — The 15 Landmark ADR Papers

| # | Citation | Core Contribution |
|---|----------|-------------------|
| 1 | Mnookin & Kornhauser (1979) 88 Yale L.J. 950 | Bargaining in the shadow of the law; legal endowments as bargaining chips |
| 2 & 8 | Genn (2010/2012) — _Judging Civil Justice_ & Yale J.L. & Human. | Civil justice as public good; adjudication as democratic practice; empirical ADR critique |
| 3 | Galanter (1983) 31 UCLA L. Rev. 4 | Dispute pyramid; repeat player / one-shotter asymmetry; "litigotiation" |
| 4 | Felstiner, Abel & Sarat (1980) 15 Law & Soc. Rev. 631 | Naming–blaming–claiming; dispute as social construction |
| 5 | Nader (1984) 132 U. Pa. L. Rev. 621 | ADR as social control; two-tier justice; macrojustice over microjustice |
| 6 & 7 | Sander (1976) 70 F.R.D. 79 | Multi-door courthouse; varieties of dispute processing |
| 9 | Fiss (1984) 93 Yale L.J. 1073 | Against settlement; adjudication as public value explication |
| 10 | Fisher & Ury (1981) _Getting to Yes_ | BATNA; principled negotiation; interests vs positions |
| 11 | Mnookin, Peppet & Tulumello (2000) _Beyond Winning_ | Psychological and cultural barriers to agreement |
| 12 | Hoffman (2004) _The Collaborative Review_ | Collaborative law in commercial disputes |
| 13 | Sander & Goldberg (1994) 10 Negotiation J. 49 | Fitting the forum to the fuss; dispute system design |
| 14 | Luban (1995) 83 Georgetown L.J. 2619 | Settlements and erosion of the public realm |
| 15 | Resnik (2015) 124 Yale L.J. 2804 | Diffusing disputes; mandatory arbitration; erasure of rights |

---

## Setup

### Prerequisites

- Python 3.9 or later
- An [Anthropic API key](https://console.anthropic.com/)

### Install

```bash
pip install -r requirements.txt
```

### Configure

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Optionally override the default model (`claude-opus-4-5`):

```bash
export ADR_MODEL="claude-opus-4-5"
```

---

## Usage

### As a Python library

```python
from adr_skill import ADRSkill

skill = ADRSkill()

# Full response — all four deliverables
response = skill.reason("Is mandatory mediation compatible with access to justice?")
print(response)

# Individual deliverables
print(skill.structured_argument("Does Galanter's repeat-player thesis undermine ADR?"))
print(skill.both_sides("Should settlement agreements be subject to public disclosure?"))
print(skill.novel_spike("Arbitration clauses and the erosion of class actions"))
print(skill.socratic_challenge("Fiss's 'Against Settlement' (1984)"))
```

### As a CLI

```bash
# Full four-deliverable response
python adr_skill.py "Is mandatory mediation compatible with access to justice?"

# Single deliverables
python adr_skill.py --argument "Is mandatory mediation compatible with access to justice?"
python adr_skill.py --both-sides "Does bargaining in the shadow of the law privilege repeat players?"
python adr_skill.py --novel "The multi-door courthouse and power asymmetry"
python adr_skill.py --socratic "Fiss Against Settlement"
```

---

## Output Structure

Each full response contains four clearly labelled sections:

```
DELIVERABLE 1: STRUCTURED LEGAL ARGUMENT WITH NOVEL ANGLE
...

DELIVERABLE 2: FULL LEGAL REASONING — BOTH SIDES
Side A (Proposition): ...
Side B (Opposition): ...
Synthesis: ...

DELIVERABLE 3: ⚡ NOVEL ARGUMENT SPIKE ⚡
...

DELIVERABLE 4: SOCRATIC CHALLENGE
...
```

---

## How Many Papers Should You Attach?

The skill is calibrated for **15 landmark papers** (the current corpus). This is the evidence-based optimum for doctoral-grade ADR reasoning:

- **Fewer than 8** leaves key theoretical traditions uncovered (you lose either the power-critique tradition, the empirical socio-legal tradition, or the negotiation-theory tradition)
- **15** gives you full coverage of: bargaining theory, public-good theory, dispute-transformation theory, power-critique/socio-legal, multi-door/process-design, public-values adjudication theory, principled negotiation, collaborative law, and rights-erasure theory
- **More than 20** provides diminishing returns unless the additional papers occupy a distinct subfield (e.g., online dispute resolution, investment arbitration, restorative justice)

For specialist subfields (e.g., international commercial arbitration, family mediation, labour ADR), add 3–5 field-specific papers to this base corpus.

---

## Files

```
adr_skill.py                    Main Python skill implementation
prompts/
  adr_system_prompt.md          Comprehensive system prompt (15-paper synthesis)
requirements.txt                Python dependencies
adr_papers.md                   Detailed analyses of all 15 landmark papers
README.md                       This file
```

---

## Model Notes

The skill defaults to `claude-opus-4-5` — Anthropic's most capable model — which is required for the novel-argument generation quality demanded by the deliverable specifications. Using a smaller model will degrade the quality of Deliverable 3 (Novel Argument Spike) in particular.
