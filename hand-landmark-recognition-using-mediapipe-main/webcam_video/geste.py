from enum import Enum
import cv2 as cv
import mediapipe.python.solutions.hands as mp_hands
from math import *
import calculation as calcul
class Gesture(Enum):
    thumbs_up = "Pouce en l'air"   # pouce en l'air
    thumbs_down = "Pouce en bas"
    say_shush = "Chut beau gosse"   # met l'index vers le haut (comme pour dire chut)
    vertical_hand = "La main verticale"
    horizontal_hand = "la main horizontal"
    peace_sign = "peace"
    thumbs_mid = "Pouce au milieu"
    ok = "Ok"
    sign_to_stop = "sign to stop"
    nothing = "Aucun gestes detectés"

    

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
        #detect_say_shush,
        detect_thumbs_up, 
        detect_thumbs_down,
        detect_peace_sign,
        detect_vertical_hand,
        detect_horizontal_hand,
        detect_ok
        #detect_thumbs_mid
    ]

    for function_detection in list_function_detection :
        gesture = function_detection(joint_from_hand)
        if gesture  != None :
            #print(gesture.value)
            return gesture
        
    return Gesture.nothing



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
        and (calcul.distance_euclidienne(Wrist, Index_tip) < 0.23) 
        and (calcul.distance_euclidienne(Wrist, Middle_tip) < 0.22) 
        and (calcul.distance_euclidienne(Wrist, Ring_tip) < 0.22) 
        and (calcul.distance_euclidienne(Wrist, Pinky_tip) < 0.22)
        and (calcul.distance_euclidienne(Wrist, Thumb_tip) > 0.3)) :
        return Gesture.thumbs_up
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
    print(f"Thumb MCP y={Thumb_mcp.y:.3f}, IP y={Thumb_ip.y:.3f}, TIP y={Thumb_tip.y:.3f}")
    if ((thumbs_down == True) 
        and (calcul.distance_euclidienne(Wrist, Index_tip) < 0.23) 
        and (calcul.distance_euclidienne(Wrist, Middle_tip) < 0.23) 
        and (calcul.distance_euclidienne(Wrist, Ring_tip) < 0.23) 
        and (calcul.distance_euclidienne(Wrist, Pinky_tip) < 0.23)
        and (calcul.distance_euclidienne(Wrist, Thumb_tip) > 0.2)) :
        print("Gesture.thumbs_down")
        return Gesture.thumbs_down
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
        and (calcul.distance_euclidienne(Wrist, Thumb_tip) < 0.3) 
        and (calcul.distance_euclidienne(Wrist, Middle_tip) < 0.22) 
        and (calcul.distance_euclidienne(Wrist, Ring_tip) < 0.22) 
        and (calcul.distance_euclidienne(Wrist, Pinky_tip) < 0.22)) :
        return Gesture.say_shush
    else : 
        return None


def detect_vertical_hand(joint_from_hand) -> Gesture :

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
    """index_up = (Index_tip.y < Index_dip.y < Index_pip.y)
    thumb_up = (Thumb_tip.y < Thumb_ip.y < Thumb_mcp.y)
    middle_finger_up = (Middle_tip.y < Middle_dip.y < Middle_pip.y)
    ring_finger_up = (Ring_tip.y < Ring_dip.y < Ring_pip.y)
    pinky_up = (Pinky_tip.y < Pinky_dip.y < Pinky_pip.y)"""

    thumb_up = (Thumb_tip.y < Thumb_ip.y < Thumb_mcp.y)
    index_up = (Index_tip.y < Index_dip.y < Index_pip.y)
    middle_finger_up = (Middle_tip.y < Middle_dip.y < Middle_pip.y)
    ring_finger_up = (Ring_tip.y < Ring_dip.y < Ring_pip.y)
    pinky_up = (Pinky_tip.y < Pinky_dip.y < Pinky_pip.y)


    if (index_up 
        and thumb_up 
        and middle_finger_up 
        and ring_finger_up 
        and pinky_up
        and (calcul.distance_euclidienne(Pinky_tip, Ring_dip) < 0.07) 
        and (calcul.distance_euclidienne(Ring_tip, Middle_tip) < 0.07) 
        and (calcul.distance_euclidienne(Middle_tip, Index_tip) < 0.07) 
        and (calcul.distance_euclidienne(Thumb_tip, Index_pip) < 0.07)) :
        return Gesture.vertical_hand
    else : 
        return None
    

    
def detect_horizontal_hand(joint_from_hand) -> Gesture :
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

    #print(f"Index_tip.y : {Index_tip.y}, Index_dip.y : {Index_dip.y}")
    #verify that all fingers are up 
    index_mid = (calcul.distanceMax(Index_tip.y, Index_dip.y, 5)  and  calcul.distanceMax(Index_dip.y, Index_pip.y, 5))
    thumb_mid = (calcul.distanceMax(Thumb_tip.y, Thumb_ip.y, 5)  and  calcul.distanceMax(Thumb_ip.y, Thumb_mcp.y, 5))
    middle_finger_mid = (calcul.distanceMax(Middle_tip.y, Middle_dip.y, 5)  and  calcul.distanceMax(Middle_dip.y, Middle_pip.y, 5))
    ring_finger_mid = (calcul.distanceMax(Ring_tip.y, Ring_dip.y, 5)  and  calcul.distanceMax(Ring_dip.y, Ring_pip.y, 5))
    pinky_mid = (calcul.distanceMax(Pinky_tip.y, Pinky_dip.y, 5)  and  calcul.distanceMax(Pinky_dip.y, Pinky_pip.y, 5))

    if (index_mid 
        and thumb_mid 
        and middle_finger_mid 
        and ring_finger_mid 
        and pinky_mid) :
        return Gesture.horizontal_hand
    else : 
        return None
    """and (calcul.distance_euclidienne(Pinky_tip, Ring_dip) < 0.07) 
        and (calcul.distance_euclidienne(Ring_tip, Middle_tip) < 0.07) 
        and (calcul.distance_euclidienne(Middle_tip, Index_tip) < 0.07) 
        and (calcul.distance_euclidienne(Thumb_tip, Index_pip) < 0.07)"""





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
        and (calcul.distance_euclidienne(Wrist, Index_tip) < 0.23) 
        and (calcul.distance_euclidienne(Wrist, Middle_tip) < 0.22) 
        and (calcul.distance_euclidienne(Wrist, Ring_tip) < 0.22) 
        and (calcul.distance_euclidienne(Wrist, Pinky_tip) < 0.22)
        and (calcul.distance_euclidienne(Wrist, Thumb_tip) > 0.2)) :
        return Gesture.thumbs_mid
    else : 
        return None


