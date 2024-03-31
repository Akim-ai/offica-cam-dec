import cv2


def resize(image, x1, x2, y1, y2):
    roi = image[y1:y2, x1:x2]
    bbox_width = x2 - x1
    bbox_height = y2 - y1

    # Aspect ratio of the bounding box
    aspect_ratio = bbox_width / bbox_height

    max_width = 640
    max_height = 640

    # Calculate the desired_width and desired_height while maintaining the aspect ratio
    if aspect_ratio >= 1:
        # Width is greater than height
        desired_width = min(max_width, bbox_width)
        desired_height = int(desired_width / aspect_ratio)
    else:
        # Height is greater than width
        desired_height = min(max_height, bbox_height)
        desired_width = int(desired_height * aspect_ratio)
    return cv2.resize(roi, (desired_width, desired_height))