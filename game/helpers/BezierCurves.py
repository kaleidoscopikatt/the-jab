import pygame
import random
import math

#If you want I can use CamelCase
#Yes this is AI generated I cannot be bothered to learn Bézier curves

def quadratic_bezier(p0, p1, p2, t):
    """
    Calculate a point on a quadratic Bézier curve.

    Args:
        p0: Start point (x, y)
        p1: Control point (x, y)
        p2: End point (x, y)
        t: Progress along curve (0.0 to 1.0)

    Returns:
        Tuple (x, y) representing the point on the curve
    """
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
    return (x, y)


def cubic_bezier(p0, p1, p2, p3, t):
    """
    Calculate a point on a cubic Bézier curve.

    Args:
        p0: Start point (x, y)
        p1: First control point (x, y)
        p2: Second control point (x, y)
        p3: End point (x, y)
        t: Progress along curve (0.0 to 1.0)

    Returns:
        Tuple (x, y) representing the point on the curve
    """
    x = ((1 - t) ** 3 * p0[0] +
         3 * (1 - t) ** 2 * t * p1[0] +
         3 * (1 - t) * t ** 2 * p2[0] +
         t ** 3 * p3[0])

    y = ((1 - t) ** 3 * p0[1] +
         3 * (1 - t) ** 2 * t * p1[1] +
         3 * (1 - t) * t ** 2 * p2[1] +
         t ** 3 * p3[1])

    return (x, y)


def generate_arc_curve(start_pos, direction='random', height_range=(60, 120),
                       spread_range=(40, 80), end_offset_range=(20, 50)):
    """
    Generate control points for an arc-shaped Bézier curve (goes up then down).

    Args:
        start_pos: Starting position (x, y)
        direction: 'left', 'right', or 'random'
        height_range: Tuple (min, max) for how high the arc goes
        spread_range: Tuple (min, max) for horizontal distance traveled
        end_offset_range: Tuple (min, max) for end point vertical offset

    Returns:
        Tuple (p0, p1, p2) for quadratic Bézier curve
    """
    x, y = start_pos

    # Determine direction
    if direction == 'random':
        dir_multiplier = random.choice([-1, 1])
    elif direction == 'left':
        dir_multiplier = -1
    else:  # right
        dir_multiplier = 1

    # Generate control points
    p0 = (x, y)
    p1 = (x + dir_multiplier * random.uniform(spread_range[0] // 2, spread_range[0]),
          y - random.uniform(*height_range))
    p2 = (x + dir_multiplier * random.uniform(*spread_range),
          y + random.uniform(*end_offset_range))

    return (p0, p1, p2)


def generate_wave_curve(start_pos, direction='random', amplitude_range=(30, 60),
                        wavelength_range=(80, 150)):
    """
    Generate control points for a wave-shaped cubic Bézier curve.

    Args:
        start_pos: Starting position (x, y)
        direction: 'left', 'right', or 'random'
        amplitude_range: Tuple (min, max) for wave height
        wavelength_range: Tuple (min, max) for horizontal distance

    Returns:
        Tuple (p0, p1, p2, p3) for cubic Bézier curve
    """
    x, y = start_pos

    if direction == 'random':
        dir_multiplier = random.choice([-1, 1])
    elif direction == 'left':
        dir_multiplier = -1
    else:
        dir_multiplier = 1

    wavelength = random.uniform(*wavelength_range)
    amplitude = random.uniform(*amplitude_range)

    p0 = (x, y)
    p1 = (x + dir_multiplier * wavelength * 0.33, y - amplitude)
    p2 = (x + dir_multiplier * wavelength * 0.66, y - amplitude)
    p3 = (x + dir_multiplier * wavelength, y)

    return (p0, p1, p2, p3)