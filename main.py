import time
from playsound import playsound

def play_sound_after_delay(sound_file, delay):
    time.sleep(delay)
    playsound(sound_file)

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
    playsound(sound_file)
    print("Temp set to 375")
    time.sleep(60)
    print("7 minutes have passed")
    time.sleep(60)
    print("8 minutes have passed")
    playsound(sound_file)
    print("Temp set to 400")
    time.sleep(60)
    print("9 minutes have passed")
    time.sleep(60)
    print("10 minutes have passed")
    playsound(sound_file)
    print("End session! Enjoy!")
