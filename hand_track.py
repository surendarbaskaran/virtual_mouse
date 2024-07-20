import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.8)
mp_drawing = mp.solutions.drawing_utils

# Define screen size
screen_width, screen_height = pyautogui.size()


def main():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            break

        # Flip the frame horizontally for natural viewing
        frame = cv2.flip(frame, 1)

        
        # Convert the frame to RGB color space   .COLOR_BGR2RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame to detect hands
        result = hands.process(rgb_frame)
        
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:


                
    
                # Draw hand landmarks
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Get the landmark coordinates
                landmarks = hand_landmarks.landmark
                
                # Get coordinates of the index finger tip (landmark 8)
                x = int(landmarks[0].x * frame.shape[1])
                y = int(landmarks[0].y * frame.shape[0])
                
                # Convert frame coordinates to screen coordinates
                screen_x = np.clip(int((x / frame.shape[1]) * screen_width), 0, screen_width - 1)
                screen_y = np.clip(int((y / frame.shape[0]) * screen_height), 0, screen_height - 1)
                
                # Move the mouse to the detected position
                pyautogui.moveTo(screen_x*1, screen_y*1,duration=0.3)
                
                # Optional: Draw a circle at the index finger tip
                cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
                
                # action_trigger
                if (int((landmarks[8].x-landmarks[4].x )* frame.shape[1]))<10:
                    print("thumb pinch gesture")  #thumb pinch   
                #    pyautogui.click(button='left')  # Left click
                # elif landmarks[12].y < landmarks[11].y:  # Assuming a swipe gesture
                #     print("swipe gesture")
                #     pyautogui.click(button='right')  # Right click

                # elif landmarks[8].y > landmarks[7].y:  # Example condition for scroll
                #     pyautogui.scroll(10)  # Scroll up
                # elif landmarks[8].y < landmarks[7].y:
                #     print("condition for scroll down")
                #     pyautogui.scroll(-10)  # Scroll down
                # print("thumb  :",(int(landmarks[4].x * frame.shape[1]), int(landmarks[4].y * frame.shape[0])), "index  : ",(int(landmarks[8].x * frame.shape[1]), int(landmarks[8].y * frame.shape[0])),"diff : ",(int(landmarks[8].x * frame.shape[1]))-int(landmarks[4].x * frame.shape[1]))

                #for landmark in landmarks:
                # for i in range(21):
                #     cv2.circle(frame, (int(landmarks[i].x * frame.shape[1]), int(landmarks[i].y * frame.shape[0])), 10, (0, 255, 0), -1)

        # Display the frame
        cv2.imshow('Hand Sign Detection', frame)
        
        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
