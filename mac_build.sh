#!/bin/bash

rm -rf /Users/jthorne/Developer/DHV-Session-Timer/dist/dmg
rm -rf /Users/jthorne/Developer/DHV-Session-Timer/dist/DHVSessionTimer.app
rm  /Users/jthorne/Developer/DHV-Session-Timer/dist/DHVSessionTimer.dmg
cd /Users/jthorne/Developer/DHV-Session-Timer
source venv/bin/activate
python3 -m PyInstaller DHVSessionTimer.spec
cd /Users/jthorne/Developer/DHV-Session-Timer/dist
mkdir dmg
cp -r DHVSessionTimer.app dmg/
create-dmg --volname "DHVSessionTimer" --window-pos 200 120 --window-size 600 300 --hide-extension "DHVSessionTimer.app" --app-drop-link 425 120 /Users/jthorne/Developer/DHV-Session-Timer/dist/DHVSessionTimer.dmg /Users/jthorne/Developer/DHV-Session-Timer/dist/dmg/