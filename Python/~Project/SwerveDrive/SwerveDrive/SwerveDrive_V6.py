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


class Obstacle:
    def __init__(self, x, y, shape, size):
        self.x = x
        self.y = y
        self.shape = shape
        self.size = size

    def draw(self, screen):
        if self.shape == "circle":
            pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.size)
        elif self.shape == "box":
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2))

    def collides_with_robot(self, robot_x, robot_y, robot_radius_x, robot_radius_y):
        if self.shape == "circle":
            distance = math.sqrt((robot_x - self.x) ** 2 + (robot_y - self.y) ** 2)
            return distance < self.size + max(robot_radius_x, robot_radius_y)
        elif self.shape == "box":
            return (
                robot_x + robot_radius_x > self.x - self.size and
                robot_x - robot_radius_x < self.x + self.size and
                robot_y + robot_radius_y > self.y - self.size and
                robot_y - robot_radius_y < self.y + self.size
            )

# Define obstacles
obstacles = [
    Obstacle(300, 200, "circle", 50),
    Obstacle(600, 400, "box", 40)
]

# Pathfinding function with obstacle avoidance
def find_trajectory(robot_x, robot_y, target_x, target_y, obstacles, scale_x, scale_y):
    trajectory = [(robot_x, robot_y)]
    current_x, current_y = robot_x, robot_y

    while math.sqrt((current_x - target_x) ** 2 + (current_y - target_y) ** 2) > 10:
        dx = target_x - current_x
        dy = target_y - current_y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        step_x = (dx / distance) * 10
        step_y = (dy / distance) * 10

        next_x = current_x + step_x
        next_y = current_y + step_y

        # Check for collisions with obstacles
        collision = False
        for obstacle in obstacles:
            if obstacle.collides_with_robot(next_x, next_y, robot_width_m * scale_x / 2, robot_height_m * scale_y / 2):
                collision = True
                break

        if collision:
            # Simple avoidance by adjusting direction slightly
            step_x, step_y = step_y, -step_x
            next_x = current_x + step_x
            next_y = current_y + step_y

        current_x, current_y = next_x, next_y
        trajectory.append((current_x, current_y))

    return trajectory

# Initial trajectory
trajectory = []
trajectory_index = 0


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
background_image = pygame.image.load(r"C:\Users\eatmi\OneDrive\Documents\Projek_bandha\ROBOCON_2025\SwerveDrive\BackgroundAltiumSw.png")
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Robot position and orientation
robot_angle = 0
robot_x, robot_y = screen_width // 2, screen_height // 2

# Initial velocities
vx, vy, omega = 0, 0, 0

# Movement toggle
movement_mode = 0  # 0: Translate in place, 1: Free roam

# Speed adjustment factors
translation_speed_factor = 0.1  # Adjust this value to change the translation speed
rotation_speed_factor = 0.1  # Adjust this value to change the rotation speed

# Ga ngulang
a = 0

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Set target position and calculate trajectory
            target_x, target_y = pygame.mouse.get_pos()
            trajectory = find_trajectory(robot_x, robot_y, target_x, target_y, obstacles, scale_x, scale_y)
            trajectory_index = 0
            if a == 0:
                a = 1
            

    # Get the state of all keyboard keys
    keys = pygame.key.get_pressed()

    # Update velocities based on key presses
    if (a != 1):
        vx = 0
        vy = 0
        omega = 0
    if keys[pygame.K_w]:
        vy = -1 * translation_speed_factor  # Move forward
    if keys[pygame.K_s]:
        vy = 1 * translation_speed_factor  # Move backward
    if keys[pygame.K_a]:
        vx = -1 * translation_speed_factor  # Move left
    if keys[pygame.K_d]:
        vx = 1 * translation_speed_factor  # Move right
    if keys[pygame.K_q]:
        omega = -1 * rotation_speed_factor  # Rotate counterclockwise
    if keys[pygame.K_e]:
        omega = 1 * rotation_speed_factor  # Rotate clockwise

    # Follow trajectory if available
    if trajectory and trajectory_index < len(trajectory):
        target_x, target_y = trajectory[trajectory_index]
        dx = target_x - robot_x
        dy = target_y - robot_y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > 5:
            vx = (dx / distance) * translation_speed_factor
            vy = (dy / distance) * translation_speed_factor
        else:
            trajectory_index += 1

    # Check if trajectory has been completed
    if trajectory_index >= len(trajectory):
        # Trajectory completed, stop or perform end action
        vx = 0
        vy = 0
        print("Trajectory completed.")
        # Optional: You can perform any other action here after trajectory completion.

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

    # Draw obstacles
    for obstacle in obstacles:
        obstacle.draw(screen)

    # Draw the trajectory
    if trajectory:
        for i in range(1, len(trajectory)):
            pygame.draw.line(screen, (0, 255, 0), (trajectory[i - 1][0] * scale_x, trajectory[i - 1][1] * scale_y),
                             (trajectory[i][0] * scale_x, trajectory[i][1] * scale_y), 3)

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
    clock.tick(60)
    os.system('cls')

pygame.quit()