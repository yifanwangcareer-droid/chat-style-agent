from .tools import load_style_rules

def adapt_one(text: str, country: str, age: str, scene: str) -> str:
    # TODO: paste your working agent pipeline here (rewrite -> score -> fallback)
    rules = load_style_rules(country, age, scene)
    return f"[TODO] rewrite: {text}\\n[style_rules]\\n{rules[:200]}..."

def run_eval(cases_path: str, out_dir: str):
    # TODO: paste your batch eval runner here
    print(f"[TODO] run eval on {cases_path} -> {out_dir}")
