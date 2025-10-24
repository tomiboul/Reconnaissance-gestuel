from enum import Enum
import cv2 as cv
import mediapipe.python.solutions.hands as mp_hands
from math import *

class Gesture(Enum):
    thumbs_up = "pouce en l'air"   # pouce en l'air
    say_shush = "chut beau gosse"   # met l'index vers le haut (comme pour dire chute)

def distance_euclidienne(JointA, JointB):
    return sqrt((JointA.x - JointB.x)**2 + (JointA.y - JointB.y)**2 +(JointA.z - JointB.z)**2)


def go_to_detect_gesture(joint_from_hand):
    """
        Take the set of hand landmarks and translate them in a gesture.

        PARAMETERS
        ——————————
        joint_from_hand : set of hand landmark

        RETURN
        ——————
        return 
            the gesture from the enumeration 
        OR 
            null
    """
    list_function_detection = [
        detect_say_shush,
        detect_thumbs_up
    ]

    for function_detection in list_function_detection :
        gesture = function_detection(joint_from_hand)
        if gesture  != None :
            print(gesture.value)




def detect_thumbs_up(joint_from_hand) -> Gesture :
    
    """
        Take the set of hand landmarks, take four joints from the hand and detect or not a thumbs_up

        PARAMETERS
        ——————————
        joint_from_hand : set of hand landmark

        RETURN
        ——————
        return if the gesture is a thumbs_up OR not
    """
    Wrist = joint_from_hand[mp_hands.HandLandmark.WRIST] #paume de la main
    #Thumb_cmc = joint_from_hand[mp_hands.HandLandmark.THUMB_CMC]
    Thumb_mcp = joint_from_hand[mp_hands.HandLandmark.THUMB_MCP]
    Thumb_ip = joint_from_hand[mp_hands.HandLandmark.THUMB_IP]
    Thumb_tip = joint_from_hand[mp_hands.HandLandmark.THUMB_TIP]

    Index_tip = joint_from_hand[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    Middle_tip = joint_from_hand[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    Ring_tip = joint_from_hand[mp_hands.HandLandmark.RING_FINGER_TIP]
    Pinky_tip = joint_from_hand[mp_hands.HandLandmark.PINKY_TIP]

    # est-ce que le pouce est levé avec ses positions en Y de ses articulations
    thumbs_up = (Thumb_mcp.y > Thumb_ip.y > Thumb_tip.y )

    # we see if the tips of the other fingers are near to the wrist 
    # The maximum value can be change but below 0,20 it is hard to confimr the 
    #   thumb up and over 0,25 it detects too much even if dont do a thumb up
    if ((thumbs_up == True) 
        and (distance_euclidienne(Wrist, Index_tip) < 0.23) 
        and (distance_euclidienne(Wrist, Middle_tip) < 0.22) 
        and (distance_euclidienne(Wrist, Ring_tip) < 0.22) 
        and (distance_euclidienne(Wrist, Pinky_tip) < 0.22)) :
        return Gesture.thumbs_up
    else : 
        return None






def detect_say_shush(joint_from_hand) -> Gesture :
    """
    Take the set of hand landmarks, take four joints from the hand and detect or not a thumbs_up

    PARAMETERS
    ——————————
    joint_from_hand : set of hand landmark

    RETURN
    ——————
    return if the gesture is a thumbs_up OR not
    """
    Wrist = joint_from_hand[mp_hands.HandLandmark.WRIST] #paume de la main
    Index_tip = joint_from_hand[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    Index_dip = joint_from_hand[mp_hands.HandLandmark.INDEX_FINGER_DIP]
    Index_pip = joint_from_hand[mp_hands.HandLandmark.INDEX_FINGER_PIP]


    Thumb_tip = joint_from_hand[mp_hands.HandLandmark.THUMB_TIP]
    Middle_tip = joint_from_hand[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    Ring_tip = joint_from_hand[mp_hands.HandLandmark.RING_FINGER_TIP]
    Pinky_tip = joint_from_hand[mp_hands.HandLandmark.PINKY_TIP]

    # est-ce que le pouce est levé avec ses positions en Y de ses articulations
    say_shush = (Index_tip.y < Index_dip.y < Index_pip.y)

    # we see if the tips of the other fingers are near to the wrist 
    if ((say_shush == True) 
        and (distance_euclidienne(Wrist, Thumb_tip) < 0.3) 
        and (distance_euclidienne(Wrist, Middle_tip) < 0.22) 
        and (distance_euclidienne(Wrist, Ring_tip) < 0.22) 
        and (distance_euclidienne(Wrist, Pinky_tip) < 0.22)) :
        return Gesture.say_shush
    else : 
        return None
