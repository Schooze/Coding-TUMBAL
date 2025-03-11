import math
import os
import pygame
from screeninfo import get_monitors

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
            if vx == 0 and vy == 0 and omega == 0:
                module_speed = 0
                module_angle = module.angle  # Maintain the last known angle
            else:
                module_speed = math.sqrt((vx - omega * module.y) ** 2 + (vy + omega * module.x) ** 2)
                module_angle = math.atan2(vy + omega * module.x, vx - omega * module.y)
            module.set_state(module_speed, module_angle)

# Get the monitor size
monitor = get_monitors()[0]
screen_width = monitor.width // 2
screen_height = monitor.height // 2

# Define the field dimensions in meters
field_width_m = 15
field_height_m = 9

# Define the robot size in meters
robot_width_m = 0.8
robot_height_m = 0.8

# Boundary buffer in meters (this value can be adjusted to control the boundary distance)
boundary_buffer_m = 0.07  # 7 cm buffer (you can change this value)

# Calculate the scale factor to convert meters to pixels
scale_x = screen_width / field_width_m
scale_y = screen_height / field_height_m

# Swerve Drive Pos In The Box
swerveBox = 2.7

# Define the positions of the swerve modules relative to the robot's center (in meters)
front_left = SwerveModule(robot_width_m / swerveBox, robot_height_m / swerveBox)
front_right = SwerveModule(robot_width_m / swerveBox, -robot_height_m / swerveBox)
back_left = SwerveModule(-robot_width_m / swerveBox, -robot_height_m / swerveBox)
back_right = SwerveModule(-robot_width_m / swerveBox, robot_height_m / swerveBox)

# Create the kinematics object
kinematics = SwerveDriveKinematics([front_left, front_right, back_left, back_right])

# Initialize Pygame
pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)  # Position the window at the top-left corner
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)  # Set the window size to 1/4 of the screen and make it resizable
pygame.display.set_caption("Swerve Drive Simulation")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 18)  # Smaller font size

