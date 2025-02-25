import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Open Webcam
cap = cv2.VideoCapture(0)

def is_fist(landmarks):
    """Check if the hand is making a fist (all fingers curled)."""
    tips = [8, 12, 16, 20]  # Index, Middle, Ring, and Pinky Finger Tips
    for tip in tips:
        if landmarks[tip].y < landmarks[tip - 2].y:  # Finger tip should be below its joint
            return False
    return True

def is_open_hand(landmarks):
    """Check if the hand is open (all fingers extended)."""
    tips = [8, 12, 16, 20]
    for tip in tips:
        if landmarks[tip].y > landmarks[tip - 2].y:  # Finger tip should be above its joint
            return False
    return True

def is_pointing(landmarks):
    """Check if the index finger is extended while other fingers are curled."""
    return (landmarks[8].y < landmarks[6].y and  # Index finger is extended
            landmarks[12].y < landmarks[10].y and  # Other fingers are curled
            landmarks[16].y > landmarks[14].y and
            landmarks[20].y > landmarks[18].y)

def is_scissor(landmarks):

    index_extended = landmarks[8].y < landmarks[6].y  
    middle_extended = landmarks[12].y < landmarks[10].y  
    ring_curled = landmarks[16].y > landmarks[14].y or landmarks[16].y > landmarks[12].y 
    pinky_curled = landmarks[20].y > landmarks[18].y or landmarks[20].y > landmarks[16].y 
  
    fingers_close = abs(landmarks[8].x - landmarks[12].x) < 0.05 

    return index_extended and middle_extended and ring_curled and pinky_curled and fingers_close

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if cv2.waitKey(1) & 0xFF == ord('p'): 
                print("Hand Landmarks:")
                for i, lm in enumerate(hand_landmarks.landmark):
                    print(f"Joint {i}: ({lm.x}, {lm.y}, {lm.z})")

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Convert landmarks to a list
            landmarks = [lm for lm in hand_landmarks.landmark]

            # Check hand gesture
            if is_fist(landmarks):
                cv2.putText(frame, "FIST", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif is_open_hand(landmarks):
                cv2.putText(frame, "OPEN HAND", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif is_pointing(landmarks):
                cv2.putText(frame, "POINTING", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            elif is_scissor(landmarks):
                cv2.putText(frame, "SCISSOR/PEACE", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            if cv2.waitKey(1) & 0xFF == ord("s"):
                cv2.putText(frame, "ROCK, PAPER, SCISSORS", (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Hand Gesture Recognition", frame)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
