"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

API to manage outings.
"""
import copy
import random

from gui import OutingsInterface
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
        self._looting_snd = base.loader.loadSfx(  # noqa: F821
            "sounds/looting_result.ogg"
        )
        self._interface = OutingsInterface()

    def _get_result(self, score, results):
        """Get outing results for the given score.

        Args:
            score (int): Outing score.
            results (list): All the outing results.

        Returns:
            str, dict: Result description and effects.
        """
        for result in results:
            if score in result["score"]:
                return result["desc"], result["effects"]

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

    def go_for_outing(self, outing, chars):
        """Make characters go for the given outing.

        Calculate the result according to the outing
        specifics and do the effects.

        Args:
            outing (dict): Outing description.
            chars (list): Chars assigned for the outing.
        """
        if len(chars) != outing["assignees"]:
            return

        cond_score = 0
        class_score = 0
        cond_max = 20 / len(chars)
        for char in chars:
            cond_score += calc_condition_score(cond_max, char)
            class_score += outing["class_weights"][char.class_]

        cond_score = round(cond_score, 2)
        class_score = round(class_score, 2)
        cohesion_score = base.team.calc_cohesion_for_chars(chars)  # noqa: F821

        score = cond_score
        score += class_score
        score += outing["day_part_weights"][base.world.sun.day_part]  # noqa: F821
        score += cohesion_score
        score = round(score)

        desc, effects = self._get_result(score, outing["results"])
        format_dict = {}
        for index, char in enumerate(chars, start=1):
            format_dict.update(
                {
                    "name" + str(index): char.name,
                    "heshe" + str(index): char.heshe,
                    "hisher" + str(index): char.hisher,
                    "himher" + str(index): char.himher,
                }
            )
            char.do_effects(effects.get("char_" + str(index)))

        desc = desc.format(**format_dict)

        selected_effect = effects.get("select_char")
        self._interface.show_result(
            desc,
            score,
            cond_score,
            class_score,
            cohesion_score,
            outing["day_part_weights"][base.world.sun.day_part],  # noqa: F821)
            selected_effect,
        )
        self._looting_snd.play()

        if "train" in effects:
            base.train.do_effects(effects["train"])  # noqa: F821
        if "money" in effects:
            base.dollars += effects["money"]  # noqa: F821
            base.res_interface.update_money(base.dollars)  # noqa: F821
        if "all" in effects:
            for char in base.team.chars.values():  # noqa: F821
                char.do_effects(effects["all"])


def calc_condition_score(cond_max, char):
    """Calculate score according to characters condition.

    Condition consists of health and energy points.

    Args:
        cond_max (float):
            Maximum points to get from a single character.
        char (personage.character.Character):
            Character to calculate.

    Returns:
        float: Score from the given character.
    """
    return (char.health + char.energy) / char.class_data["health"] / 2 * cond_max
