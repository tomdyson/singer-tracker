# Opera Camera Pointer

This project implements a person detection and tracking system using computer vision techniques. It's designed to assist in following performers on stage, potentially for automated camera or microphone positioning in opera or theatre productions.

In this demo, the application identifies two possible faces to track; the user selects one; the application creates a region of interest (ROI) around that face, and logs the angle which would be supplied to the attached microphone.

https://github.com/user-attachments/assets/f97125fb-ee19-4528-a267-7edaab8441be

## Features

- Real-time face detection using OpenCV's Haar Cascade Classifier
- Interactive face selection
- Microphone angle calculation based on the selected face's position
- Support for multiple camera inputs

## Limitations

- The angle is currently only calculated for the horizontal plane

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/tomdyson/singer-tracker.git
   cd singer-tracker
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Before running the script, you may want to adjust the following parameters in the script to match your setup:

- `STAGE_WIDTH`: Width of the stage in meters
- `STAGE_DEPTH`: Depth of the stage in meters
- `MIC_DISTANCE`: Distance from the microphone to the front center of the stage in meters
- `MIC_FOV`: Field of view of the microphone in degrees
- `CAMERA_INDEX`: Specifies which camera to use (set to None to prompt for selection)
- `DUMMY_MIC`: When True, uses a simulated microphone motor for testing
- `FRAME_SKIP`: Processes every nth frame for face detection, improving performance
- `ROI_SCALE`: Scale factor for the Region of Interest size relative to face size

You can adjust these parameters in the `config.py` file to fine-tune the application's behavior for your specific setup and performance requirements.

## Usage

Run the script:
```bash
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
- Initializes the camera, face detector, and microphone motor
- Processes the camera feed
- Handles user interactions (face selection, quitting)
- Calculates microphone angles based on face positions
- Controls the microphone motor movement

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

### `microphone_motor.py`
Contains classes for microphone motor control:
- `MicrophoneMotor`: Controls the real hardware motor
- `DummyMicrophoneMotor`: Simulates motor movement for testing

### `config.py`
Stores configuration parameters for the application, including:
- Stage dimensions (width and depth)
- Microphone settings (distance and field of view)
- Camera index (if a specific camera should be used)
- `DUMMY_MIC` flag to switch between real and dummy motor implementations
- `FRAME_SKIP` to control how often face detection is performed
- `ROI_SCALE` to determine the size of the Region of Interest for tracking

### `.pre-commit-config.yaml`
Configuration file for pre-commit hooks, specifying:
- Ruff for linting and formatting Python code
- A check for large files being added to the repository

### `requirements.txt`
Lists all Python package dependencies required to run the project, including:
- OpenCV for image processing and face detection
- PySerial for communication with the real microphone motor (when used)

## Microphone Motor Control

This project now includes support for controlling a microphone motor to track the selected face. The system can operate in two modes:

1. **Dummy Mode**: For development and testing purposes, using a simulated motor.
2. **Real Motor Mode**: For actual hardware control (requires additional setup).

### Configuration

The `config.py` file now includes a `DUMMY_MIC` flag to switch between the dummy and real motor implementations:

```python
# Microphone motor selection
DUMMY_MIC = True  # Set to False to use the real MicrophoneMotor
```

Set `DUMMY_MIC` to `True` for development and testing, and `False` when using actual hardware.

### Dummy Microphone Motor

The dummy motor implementation logs its actions to the console, allowing you to test the face tracking and angle calculation without physical hardware.

### Real Microphone Motor

To use the real microphone motor:

1. Ensure you have the necessary hardware setup.
2. Set `DUMMY_MIC = False` in `config.py`.
3. Configure the serial port and baudrate in the `MicrophoneMotor` class initialization to match your motor controller setup.
4. Adjust the command format in the `move_to_angle` method based on your specific motor controller protocol.

## Usage

The microphone motor control is integrated into the main face tracking system. When a face is selected:

1. The system calculates the required angle for the microphone.
2. It sends a command to move the microphone (either to the dummy or real motor).
3. The movement is logged (in dummy mode) or executed (in real motor mode).

No additional steps are required to use this feature; it operates automatically when a face is selected.

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
   ```bash
   pip install pre-commit
   ```

2. Set up the pre-commit hooks:
   ```bash
   pre-commit install
   ```

3. When you commit changes, pre-commit will automatically run the hooks. If there are any issues:
   - Ruff will attempt to fix formatting and linting issues automatically.
   - If Ruff makes changes, stage these changes and commit again.
   - For issues Ruff can't fix automatically, you'll need to resolve them manually before committing.

You can also run the pre-commit hooks manually on all files:
```bash
pre-commit run --all-files
```

If you're using Claude projects, you can synchronise this codebase with your project, using [ClaudeSync](https://github.com/jahwag/ClaudeSync):

```bash
claudesync api login claude.ai # Login to your Claude account
claudesync sync # Sync this codebase with your Claude project
```

## Testing

To run the tests, use the following command:

```bash
make test
```

This will run all the tests in `test_person_tracking.py`.

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
