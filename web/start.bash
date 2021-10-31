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
if [ ! -d "venv" ]; then
  virtualenv --python=python3 venv
fi
source venv/bin/activate
pip3 install pip==21.3.1 pip-tools==6.4.0
pip-sync
venv/bin/gunicorn app:app --reload -b localhost:8003

