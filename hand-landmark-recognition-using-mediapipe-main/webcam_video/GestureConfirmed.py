import time
from geste import Gesture
class GestureConfirmed : 
    def __init__(self, time_needed = 1, minimum_detection = 3):
        self.listOfGesture = []
        self.time_needed = time_needed
        self.minimum_detection = minimum_detection
    
    def analyseGesture(self, gesture):
        timer = time.time()
        
        if (timer > 1) :
            timer = 0
            self.listOfGesture = []
        else :
            if gesture in Gesture :
                self.listOfGesture.append(gesture)
            for typeOfGesture in Gesture:
                if self.listOfGesture.count(typeOfGesture) >= self.minimum_detection :
                    print(typeOfGesture + " is confirmed")
                    return typeOfGesture
