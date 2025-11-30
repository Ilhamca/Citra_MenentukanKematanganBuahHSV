

def change_brightness(image, brightness_factor):
    """
    Adjust the brightness of an image.

    Parameters:
    - image: Input image in RGB format as a NumPy array.
    - brightness_factor: A float value where 1.0 means no change,
                         less than 1.0 darkens the image,
                         and greater than 1.0 brightens the image.

    Returns:
    - Brightness adjusted image as a NumPy array.
    """
    import cv2
    import numpy as np

    # Convert to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # Scale the V channel
    hsv_image[:, :, 2] = np.clip(hsv_image[:, :, 2] * brightness_factor, 0, 255)

    # Convert back to RGB color space
    brightened_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2RGB)

    return brightened_image