import argparse
from .agent import adapt_one, run_eval

def main():
    p = argparse.ArgumentParser(prog="chat-style-agent")
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("rewrite")
    r.add_argument("--text", required=True)
    r.add_argument("--country", required=True)
    r.add_argument("--age", required=True)
    r.add_argument("--scene", required=True)

    e = sub.add_parser("eval")
    e.add_argument("--cases", required=True)
    e.add_argument("--out", default="outputs/")

    args = p.parse_args()
    if args.cmd == "rewrite":
        res = adapt_one(args.text, args.country, args.age, args.scene)
        print(res)
    elif args.cmd == "eval":
        run_eval(args.cases, args.out)
