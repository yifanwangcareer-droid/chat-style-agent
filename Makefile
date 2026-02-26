.PHONY: venv install dev test lint run eval

venv:
	python3 -m venv .venv

install:
	pip install -e .

dev:
	pip install -e ".[dev]"

test:
	pytest -q

lint:
	ruff check src tests

run:
	chat-style-agent rewrite --text "I am running late by 10 minutes." --country UK --age 25-34 --scene work

eval:
	chat-style-agent eval --cases configs/eval_cases.json --out outputs/
