import mediapipe as mp
import cv2
import time
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_face_mesh = mp.solutions.face_mesh


# Chut gestuel


def chut(results, hands):

    # loop on the two hands

    for hand_name, hand_landmarks in hands.items():

        if hand_landmarks and results.face_landmarks:

            face = results.face_landmarks.landmark
            hand = hand_landmarks.landmark

            # required variable

            index_tip = hand[8]
            index_base = hand[5]
            wrist = hand[0]
            mouth_center_x = (face[13].x + face[14].x) / 2
            mouth_center_y = (face[13].y + face[14].y) / 2
            
            #distance for the up finger
            up_index = (index_tip.y < index_base.y < wrist.y) and (abs(index_tip.x - index_base.x) < 0.05)

            # compute the distance between two points with pythagore

            dx = index_tip.x - mouth_center_x
            dy = index_tip.y - mouth_center_y
            distance = (dx**2 + dy**2) ** 0.5

            if up_index and distance < 0.08:
                print("chut détecté")


# Just a raised index finger


def raised_finger(hands):

    # I cannot just make a code with a raised finger because it will be detected with the 'chut'
    # loop on the two hands

    for hand_name, hand_landmarks in hands.items():

        if hand_landmarks and results.face_landmarks:

            face = results.face_landmarks.landmark
            hand = hand_landmarks.landmark

            # required variable

            index_tip = hand[8]
            index_base = hand[5]
            wrist = hand[0]
            mouth_center_x = (face[13].x + face[14].x) / 2
            mouth_center_y = (face[13].y + face[14].y) / 2
            
            #distance for the up finger
            up_index = (index_tip.y < index_base.y < wrist.y) and (abs(index_tip.x - index_base.x) < 0.05)

            # compute the distance between two points with pythagore

            dx = index_tip.x - mouth_center_x
            dy = index_tip.y - mouth_center_y
            distance = (dx**2 + dy**2) ** 0.5
            # this is the only difference with the 'chut' because i need to differenciate this gestuel with just a raised finger

            if up_index and distance > 0.08:
                print("index levé detecté")


chin_initial_y = None
number_of_nod = 0
head_down = False
head_up = False
current_time = None
last_time = None

def nod_head(results):

    # the initial position for the chin and number need to be global

    global chin_initial_y
    global number_of_nod
    global head_down
    global head_up 
    global current_time
    global last_time


    if results.face_landmarks:

        # chin
        chin_center = results.face_landmarks.landmark[152]
        #if the position of the chin doesnt change we left the function
        if chin_initial_y == None:
            current_time = last_time
            chin_initial_y = chin_center.y
            return False
        
        #distance to detecte a head up
        if head_up == False and chin_center.y - chin_initial_y < -0.025 :
            print("HEAD UP")
            current_time = time.time() 
            head_up = True


        
        #distance to detect a head down
        if head_down == False and head_up == True and abs(chin_center.y - chin_initial_y) < 0.015: 
            print("HEAD DOWN")
            last_time = time.time()
            head_down = True
            head_up = False


            if current_time and last_time : 
                if last_time - current_time <= 2 :
                    number_of_nod += 1
                else : 
                    number_of_nod = 0
            
            if number_of_nod >= 1 :
                print("Oui de la tete")              
                #reset de number of nod after every nod
                head_down = False
                head_up = False
                number_of_nod = 0
                last_time = None
                current_time = None
                return True
            head_down = False
            head_up = False
        

            


       
            


cap = cv2.VideoCapture(0)
# Initiate holistic model

with mp_holistic.Holistic(
    min_detection_confidence=0.5, min_tracking_confidence=0.5
) as holistic:

    while cap.isOpened():
        ret, frame = cap.read()
        frame_for_mp = frame.copy()

        frame_display = cv2.flip(frame, 1)
        
        # Recolor Feed
        image = cv2.cvtColor(frame_display, cv2.COLOR_BGR2RGB)
        # Make Detections

        results = holistic.process(image)
        # print(results.face_landmarks)

        # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks

        # Recolor image back to BGR for rendering

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Draw face landmarks

        mp_drawing.draw_landmarks(
            image, results.face_landmarks, mp_face_mesh.FACEMESH_CONTOURS
        )

        # Right hand

        mp_drawing.draw_landmarks(
            image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS
        )

        # Left Hand

        mp_drawing.draw_landmarks(
            image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS
        )

        # Pose Detections

        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS
        )

        cv2.imshow("Raw Webcam Feed", image)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break
        # dictionary of the two hands

        hands = {
            "right": results.right_hand_landmarks,
            "left": results.left_hand_landmarks,
        }
        # call functions

        chut(results, hands)
        raised_finger(hands)
        nod_head(results)
cap.release()
cv2.destroyAllWindows()

mp_holistic.POSE_CONNECTIONS
