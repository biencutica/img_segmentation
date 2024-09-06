import cv2 as cv
import sys
import numpy as np

img = cv.imread("C:\\Users\\Bianca\\Desktop\\practica\\blank_white.jpg")
# check if image is loaded correctly
if img is None:
    sys.exit("Could not read image.")

# example of translating
# ball = img[280:340, 330:390]
# img[273:333, 100:160] = ball

# drawing the shape on the image
height, width, channels = img.shape
center = (width//2, height//2)
radius = 50
color = (0, 255, 0)
thickness = 3
cv.circle(img, center, radius, color, thickness)

# create bounding box
top_left = (center[0] - radius, center[1] - radius)  # (x, y) coordinates
bottom_right = (center[0] + radius, center[1] + radius)

# Extract the circular region from the image
circle_region = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

# Create a mask for the circular region
mask_size = (2 * radius, 2 * radius)
mask = np.zeros(mask_size, dtype=np.uint8)
cv.circle(mask, (radius, radius), radius, 255, thickness=-1)  # White circle on black background

# Resize the mask to match the size of the circle_region
mask_resized = cv.resize(mask, (circle_region.shape[1], circle_region.shape[0]))

# Apply the mask to the circular region
contour = cv.bitwise_and(circle_region, circle_region, mask_resized)

displacement = (100, 50)

# Display the results
cv.imshow("Circle Mask", mask)
cv.imshow("Circular Region", contour)
cv.imshow("Image with Circle", img)

cv.waitKey(0)
cv.destroyAllWindows()






