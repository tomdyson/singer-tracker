# Opera Camera Pointer

This project implements a person detection and tracking system using computer vision techniques. It's designed to assist in following performers on stage, potentially for automated camera or microphone positioning in opera or theatre productions.

## Features

- Real-time face detection using OpenCV's Haar Cascade Classifier
- Interactive face selection
- Microphone angle calculation based on the selected face's position
- Support for multiple camera inputs

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/tomdyson/singer-tracker.git
   cd singer-tracker
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Before running the script, you may want to adjust the following parameters in the script to match your setup:

- `STAGE_WIDTH`: Width of the stage in meters
- `STAGE_DEPTH`: Depth of the stage in meters
- `MIC_DISTANCE`: Distance from the microphone to the front center of the stage in meters
- `MIC_FOV`: Field of view of the microphone in degrees

## Usage

Run the script:
```
python face_detection_mic_angle.py
```

- You will be prompted to select a camera input.
- The application window will open, showing the camera feed with detected faces outlined in green.
- Click on a face to select it for tracking. The selected face will be outlined in red.
- The calculated microphone angle for the selected face will be displayed above the face.
- Press 'r' to reset the face selection.
- Press 'q' to quit the application.

## How it Works

1. The script uses OpenCV's Haar Cascade Classifier to detect faces in each frame from the camera.
2. When a face is selected, the script calculates its position relative to the stage dimensions.
3. Using this position and the predefined microphone distance, the script calculates the angle the microphone should point to focus on the selected face.
4. The angle is clamped to stay within the microphone's field of view.

## Notes

- Face detection accuracy may vary depending on lighting conditions and face angles.
- Ensure your camera has a clear view of the stage for best results.
- The script assumes the camera's field of view matches the stage dimensions. Adjustments may be needed for different setups.

## Contributing

Contributions to improve the project are welcome. Please feel free to submit issues or pull requests.

## License

[MIT License](https://opensource.org/licenses/MIT)

## Acknowledgements

- OpenCV is used for image processing and computer vision tasks.

## Future Improvements

- Add support for multiple camera views
- Improve tracking persistence when a person is temporarily obscured
- Implement a graphical user interface for easier control
