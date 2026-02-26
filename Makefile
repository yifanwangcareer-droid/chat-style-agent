.PHONY: venv install dev test lint run eval

venv:
\tpython3 -m venv .venv

install:
\tpip install -e .

dev:
\tpip install -e ".[dev]"

test:
\tpytest -q

lint:
\truff check src tests

run:
\tchat-style-agent rewrite --text "I am running late by 10 minutes." --country UK --age 25-34 --scene work

eval:
\tchat-style-agent eval --cases configs/eval_cases.json --out outputs/
