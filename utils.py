"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Small common utils for the game logic.
"""
import random
import os.path

from const import MOD_DIR


def address(name):
    """Return full address of the given model.

    Args:
        name (str): Model name.

    Returns:
        str: Full model file address.
    """
    return MOD_DIR + name + ".bam"


def chance(percent):
    """Return True with percent possibility.

    Args:
        percent (int): Possibility percent.

    Returns:
        bool:
            Random boolean value with the given
            possibility of True.
    """
    return random.randint(1, 100) <= percent


def drown_snd(snd, task):
    """Drown the given sound.

    Args:
        snd (panda3d.core.AudioSound): Sound to drown.
    """
    volume = snd.getVolume()
    if volume <= 0:
        snd.stop()
        snd.setVolume(1)
        return task.done

    snd.setVolume(volume - 0.1)
    return task.again


def save_exists():
    """Indicates if a saved game exists.

    Returns:
        bool: True if a valid game save exists, False otherwise.
    """
    return all(
        (
            os.path.exists("saves/save1.dat"),
            os.path.exists("saves/save1.bak"),
            os.path.exists("saves/save1.dir"),
            os.path.exists("saves/world.dat"),
            os.path.exists("saves/world.bak"),
            os.path.exists("saves/world.dir"),
        )
    )


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
