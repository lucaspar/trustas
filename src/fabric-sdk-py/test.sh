#!/bin/bash
set -e

# checks /usr/bin/python version
currentver="$(/usr/bin/python -V)"
requiredver="3.0.0"
if [ "$(printf '%s\n' "$requiredver" "$currentver" | sort -V | head -n1)" = "$requiredver" ]; then
    exit_code=0
else
    exit_code=1
fi

if [ $exit_code -gt 0 ]; then
    echo "ERROR: /usr/bin/python has to be version 3.x.x  :/"
    exit $exit_code
fi

# prepare virtual environment
make venv
source venv/bin/activate
pip install -r requirements-test.txt

# run tests
make check
