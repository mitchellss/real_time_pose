from constants.constants import *


def bp2p_x(value: float) -> float:
    """BlazePose to Pixel X

    Args:
        value (float): BlazePose coordinate

    Returns:
        float: Pixel X coordinate
    """
    return value*PIXEL_SCALE+PIXEL_X_OFFSET

def bp2p_y(value: float) -> float:
    """BlazePose to Pixel Y

    Args:
        value (float): BlazePose coordinate

    Returns:
        float: Pixel Y coordinate
    """
    return value*PIXEL_SCALE+PIXEL_Y_OFFSET

def p2bp_x(value: float) -> float:
    """Pixel to BlazePose X

    Args:
        value (float): Pixel coordinate

    Returns:
        float: BlazePose X coordinate
    """
    return (value-PIXEL_X_OFFSET)/PIXEL_SCALE

def p2bp_y(value: float) -> float:
    """Pixel to BlazePose Y

    Args:
        value (float): Pixel coordinate

    Returns:
        float: BlazePose Y coordinate
    """
    return (value-PIXEL_Y_OFFSET)/PIXEL_SCALE
