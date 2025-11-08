# Video permettant dew comprendre comment manipuler les sons avec python
# https://www.youtube.com/watch?v=qq8W5tMYb4w
import pygame
import os
import time
from geste import Gesture 
from enum import Enum



# helped by ChatGpt for this function
def buildThePath(nameOfAudio : str) :
    # Get the current path of this file
    BASE_DIR = os.path.dirname(__file__)
    return os.path.join(BASE_DIR, "Audios", nameOfAudio)


"""
Pay attention when you add a new AudioGesture to have the same name of Gesture
    than the gesture corresponding in 'Gesture' class from geste.py
"""
class AudioGesture(Enum): 
    thumbs_up = buildThePath("sound for Thumbs Up.mp3")
    thumbs_down = buildThePath("sound for thumb down.mp3")
    peace_sign = buildThePath("sound for sign peace.mp3")
    ok = buildThePath("sound to say OK.mp3")
    sign_to_stop = buildThePath("sound for sign to stop.mp3")




def startTheSong(gesture : Gesture, timeOfSongInSeconds = 1 ) :
    if gesture.name in AudioGesture.__members__:
        audioGesture = AudioGesture[gesture.name]
        playTheSong(audioGesture, timeOfSongInSeconds)
    else :
        
        print(f"\nWe found no song for this gesture. result :{gesture}")


def playTheSong(gesture : AudioGesture, timeOfSongInSeconds : int ):
    pygame.mixer.init()
    gestureToPlay = pygame.mixer.Sound(gesture.value)
    gestureToPlay.play()
    time.sleep(timeOfSongInSeconds)


