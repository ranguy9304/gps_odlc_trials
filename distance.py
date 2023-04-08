import cv2
import math

# Load the image
img = cv2.imread('/home/ranguy/main/manas/datasets/480_centering/1126_13.34782_74.7922138_107.38_-0.04047403484582901_0.02487803064286709_0.2721126973628998.jpg')
img=cv2.resize(img,[500,500])
# Define the camera specifications
sensor_size = 6.17  # mm
fov = 120 # degrees
amsl=75
altitude = 107.71 - amsl# meters
# altitude=altitude*0.3048
altitude=altitude*1.7048
# Calculate the constant factor for distance conversion
distance_factor = (2 * math.tan(math.radians(fov / 2)) * altitude) / (1000 * sensor_size)

# Define the event handler function for mouse clicks
def mouse_callback(event, x, y, flags, params):
    # If left mouse button is clicked, save the point
    if event == cv2.EVENT_LBUTTONDOWN:
        # Save the point as a tuple (x, y)
        params.append((x, y))
        # Draw a circle at the clicked point
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
        # If two points have been clicked, calculate the distance and display it
        if len(params) == 2:
            # Calculate the distance between the two points using the formula
            distance = math.sqrt((params[1][0] - params[0][0])**2 + (params[1][1] - params[0][1])**2)
            # Convert distance to meters using the distance factor
            distance_m = distance * distance_factor
            # Display the distance on the image
            cv2.putText(img, f'{distance_m:.2f} m', (int((params[0][0]+params[1][0])/2), int((params[0][1]+params[1][1])/2)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # Clear the clicked points
            params.clear()

# Create a window to display the image
cv2.namedWindow('image')

# Create an empty list to store the clicked points
clicked_points = []

# Set the mouse callback function for the window
cv2.setMouseCallback('image', mouse_callback, clicked_points)

while True:
    # Display the image
    cv2.imshow('image', img)
    # Wait for a key press
    key = cv2.waitKey(1)
    # If the 'q' key is pressed, exit the loop
    if key == ord('q'):
        break

# Destroy all windows
cv2.destroyAllWindows()