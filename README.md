# Cross-Cultural Chat Style Adaptation Agent

A production-style LLM agent for locale-conditioned rewriting with strictly structured JSON outputs.

## Overview

This project implements a controllable LLM-based rewriting agent supporting:
- Locale-specific tone adaptation
- Age-group conditioning
- Structured JSON outputs
- Schema validation + retry guardrails

## Architecture

User Input  
→ Context Engineering (style rule retrieval)  
→ Prompt Construction  
→ LLM Generation  
→ Schema Validation  
→ Retry Guardrail  
→ Structured Output

## Evaluation

- On processing, collecting more real word data...

## Quickstart

```bash
pip install -e .
bash scripts/run_eval.sh
