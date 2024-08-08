import math
from typing import List, Tuple

import cv2
import numpy as np

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
# mic_motor = None


def select_face(event, x, y, flags, param):
    """
    Mouse callback function for selecting a face in the video frame.

    Args:
        event (int): The type of mouse event.
        x (int): The x-coordinate of the mouse event.
        y (int): The y-coordinate of the mouse event.
        flags (int): Any relevant flags passed by OpenCV.
        param (list): List of face coordinates (x, y, w, h) for each detected face.

    Global Variables:
        selected_face_id (int): The ID of the selected face.
    """
    global selected_face_id
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, (fx, fy, fw, fh) in enumerate(param):
            if fx < x < fx + fw and fy < y < fy + fh:
                selected_face_id = i
                break


def calculate_mic_angle(frame_width, frame_height, face_x, face_y):
    """
    Calculate the microphone angle based on the position of a face in the frame.

    Args:
        frame_width (int): Width of the video frame.
        frame_height (int): Height of the video frame.
        face_x (float): X-coordinate of the face center.
        face_y (float): Y-coordinate of the face center.

    Returns:
        float: The calculated microphone angle, clamped to the microphone's field of view.
    """
    stage_x = (face_x / frame_width - 0.5) * STAGE_WIDTH
    stage_y = (1 - face_y / frame_height) * STAGE_DEPTH
    angle = math.degrees(math.atan2(stage_x, MIC_DISTANCE + stage_y))
    clamped_angle = max(min(angle, MIC_FOV / 2), -MIC_FOV / 2)
    return clamped_angle


def get_roi(frame, face):
    """
    Calculate the Region of Interest (ROI) for a given face in the frame.

    Args:
        frame (numpy.ndarray): The video frame.
        face (tuple): Face coordinates (x, y, w, h).

    Returns:
        tuple: ROI coordinates (x, y, w, h).
    """
    frame_height, frame_width = frame.shape[:2]
    x, y, w, h = face
    roi_size = int(max(w, h) * ROI_SCALE)
    roi_x = max(0, x + w // 2 - roi_size // 2)
    roi_y = max(0, y + h // 2 - roi_size // 2)
    roi_w = min(roi_size, frame_width - roi_x)
    roi_h = min(roi_size, frame_height - roi_y)
    return (roi_x, roi_y, roi_w, roi_h)


def setup_window():
    cv2.namedWindow("Face Detection and Tracking")
    cv2.setMouseCallback("Face Detection and Tracking", select_face)


def process_roi(
    frame: np.ndarray, roi: Tuple[int, int, int, int], face_detector: FaceDetector
) -> List[Tuple[int, int, int, int]]:
    roi_x, roi_y, roi_w, roi_h = roi
    roi_frame = frame[roi_y : roi_y + roi_h, roi_x : roi_x + roi_w]
    roi_faces = face_detector.detect_faces(roi_frame)

    if len(roi_faces) > 0:
        x, y, w, h = roi_faces[0]
        return [(x + roi_x, y + roi_y, w, h)]
    return []


def process_full_frame(
    frame: np.ndarray, face_detector: FaceDetector
) -> List[Tuple[int, int, int, int]]:
    return face_detector.detect_faces(frame)


def draw_faces(
    frame: np.ndarray, faces: List[Tuple[int, int, int, int]], selected_face_id: int
):
    for i, (x, y, w, h) in enumerate(faces):
        color = (0, 0, 255) if i == selected_face_id else (0, 255, 0)
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        label = f"Face {i}"
        if i == selected_face_id:
            label += " (Selected)"
        cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def handle_selected_face(
    frame: np.ndarray,
    faces: List[Tuple[int, int, int, int]],
    selected_face_id: int,
    frame_count: int,
    mic_motor: MicrophoneMotor,
) -> Tuple[float, str]:
    x, y, w, h = faces[selected_face_id]
    face_center_x = x + w / 2
    face_center_y = y + h / 2
    frame_height, frame_width = frame.shape[:2]
    mic_angle = calculate_mic_angle(
        frame_width, frame_height, face_center_x, face_center_y
    )

    label = f" Angle: {mic_angle:.2f}°"
    if frame_count % FRAME_SKIP == 0:
        if mic_motor.move_to_angle(mic_angle):
            label += " (Mic Moved)"
        else:
            label += " (Mic Move Failed)"

    return mic_angle, label


def process_camera_feed(
    camera: Camera, face_detector: FaceDetector, mic_motor: MicrophoneMotor
):
    global selected_face_id

    setup_window()

    frame_count = 0
    last_faces = []
    roi = None

    while True:
        frame = camera.get_frame()
        frame_count += 1

        if frame_count % FRAME_SKIP == 0:
            if selected_face_id is not None and roi:
                last_faces = process_roi(frame, roi, face_detector)
                if last_faces:
                    roi = get_roi(frame, last_faces[0])
                else:
                    last_faces = process_full_frame(frame, face_detector)
                    if selected_face_id < len(last_faces):
                        roi = get_roi(frame, last_faces[selected_face_id])
                    else:
                        selected_face_id = None
                        roi = None
            else:
                last_faces = process_full_frame(frame, face_detector)
                if selected_face_id is not None and selected_face_id < len(last_faces):
                    roi = get_roi(frame, last_faces[selected_face_id])

        draw_faces(frame, last_faces, selected_face_id)

        if selected_face_id is not None and selected_face_id < len(last_faces):
            mic_angle, label = handle_selected_face(
                frame, last_faces, selected_face_id, frame_count, mic_motor
            )
            x, y, _, _ = last_faces[selected_face_id]
            cv2.putText(
                frame, label, (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2
            )

        if roi:
            roi_x, roi_y, roi_w, roi_h = roi
            cv2.rectangle(
                frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), (255, 0, 0), 2
            )

        cv2.setMouseCallback(
            "Face Detection and Tracking", select_face, param=last_faces
        )
        cv2.imshow("Face Detection and Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        elif cv2.waitKey(1) & 0xFF == ord("r"):
            selected_face_id = None
            roi = None

    cv2.destroyAllWindows()


def main():
    """
    Main function to initialize and run the face detection and microphone control system.

    This function sets up the camera, face detector, and microphone motor, then starts
    the main processing loop.
    """
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
        process_camera_feed(camera, face_detector, mic_motor)
    finally:
        camera.release()
        mic_motor.close()  # Close the connection to the motor controller


if __name__ == "__main__":
    main()
