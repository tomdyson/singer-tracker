import cv2


class Camera:
    def __init__(self, camera_index):
        self.camera_index = camera_index
        self.cap = None

    def connect(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            raise ValueError(f"Could not open camera {self.camera_index}")

    def get_frame(self):
        if self.cap is None:
            raise ValueError("Camera is not connected. Call connect() first.")
        ret, frame = self.cap.read()
        if not ret:
            raise RuntimeError("Failed to capture frame")
        return frame

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    @staticmethod
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