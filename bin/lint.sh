#!/usr/bin/env bash

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

if [ "$1" == "--fix" ]; then
  ruff check . --fix && black ./myapp
else
  ruff check . && black ./myapp --check
fi
