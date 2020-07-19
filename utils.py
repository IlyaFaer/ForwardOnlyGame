"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

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


def take_random(list_):
    """Take a random element from the given list.

    The chosen element will be deleted from the list.

    Args:
        list_ (list): List to take an element from.

    Returns:
        Any: The chosen element.
    """
    element = random.choice(list_)
    list_.remove(element)
    return element
