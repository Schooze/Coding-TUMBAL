import pygame
import time
import os

# Initialize pygame
pygame.init()

# Check for connected joysticks
if pygame.joystick.get_count() == 0:
    print("No joystick detected.")
    pygame.quit()
    exit()

# Initialize the joystick (assuming it's the first one)
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick initialized: {joystick.get_name()}")

# Run the program and check for events
try:
    running = True
    while running:
        pygame.event.pump()  # Update the joystick state
        
        # Left joystick (typically axes 0 and 1)
        left_x_axis = joystick.get_axis(0)  # Left stick - Horizontal axis
        left_y_axis = joystick.get_axis(2)  # Left stick - Vertical axis
        
        # Right joystick (typically axes 2 and 3)
        right_x_axis = joystick.get_axis(3)  # Right stick - Horizontal axis
        right_y_axis = joystick.get_axis(4)  # Right stick - Vertical axis
        
        # Get button states for both joysticks (e.g., button 0 and button 1 for testing)
        button_1 = joystick.get_button(0)  # Button 1 (typically 'A' on Xbox controllers)
        button_2 = joystick.get_button(1)  # Button 2 (typically 'B')
        
        # Print out the status of the joysticks and buttons
        print(f"\nLeft Joystick - X Axis: {left_x_axis:.2f}, Y Axis: {left_y_axis:.2f}")
        print(f"Right Joystick - X Axis: {right_x_axis:.2f}, Y Axis: {right_y_axis:.2f}")
        print(f"Button 1 (A): {'Pressed' if button_1 else 'Released'}")
        print(f"Button 2 (B): {'Pressed' if button_2 else 'Released'}")
        
        # Wait for a short time to avoid spamming the console too much
        time.sleep(0.01)
        os.system('cls')

except KeyboardInterrupt:
    print("\nProgram exited.")
finally:
    pygame.quit()
