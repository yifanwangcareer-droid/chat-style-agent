from pathlib import Path

def load_style_rules(country: str, age: str, scene: str) -> str:
    path = Path("styles") / f"{country}_{age}_{scene}.md"
    if path.exists():
        return path.read_text(encoding="utf-8")
    fallback = list(Path("styles").glob(f"{country}_*_{scene}.md"))
    if fallback:
        return fallback[0].read_text(encoding="utf-8")
    return "No specific style rules found. Use a neutral, concise tone."
