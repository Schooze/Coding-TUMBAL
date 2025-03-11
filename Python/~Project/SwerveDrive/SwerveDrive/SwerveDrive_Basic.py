import math
import os
import random
import time


class SwerveModule:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0

    def set_state(self, speed, angle):
        self.speed = speed
        self.angle = angle

class SwerveDriveKinematics:
    def __init__(self, modules):
        self.modules = modules

    def to_swerve_module_states(self, vx, vy, omega):
        for module in self.modules:
            module_speed = math.sqrt((vx - omega * module.y) ** 2 + (vy + omega * module.x) ** 2)
            module_angle = math.atan2(vy + omega * module.x, vx - omega * module.y)
            module.set_state(module_speed, module_angle)

# Define the positions of the swerve modules relative to the robot's center
front_left = SwerveModule(0.381, 0.381)
front_right = SwerveModule(0.381, -0.381)
back_left = SwerveModule(-0.381, 0.381)
back_right = SwerveModule(-0.381, -0.381)

# Create the kinematics object
kinematics = SwerveDriveKinematics([front_left, front_right, back_left, back_right])

while True:
    # Example chassis speeds (vx, vy, omega)
    vx = random.random()  # Forward velocity in meters per second
    vy = random.random()  # Sideways velocity in meters per second
    omega = random.random()  # Angular velocity in radians per second

    # Calculate the swerve module states
    kinematics.to_swerve_module_states(vx, vy, omega)

    # Print the results
    for i, module in enumerate(kinematics.modules):
        print(f"Module {i+1}: Speed = {module.speed:.2f} m/s, Angle = {math.degrees(module.angle):.2f} degrees")

    time.sleep(2)
    os.system('cls')

