import math

import cv2
import numpy as np

from config import CAMERA_INDEX, MIC_DISTANCE, MIC_FOV, STAGE_DEPTH, STAGE_WIDTH


def list_available_cameras():
    index = 0
    cameras = []
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        else:
            cameras.append(index)
        cap.release()
        index += 1
    return cameras

def load_face_detector():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    return face_cascade

def detect_faces(frame, face_cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def select_face(event, x, y, flags, param):
    global selected_face_id
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, (fx, fy, fw, fh) in enumerate(param):
            if fx < x < fx + fw and fy < y < fy + fh:
                selected_face_id = i
                break

def calculate_mic_angle(frame_width, frame_height, face_x, face_y):
    # Convert frame coordinates to stage coordinates
    stage_x = (face_x / frame_width - 0.5) * STAGE_WIDTH
    stage_y = (1 - face_y / frame_height) * STAGE_DEPTH

    # Calculate angle
    angle = math.degrees(math.atan2(stage_x, MIC_DISTANCE + stage_y))

    # Ensure the angle is within the microphone's field of view
    clamped_angle = max(min(angle, MIC_FOV/2), -MIC_FOV/2)

    return clamped_angle

def connect_to_camera(camera_index):
    global selected_face_id
    selected_face_id = None
    
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}.")
        return

    face_cascade = load_face_detector()
    cv2.namedWindow('Face Detection and Tracking')
    cv2.setMouseCallback('Face Detection and Tracking', select_face)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break

        frame_height, frame_width = frame.shape[:2]
        faces = detect_faces(frame, face_cascade)

        for i, (x, y, w, h) in enumerate(faces):
            color = (0, 0, 255) if i == selected_face_id else (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            label = f"Face {i}"
            if i == selected_face_id:
                label += " (Selected)"
                # Calculate center of the face
                face_center_x = x + w / 2
                face_center_y = y + h / 2
                mic_angle = calculate_mic_angle(frame_width, frame_height, face_center_x, face_center_y)
                label += f" Angle: {mic_angle:.2f}°"
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        cv2.setMouseCallback('Face Detection and Tracking', select_face, param=faces)
        cv2.imshow('Face Detection and Tracking', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            selected_face_id = None

    cap.release()
    cv2.destroyAllWindows()

def main():
    if CAMERA_INDEX is not None:
        print(f"Using camera index {CAMERA_INDEX} from config.")
        connect_to_camera(CAMERA_INDEX)
    else:
        available_cameras = list_available_cameras()
        
        if not available_cameras:
            print("No cameras found.")
            return

        print("Available cameras:")
        for i, camera in enumerate(available_cameras):
            print(f"{i}: Camera {camera}")

        selection = input("Select a camera by entering its number: ")
        try:
            camera_index = available_cameras[int(selection)]
            connect_to_camera(camera_index)
        except (ValueError, IndexError):
            print("Invalid selection. Please run the script again and enter a valid number.")

if __name__ == "__main__":
    main()