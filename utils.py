"""Small utils for game logic."""
import random


def chance(percent):
    """Return True with percent possibility.

    Args:
        percent (int): Possibility percent.

    Returns:
        bool: Random boolean value with given possibility of True.
    """
    return random.randint(1, 100) <= percent
