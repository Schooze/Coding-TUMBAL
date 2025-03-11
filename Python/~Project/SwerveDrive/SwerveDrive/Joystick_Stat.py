import pygame

# Initialize pygame and joystick subsystem
pygame.init()
pygame.joystick.init()

# Get the number of connected joysticks
joystick_count = pygame.joystick.get_count()

# Print the number of connected controllers
print(f"Controllers: {joystick_count}")

# Loop through each connected joystick to display its details
for i in range(joystick_count):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()

    # Get battery level, controller type, and number of axes
    battery_level = joystick.get_power_level() if hasattr(joystick, 'get_power_level') else "N/A"  # Not all controllers have this
    controller_type = joystick.get_name()
    num_axes = joystick.get_numaxes()

    # Print each joystick's details to the terminal
    print(f"Controller {i+1}: {controller_type}")
    print(f"Battery Level: {battery_level}")
    print(f"Number of Axes: {num_axes}")
    print()  # Blank line for readability

# Quit pygame
pygame.quit()
