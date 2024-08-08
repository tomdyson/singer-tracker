# Stage and microphone setup parameters
STAGE_WIDTH = 10  # meters
STAGE_DEPTH = 5  # meters
MIC_DISTANCE = 15  # meters from the front center of the stage
MIC_FOV = 90  # degrees, field of view of the microphone

# Camera selection
# Set to None to prompt for camera selection, or specify the camera index (e.g., 0, 1, 2)
CAMERA_INDEX = 0

# Microphone motor selection
DUMMY_MIC = True  # Set to False to use the real MicrophoneMotor

# Frame processing
FRAME_SKIP = (
    3  # Process every 3rd frame. Bigger values mean less frequent face detection.
)

# Region of Interest (ROI) tracking
ROI_SCALE = 1.5  # Scale factor for ROI size relative to face size. Larger values increase ROI size.
