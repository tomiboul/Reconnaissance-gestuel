import mediapipe as mp
import cv2
import time
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_face_mesh = mp.solutions.face_mesh


chin_initial_y = None
chin_initial_x = None
number_of_nod = 0
head_down = False
head_up = False
head_right = False
head_left = False
current_time = None
last_time = None
number_of_shake = 0

def nod_head(results):
    """
    Function to detect a nod (yes)
    -----
    PARAMETERS
    -----
    results : element from Mediapipe that contains the landmarks
    ------
    RETURN
    ------
    bool : True if a nod is detected false otherwise

    """

    # global variable

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
                if last_time - current_time <= 1 :
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
        

            


def head_shake(results):
    """
    Function to detect a head shake (no)
    -----
    PARAMETERS
    -----
    results : element from Mediapipe that contains the landmarks
    ------
    RETURN
    ------
    bool : True if a head shake is detected false otherwise

    """

    # global variable

    global chin_initial_x
    global number_of_shake
    global head_right
    global head_left 
    global current_time
    global last_time

    if results.face_landmarks:

        # chin
        chin_center = results.face_landmarks.landmark[152]
        #if the position of the chin doesnt change we left the function
        if chin_initial_x == None:
            current_time = last_time
            chin_initial_x = chin_center.x
            return False
        
        #distance to detecte a head right
        if head_right == False and chin_center.x - chin_initial_x > 0.02:
            print("HEAD RIGHT")
            current_time = time.time() 
            head_right = True

         #distance to detect a head down
        if head_right and head_left == False and chin_initial_x - chin_center.x  > 0.02:
            print("HEAD left")
            last_time = time.time()
            head_left = True

            if current_time and last_time : 
                if last_time - current_time <= 1 :
                    number_of_shake += 1
                else : 
                    number_of_shake = 0
            
            if number_of_shake >= 1 :
                print("Non de la tete")              
                head_right = False
                head_left = False          
                #reset the number of shake after every shake
                number_of_shake = 0
                last_time = None
                current_time = None
                return True
            head_right = False
            head_left = False


       
            


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
        head_shake(results)
        nod_head(results)
cap.release()
cv2.destroyAllWindows()

mp_holistic.POSE_CONNECTIONS
