#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
rm -rf "$SCRIPT_DIR/src/dist/dmg"
rm -rf "$SCRIPT_DIR/src/dist/DHVSessionTimer.app"
rm  "$SCRIPT_DIR/src/dist/DHVSessionTimer.dmg"
cd "$SCRIPT_DIR"
source venv/bin/activate
python3 -m PyInstaller src/DHVSessionTimer.spec
cd "$SCRIPT_DIR/src/dist"
mkdir dmg
cp -r DHVSessionTimer.app dmg/
create-dmg --volname "DHVSessionTimer" --window-pos 200 120 --window-size 600 300 --hide-extension "DHVSessionTimer.app" --app-drop-link 425 120 "$SCRIPT_DIR/dist/DHVSessionTimer.dmg" "$SCRIPT_DIR/src/dist/dmg/"