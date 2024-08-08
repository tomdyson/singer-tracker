import cv2
import numpy as np
import pytest

from camera import Camera
from face_detector import FaceDetector
from person_tracking import calculate_mic_angle


def test_calculate_mic_angle():
    # Test center of frame
    assert calculate_mic_angle(1000, 1000, 500, 500) == pytest.approx(0, abs=1e-6)

    # Test left edge of frame
    assert calculate_mic_angle(1000, 1000, 0, 500) < 0

    # Test right edge of frame
    assert calculate_mic_angle(1000, 1000, 1000, 500) > 0


def test_camera_list_available_cameras(mocker):
    # Mock cv2.VideoCapture to simulate available cameras
    mock_capture = mocker.Mock()
    mock_capture.isOpened.return_value = True
    mock_capture.read.side_effect = [(True, None), (True, None), (False, None)]

    mocker.patch("cv2.VideoCapture", return_value=mock_capture)

    available_cameras = Camera.list_available_cameras()
    assert available_cameras == [0, 1]


def test_face_detector():
    # Create a more complex test image that simulates a face
    test_image = np.zeros((300, 300, 3), dtype=np.uint8)

    # Draw an ellipse for the face
    cv2.ellipse(test_image, (150, 150), (100, 130), 0, 0, 360, (255, 255, 255), -1)

    # Draw two circles for eyes
    cv2.circle(test_image, (110, 120), 20, (0, 0, 0), -1)
    cv2.circle(test_image, (190, 120), 20, (0, 0, 0), -1)

    # Draw a rectangle for mouth
    cv2.rectangle(test_image, (120, 200), (180, 220), (0, 0, 0), -1)

    detector = FaceDetector()
    faces = detector.detect_faces(test_image)

    assert len(faces) > 0, "Face detector should detect at least one face-like object"


# Add more tests as needed
