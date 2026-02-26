import os
from pathlib import Path

def load_style_rules(country: str, age: str, scene: str) -> str:
    path = Path("styles") / f"{country}_{age}_{scene}.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    # fallback: try partial fallback by ignoring age
    fallback = list(Path("styles").glob(f"{country}_*_{scene}.md"))
    if fallback:
        return fallback[0].read_text(encoding="utf-8")
    return "No specific style rules found. Use a neutral, concise tone."

def ensure_dirs():
    os.makedirs("outputs", exist_ok=True)

def write_bad_case(case_id: str, content: str):
    with open("bad_cases.md", "a", encoding="utf-8") as f:
        f.write(f"\n## {case_id}\n{content}\n")