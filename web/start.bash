#!/bin/bash
set -e
if [ ! -f 'app.py' ]; then
  echo 'Only run from within the dir'
  exit 1
fi
if [ ! -f 'config.py' ]; then
  cp config.example config.py
  echo 'Please edit the config file: config.py'
  exit 1
fi
~/.local/bin/uv sync --no-dev

~/.local/bin/uv run --no-dev gunicorn app:app -b localhost:${PORT:-8003}

