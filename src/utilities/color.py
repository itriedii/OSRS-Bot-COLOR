from typing import List, Union

import cv2
import numpy as np


class Color:
    def __init__(self, lower: List[int], upper: List[int] = None):
        """
        Defines a color or range of colors. This class converts RGB colors to BGR to satisfy OpenCV's color format.
        Args:
            lower: The lower bound of the color range [R, G, B].
            upper: The upper bound of the color range [R, G, B]. Exclude this arg if you're defining a solid color.
        """
        self.lower = np.array(lower[::-1])
        self.upper = np.array(upper[::-1]) if upper else np.array(lower[::-1])


def isolate_colors(image: cv2.Mat, colors: Union[Color, List[Color]]) -> cv2.Mat:
    """
    Isolates ranges of colors within an image and saves a new resulting image.
    Args:
        image: The image to process.
        colors: A Color or list of Colors.
    Returns:
        The image with the isolated colors (all shown as white).
    """
    if not isinstance(colors, list):
        colors = [colors]
    # Generate masks for each color
    masks = [cv2.inRange(image, color.lower, color.upper) for color in colors]
    # Create black mask
    h, w = image.shape[:2]
    mask = np.zeros([h, w, 1], dtype=np.uint8)
    # Combine masks
    for mask_ in masks:
        mask = cv2.bitwise_or(mask, mask_)
    return mask


"""Solid colors"""
BLACK = Color([0, 0, 0])
BLUE = Color([0, 0, 255])
CYAN = Color([0, 255, 255])
GREEN = Color([0, 255, 0])
ORANGE = Color([255, 144, 64])
PINK = Color([255, 0, 231])
PURPLE = Color([170, 0, 255])
RED = Color([255, 0, 0])
WHITE = Color([255, 255, 255])
YELLOW = Color([255, 255, 0])
DARK_YELLOW = Color([149, 146, 15])
DARKER_YELLOW = Color([112, 110, 17])
DARK_BLUE = Color([20, 95, 94])
DARK_PURPLE = Color([106, 32, 110])
DARK_GREEN = Color([18, 234, 28])
DARKER_GREEN = Color([0, 95, 0])
DARK_ORANGE = Color([255, 120, 24])
LIGHT_RED = Color([242, 125, 98])
LIGHT_PURPLE  = Color([74, 133, 245])
LIGHT_BROWN = Color([166, 116, 80])
LIGHT_CYAN = Color([0, 183, 255])
TEXT_RED = Color([239,16,32])
DODGY_NECKLACE_RED = Color([255, 255, 1])
TEXT_GREEN = Color([6, 96, 12])
ANTIFIRE = Color([100, 0, 95], [150, 10, 165])
POISON = Color([94, 0, 90])
ABSORPTION_POTION = Color([0, 77, 0], [0, 115, 0])

"""Colors for use with semi-transparent text"""
OFF_CYAN = Color([0, 200, 200], [70, 255, 255])
OFF_GREEN = Color([0, 100, 0], [30, 255, 255])
OFF_ORANGE = Color([180, 100, 30], [255, 166, 103])
OFF_WHITE = Color([190, 190, 190], [255, 255, 255])
OFF_YELLOW = Color([190, 190, 0], [255, 255, 120])

"""Colors for use with minimap orb text"""
ORB_GREEN = Color([0, 255, 0], [255, 255, 0])
ORB_RED = Color([255, 0, 0], [255, 255, 0])
