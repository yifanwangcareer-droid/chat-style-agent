import json
from pathlib import Path
from chat_style_agent.agent import adapt_one

INPUT_FILE = Path("tests/eval_cases.jsonl")
OUTPUT_FILE = Path("outputs/eval_outputs.jsonl")


def is_valid_json(text: str) -> bool:
    try:
        json.loads(text)
        return True
    except Exception:
        return False


def main():
    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    total = 0
    valid = 0

    with INPUT_FILE.open("r", encoding="utf-8") as fin, \
         OUTPUT_FILE.open("w", encoding="utf-8") as fout:

        for line in fin:
            case = json.loads(line)
            total += 1

            raw = adapt_one(
                case["text"],
                case["country"],
                case["age"],
                case["scene"],
            )

            if isinstance(raw, dict):
                raw_str = json.dumps(raw, ensure_ascii=False)
            else:
                raw_str = str(raw)

            ok = is_valid_json(raw_str)
            if ok:
                valid += 1

            fout.write(json.dumps({
                "id": case.get("id", total),
                "valid": ok,
                "raw": raw_str
            }, ensure_ascii=False) + "\n")

    rate = (valid / total) * 100 if total else 0
    print(f"JSON valid: {valid}/{total} = {rate:.1f}%")


if __name__ == "__main__":
    main()
    