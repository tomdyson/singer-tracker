import math

import cv2

from camera import Camera
from config import (
    CAMERA_INDEX,
    DUMMY_MIC,
    FRAME_SKIP,
    MIC_DISTANCE,
    MIC_FOV,
    ROI_SCALE,
    STAGE_DEPTH,
    STAGE_WIDTH,
)
from face_detector import FaceDetector
from microphone_motor import DummyMicrophoneMotor, MicrophoneMotor

selected_face_id = None
mic_motor = None


def select_face(event, x, y, flags, param):
    global selected_face_id
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, (fx, fy, fw, fh) in enumerate(param):
            if fx < x < fx + fw and fy < y < fy + fh:
                selected_face_id = i
                break


def calculate_mic_angle(frame_width, frame_height, face_x, face_y):
    stage_x = (face_x / frame_width - 0.5) * STAGE_WIDTH
    stage_y = (1 - face_y / frame_height) * STAGE_DEPTH
    angle = math.degrees(math.atan2(stage_x, MIC_DISTANCE + stage_y))
    clamped_angle = max(min(angle, MIC_FOV / 2), -MIC_FOV / 2)
    return clamped_angle


def get_roi(frame, face):
    frame_height, frame_width = frame.shape[:2]
    x, y, w, h = face
    roi_size = int(max(w, h) * ROI_SCALE)
    roi_x = max(0, x + w // 2 - roi_size // 2)
    roi_y = max(0, y + h // 2 - roi_size // 2)
    roi_w = min(roi_size, frame_width - roi_x)
    roi_h = min(roi_size, frame_height - roi_y)
    return (roi_x, roi_y, roi_w, roi_h)


def process_camera_feed(camera, face_detector):
    global selected_face_id, mic_motor
    cv2.namedWindow("Face Detection and Tracking")
    cv2.setMouseCallback("Face Detection and Tracking", select_face)

    frame_count = 0
    last_faces = []
    roi = None

    while True:
        frame = camera.get_frame()
        frame_count += 1
        frame_height, frame_width = frame.shape[:2]

        if frame_count % FRAME_SKIP == 0:
            if selected_face_id is not None and roi:
                # Perform face detection only in ROI
                roi_x, roi_y, roi_w, roi_h = roi
                roi_frame = frame[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]
                roi_faces = face_detector.detect_faces(roi_frame)

                if len(roi_faces) > 0:  # Check if any faces were detected in ROI
                    # Adjust face coordinates to full frame
                    x, y, w, h = roi_faces[0]
                    adjusted_face = (x + roi_x, y + roi_y, w, h)
                    last_faces = [adjusted_face]
                    roi = get_roi(frame, adjusted_face)
                else:
                    # If face not found in ROI, search in full frame
                    faces = face_detector.detect_faces(frame)
                    last_faces = faces
                    if selected_face_id < len(faces):
                        roi = get_roi(frame, faces[selected_face_id])
                    else:
                        selected_face_id = None
                        roi = None
            else:
                # Perform face detection on full frame
                faces = face_detector.detect_faces(frame)
                last_faces = faces
                if selected_face_id is not None and selected_face_id < len(faces):
                    roi = get_roi(frame, faces[selected_face_id])

        for i, (x, y, w, h) in enumerate(last_faces):
            color = (0, 0, 255) if i == selected_face_id else (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            label = f"Face {i}"
            if i == selected_face_id:
                label += " (Selected)"
                face_center_x = x + w / 2
                face_center_y = y + h / 2
                mic_angle = calculate_mic_angle(
                    frame_width, frame_height, face_center_x, face_center_y
                )
                label += f" Angle: {mic_angle:.2f}°"

                if frame_count % FRAME_SKIP == 0:
                    if mic_motor.move_to_angle(mic_angle):
                        label += " (Mic Moved)"
                    else:
                        label += " (Mic Move Failed)"

            cv2.putText(
                frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
            )

        # Draw ROI if it exists
        if roi:
            roi_x, roi_y, roi_w, roi_h = roi
            cv2.rectangle(
                frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (255, 0, 0), 2
            )

        cv2.setMouseCallback(
            "Face Detection and Tracking", select_face, param=last_faces
        )
        cv2.imshow("Face Detection and Tracking", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("r"):
            selected_face_id = None
            roi = None

    cv2.destroyAllWindows()


def main():
    global mic_motor

    if CAMERA_INDEX is not None:
        print(f"Using camera index {CAMERA_INDEX} from config.")
        camera = Camera(CAMERA_INDEX)
    else:
        available_cameras = Camera.list_available_cameras()
        if not available_cameras:
            print("No cameras found.")
            return

        print("Available cameras:")
        for i, camera_index in enumerate(available_cameras):
            print(f"{i}: Camera {camera_index}")

        selection = input("Select a camera by entering its number: ")
        try:
            camera_index = available_cameras[int(selection)]
            camera = Camera(camera_index)
        except (ValueError, IndexError):
            print(
                "Invalid selection. Please run the script again and enter a valid number."
            )
            return

    face_detector = FaceDetector()

    if DUMMY_MIC:
        print("Using DummyMicrophoneMotor")
        mic_motor = DummyMicrophoneMotor()
    else:
        print("Using real MicrophoneMotor")
        mic_motor = MicrophoneMotor()

    try:
        camera.connect()
        process_camera_feed(camera, face_detector)
    finally:
        camera.release()
        mic_motor.close()  # Close the connection to the motor controller


if __name__ == "__main__":
    main()
