import time

import serial


class MicrophoneMotor:
    def __init__(self, port="/dev/ttyUSB0", baudrate=9600):
        self.serial_connection = serial.Serial(port, baudrate, timeout=1)
        self.current_angle = 0

    def move_to_angle(self, target_angle):
        # Ensure the angle is within the valid range (-45 to 45 degrees)
        target_angle = max(min(target_angle, 45), -45)

        # Calculate the number of steps to move
        steps = int(
            (target_angle - self.current_angle) * (200 / 90)
        )  # Assuming 200 steps per 90 degrees

        # Send the command to the motor controller
        command = f"MOVE {steps}\n"
        self.serial_connection.write(command.encode())

        # Wait for the movement to complete
        response = self.serial_connection.readline().decode().strip()
        if response == "OK":
            self.current_angle = target_angle
            return True
        else:
            return False

    def close(self):
        self.serial_connection.close()


class DummyMicrophoneMotor:
    def __init__(self):
        self.current_angle = 0
        print("DummyMicrophoneMotor initialized")

    def move_to_angle(self, target_angle):
        # Ensure the angle is within the valid range (-45 to 45 degrees)
        target_angle = max(min(target_angle, 45), -45)

        # Simulate movement time
        movement_time = (
            abs(target_angle - self.current_angle) * 0.1
        )  # 0.1 seconds per degree
        time.sleep(movement_time)

        print(
            f"Moving microphone from {self.current_angle:.2f}° to {target_angle:.2f}°"
        )
        self.current_angle = target_angle
        return True

    def close(self):
        print("DummyMicrophoneMotor connection closed")
