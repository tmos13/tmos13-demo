# TMOS13 Demo CLI

**Protocol-governed AI sessions. Deploy Yourself.**

tmos13.ai

---

## What this is

TMOS13 is a protocol-governed AI operating system. Instead of prompting a chatbot, you run **packs** — behavioral specification files that define exactly what an AI session is authorized to do, what questions it must ask, what fields it must capture, and what structured deliverable it produces.

This repository is a minimal public demo of that architecture. Three packs. One Python file. No database. No cloud infrastructure. Just the protocol, the model, and the output.

---

## Setup

```bash
git clone https://github.com/tmos13/tmos13-demo.git
cd tmos13-demo
pip install -r requirements.txt
cp .env.example .env
# Add your Anthropic API key to .env
python demo.py
```

Requires Python 3.10+ and an Anthropic API key.

---

## How it works

```
packs/
  legal_intake/MANIFEST.md      ← behavioral specification
  lead_qualification/MANIFEST.md
  compliance_audit/MANIFEST.md

demo.py                          ← engine (reads packs, runs sessions, writes output)

output/
  legal_intake_20260314_093012.md  ← structured deliverable
```

A **pack manifest** is a plain text file that governs an AI session:
- What the session is authorized to do (and not do)
- What fields it must capture
- What routing rules apply
- What the deliverable looks like

The engine reads the manifest, builds a system prompt, runs the session through the Claude API, and writes the deliverable to `output/`.

That's it. No training. No fine-tuning. No prompt engineering by the operator. The protocol is the product.

---

## The three demo packs

| Pack | What it does |
|------|-------------|
| `legal_intake` | Qualifies a legal matter and produces a case intake brief |
| `lead_qualification` | Runs a BANT discovery conversation and produces a scored lead report |
| `compliance_audit` | Assesses a compliance audit engagement and flags structural risks |

---

## The full platform

This demo shows the architecture. The full TMOS13 platform includes:

- **356 active packs** across 24 categories — criminal justice, diplomatic, education, consulting, creative, agriculture, and more
- **Dimensional Vault** — 8-angle addressed persistent memory across sessions
- **FastAPI engine** — 54 modules, 77 endpoints, 1,039+ passing tests
- **React/TypeScript frontend** — tmos13.ai
- **MCP integration** — GitHub, Gmail, Google Calendar, Vercel

→ [tmos13.ai](https://tmos13.ai)

---

## Architecture note

The governance insight: the difference between a useful AI interaction and a deployable AI workflow is behavioral specification. Every enterprise AI failure — hallucination, scope creep, inconsistent output — traces back to the same root cause: the model was given a task without a contract.

Pack manifests are the contract. The model executes. The session produces a structured artifact. The Vault stores it.

**The code is the organization. The organization is the code.**

---

*TMOS13, LLC · Jersey City, NJ · rob@tmos13.ai*
*Two provisional patents filed February 21, 2026*
