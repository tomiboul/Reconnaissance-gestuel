import cv2 as cv
import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles
import geste
import GestureConfirmed
import AudioGesture

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,                # we can modify here the number of hands detected
    min_detection_confidence=0.5)

# Set the desired resolution (e.g., 1280x720)
width, height = 1280, 720

cam = cv.VideoCapture(0)
cam.set(8, width)  # Set the width
cam.set(6, height)  # Set the height

i = 0 ;
gestureConfirmedRight = GestureConfirmed.GestureConfirmed() # crée l'objet permettant de confirmer un geste
gestureConfirmedLeft = GestureConfirmed.GestureConfirmed() # crée l'objet permettant de confirmer un geste 
gestureRight = geste.Gesture.nothing
gestureLeft = geste.Gesture.nothing

while cam.isOpened():
    success, img_rgb = cam.read()
    if not success:
        print("Camera Frame not available")
        continue

    # Convert image to RGB format
    img_rgb = cv.cvtColor(img_rgb, cv.COLOR_BGR2RGB)
    hands_detected = hands.process(img_rgb)         

    # Convert image to RGB format
    img_rgb = cv.cvtColor(img_rgb, cv.COLOR_RGB2BGR)


    if hands_detected.multi_hand_landmarks:

        # separer les 2 mains
        gestures = {}
        for hand_landmarks, hand_handedness in zip(hands_detected.multi_hand_landmarks, hands_detected.multi_handedness): # attention l'idée de la fonction zip a été fournie par ChatGpt
            
            hand_label = hand_handedness.classification[0].label
            
            drawing.draw_landmarks(
                img_rgb,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                drawing_styles.get_default_hand_landmarks_style(),
                drawing_styles.get_default_hand_connections_style(),
            )
            landmarks = hand_landmarks.landmark

            if hand_label == "Right" :
                gestureRight = geste.go_to_detect_gesture(landmarks)
                gestures[hand_label] = gestureRight
                gestureConfirmedRight.listOfGesture.append(gestureRight)
                gestureRight = gestureConfirmedRight.analyseGesture()
                if len(gestureConfirmedRight.listOfGesture) > 8:
                    del gestureConfirmedRight.listOfGesture[0]

            elif hand_label == "Left" :
                gestureLeft = geste.go_to_detect_gesture(landmarks)
                gestures[hand_label] = gestureLeft
                gestureConfirmedLeft.listOfGesture.append(gestureLeft)
                gestureLeft = gestureConfirmedLeft.analyseGesture()
                if len(gestureConfirmedLeft.listOfGesture) > 8:
                    del gestureConfirmedLeft.listOfGesture[0]

            else :
                print("Problem with the detection of hands")

        if ("Left" in gestures and "Right" in gestures) : 
            if ((gestures["Left"] == geste.Gesture.horizontal_hand and gestures["Right"] == geste.Gesture.vertical_hand)
                or (gestures["Right"] == geste.Gesture.horizontal_hand and gestures["Left"] == geste.Gesture.vertical_hand)) :
                print(f"Signe stop détecté {geste.Gesture.sign_to_stop} \n ") 
                AudioGesture.startTheSong(geste.Gesture.sign_to_stop)

        if (gestureLeft != geste.Gesture.nothing 
            and gestureLeft != geste.Gesture.vertical_hand
            and gestureLeft != geste.Gesture.horizontal_hand):
            print("left succes " + str(gestureLeft))
            AudioGesture.startTheSong(gestureLeft)
            gestureLeft = geste.Gesture.nothing

        if (gestureRight != geste.Gesture.nothing
            and gestureRight != geste.Gesture.vertical_hand
            and gestureRight != geste.Gesture.horizontal_hand) :
            print("right succes " + str(gestureRight))
            AudioGesture.startTheSong(gestureRight)
            gestureRight = geste.Gesture.nothing

    # If no hands detected we add to the object gestureConfirmedLeft and 
    # gestureConfirmedRight that no gesture are deteted and remove the oldest gesture
    else :  
        gestureConfirmedLeft.listOfGesture.append(geste.Gesture.nothing)
        gestureConfirmedRight.listOfGesture.append(geste.Gesture.nothing)
        if len(gestureConfirmedRight.listOfGesture) > 8:
            del gestureConfirmedRight.listOfGesture[0]
        if len(gestureConfirmedLeft.listOfGesture) > 8:
            del gestureConfirmedLeft.listOfGesture[0]

    #print( f"{i} : {gestureConfirmedLeft.listOfGesture} and {gestureConfirmedRight.listOfGesture}" )
    print(i)
    i = i+1
            

    cv.imshow("Show Video", cv.flip(img_rgb, 1))

    if cv.waitKey(20) & 0xff == ord('q'):
        break

cam.release()

