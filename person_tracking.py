import cv2
import numpy as np


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

def load_model():
    config_file = "deploy.prototxt"
    model_file = "mobilenet_iter_73000.caffemodel"
    net = cv2.dnn.readNetFromCaffe(config_file, model_file)
    return net

def detect_persons(frame, net):
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()
    return detections

def draw_detections(frame, detections, confidence_threshold=0.2):
    height, width = frame.shape[:2]
    boxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > confidence_threshold:
            class_id = int(detections[0, 0, i, 1])
            if class_id == 15:  # Class ID 15 represents the "person" class in MobileNet-SSD
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                (startX, startY, endX, endY) = box.astype("int")
                boxes.append((startX, startY, endX, endY))
    return boxes

def select_person(event, x, y, flags, param):
    global selected_person_id
    if event == cv2.EVENT_LBUTTONDOWN:
        for i, box in enumerate(param):
            if box[0] < x < box[2] and box[1] < y < box[3]:
                selected_person_id = i
                break

def connect_to_camera(camera_index):
    global selected_person_id
    selected_person_id = None
    
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}.")
        return

    net = load_model()
    cv2.namedWindow('Person Detection and Tracking')
    cv2.setMouseCallback('Person Detection and Tracking', select_person)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Can't receive frame (stream end?). Exiting ...")
            break

        detections = detect_persons(frame, net)
        boxes = draw_detections(frame, detections)

        for i, (startX, startY, endX, endY) in enumerate(boxes):
            color = (0, 0, 255) if i == selected_person_id else (0, 255, 0)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            label = f"Person {i}"
            if i == selected_person_id:
                label += " (Selected)"
            cv2.putText(frame, label, (startX, startY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        cv2.setMouseCallback('Person Detection and Tracking', select_person, param=boxes)
        cv2.imshow('Person Detection and Tracking', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            selected_person_id = None

    cap.release()
    cv2.destroyAllWindows()

def main():
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