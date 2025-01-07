# DHV Session Timer
A quick QT based timer, with a ding at adjustable intervals. Useful for reminding yourself to 
adjust the temperature on your Dry Herb Vape session.

This is built using the Solo 3 in mind, and so time and temperature limits are because of that. 

## Installation
Should work on most versions of Python 3, but was built with Python 3.13

The following dependencies are needed:
- playsound
- pyqt5

Once installed, you should be able to run the python file. 

## Defaults
### Temp
Temperature defaults to Fahrenheit

Start temp: 350 
2nd temp:   375
3rd temp:   400

### Time
1st adjustment:  6 minutes
2nd adjustment:  8 minutes
Session end:    10 minutes

## Notes
I had a Stop button, but I had it tied to Reset, so may as well just keep Reset. Given the use-case for this, I doubt "Stop" is needed, so I pulled it. 

The temperature automatically converts if you switch between Celsius and Fahrenheit, but it's not perfect, so some manual editing may need to occur there.

~~Using the reset button in settings won't save the reset settings, you have to hit save after as well (Looking in to this for a future update)~~ This is no longer the case, settings are saved when reset, and hitting "Save" is no longer necessary