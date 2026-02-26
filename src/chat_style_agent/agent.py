import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from openai import OpenAI

from .tools import load_style_rules

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY. Please set it in your .env file.")

client = OpenAI(api_key=API_KEY)
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = (
    "You are a cross-cultural chat style adaptation agent.\n"
    "Your goal is to rewrite messages into natural internet-native expressions "
    "for a specific country, age group, and scene.\n\n"
    "Focus on tone and register (slang level, brevity, politeness).\n"
    "Avoid stereotypes or offensive assumptions.\n"
    "Return valid JSON only."
)


def validate_variants(data: Any) -> bool:
    """Validate output schema:
    {
      "variants": [
        {"name": "natural", "text": "..."},
        {"name": "polite", "text": "..."},
        {"name": "short", "text": "..."}
      ]
    }
    """
    if not isinstance(data, dict):
        return False

    variants = data.get("variants")
    if not isinstance(variants, list) or len(variants) != 3:
        return False

    required_names = {"natural", "polite", "short"}
    seen = set()

    for v in variants:
        if not isinstance(v, dict):
            return False
        if "name" not in v or "text" not in v:
            return False
        if v["name"] not in required_names:
            return False
        if not isinstance(v["text"], str) or not v["text"].strip():
            return False
        # enforce one-line bullet/sentence
        if "\n" in v["text"]:
            return False
        seen.add(v["name"])

    return seen == required_names


def _chat(prompt: str, temperature: float = 0.7) -> str:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
    )
    return (resp.choices[0].message.content or "").strip()


def polish_sentence(sentence: str, country: str) -> str:
    """Polish a single sentence without changing meaning. Returns one sentence."""
    polish_prompt = f"""
You are a copy editor. Fix grammar and unnatural phrasing.

Rules:
- Do NOT change meaning.
- Keep ONE sentence.
- Keep tone consistent with {country}.
- Output only the corrected sentence (no quotes, no extra text).

Sentence:
{sentence}
""".strip()

    out = _chat(polish_prompt, temperature=0.2)
    # hard guard: keep one line
    out = out.replace("\n", " ").strip()
    return out if out else sentence


def adapt_one(
    text: str,
    country: str,
    age: str,
    scene: str,
    *,
    polish: bool = True,
    max_retries: int = 2,
) -> str:
    """Rewrite one message and return JSON string."""
    style_rules = load_style_rules(country, age, scene)

    base_prompt = f"""
Rewrite the following message into the style of:
Country: {country}
Age group: {age}
Scene: {scene}

Style rules:
{style_rules}

Message:
{text}

Provide 3 variants:
1. natural
2. polite
3. short

Return JSON in this format:
{{
  "variants": [
    {{"name": "natural", "text": "..."}},
    {{"name": "polite", "text": "..."}},
    {{"name": "short", "text": "..."}}
  ]
}}
""".strip()

    last_error: Optional[str] = None
    prompt = base_prompt

    for attempt in range(max_retries + 1):
        content = _chat(prompt, temperature=0.7)

        try:
            parsed = json.loads(content)
        except Exception:
            last_error = "JSON parsing failed"
            parsed = None

        if parsed is not None and validate_variants(parsed):
            if polish:
                for v in parsed["variants"]:
                    v["text"] = polish_sentence(v["text"], country)
            return json.dumps(parsed, indent=2, ensure_ascii=False)

        last_error = last_error or "Invalid schema structure"
        # strengthen prompt for retry
        prompt = (
            base_prompt
            + "\n\nIMPORTANT:\n"
              "- Output MUST be valid JSON only.\n"
              "- Follow schema EXACTLY.\n"
              "- 'variants' must contain exactly 3 items: natural, polite, short.\n"
              "- Each 'text' must be a single line (no newline).\n"
              "- Do not add any extra keys.\n"
        )

    raise ValueError(f"Model failed after retries. Last error: {last_error}")


def run_eval(cases_path: str, out_dir: str) -> None:
    cases: List[Dict[str, Any]] = json.load(open(cases_path, "r", encoding="utf-8"))
    os.makedirs(out_dir, exist_ok=True)

    results = []
    for case in cases:
        result = adapt_one(
            text=case["text"],
            country=case["target_country"],
            age=case["target_age"],
            scene=case["scene"],
        )
        results.append({"id": case["id"], "result": result})

    out_path = Path(out_dir) / "all_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(results)} results to {out_dir}")