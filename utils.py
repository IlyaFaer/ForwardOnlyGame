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


def clear_wids(wids):
    """Clear all the GUI given in the given list.

    Args:
        wids (list): List of Panda3D GUI objects.
    """
    for wid in wids:
        wid.destroy()

    wids.clear()


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


def save_exists(num):
    """Indicates if a saved game exists in the given slot.

    Args:
        num (int): The save slot number.

    Returns:
        bool: True if a valid game save exists, False otherwise.
    """
    return all(
        (
            os.path.exists("saves/save{}.dat".format(num)),
            os.path.exists("saves/save{}.bak".format(num)),
            os.path.exists("saves/save{}.dir".format(num)),
            os.path.exists("saves/world{}.dat".format(num)),
            os.path.exists("saves/world{}.bak".format(num)),
            os.path.exists("saves/world{}.dir".format(num)),
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
    return list_.pop(random.randint(0, len(list_) - 1))
