import cv2 as cv
import numpy as np
import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_styles as drawing_styles
from mediapipe.python.solutions import drawing_utils


def is_drawing_mode(landmarks):
    # coordinates of tips of fingers
    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    distance = np.sqrt((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2)

    return distance < 0.10


# initialize the Hands model
hands = mp_hands.Hands(
    static_image_mode=False,  # set to false for processing video frames
    max_num_hands=2,  # maximum number of hands to detect
    min_detection_confidence=0.5  # minimum confidence threshold for hand detection
)

# open the camera
cam = cv.VideoCapture(0)
drawing_mode = False
prev_x, prev_y = None, None
# create a canvas
canvas = None

while cam.isOpened():
    # read a frame from the camera
    success, frame = cam.read()
    frame = cv.flip(frame, 1)
    h, w, c = frame.shape

    # if the frame is not available, skip this iteration
    if not success:
        print("Camera Frame not available")
        continue

    if canvas is None:
        canvas = np.zeros_like(frame)

    # convert the frame from BGR to RGB
    frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

    # process the frame for hand detection and tracking
    hands_detected = hands.process(frame)

    # convert the frame back from RGB to BGR
    frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

    # if hands are detected, draw landmarks and connections on the frame
    if hands_detected.multi_hand_landmarks:
        for hand_landmarks in hands_detected.multi_hand_landmarks:
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            x = int(index_finger_tip.x * w)  # index_finger_tip range is from [0,1]
            y = int(index_finger_tip.y * h)

            drawing_mode = is_drawing_mode(hand_landmarks.landmark)

            # if drawing mode is on
            if drawing_mode:
                # make the index finger draw lines
                if prev_x is not None and prev_y is not None:
                    cv.line(canvas, (prev_x, prev_y), (x, y), (255, 255, 255), 5)
                prev_x, prev_y = x, y
            else:
                prev_x, prev_y = None, None

    combine = cv.add(frame, canvas)

    # display the frame with annotations
    cv.imshow("Webcam", combine)

    # exit the loop if 'q' key is pressed
    if cv.waitKey(20) & 0xff == ord('q'):
        break

# release the camera
cam.release()
cv.destroyAllWindows()
