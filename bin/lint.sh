#!/usr/bin/env bash

if [ -d "venv" ]; then
    source venv/bin/activate
fi

if [ "$1" == "--fix" ]; then
  python -m isort . && python -m black ./myapp/ && python -m flake8 ./myapp
else
  python -m isort . --check-only &&
  python -m black ./myapp/ --check &&
  python -m flake8 ./myapp
fi
