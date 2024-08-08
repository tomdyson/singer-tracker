# Opera Camera Pointer

This project implements a person detection and tracking system using computer vision techniques. It's designed to assist in following performers on stage, potentially for automated camera or microphone positioning in opera or theater productions.

## Features

- Detects multiple persons in a video stream
- Allows user to select a specific person to track
- Highlights the selected person with a different color bounding box
- Supports multiple camera inputs

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher
- OpenCV with contrib modules
- A webcam or other camera connected to your computer

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/opera-camera-pointer.git
   cd opera-camera-pointer
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Download the model files from https://github.com/chuanqi305/MobileNet-SSD/tree/master:
   - `deploy.prototxt`
   - `mobilenet_iter_73000.caffemodel`

   Place these files in the project root directory.

## Usage

To run the application:

1. Ensure your camera is connected.
2. Run the script:
   ```
   python person_tracking.py
   ```
3. Select a camera when prompted.
4. The application window will open, showing the camera feed with detected persons in green bounding boxes.
5. Click on a person to select them for tracking. The selected person will be highlighted with a red bounding box.
6. Press 'r' to reset the selection.
7. Press 'q' to quit the application.

## File Descriptions

- `person_tracking.py`: The main Python script containing the person detection and tracking logic.
- `requirements.txt`: Lists all the Python dependencies for this project.
- `deploy.prototxt`: The model architecture file for the MobileNet-SSD neural network.
- `mobilenet_iter_73000.caffemodel`: The pre-trained weights for the MobileNet-SSD model.

## Contributing

Contributions to this project are welcome. Please fork the repository and create a pull request with your changes.

## License

[MIT License](https://opensource.org/licenses/MIT)

## Acknowledgements

- This project uses the MobileNet-SSD model for person detection.
- OpenCV is used for image processing and computer vision tasks.

## Future Improvements

- Implement angle calculation for motor control
- Add support for multiple camera views
- Improve tracking persistence when a person is temporarily obscured
- Implement a graphical user interface for easier control