def detect_ok(joint_from_hand) -> Gesture :
    """
    Take the set of hand landmarks, take four joints from the hand and detect or not an "Ok" sign

    PARAMETERS
    ——————————
    joint_from_hand : set of hand landmark

    RETURN
    ——————
    return the ok_sign gesture or nothing
    """
    
    Pinky_tip = joint_from_hand[mp_hands.HandLandmark.PINKY_TIP]
    Pinky_dip = joint_from_hand[mp_hands.HandLandmark.PINKY_DIP]
    Pinky_pip = joint_from_hand[mp_hands.HandLandmark.PINKY_PIP]
    Pinky_mcp = joint_from_hand[mp_hands.HandLandmark.PINKY_MCP]

    Ring_tip = joint_from_hand[mp_hands.HandLandmark.RING_FINGER_TIP]
    Ring_dip = joint_from_hand[mp_hands.HandLandmark.RING_FINGER_DIP]
    Ring_pip = joint_from_hand[mp_hands.HandLandmark.RING_FINGER_PIP]
    Ring_mcp = joint_from_hand[mp_hands.HandLandmark.RING_FINGER_MCP]

    Middle_tip = joint_from_hand[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    Middle_dip = joint_from_hand[mp_hands.HandLandmark.MIDDLE_FINGER_DIP]
    Middle_pip = joint_from_hand[mp_hands.HandLandmark.MIDDLE_FINGER_PIP]
    Middle_mcp = joint_from_hand[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

    Index_tip = joint_from_hand[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    Index_dip = joint_from_hand[mp_hands.HandLandmark.INDEX_FINGER_DIP]
    Index_pip = joint_from_hand[mp_hands.HandLandmark.INDEX_FINGER_PIP]
    Index_mcp = joint_from_hand[mp_hands.HandLandmark.INDEX_FINGER_MCP]

    Thumb_tip = joint_from_hand[mp_hands.HandLandmark.THUMB_TIP]
    Thumb_ip = joint_from_hand[mp_hands.HandLandmark.THUMB_IP]
    Thumb_mcp = joint_from_hand[mp_hands.HandLandmark.THUMB_MCP]

    Wrist = joint_from_hand[mp_hands.HandLandmark.WRIST] #paume de la main

    # Wrist has to be lower than all other joints
    # -> lower than all mcp's and all tips 

    # # Calculate distance with each mcp (+ thumb_ip)
    # wrist_to_thumb_ip = calcul.distance_euclidienne(Wrist, Thumb_ip)
    # wrist_to_index_mcp = calcul.distance_euclidienne(Wrist, Index_mcp)
    # wrist_to_middle_mcp = calcul.distance_euclidienne(Wrist, Middle_mcp)
    # wrist_to_ring_mcp = calcul.distance_euclidienne(Wrist, Ring_mcp)
    # wrist_to_pinky_mcp = calcul.distance_euclidienne(Wrist, Pinky_mcp)

    # # Calculate distance with each tip
    # wrist_to_thumb_tip = calcul.distance_euclidienne(Wrist, Thumb_tip)
    # wrist_to_index_tip = calcul.distance_euclidienne(Wrist, Index_tip)
    # wrist_to_middle_tip = calcul.distance_euclidienne(Wrist, Middle_tip)
    # wrist_to_ring_tip = calcul.distance_euclidienne(Wrist, Ring_tip)
    # wrist_to_pinky_tip = calcul.distance_euclidienne(Wrist, Pinky_tip)

    # Check if wrist is below all MCP and TIP landmarks
    wrist_at_lowest = all(
        Wrist.y < joint.y for joint in [
            Thumb_mcp, Index_mcp, Middle_mcp, Ring_mcp, Pinky_mcp,
            Thumb_tip, Index_tip, Middle_tip, Ring_tip, Pinky_tip
        ]
    )
        
    # Calculate distance between thumb tip and index tip
    thumb_index_tips_distance = calcul.distance_euclidienne(Thumb_tip, Index_tip)

    # Middle and Ring tips must be higher than Index pip
    index_pip_y = Index_pip.y
    middle_tip_y = Middle_tip.y
    ring_tip_y = Ring_tip.y

    if middle_tip_y < index_pip_y or ring_tip_y < index_pip_y:
        print("Middle or Ring finger below Index Pip (for OK gesture)")
        return None

    if not wrist_at_lowest :
        print("Wrist is not at the lowest point (for OK gesture)")
        return None

    if thumb_index_tips_distance < 0.2:
        return Gesture.ok
    else:
        return None