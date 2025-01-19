import cv2
import numpy as np


class Button:
    def __init__(self, image_path, position, size):
        self.image_path = image_path
        self.position = position
        self.size = size
        self.image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)  # Load image with transparency (if any)
        
        # Check if the image is loaded successfully
        if self.image is None:
            print(f"Error: The image {image_path} could not be loaded.")
            return
        
        # Resize the button to the desired size
        self.image = cv2.resize(self.image, size)

        # If the image has an alpha channel (transparency), separate the alpha channel
        if self.image.shape[2] == 4:  # RGBA image (includes alpha channel)
            self.image_rgb = self.image[:, :, :3]
            self.alpha_channel = self.image[:, :, 3]
        else:
            self.image_rgb = self.image
            self.alpha_channel = None

    def draw(self, img):
        # Ensure the button is drawn within the image bounds
        button_h, button_w, _ = self.image_rgb.shape
        x, y = self.position
        if self.alpha_channel is not None:  # If there's transparency
            # Create an ROI (Region of Interest) where the button should be placed
            roi = img[y:y+button_h, x:x+button_w]
            
            # Blend the button with the background image using the alpha channel
            for i in range(3):  # For each channel (BGR)
                roi[:, :, i] = (self.alpha_channel / 255.0) * self.image_rgb[:, :, i] + (1 - self.alpha_channel / 255.0) * roi[:, :, i]
        else:
            img[y:y+button_h, x:x+button_w] = self.image_rgb  # No transparency, just overlay the image


    def is_clicked(self, x, y):
        # Check if the button was clicked
        button_x, button_y = self.position
        if button_x <= x <= button_x + self.size[0] and button_y <= y <= button_y + self.size[1]:
            return True
        return False


def main():
    # Load the game screen image (replace 'game_screen.jpg' with your actual image file)
    image = cv2.imread('image.png')
    
    if image is None:
        print("Error: Game screen image could not be loaded.")
        return

    # Set the button position (x=100, y=200 for example)
    button_x = 50 # Horizontal distance from the left
    button_y = 50 # Vertical distance from the top
    
    # Set the button size
    button_width = 100
    button_height = 50
    
    # Create the exit button (load 'exit.png' as the button image)
    exit_button = Button('exit.png', (button_x, button_y), (button_width, button_height))
    
    # Draw the exit button on top of the game screen
    exit_button.draw(image)

    # Display the game screen with the button
    cv2.imshow('Game Screen with Exit Button', image)

    # Define a function to handle mouse click events
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Check if the exit button is clicked
            if exit_button.is_clicked(x, y):
                print("Exiting...")
                cv2.destroyAllWindows()

    # Set the mouse callback function
    cv2.setMouseCallback('Game Screen with Exit Button', mouse_callback)

    # Wait for the user to click on the exit button or close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
