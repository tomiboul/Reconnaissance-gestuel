from enum import Enum
import cv2 as cv
import mediapipe.python.solutions.hands as mp_hands
from math import *

class Gesture(Enum):
    thumbs_up = "Pouce en l'air"   # pouce en l'air
    thumbs_down = "Pouce en bas"
    say_shush = "Chut beau gosse"   # met l'index vers le haut (comme pour dire chut)
    vertical_hand = "La main verticale"
    horizontal_hand = "la main horizontal"
    peace_sign = "peace"
    thumbs_mid = "Pouce au milieu"

    nothing = "Aucun gestes detectés"

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
        detect_thumbs_up, 
        detect_vertical_right_hand,
        detect_thumbs_down,
        detect_peace_sign,
        detect_thumbs_mid
    ]

    for function_detection in list_function_detection :
        gesture = function_detection(joint_from_hand)
        if gesture  != None :
            print(gesture.value)
            return gesture



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
    Wrist = joint_from_hand[mp_hands.HandLandmark.WRIST] # le poignet de la main

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
        and (distance_euclidienne(Wrist, Pinky_tip) < 0.22)
        and (distance_euclidienne(Wrist, Thumb_tip) > 0.3)) :
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
    Wrist = joint_from_hand[mp_hands.HandLandmark.WRIST] #poignet de la main
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


