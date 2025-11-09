import mediapipe as mp
import cv2
mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_face_mesh = mp.solutions.face_mesh

#for the webcam
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    cv2.imshow('Raw Webcam Feed', frame)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
cap.release()
cv2.destroyAllWindows()


#Chut gestuel 
def chut(results, hands):

    #loop on the two hands
    for hand_name, hand_landmarks in hands.items() :
    
        if hand_landmarks and results.face_landmarks:
       
            face = results.face_landmarks.landmark
            hand = hand_landmarks.landmark
    
            #required variable 
            index_tip = hand[8]
            index_base = hand[5]
            mouth_center_x = (face[13].x + face[14].x) / 2
            mouth_center_y = (face[13].y + face[14].y) / 2
            
            #distance for the up finger
            up_index = index_tip.y < index_base.y

            #compute the distance between two points with pythagore
            dx = index_tip.x - mouth_center_x
            dy = index_tip.y - mouth_center_y
            distance = (dx**2 + dy**2)**0.5

            if up_index and distance < 0.08 :
                print("chut détecté")


#Just a raised index finger 
def raised_finger(hands):

    #I cannot just make a code with a raised finger because it will be detected with the 'chut' 
   #loop on the two hands
    for hand_name, hand_landmarks in hands.items() :
    
        if hand_landmarks and results.face_landmarks:
       
            face = results.face_landmarks.landmark
            hand = hand_landmarks.landmark
    
            #required variable 
            index_tip = hand[8]
            index_base = hand[5]
            mouth_center_x = (face[13].x + face[14].x) / 2
            mouth_center_y = (face[13].y + face[14].y) / 2
            
            #distance for the up finger
            up_index = index_tip.y < index_base.y

            #compute the distance between two points with pythagore
            dx = index_tip.x - mouth_center_x
            dy = index_tip.y - mouth_center_y
            distance = (dx**2 + dy**2)**0.5
            #this is the only difference with the 'chut' because i need to differenciate this gestuel with just a raised finger
            if up_index and distance > 0.08 :
                print("index levé detecté")

chin_initial_y = None
number_of_nod = 0
def nod_head(results):
    
    #the initial position for the chin and number need to be global
    global chin_initial_y
    global number_of_nod


    if results.face_landmarks :
            
        #chin
        chin_center = results.face_landmarks.landmark[152]
        #forehead
        forehead_center = results.face_landmarks.landmark[10]
        #if the position of the chin doesnt change we left the function
        if chin_initial_y == None:
            chin_initial_y = chin_center.y
            return False
        #if there is a certain number of nod then we have the nodding
        if chin_center.y - chin_initial_y > 0.02 :
            number_of_nod += 1
            if number_of_nod >= 4 :
            
                print("Oui de la tete")
                #reset de number of nod after every nod
                number_of_nod = 0
                return True
            







#for the hand, face and body detection
cap = cv2.VideoCapture(0)
# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Make Detections
        results = holistic.process(image)
        # print(results.face_landmarks)
        
        # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
        
        # Recolor image back to BGR for rendering
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Draw face landmarks
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_face_mesh.FACEMESH_CONTOURS)
        
        # Right hand
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # Left Hand
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

        # Pose Detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
                        
        cv2.imshow('Raw Webcam Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

        #dictionary of the two hands 
        hands = {
                "right": results.right_hand_landmarks,
                "left": results.left_hand_landmarks
            }
        #call functions
        chut(results, hands)
        raised_finger(hands)
        nod_head(results)

cap.release()
cv2.destroyAllWindows()

mp_holistic.POSE_CONNECTIONS



#styling 
mp_drawing.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
mp_drawing.draw_landmarks

cap = cv2.VideoCapture(0)
# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Make Detections
        results = holistic.process(image)
        # print(results.face_landmarks)
        
        # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
        
        # Recolor image back to BGR for rendering
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # 1. Draw face landmarks
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_face_mesh.FACEMESH_CONTOURS, 
                                 mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                 mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                 )
        
        # 2. Right hand
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                 )

        # 3. Left Hand
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                 )

        # 4. Pose Detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                 )
                        
        cv2.imshow('Raw Webcam Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
