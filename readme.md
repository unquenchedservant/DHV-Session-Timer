# DHV Session Timer
The best way to use a dry herb vaporizer is to slowly ramp up the heat. The Solo line also benefits from this method. 

This is built using the Solo 3 in mind, and so time and temperature limits are because of that. 

Assuming default settings, at 6 minutes a ding will sound and a notification will display saying you're on stage 2 and what temperature you should be at, the timer will show 350F.  

## Installation
Should work on most versions of Python 3, but was built with Python 3.13

In your virtual environment, run `pip3 install requirements.txt`

Once installed, you should be able to run the python file. 

## Features
The best way to use a dry herb vaporizer is to slowly ramp up the heat. The Solo line also benefits from this method. 

## Screenshots
(current screenshots are taken on a tiled Linux and may not accurately reflect default experience)
![image](https://github.com/user-attachments/assets/8b9f4cb8-27e2-4d71-8513-e59bfe10cab2)
![image](https://github.com/user-attachments/assets/24880cf2-b80b-4040-a0ce-ed180e5c86f0)
![image](https://github.com/user-attachments/assets/464abdf5-e973-44b9-9763-ce6f979ea416)

## Defaults
### Temp
Temperature defaults to Fahrenheit

Start temp: 350 
2nd temp:   375
3rd temp:   400

Notifications: True

### Time
1st adjustment:  6 minutes
2nd adjustment:  8 minutes
Session end:    10 minutes
Timeout:        10 seconds
Ding:           True
## Notes
- For some reason the Mac version takes forever to open, this may be because I was using iOS 26 which at the time is in early beta.
- The way the mac app handles notifications is slightly different, but still _technically_ uses the plyer library, it's just modified. See notification.py in the root directory for more information
- Mac notifications give a sound by default, but you may or may not want the ding sound in addition, hence the ding sound is a toggle.
- Mac notifications (currently) don't have a proper timeout function. I'm looking in to this. 


The temperature automatically converts if you switch between Celsius and Fahrenheit, but it's not perfect, so some manual editing may need to occur there.
