"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

API to manage outings.
"""
import copy
import random

from gui import OutingsInterface
from .outings_data import OUTINGS


class OutingsManager:
    """An object to manage outings.

    Rules the outings planning, manipulating, results
    calculating and GUI.

    Args:
        location (str): Location to manage outings for.
    """

    def __init__(self, location):
        self._threshold = random.randint(35, 55)
        self._outings = copy.deepcopy(OUTINGS[location])
        self._types = tuple(self._outings.keys())
        self._snds = {
            "Looting": loader.loadSfx("sounds/looting_result.ogg"),  # noqa: F821
            "Enemy Camp": loader.loadSfx("sounds/enemy_camp_result.ogg"),  # noqa: F821
        }
        self._gui = OutingsInterface()

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
        self._gui.start(random.choice(self._outings[type_]))

    def plan_outing(self):
        """Generate an outing.

        Returns:
            str: if outing planned, None otherwise.
        """
        self._threshold -= 1

        if self._threshold <= 0:
            self._threshold = random.randint(35, 55)
            return random.choice(self._types)

    def show_upcoming(self, type_):
        """Show upcoming outing info.

        Args:
            type(str): Outing type.
        """
        self._gui.show_upcoming_outing(type_)

    def show_city(self):
        """Show upcoming city info."""
        self._gui.show_city()

    def show_upcoming_closer(self):
        """Show that 1 mile left until available outing."""
        self._gui.show_upcoming_closer()

    def show_can_start(self):
        """Show that outing can be started."""
        self._gui.show_can_start()

    def hide_outing(self):
        """Hide outing icon."""
        self._gui.hide_outing()

    def go_for_outing(self, outing, chars):
        """Make characters go for the given outing.

        Calculate the result according to the outing
        specifics, and do the effects.

        Args:
            outing (dict): Outing description.
            chars (list): Chars assigned for the outing.
        """
        if len(chars) != outing["assignees"]:
            return

        base.world.drop_outing_ability()  # noqa: F821

        cond_score = 0
        class_score = 0
        cond_max = 25 / len(chars)
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
        self._gui.show_result(
            desc,
            score,
            cond_score,
            class_score,
            cohesion_score,
            outing["day_part_weights"][base.world.sun.day_part],  # noqa: F821)
            selected_effect,
        )
        self._snds[outing["type"]].play()

        if "train" in effects:
            base.train.do_effects(effects["train"])  # noqa: F821

        if "money" in effects:
            base.dollars += effects["money"]  # noqa: F821
        if "medicine_boxes" in effects:
            base.medicine_boxes += effects["medicine_boxes"]  # noqa: F821
        if "smoke_filters" in effects:
            base.smoke_filters += effects["smoke_filters"]  # noqa: F821
        if "stimulators" in effects:
            base.stimulators += effects["stimulators"]  # noqa: F821

        if "all" in effects:
            for char in base.team.chars.values():  # noqa: F821
                char.do_effects(effects["all"])

        if "assignees" in effects:
            for char in chars:  # noqa: F821
                char.do_effects(effects["assignees"])

        base.team.increase_cohesion_for_chars(chars, score)  # noqa: F821


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
    return (char.health + char.energy) / (char.class_data["health"] + 100) * cond_max
