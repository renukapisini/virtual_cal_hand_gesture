import cv2
import mediapipe as mp
import numpy as np
import math

# Initialize Mediapipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(model_complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)
# Calculator display
equation = ""

# Button positions
buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', 'C', '=', '+'],

]


# Button size
button_w, button_h = 80, 80

# Create blank canvas for calculator UI
def draw_calculator(frame):
    # Draw display
    cv2.rectangle(frame, (50, 50), (390, 130), (200, 200, 200), -1)
    cv2.putText(frame, equation, (60, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Draw buttons
    for i in range(len(buttons)):
        for j in range(len(buttons[i])):
            x = 50 + j * (button_w + 10)
            y = 150 + i * (button_h + 10)
            cv2.rectangle(frame, (x, y), (x + button_w, y + button_h), (150, 150, 150), -1)
            cv2.putText(frame, buttons[i][j], (x + 25, y + 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    return frame

# Detect button press
def check_button_press(x, y):
    for i in range(len(buttons)):
        for j in range(len(buttons[i])):
            bx = 50 + j * (button_w + 10)
            by = 150 + i * (button_h + 10)
            if bx < x < bx + button_w and by < y < by + button_h:
                return buttons[i][j]
    return None

cap = cv2.VideoCapture(0)
prev_click_time = 0
click_delay = 0.8  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    frame = draw_calculator(frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            index_finger_tip = hand_landmarks.landmark[8]  # Index finger tip
            h, w, _ = frame.shape
            cx, cy = int(index_finger_tip.x * w), int(index_finger_tip.y * h)

            cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)

            # Check if button pressed
            current_time = cv2.getTickCount() / cv2.getTickFrequency()
            if current_time - prev_click_time > click_delay:
                pressed = check_button_press(cx, cy)
                if pressed:
                    if pressed == 'C':
                        equation = ""
                    elif pressed == '=':
                        try:
                            equation = str(eval(equation))
                        except:
                            equation = "Error"
                    else:
                        equation += pressed
                    prev_click_time = current_time

    cv2.imshow("Virtual Calculator", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
