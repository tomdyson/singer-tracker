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

## Details

This project is structured into the following key files:

### `person_tracking.py`
The main script that orchestrates the application. It:
- Initializes the camera and face detector
- Processes the camera feed
- Handles user interactions (face selection, quitting)
- Calculates microphone angles based on face positions

### `camera.py`
Contains the `Camera` class, which encapsulates all camera-related functionality:
- Connecting to a camera
- Capturing frames
- Releasing the camera connection
- Listing available cameras

### `face_detector.py`
Houses the `FaceDetector` class, responsible for:
- Loading the Haar Cascade Classifier
- Detecting faces in a given frame

### `config.py`
Stores configuration parameters for the application, including:
- Stage dimensions (width and depth)
- Microphone settings (distance and field of view)
- Camera index (if a specific camera should be used)

### `.pre-commit-config.yaml`
Configuration file for pre-commit hooks, specifying:
- Ruff for linting and formatting Python code
- A check for large files being added to the repository

### `requirements.txt`
Lists all Python package dependencies required to run the project.

## Notes

- Face detection accuracy may vary depending on lighting conditions and face angles.
- Ensure your camera has a clear view of the stage for best results.
- The script assumes the camera's field of view matches the stage dimensions. Adjustments may be needed for different setups.

## Development

This project uses pre-commit hooks to maintain code quality and consistency. The pre-commit configuration includes:

- Ruff for linting and formatting Python code
- A check for large files being added to the repository

Before committing changes, make sure to:

1. Install pre-commit if you haven't already:
   ```
   pip install pre-commit
   ```

2. Set up the pre-commit hooks:
   ```
   pre-commit install
   ```

3. When you commit changes, pre-commit will automatically run the hooks. If there are any issues:
   - Ruff will attempt to fix formatting and linting issues automatically.
   - If Ruff makes changes, stage these changes and commit again.
   - For issues Ruff can't fix automatically, you'll need to resolve them manually before committing.

You can also run the pre-commit hooks manually on all files:
```
pre-commit run --all-files
```

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