def detect_vertical_right_hand(joint_from_hand) -> Gesture :

    Wrist = joint_from_hand[mp_hands.HandLandmark.WRIST] #paume de la main

    Index_tip = joint_from_hand[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    Index_dip = joint_from_hand[mp_hands.HandLandmark.INDEX_FINGER_DIP]
    Index_pip = joint_from_hand[mp_hands.HandLandmark.INDEX_FINGER_PIP]

    Thumb_tip = joint_from_hand[mp_hands.HandLandmark.THUMB_TIP]
    Thumb_ip = joint_from_hand[mp_hands.HandLandmark.THUMB_IP]
    Thumb_mcp = joint_from_hand[mp_hands.HandLandmark.THUMB_MCP]

    Middle_tip = joint_from_hand[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    Middle_dip = joint_from_hand[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
    Middle_pip = joint_from_hand[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]

    Ring_tip = joint_from_hand[mp_hands.HandLandmark.RING_FINGER_TIP]
    Ring_dip = joint_from_hand[mp_hands.HandLandmark.RING_FINGER_DIP]
    Ring_pip = joint_from_hand[mp_hands.HandLandmark.RING_FINGER_PIP]

    Pinky_tip = joint_from_hand[mp_hands.HandLandmark.PINKY_TIP]
    Pinky_dip = joint_from_hand[mp_hands.HandLandmark.PINKY_DIP]
    Pinky_pip = joint_from_hand[mp_hands.HandLandmark.PINKY_PIP]

    #verify that all fingers are up 
    index_up = (Index_tip.y < Index_dip.y < Index_pip.y)
    thumb_up = (Index_tip.y < Thumb_ip.y < Thumb_mcp.y)
    middle_finger_up = (Index_tip.y < Middle_dip.y < Middle_pip.y)
    ring_finger_up = (Index_tip.y < Ring_dip.y < Ring_pip.y)
    pinky_up = (Index_tip.y < Pinky_dip.y < Pinky_pip.y)

    if (index_up 
        and thumb_up 
        and middle_finger_up 
        and ring_finger_up 
        and pinky_up
        and (distance_euclidienne(Pinky_tip, Ring_dip) < 0.07) 
        and (distance_euclidienne(Ring_tip, Middle_tip) < 0.07) 
        and (distance_euclidienne(Middle_tip, Index_tip) < 0.07) 
        and (distance_euclidienne(Thumb_tip, Index_pip) < 0.07)) :
        return Gesture.vertical_hand
    else : 
        return None
    


def detect_thumbs_down(joint_from_hand) -> Gesture :
    """
    Take the set of hand landmarks, take four joints from the hand and detect or not a thumbs_down

    PARAMETERS
    ——————————
    joint_from_hand : set of hand landmark

    RETURN
    ——————
    return the thumbs_down gesture or nothing
    """
    Wrist = joint_from_hand[mp_hands.HandLandmark.WRIST] 
    Thumb_mcp = joint_from_hand[mp_hands.HandLandmark.THUMB_MCP]
    Thumb_ip = joint_from_hand[mp_hands.HandLandmark.THUMB_IP]
    Thumb_tip = joint_from_hand[mp_hands.HandLandmark.THUMB_TIP]

    Index_tip = joint_from_hand[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    Middle_tip = joint_from_hand[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    Ring_tip = joint_from_hand[mp_hands.HandLandmark.RING_FINGER_TIP]
    Pinky_tip = joint_from_hand[mp_hands.HandLandmark.PINKY_TIP]

    thumbs_down = (Thumb_mcp.y < Thumb_ip.y < Thumb_tip.y )

    if ((thumbs_down == True) 
        and (distance_euclidienne(Wrist, Index_tip) < 0.23) 
        and (distance_euclidienne(Wrist, Middle_tip) < 0.22) 
        and (distance_euclidienne(Wrist, Ring_tip) < 0.22) 
        and (distance_euclidienne(Wrist, Pinky_tip) < 0.22)
        and (distance_euclidienne(Wrist, Thumb_tip) > 0.2)) :
        return Gesture.thumbs_down
    else : 
        return None



def detect_peace_sign(joint_from_hand) -> Gesture :
    """
    Take the set of hand landmarks, take four joints from the hand and detect or not a peace sign

    PARAMETERS
    ——————————
    joint_from_hand : set of hand landmark

    RETURN
    ——————
    return the peace_sign gesture or nothing
    """
    Wrist = joint_from_hand[mp_hands.HandLandmark.WRIST] 

    Index_tip = joint_from_hand[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    Index_dip = joint_from_hand[mp_hands.HandLandmark.INDEX_FINGER_DIP]
    Index_pip = joint_from_hand[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    Middle_tip = joint_from_hand[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    Middle_dip = joint_from_hand[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
    Middle_pip = joint_from_hand[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    Ring_tip = joint_from_hand[mp_hands.HandLandmark.RING_FINGER_TIP]
    Ring_dip = joint_from_hand[mp_hands.HandLandmark.RING_FINGER_DIP]
    Ring_pip = joint_from_hand[mp_hands.HandLandmark.RING_FINGER_PIP]
    Pinky_tip = joint_from_hand[mp_hands.HandLandmark.PINKY_TIP]
    Pinky_dip = joint_from_hand[mp_hands.HandLandmark.PINKY_DIP]
    Pinky_pip = joint_from_hand[mp_hands.HandLandmark.PINKY_PIP]

    index_finger = (Index_tip.y < Index_dip.y < Index_pip.y )
    middle_finger = (Middle_tip.y < Middle_dip.y < Middle_pip.y )
    ring_finger = (Ring_tip.y > Ring_dip.y > Ring_pip.y )
    pinky_finger = (Pinky_tip.y > Pinky_dip.y > Pinky_pip.y )

    if ((index_finger == True) 
        and (middle_finger == True)
        and (ring_finger == True) 
        and (pinky_finger == True)
        ) :
        return Gesture.peace_sign
    else : 
        return None


def detect_thumbs_mid(joint_from_hand) -> Gesture :
    """
    Take the set of hand landmarks, take four joints from the hand and detect or not a mid thumbs

    PARAMETERS
    ——————————
    joint_from_hand : set of hand landmark

    RETURN
    ——————
    return the thumbs_mid gesture or nothing
    """
    Wrist = joint_from_hand[mp_hands.HandLandmark.WRIST] 
    Thumb_mcp = joint_from_hand[mp_hands.HandLandmark.THUMB_MCP]
    Thumb_ip = joint_from_hand[mp_hands.HandLandmark.THUMB_IP]
    Thumb_tip = joint_from_hand[mp_hands.HandLandmark.THUMB_TIP]

    Index_tip = joint_from_hand[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    Middle_tip = joint_from_hand[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    Ring_tip = joint_from_hand[mp_hands.HandLandmark.RING_FINGER_TIP]
    Pinky_tip = joint_from_hand[mp_hands.HandLandmark.PINKY_TIP]

    thumbs_mid_right = (Thumb_mcp.x < Thumb_ip.x < Thumb_tip.x )
    thumbs_mid_left = (Thumb_mcp.x > Thumb_ip.x > Thumb_tip.x )

    if ((thumbs_mid_right == True or thumbs_mid_left == True) 
        and (distance_euclidienne(Wrist, Index_tip) < 0.23) 
        and (distance_euclidienne(Wrist, Middle_tip) < 0.22) 
        and (distance_euclidienne(Wrist, Ring_tip) < 0.22) 
        and (distance_euclidienne(Wrist, Pinky_tip) < 0.22)
        and (distance_euclidienne(Wrist, Thumb_tip) > 0.2)) :
        return Gesture.thumbs_mid
    else : 
        return None