#!/bin/bash

source venv/bin/activate
python3 -m PyInstaller src/DHVSessionTimer.spec
sudo cp src/dist/DHVSessionTimer /usr/bin/DHVSessionTimer
DHVSessionTimer