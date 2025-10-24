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
        for hand_landmarks in hands_detected.multi_hand_landmarks:
            drawing.draw_landmarks(
                img_rgb,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                drawing_styles.get_default_hand_landmarks_style(),
                drawing_styles.get_default_hand_connections_style(),
            )
            landmarks = hand_landmarks.landmark
            geste.go_to_detect_gesture(landmarks)
            print(i)
            i = i+1
            



    cv.imshow("Show Video", cv.flip(img_rgb, 1))

    if cv.waitKey(20) & 0xff == ord('q'):
        break

cam.release()


"""
code pour le pouce en l'air — CHATGPT

            # --- Analyse du geste ---
            landmarks = hand_landmarks.landmark

            # On récupère la hauteur (axe Y) des extrémités des doigts
            thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP].y
            thumb_ip = landmarks[mp_hands.HandLandmark.THUMB_IP].y
            index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
            ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y
            pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP].y

            # Le pouce levé : thumb_tip < thumb_ip (donc pouce vers le haut)
            # et les autres doigts sont plus bas (repliés)
            if (thumb_tip < thumb_ip and
                index_tip > landmarks[mp_hands.HandLandmark.INDEX_FINGER_MCP].y and
                middle_tip > landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y and
                ring_tip > landmarks[mp_hands.HandLandmark.RING_FINGER_MCP].y and
                pinky_tip > landmarks[mp_hands.HandLandmark.PINKY_MCP].y):
                cv.putText(img_rgb, "Pouce en l'air 👍", (50, 100),
                           cv.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 4)

"""