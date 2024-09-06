import cv2 as cv
import numpy as np
import sys


def generate_contour(center, axes, num_points=50):
    a, b = axes
    angles = np.linspace(0, 2 * np.pi, num_points)  # matlab
    contour = np.array([
        (int(center[0] + a * np.cos(angle)), int(center[1] + b * np.sin(angle)))
        for angle in angles
    ])
    return contour


# TO DO
def elongate(part, center, axes, elongation_factor, part_type):
    major, minor = axes
    if part_type == 'bottom' or part_type == 'top':
        angles = np.linspace(0, 2 * np.pi, len(part))  # matlab
        new_minor = minor * elongation_factor
        modified_part = np.array([
            (int(center[0] + major * np.cos(angle)), int(center[1] + new_minor * np.sin(angle)))
            for angle in angles
        ])

    return modified_part


def draw(img, contour, color):
    for point in contour:
        cv.circle(img, tuple(point), 1, color, -1)  # just draws really, tiny filled circles
    return img


def translate(contour, displacement):
    return contour + np.array(displacement)


def scale(center, axes, scalar):
    scaled_axes = (axes[0] * scalar, axes[1] * scalar)
    return generate_contour(center, scaled_axes)


def split_ellipse(contour, center):
    top = [point for point in contour if point[1] <= center[1]]  # list filtering
    bottom = [point for point in contour if point[1] > center[1]]
    right = [point for point in contour if point[0] <= center[0]]
    left = [point for point in contour if point[0] > center[0]]
    return np.array(top), np.array(bottom), np.array(right), np.array(left)


img = cv.imread("C:\\Users\\Bianca\\Desktop\\practica\\blank_white.jpg")
if img is None:
    sys.exit("Could not read image.")

# center, axes, angle
center = (img.shape[1] // 2, img.shape[0] // 2)  # center of the image (x, y)
axes = (100, 50)  # major and minor axes
green_color = (0, 255, 0)
red_color = (0, 0, 255)
blue_color = (255, 0, 0)

# generating the vector
contour = generate_contour(center, axes)
top, bottom, left, right = split_ellipse(contour, center)

# translation
displacement = (100, 120)
translated_contour = translate(contour, displacement)

# scaling
scalar = 1.5
scaled_contour = scale(center, axes, scalar)

# partial translation - top bottom
displacement2 = (0, 50)
translated_side = translate(bottom, displacement2)
final_contour = np.vstack((top, translated_side))

# elongation
# elongation_factor = 1.5
# elongated_half = elongate()

final_img = np.copy(img)
# final_img = draw(final_img, contour, green_color)
# final_img = draw(final_img, translated_contour, blue_color)
final_img = draw(final_img, final_contour, green_color)

# display the result
cv.imshow('Ellipse', final_img)
cv.waitKey(0)
cv.destroyAllWindows()
