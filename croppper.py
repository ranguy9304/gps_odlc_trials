import cv2
import webbrowser
import os.path
from geographiclib.geodesic import Geodesic
import math
sensor_size = 6.17  # mm
fov = 123 # degrees
amsl=75
altitude = 115.99 - amsl# meters
# altitude=altitude*0.3048
altitude=altitude*1.7048
# Calculate the constant factor for distance conversion
distance_factor = (2 * math.tan(math.radians(fov / 2)) * altitude) / (1000 * sensor_size)

def get_gps_coords(center_lat, center_lon, altitude, pitch, yaw, x_offset, y_offset,img):
    # Convert altitude from meters to kilometers
    altitude_km = altitude / 1000

    # Convert pitch and yaw from degrees to radians
    pitch_rad = math.radians(pitch)
    yaw_rad = math.radians(yaw)

    # Calculate the distance from the center of the image to the specified area

    # Calculate the bearing from the center of the image to the specified area
   
    # If two points have been clicked, calculate the distance and display it
 
    # Calculate the distance between the two points using the formula
    distance = math.sqrt((x_offset)**2 + (y_offset)**2)
    # Convert distance to meters using the distance factor
    distance_m = distance * distance_factor
    # Display the distance on the image
    
  
    bearing = math.atan2(y_offset, x_offset) +yaw_rad+3*math.pi/2

    # Calculate the geodesic from the center of the image to the specified area
    geod = Geodesic.WGS84.Direct(center_lat, center_lon, bearing*180/math.pi, distance_m)
    # draw circle on the center and the point which is at offset distance

    
    print("draw circle")
    



    # Calculate the new latitude and longitude based on the center of the image, distance, bearing, and altitude
    # lat2, lon2, _ = Geodesic.WGS84.Direct(geod['lat2'], geod['lon2'], yaw_rad, pitch_rad, altitude_km)

    # Return the new latitude and longitude
    return geod['lat2'], geod['lon2'],distance_m
# Define the path to the image file

filename = '/home/ranguy/main/manas/image_pipeline/odcl_web_app/client/build/rocket_images/5_13.3479189_74.792213_115.96_-0.05842120945453644_-0.0025123488157987595_0.33536413311958313.jpg'

# Define the path to the image metadata file
name=filename.split('/')[-1]
metadata_filename = name.split('_')[1:]
metadata_filename[-1]=metadata_filename[-1].split('.')[0]

# Read the image metadata
# print(metadata_filename)

# Extract the metadata values
center_lat = float(metadata_filename[0])
center_lon = float(metadata_filename[1])
altitude = float(metadata_filename[2])
roll = float(metadata_filename[3])
pitch = float(metadata_filename[4])
yaw = float(metadata_filename[5])

# Define the image file path
image_path = filename

# Load the image
img = cv2.imread(image_path)
# print(img)

img=cv2.resize(img,[500,500])

# # Display the image
# cv2.imshow('image', img)

# # Wait for the user to select a point
# print('Select a point on the image and press any key...')
# x, y = cv2.waitKey(0) & 0xff, cv2.waitKey(0) & 0xff

# # Calculate the coordinates of the selected point
# x_offset = x - img.shape[1] / 2
# y_offset = img.shape[0] / 2 - y
# lat, lon = get_gps_coords(center_lat, center_lon, altitude, pitch, yaw, x_offset, y_offset)

# # Open Google Maps with the selected point's coordinates
# url = f'https://www.google.com/maps/place/{lat},{lon}'
# webbrowser.open_new(url)



center_x=(img.shape[1] / 2 )-30
center_y=(img.shape[0] / 2 )+125

print(img.shape[1])
# Define the callback function for mouse clicks
def mouse_callback(event, x, y, flags, param):
    img=param
    if event == cv2.EVENT_LBUTTONDOWN:
        # Calculate the coordinates of the selected point
        x_offset = x - center_x
        y_offset = y-center_y 
        lat, lon ,dist= get_gps_coords(center_lat, center_lon, altitude, pitch, yaw, x_offset, y_offset,img)
        cv2.circle(img, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)
        cv2.circle(img, (x, y), 5, (0, 0, 255), -1)

        cv2.putText(img, f'{dist:.2f} m', (int(((center_x)+x)/2), int((((center_y)+y)/2))),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Open Google Maps with the selected point's coordinates
        url = f'https://www.google.com/maps/place/{lat},{lon}'
        url2 = f'https://www.google.com/maps/place/{center_lat},{center_lon}'
        webbrowser.open_new(url)
        webbrowser.open_new(url2)
        cv2.imshow('image', img)

# Load the image
# img = cv2.imread('image.jpg')
width=6.27
height=8.33
factor=500/100
xt=43  +width/2
yt=37 +height/2
xFinal = xt - 50 + width / 2;
yFinal = -1 * (yt - 50 + height / 2);
# Display the image and set the mouse callback
cv2.circle(img, (int(xt*factor) ,int(yt*factor) ), 10, (255, 0, 0), -1)
cv2.imshow('image', img)
cv2.setMouseCallback('image', mouse_callback,param=img)

# Wait for the user to select a point
print('Select a point on the image and press any key...')
cv2.waitKey(0)

# Close the window
cv2.destroyAllWindows()


