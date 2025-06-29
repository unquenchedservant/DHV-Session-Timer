# DHV Session Timer
The best way to use a dry herb vaporizer is to slowly ramp up the heat. The Solo line also benefits from this method. 

This is built using the Solo 3 in mind, and so time and temperature limits are because of that. 

Assuming default settings, at 6 minutes a ding will sound and a notification will display saying you're on stage 2 and what temperature you should be at, the timer will show 350F.  

# Installation
Should work on most versions of Python 3, but was built with Python 3.13

In your virtual environment, run `pip3 install requirements.txt`

Once installed, you should be able to run the python file. 

For build instructions see [Build](#Build)

# Features
The best way to use a dry herb vaporizer is to slowly ramp up the heat. The Solo line also benefits from this method. 

# Screenshots
(current screenshots are taken on a tiled Linux and may not accurately reflect default experience)

- Main timer page

![image](https://github.com/user-attachments/assets/03ff3a2c-3ea2-4308-b499-f0b6bfb972e4)

- Settings screen

![image](https://github.com/user-attachments/assets/c28e4d2c-96de-4b8d-8044-55a6c70040a8)

- Example notification (on linux using swaync)

![image](https://github.com/user-attachments/assets/464abdf5-e973-44b9-9763-ce6f979ea416)

- Notification grouping (confirmed on Linux, will look different on other platforms)

![image](https://github.com/user-attachments/assets/753a2d6f-2d59-4bb1-b1b0-50811740d324)


# Defaults
only changeable items listed. Pressing "Reset" in the settings menu should reset all listed variables to the corresponding value in the below table.

|Setting Name|Variable Name|Value|
|---|---|---|
| Temp Unit | temp_type | "F" |
| Temp 1 | temp1 | 350 |
| Temp 2 | temp2 | 375 |
| Temp 3 | temp3 | 400 |
| Temp Unit | temp_type | "F" |
| Notifications | notifications | True |
| Stg. 2 Time (min) | time2 | 6 |
| Stg. 3 Time (min) | time3 | 8 | 
| End Time (min) | time4 | 10 |
| Notif. Timeout | timeout | 10 |
| Ding | almightyDing | True |
| Keep Win on Top by Default | keep_active_default | False |

# Build
PyInstaller is the builder of choice, use `python3 -m PyInstaller DHVSessionTimer.spec` to build

Some handy build scripts have been provided, two for linux (one just builds, the other builds and runs) and one for Mac. These run PyInstaller on your behalf

Windows building isn't necessary, as we have a GitHub Action set up to build a Windows artifact. 

## Notes
- For some reason the Mac version takes forever to open, this may be because I was using iOS 26 which at the time is in early beta.
- The way the mac app handles notifications is slightly different, but still _technically_ uses the plyer library, it's just modified. See [notification.py](https://github.com/unquenchedservant/DHV-Session-Timer/blob/main/notification.py) in the root directory for more information
- Mac notifications give a sound by default, but you may or may not want the ding sound in addition, hence the ding sound is a toggle.
- Mac notifications (currently) don't have a proper timeout function. I'm looking in to this. 


The temperature automatically converts if you switch between Celsius and Fahrenheit, but it's not perfect, so some manual editing may need to occur there.
