import cv2


# Load the image (replace 'game_screen_image.jpg' with your image file path)
image = cv2.imread('image.png')
resized_image = cv2.resize(image, (15, 15))  # Adjust (800, 600) to your preferred dimensions
cv2.namedWindow('Game Screen with Scoreboard', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Game Screen with Scoreboard', 1200, 800)  # Adjust these values as needed
# Define scoreboard text and position
score_player_1 = 0  # Replace this with Player 1's actual score
score_player_2 = 0  # Replace this with Player 2's actual score

scoreboard_text_1 = f"Player 1: {score_player_1}"
scoreboard_text_2 = f"Player 2: {score_player_2}"

# Set font, scale, color, and thickness for the text
font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 6
font_color = (0, 0, 0)  # black
thickness = 10

# Get the size of the text to position it correctly
(text_width_1, text_height_1), baseline_1 = cv2.getTextSize(scoreboard_text_1, font, font_scale, thickness)
(text_width_2, text_height_2), baseline_2 = cv2.getTextSize(scoreboard_text_2, font, font_scale, thickness)

# Position the text (adjust coordinates as needed)
text_x_1 = 375  # Position for Player 1
text_y_1 = 2825   # Position for Player 1

text_x_2 = 2570  # Position for Player 2 (you can adjust this to the right, bottom, etc.)
text_y_2 = 2825  # Position for Player 2 (you can adjust this)

# Add text to the image
cv2.putText(image, scoreboard_text_1, (text_x_1, text_y_1), font, font_scale, font_color, thickness)
cv2.putText(image, scoreboard_text_2, (text_x_2, text_y_2), font, font_scale, font_color, thickness)

# Save the image with the scoreboard
cv2.imwrite('game_screen_with_scoreboard.jpg', image)

# Display the image (optional, for testing)
cv2.imshow('Game Screen with Scoreboard', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
