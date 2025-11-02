import time
from geste import Gesture
class GestureConfirmed : 
    def __init__(self, minimum_detection = 3):
        """
        Create an object to detect and confirm a gesture into a frame of 10 gestures 
        """
        self.listOfGesture = []
        self.minimum_detection = minimum_detection
    
    def analyseGesture(self)-> Gesture :
        """
        Look into the object GestureConfirmed and confirm a getsure if there is the minimal number of this gesture 
        into the list of GestureConfirmed.listOfGesture

        RETURN
        ——————
        A gesture with the minimal detection in GestureConfirmed.listOfGesture
        """
        i = len(self.listOfGesture)-1     
        temp_list = []    
        while i>=0 :    
            temp_list.append(self.listOfGesture[i])   

            if self.listOfGesture[i] != Gesture.nothing :
                if (self.listOfGesture.count(self.listOfGesture[i]) >= self.minimum_detection 
                    and self.listOfGesture[i] != Gesture.say_shush): 
                    #deleteElementBeforeLastGesture(self.listOfGesture, i)
                    return self.listOfGesture[i]
                elif (self.listOfGesture.count(self.listOfGesture[i]) >= (self.minimum_detection +2) 
                    and self.listOfGesture[i] == Gesture.say_shush):
                    #deleteElementBeforeLastGesture(self.listOfGesture, i)
                    return self.listOfGesture[i]

            i = i - 1
        return Gesture.nothing



"""def deleteElementBeforeLastGesture(listeOfGesture, positionInTheList): 
    listeTemp  = []
    for lastGesture in reversed(listeOfGesture):
        if lastGesture == listeOfGesture[positionInTheList] :
            return list(reversed(listeTemp))
        else :
            listeTemp.append(lastGesture)
    return listeOfGesture"""

"""
listOfGesture = [1,2,9,2,8,0]
positionInTheList = 1
liste = deleteElementBeforeLastGesture(listOfGesture, positionInTheList)
print(liste)"""
