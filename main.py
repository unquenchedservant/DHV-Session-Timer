import time
from playsound import playsound

#keeping this for later, for adjustability
def play_sound_after_delay(sound_file, delay):
    time.sleep(delay)
    playsound(sound_file)

#default is 10 minutes, with a temp change at 6 minutes and
# another at 8 minutes

# plan is to have the timer be a little bit more...flowy.
# Will probably make PyQT timer for this later to allow
# for a settings page
if __name__ == "__main__":
    sound_file = 'asset/ding.mp3'
    time.sleep(60)
    print("1 minute has passed")
    time.sleep(60)
    print("2 minutes have passed")
    time.sleep(60)
    print("3 minutes have passed")
    time.sleep(60)
    print("4 minutes have passed")
    time.sleep(60)
    print("5 minutes have passed")
    time.sleep(60)
    print("6 minutes have passed")
    print("Temp set to 375")
    playsound(sound_file)
    time.sleep(60)
    print("7 minutes have passed")
    time.sleep(60)
    print("8 minutes have passed")
    print("Temp set to 400")
    playsound(sound_file)
    time.sleep(60)
    print("9 minutes have passed")
    time.sleep(60)
    print("End session! Enjoy!")
    playsound(sound_file)
