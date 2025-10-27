import cv2 as cv
import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles
import geste

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

while cam.isOpened():
    success, img_rgb = cam.read()
    if not success:
        print("Camera Frame not available")
        continue

    # Convert image to RGB format
    img_rgb = cv.cvtColor(img_rgb, cv.COLOR_BGR2RGB)
    hands_detected = hands.process(img_rgb)         # the result

    # Convert image to RGB format
    img_rgb = cv.cvtColor(img_rgb, cv.COLOR_RGB2BGR)


    if hands_detected.multi_hand_landmarks:

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
                gestures[hand_label] =geste.go_to_detect_gesture(landmarks)
            elif hand_label == "Left" :
                gestures[hand_label] = geste.go_to_detect_gesture(landmarks)
            else :
                print("Problem with the detection of hands")

        if ("Left" in gestures and "Right" in gestures) : 
            if ((gestures["Left"] == geste.Gesture.horizontal_hand and gestures["Right"] == geste.Gesture.vertical_hand)
                or (gestures["Right"] == geste.Gesture.horizontal_hand and gestures["Left"] == geste.Gesture.vertical_hand)) :
                print("Signe stop détecté \n ") 
                
        print(i)
        i = i+1

    """
    if hands_detected.multi_hand_landmarks:
        for hand_landmarks in hands_detected.multi_hand_landmarks:
            drawing.draw_landmarks(
                img_rgb,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                drawing_styles.get_default_hand_landmarks_style(),
                drawing_styles.get_default_hand_connections_style(),
            )
            landmarks = hand_landmarks.landmark
            gestureSend = geste.go_to_detect_gesture(landmarks)

            print(i)
            i = i+1"""
            



    cv.imshow("Show Video", cv.flip(img_rgb, 1))

    if cv.waitKey(20) & 0xff == ord('q'):
        break

cam.release()

