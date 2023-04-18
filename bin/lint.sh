#!/usr/bin/env bash

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

if [ "$1" == "--fix" ]; then
  isort . && black ./myapp/ && flake8 ./myapp
else
  isort . --check-only &&
  black ./myapp/ --check &&
  flake8 ./myapp
fi
