import math
import os
import random
import time
import pygame

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

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Swerve Drive Simulation")
clock = pygame.time.Clock()

# Robot position and orientation
robot_x, robot_y = 400, 300
robot_angle = 0

# Initial velocities
vx, vy, omega = 0, 0, 0

# Store the last known angles of the swerve modules
last_angles = [0, 0, 0, 0]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    # Update velocities based on key presses
    vx = 0
    vy = 0
    omega = 0
    if keys[pygame.K_w]:
        vy = -1  # Move forward
    if keys[pygame.K_s]:
        vy = 1  # Move backward
    if keys[pygame.K_a]:
        vx = -1  # Move left
    if keys[pygame.K_d]:
        vx = 1  # Move right
    if keys[pygame.K_q]:
        omega = -0.1  # Rotate counterclockwise
    if keys[pygame.K_e]:
        omega = 0.1  # Rotate clockwise

    # Calculate the swerve module states
    kinematics.to_swerve_module_states(vx, vy, omega)

    # Update robot orientation
    robot_angle += omega

    # Print the movement details to the terminal
    print(f"Robot Position: ({robot_x:.2f}, {robot_y:.2f}), Angle: {math.degrees(robot_angle):.2f} degrees")
    for i, module in enumerate(kinematics.modules):
        if vx == 0 and vy == 0 and omega == 0:
            module.angle = last_angles[i]
        else:
            last_angles[i] = module.angle
        module.speed = round(module.speed, 2)  # Round the speed to avoid floating-point precision errors
        print(f"Module {i+1}: Speed = {module.speed:.2f} m/s, Angle = {math.degrees(module.angle):.2f} degrees")

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the robot as a rotated rectangle in the center of the screen
    robot_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
    robot_surface.fill((0, 255, 0))
    rotated_robot = pygame.transform.rotate(robot_surface, -math.degrees(robot_angle))
    robot_rect = rotated_robot.get_rect(center=(400, 300))
    screen.blit(rotated_robot, robot_rect.topleft)

    # Draw the swerve modules
    for module in kinematics.modules:
        module_x = 400 + module.x * 100 * math.cos(robot_angle) - module.y * 100 * math.sin(robot_angle)
        module_y = 300 + module.x * 100 * math.sin(robot_angle) + module.y * 100 * math.cos(robot_angle)
        pygame.draw.circle(screen, (255, 0, 0), (int(module_x), int(module_y)), 10)
        # Adjust the line drawing to account for robot-centric rotation and world-centric translation
        if omega != 0:
            pygame.draw.line(screen, (255, 255, 255), (module_x, module_y), 
                             (module_x + 20 * math.cos(module.angle + robot_angle), module_y + 20 * math.sin(module.angle + robot_angle)), 2)
        else:
            pygame.draw.line(screen, (255, 255, 255), (module_x, module_y), 
                             (module_x + 20 * math.cos(module.angle), module_y + 20 * math.sin(module.angle)), 2)

    # Update the display
    pygame.display.flip()

    # Delay for a short period
    clock.tick(30)
    os.system('cls')

pygame.quit()
