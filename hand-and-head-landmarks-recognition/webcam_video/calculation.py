from math import *


def distance_euclidienne(JointA, JointB):
    return sqrt((JointA.x - JointB.x)**2 + (JointA.y - JointB.y)**2 +(JointA.z - JointB.z)**2)



def distanceMax(Y1, Y2, DistanceMax):
    result = abs(Y1 - Y2)
    if result <= DistanceMax :
        return True
    else :
        return False