# Load the background image
background_image = pygame.image.load(r"C:\Users\dara\Documents\Coding\Python\~Project\SwerveDrive\SwerveDrive\BackgroundAltiumSw.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Robot position and orientation
robot_angle = 0
robot_x, robot_y = screen_width // 2, screen_height // 2

# Initial velocities
vx, vy, omega = 0, 0, 0

# Movement toggle
movement_mode = 0  # 0: Translate in place, 1: Free roam

# Speed adjustment factors
translation_speed_factor = 0.05  # Adjust this value to change the translation speed
rotation_speed_factor = 0.1  # Adjust this value to change the rotation speed

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            background_image = pygame.transform.scale(background_image, (event.w, event.h))
            scale_x = event.w / field_width_m
            scale_y = event.h / field_height_m
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                movement_mode = (movement_mode + 1) % 2
                if movement_mode == 0:
                    robot_x, robot_y = screen_width // 2, screen_height // 2

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    # Get the state of the joysticks
    pygame.event.pump()  # Update the joystick state
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # Left Joystick (translation: vx and vy)
    left_x_axis = joystick.get_axis(0)  # Left stick - Horizontal axis (vx)
    left_y_axis = joystick.get_axis(2)  # Left stick - Vertical axis (vy)

    # Right Joystick (omega / rotation)
    right_x_axis = joystick.get_axis(3)  # Right stick - Horizontal axis (omega)
    right_y_axis = joystick.get_axis(4)  # Right stick - Vertical axis (Unused, for simplicity)

    # Map the left joystick to vx and vy
    vx = left_x_axis  # Control side-to-side motion (left-right)
    vy = left_y_axis  # Control forward/backward motion (up-down), invert the Y-axis for proper control

    # Map the right joystick to omega (rotation)
    omega = right_x_axis * 0.5  # Adjust the scaling factor for angular speed (rotation speed)

    # Calculate the swerve module states
    kinematics.to_swerve_module_states(vx, vy, omega)

    # Update robot orientation
    robot_angle += omega

    # Update robot position based on movement mode
    if movement_mode == 1:  # Free roam
        robot_x += vx * scale_x
        robot_y += vy * scale_y

    # Get the current screen size
    screen_width, screen_height = screen.get_size()

    # Calculate the bounding box of the robot after rotation
    robot_radius_x = robot_width_m * scale_x / 2
    robot_radius_y = robot_height_m * scale_y / 2

    # Robot corners (relative to the center)
    corners = [
        (robot_x + robot_radius_x * math.cos(robot_angle) - robot_radius_y * math.sin(robot_angle),
         robot_y + robot_radius_x * math.sin(robot_angle) + robot_radius_y * math.cos(robot_angle)),  # front-right
        (robot_x - robot_radius_x * math.cos(robot_angle) - robot_radius_y * math.sin(robot_angle),
         robot_y - robot_radius_x * math.sin(robot_angle) + robot_radius_y * math.cos(robot_angle)),  # back-right
        (robot_x - robot_radius_x * math.cos(robot_angle) + robot_radius_y * math.sin(robot_angle),
         robot_y - robot_radius_x * math.sin(robot_angle) - robot_radius_y * math.cos(robot_angle)),  # back-left
        (robot_x + robot_radius_x * math.cos(robot_angle) + robot_radius_y * math.sin(robot_angle),
         robot_y + robot_radius_x * math.sin(robot_angle) - robot_radius_y * math.cos(robot_angle))   # front-left
    ]

    # Get the min and max x and y coordinates of the corners to determine the bounding box
    min_x = min(corner[0] for corner in corners)
    max_x = max(corner[0] for corner in corners)
    min_y = min(corner[1] for corner in corners)
    max_y = max(corner[1] for corner in corners)

    # Apply boundary checks for the bounding box with the adjustable boundary buffer
    if min_x < boundary_buffer_m * scale_x:  # Left boundary
        robot_x += boundary_buffer_m * scale_x - min_x
    if max_x > screen_width - boundary_buffer_m * scale_x:  # Right boundary
        robot_x -= max_x - (screen_width - boundary_buffer_m * scale_x)
    if min_y < boundary_buffer_m * scale_y:  # Top boundary
        robot_y += boundary_buffer_m * scale_y - min_y
    if max_y > screen_height - boundary_buffer_m * scale_y:  # Bottom boundary
        robot_y -= max_y - (screen_height - boundary_buffer_m * scale_y)

    # Calculate the line length from robot center to the center of the screen
    line_end_x = screen_width - 100
    line_end_y = screen_height // 2
    line_length_px = math.sqrt((robot_x - line_end_x) ** 2 + (robot_y - line_end_y) ** 2)
    line_length_m = line_length_px / scale_x  # Convert to meters

    # Clear the screen and draw the background image
    screen.blit(background_image, (0, 0))

    # Draw the robot as a rotated rectangle in the center of the screen
    robot_surface = pygame.Surface((robot_width_m * scale_x, robot_height_m * scale_y), pygame.SRCALPHA)
    robot_surface.fill((0, 255, 0))
    rotated_robot = pygame.transform.rotate(robot_surface, -math.degrees(robot_angle))
    robot_rect = rotated_robot.get_rect(center=(robot_x, robot_y))
    screen.blit(rotated_robot, robot_rect.topleft)

    # Draw the swerve modules and their direction lines
    for i, module in enumerate(kinematics.modules):
        module_x = robot_x + module.x * scale_x * math.cos(robot_angle) - module.y * scale_y * math.sin(robot_angle)
        module_y = robot_y + module.x * scale_x * math.sin(robot_angle) + module.y * scale_y * math.cos(robot_angle)
        pygame.draw.circle(screen, (255, 0, 0), (int(module_x), int(module_y)), 10)
        # Adjust the line drawing to account for robot-centric rotation and world-centric translation
        if omega != 0:  
            pygame.draw.line(screen, (255, 255, 255), (module_x, module_y), 
                             (module_x + 20 * math.cos(module.angle + robot_angle), module_y + 20 * math.sin(module.angle + robot_angle)), 2)
        else:
            pygame.draw.line(screen, (255, 255, 255), (module_x, module_y), 
                             (module_x + 20 * math.cos(module.angle), module_y + 20 * math.sin(module.angle)), 2)
        # Draw the module number
        module_number = font.render(str(i + 1), True, (0, 0, 0))  # Change text color to black
        screen.blit(module_number, (module_x - 10, module_y - 30))

    # Draw the line from the center of the robot to the center of the screen
    pygame.draw.line(screen, (0, 255, 255), (robot_x, robot_y), (screen_width - 100, screen_height // 2), 2)

    # Display the movement details on the screen
    details = [
        f"Robot Position: ({robot_x:.2f}, {robot_y:.2f})",
        f"Angle: {math.degrees(robot_angle):.2f} degrees",
        f"Line Length: {line_length_m:.2f} meters"  # Add the line length to the display
    ]
    for i, module in enumerate(kinematics.modules):
        details.append(f"Module {i+1}: Speed = {module.speed:.2f} m/s, Angle = {math.degrees(module.angle):.2f} degrees")
    
    for i, detail in enumerate(details):
        text_surface = font.render(detail, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        if i < 2:
            text_rect.topleft = (10, 10 + i * 15)  # Top left
        else:
            text_rect.topleft = (10, screen_height - (len(details) - i) * 15)  # Bottom left
        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(10, 10))  # Draw background box
        screen.blit(text_surface, text_rect.topleft)

    # Update the display
    pygame.display.flip()

    # Delay for a short period
    clock.tick(30)
    os.system('cls')

pygame.quit()