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
  #virtualenv --python=python3.12 venv
  python3.8 -m venv venv
fi
source venv/bin/activate
pip3 install pip==25.0 pip-tools==7.4.1
pip-sync setup/requirements.txt

gunicorn app:app --reload -b localhost:8003

