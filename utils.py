"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnly/blob/master/LICENSE.md

Small utils for game logic.
"""
import random

MOD_DIR = "models/bam/"


def chance(percent):
    """Return True with percent possibility.

    Args:
        percent (int): Possibility percent.

    Returns:
        bool: Random boolean value with given possibility of True.
    """
    return random.randint(1, 100) <= percent


def address(name):
    """Return full address of the given model.

    Args:
        name (str): Model name.

    Returns:
        str: Full model file address.
    """
    return MOD_DIR + name + ".bam"
