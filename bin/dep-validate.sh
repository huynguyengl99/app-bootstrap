#!/usr/bin/env bash
set -e

export PATH="./venv/bin:$PATH"

poetry check
poetry lock --check
