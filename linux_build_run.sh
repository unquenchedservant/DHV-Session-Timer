#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
source venv/bin/activate
killall DHVSessionTimer
cd "$SCRIPT_DIR/src"
python3 -m PyInstaller DHVSessionTimer.spec
sudo cp dist/DHVSessionTimer /usr/bin/DHVSessionTimer
DHVSessionTimer