#!/bin/sh
# Gate: content validates and the generated files are current, then node tests.
set -e
cd "$(dirname "$0")/.."
python3 tools/build_content.py --check
python3 tools/check_sw.py
node --test
echo "gate: OK"
