"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

API to manage outings.
"""
import copy
import random

from gui import OutingsGUI

from utils import chance, take_random
from .outings_data import ENEMY_CAMP, LOOTING, MEET


class OutingsManager:
    """An object to manage outings.

    Rules the outings planning, manipulating, results calculating and GUI.

    Args:
        prefered_type (str): Optional. Name of the prefered outing type.
    """

    def __init__(self, prefered_type=None):
        self._threshold = random.randint(25, 33)
        self._outings = {
            "Enemy Camp": copy.deepcopy(ENEMY_CAMP),
            "Looting": copy.deepcopy(LOOTING),
            "Meet": copy.deepcopy(MEET),
        }
        self._snds = {
            "Looting": loader.loadSfx("sounds/GUI/looting_result.ogg"),  # noqa: F821
            "Enemy Camp": loader.loadSfx(  # noqa: F821
                "sounds/GUI/enemy_camp_result.ogg"
            ),
            "Meet": loader.loadSfx("sounds/GUI/meet_result.ogg"),  # noqa: F821
        }
        self._gui = OutingsGUI()
        self._prefered = prefered_type

    @property
    def gui_is_shown(self):
        """Indicator if the outing GUI is shown.

        Returns:
            bool: True if the outings GUI is currently shown.
        """
        return self._gui.is_shown

    def _get_result(self, score, outing):
        """Get outing results for the given score.

        Args:
            score (int): Outing score.
            outing (dict): Outing description.

        Returns:
            str, dict: Result description and effects.
        """
        for index, result in enumerate(outing["results"]):
            if score in range(*result["score"]):
                return (
                    base.labels.OUTINGS[outing["index"]]["results"][  # noqa: F821
                        index
                    ],
                    result["effects"],
                )

    def hide_outing(self):
        """Hide outing icon."""
        self._gui.hide_outing()

    def plan_outing(self):
        """Generate an outing.

        Returns:
            str: if outing planned, None otherwise.
        """
        self._threshold -= 1

        if self._threshold <= 0:
            self._threshold = random.randint(21, 30)

            if self._prefered and chance(11):
                return self._prefered

            return random.choice(("Meet", "Enemy Camp", "Looting"))

    def show_can_start(self):
        """Show that outing can be started."""
        self._gui.show_can_start()

    def show_city(self):
        """Show upcoming city info."""
        self._gui.show_city()

    def show_place_of_interest(self):
        """Show upcoming place of interest."""
        self._gui.show_place_of_interest()

    def show_upcoming(self, type_):
        """Show upcoming outing info.

        Args:
            type(str): Outing type.
        """
        self._gui.show_upcoming_outing(
            type_, base.labels.OUTING_TYPES[type_]  # noqa: F821
        )

    def show_upcoming_closer(self):
        """Show that 1 mile left until available outing."""
        self._gui.show_upcoming_closer()

    def start_outing(self, type_):
        """Choose and start outing scenario.

        Args:
            type_ (str): Outing type.
        """
        if not self._outings[type_]:
            if type_ == "Looting":
                self._outings[type_] = copy.deepcopy(LOOTING)
            elif type_ == "Enemy Camp":
                self._outings[type_] = copy.deepcopy(ENEMY_CAMP)
            else:
                self._outings[type_] = copy.deepcopy(MEET)

        self._gui.start(take_random(self._outings[type_]))

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

        # calculate outing score
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

        # do the outing result effects
        desc, effects = self._get_result(score, outing)
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
        recruit_effect = effects.get("recruit")

        prev_coh = base.team.current_cohesion[0]  # noqa: F821
        base.team.increase_cohesion_for_chars(chars, score)  # noqa: F821

        # show the outing result on the GUI
        self._gui.show_result(
            desc,
            score,
            cond_score,
            class_score,
            cohesion_score,
            outing["day_part_weights"][base.world.sun.day_part],  # noqa: F821)
            selected_effect,
            recruit_effect,
            base.team.current_cohesion[0] - prev_coh,  # noqa: F821
        )
        self._snds[outing["type"]].play()  # noqa: F821

        if "train" in effects:
            base.train.do_effects(effects["train"])  # noqa: F821

        if "money" in effects:
            base.dollars += effects["money"]  # noqa: F821
        if "medicine_boxes" in effects:
            base.plus_resource(  # noqa: F821
                "medicine_boxes", effects["medicine_boxes"]
            )
        if "smoke_filters" in effects:
            base.plus_resource("smoke_filters", effects["smoke_filters"])  # noqa: F821

        if "stimulators" in effects:
            base.plus_resource("stimulators", effects["stimulators"])  # noqa: F821

        if "cohesion_gain" in effects:
            base.team.spend_cohesion(-effects["cohesion_gain"])  # noqa: F821

        if "all" in effects:
            for char in base.team.chars.values():  # noqa: F821
                char.do_effects(effects["all"])

        if "assignees" in effects:
            for char in chars:  # noqa: F821
                char.do_effects(effects["assignees"])


def calc_condition_score(cond_max, char):
    """Calculate score according to characters condition.

    Condition consists of health and energy points.

    Args:
        cond_max (float):
            Maximum points to get from a single character.
        char (units.crew.character.Character):
            Character to calculate.

    Returns:
        float: Score from the given character.
    """
    return (char.health + char.energy) / (char.class_data["health"] + 100) * cond_max
