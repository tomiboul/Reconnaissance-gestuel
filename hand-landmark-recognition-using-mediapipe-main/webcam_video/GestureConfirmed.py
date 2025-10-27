import time
from geste import Gesture
class GestureConfirmed : 
    def __init__(self, minimum_detection = 3):
        self.listOfGesture = []
        self.minimum_detection = minimum_detection
    
    def analyseGesture(self)-> Gesture :
        i = len(self.listOfGesture)-1     
        temp_list = []    
        while i>=0 :    
            temp_list.append(self.listOfGesture[i])   

            if self.listOfGesture[i] != Gesture.nothing :
                if (self.listOfGesture.count(self.listOfGesture[i]) >= self.minimum_detection 
                    and self.listOfGesture[i] != Gesture.say_shush):  
                    return self.listOfGesture[i]
                elif (self.listOfGesture.count(self.listOfGesture[i]) >= (self.minimum_detection +2) 
                    and self.listOfGesture[i] == Gesture.say_shush):
                    return self.listOfGesture[i]

            i = i - 1
        return Gesture.nothing

