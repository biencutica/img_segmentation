import cv2 as cv
import sys

image = cv.imread("C:/Users/Bianca/Desktop/practica/honda.jpg")
if image is None:
    sys.exit("Image could not be read.")

imgray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
imgray = cv.blur(imgray, (10, 10))

ret, thresh = cv.threshold(imgray, 127, 255, cv.THRESH_BINARY)
contours, hierarchy = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)  # SIMPLE saves only the 4 corners

cnt1 = contours[21]
x1, y1, w1, h1 = cv.boundingRect(cnt1)
cv.rectangle(image, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 2)
cnt2 = contours[24]
x2, y2, w2, h2 = cv.boundingRect(cnt2)
cv.rectangle(image, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 2)

intersection_x1 = max(x1, x2)
intersection_y1 = max(y1, y2)
intersection_x2 = min(x1 + w1, x2 + w2)
intersection_y2 = min(y1 + h1, y2 + h2)

intersection_width = intersection_x2 - intersection_x1
intersection_height = intersection_y2 - intersection_y1

if intersection_width <= 0 or intersection_height <= 0:
    print("Values do not intersect.")

intersection_area = intersection_width * intersection_height

cnt1_area = w1*h1
cnt2_area = w2*h2

union_area = cnt1_area + cnt2_area - intersection_area

iou = intersection_area / union_area
print(iou)

# for contour in contours:
# Get the bounding box coordinates for each contour
# x, y, w, h = cv.boundingRect(contour)

# Draw the bounding box
# cv.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv.imshow("Binary", image)

cv.waitKey(0)
cv.destroyAllWindows()
