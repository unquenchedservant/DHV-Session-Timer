#!/bin/bash

source venv/bin/activate
python3 -m PyInstaller DHVSessionTimer.spec
sudo cp dist/DHVSessionTimer /usr/bin/DHVSessionTimer
DHVSessionTimer