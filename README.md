# Chat Style Agent — Cross-Cultural Tone Adapter

A lightweight **tool-use LLM agent** that rewrites a message into **age- and locale-specific internet-native chat style** using:
- **Context retrieval** from local style rules (Markdown)
- **Prompt-based rewriting** (3 variants: natural / polite / short)
- **Evaluation loop** scoring naturalness, politeness, brevity + risk flagging
- **Bad-case logging** for iterative prompt/rule refinement

## Quickstart

### 1) Setup
\`\`\`bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e ".[dev]"
cp .env.example .env
\`\`\`

### 2) Run a single rewrite
\`\`\`bash
chat-style-agent rewrite --text "我今天太累了，不想出门了。" --country US --age 18-24 --scene friends
\`\`\`

### 3) Run evaluation batch
\`\`\`bash
chat-style-agent eval --cases configs/eval_cases.json --out outputs/
\`\`\`

## Project Structure
- \`src/chat_style_agent/\`: agent core + CLI
- \`styles/\`: style rules knowledge base
- \`configs/\`: evaluation cases
- \`outputs/\`: generated results (ignored by git)
- \`tests/\`: minimal tests

## Notes on Responsible Styling
This project adapts **tone/register** (brevity, politeness, slang level) and avoids identity stereotypes.
