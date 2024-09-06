import sys
import cv2
import numpy as np

img = cv2.imread('C:\\Users\\Bianca\\Desktop\\red-lilies.jpg', cv2.IMREAD_COLOR)
# check if image is loaded correctly
if img is None:
    sys.exit("Could not read image.")

brightness = 30  # [0-100]
contrast = 1.4  # [1.0-3.0]

modified_img = cv2.addWeighted(img, contrast, np.zeros(img.shape, img.dtype), 0, brightness)

cv2.imwrite('modified_img.jpg', modified_img)

cv2.imshow("Image", img)
cv2.imshow("New Image", modified_img)
k = cv2.waitKey(0)

# image is written to file if s is pressed
if k == ord("s"):
    cv2.imwrite("red-lilies.jpg", img)

# remove GUI window from screen and memory
cv2.destroyAllWindows()


