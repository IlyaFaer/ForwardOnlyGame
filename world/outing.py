"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

API to manage outings.
"""
import copy
import random

from gui.interface import OutingsInterface
from utils import chance
from .outings_data import OUTINGS


class OutingsManager:
    """An object to manage outings.

    Rules the outings planning, manipulating, results
    calculating and gui.

    Args:
        location (str): Location to manage outings for.
    """

    def __init__(self, location):
        self._threshold = 70
        self._outings = copy.deepcopy(OUTINGS[location])
        self._types = tuple(self._outings.keys())
        self._interface = OutingsInterface()

    def start_outing(self, type_):
        """Choose and start outing scenario.

        Args:
            type_ (str): Outing type.
        """
        self._interface.start(random.choice(self._outings[type_]))

    def plan_outing(self):
        """Generate an outing.

        Returns:
            str: if outing planned, None otherwise.
        """
        self._threshold -= 1

        if self._threshold <= 0 and chance(40):
            self._threshold = 70
            return random.choice(self._types)

    def show_upcoming(self, type_):
        """Show upcoming outing info.

        Args:
            type(str): Outing type.
        """
        self._interface.show_upcoming(type_)

    def show_upcoming_closer(self):
        """Show that 1 mile left until available outing."""
        self._interface.show_upcoming_closer()

    def show_can_start(self):
        """Show that outing can be started."""
        self._interface.show_can_start()

    def hide_outing(self):
        """Hide outing icon."""
        self._interface.hide_outing()
