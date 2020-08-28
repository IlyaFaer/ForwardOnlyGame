"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Player characters as a single team API.
"""
import copy
import random
from .character import generate_char, load_char

COHESION_FACTORS = {("soldier", "soldier"): 0.5}


class Team:
    """All characters (player units) object."""

    def __init__(self):
        self._char_id = 0  # variable to count character ids
        self._relations = {}

        self.chars = {}
        self.cover_fire = False
        self.cohesion_cooldown = False
        self.cohesion = 0
        self.hold_together = False

        base.taskMgr.doMethodLater(  # noqa: F821
            5, self._calc_cohesion, "calc_cohesion"
        )

    @property
    def current_cohesion(self):
        """Current team cohesion values.

        Returns:
            float, dict:
                Total team cohesion, relations index.
        """
        return self.cohesion, self._relations

    @property
    def description(self):
        """Saveable team description.

        Returns:
            list: Saveable description of every unit.
        """
        return [char.description for char in self.chars.values()]

    def gen_default(self, train_parts):
        """Generate default team.

        Args:
            train_pargs (dict):
                Train parts to set characters on.
        """
        for part, sex in (
            (train_parts["part_locomotive_right"], "male"),
            (train_parts["part_locomotive_right"], "male"),
            (train_parts["part_locomotive_front"], "female"),
        ):
            self._char_id += 1

            char = generate_char(self._char_id, "soldier", sex, self)
            char.prepare()
            char.move_to(part)

            self.chars[char.id] = char

    def load(self, description, parts):
        """Load the team according to the given description.

        Args:
            description (list): Characters descriptions.
            parts (dict): Train parts index.
        """
        for char_desc in description:
            char = load_char(char_desc, self, parts)
            self.chars[char.id] = char

    def gen_recruits(self):
        """Generate several recruits.

        Used in cities.

        Returns:
            dict: Recruits index.
        """
        chars = {}
        for _ in range(random.randint(1, 4)):
            self._char_id += 1

            chars["character_" + str(self._char_id)] = generate_char(
                self._char_id, "soldier", random.choice(("male", "female")), self
            )
        return chars

    def cohesion_recall(self):
        """Do cohesion ability "Recall the past"."""
        if self.cohesion_cooldown or self.cohesion < 20:
            return

        for char in self.chars.values():
            char.energy += 15

        self._plan_cohesion_cooldown(900)

    def cohesion_cover_fire(self):
        """Do cohesion ability "Cover fire"."""
        if self.cohesion_cooldown or self.cohesion < 40:
            return

        self.cover_fire = True
        base.taskMgr.doMethodLater(  # noqa: F821
            90, self._stop_cover_fire, "stop_cover_fire"
        )
        self._plan_cohesion_cooldown(600)

    def cohesion_heal_wounded(self):
        """Do cohesion ability "Not leaving ours"."""
        if self.cohesion_cooldown or self.cohesion < 60:
            return

        for char in self.chars.values():
            if char.health <= 30:
                char.health += 20

        self._plan_cohesion_cooldown(900)

    def cohesion_rage(self):
        """Do cohesion ability "Common rage"."""
        if self.cohesion_cooldown or self.cohesion < 80:
            return

        for char in self.chars.values():
            char.clear_damage = copy.copy(char.damage)
            char.damage[0] = round(char.damage[0] * 1.3)
            char.damage[1] = round(char.damage[1] * 1.3)

        base.taskMgr.doMethodLater(90, self._stop_rage, "stop_rage")  # noqa: F821
        self._plan_cohesion_cooldown(900)

    def cohesion_hold_together(self):
        """Do cohesion ability "Hold together"."""
        if self.cohesion_cooldown or self.cohesion < 100:
            return

        self.hold_together = True
        base.taskMgr.doMethodLater(  # noqa: F821
            90, self._stop_hold_together, "stop_hold_together"
        )
        self._plan_cohesion_cooldown(1200)

    def rest_all(self):
        """Make all the characters rest."""
        for char in self.chars.values():
            if not char.current_part.name.startswith("part_rest_"):
                char.rest()

    def stop_rest_all(self):
        """Stop the team rest."""
        for char in self.chars.values():
            if not char.current_part.name.startswith("part_rest_"):
                char.stop_rest()

    def _stop_cover_fire(self, task):
        """Stop "Cover fire" cohesion ability."""
        self.cover_fire = False
        return task.done

    def _stop_rage(self, task):
        """Stop "Common rage" cohesion ability."""
        for char in self.chars.values():
            char.damage = copy.copy(char.clear_damage)

        return task.done

    def _stop_hold_together(self, task):
        """Stop "Hold together" cohesion ability."""
        self.hold_together = False
        return task.done

    def _stop_cohesion_cooldown(self, task):
        """End cohesion abilities cooldown."""
        self.cohesion_cooldown = False
        base.res_interface.update_cohesion(self.cohesion)  # noqa: F821
        return task.done

    def _plan_cohesion_cooldown(self, delay):
        """Start cohesion abilities cooldown.

        Args:
            delay (int): Cooldown length in seconds.
        """
        self.cohesion_cooldown = True
        base.res_interface.disable_cohesion()  # noqa: F821

        base.taskMgr.doMethodLater(  # noqa: F821
            delay, self._stop_cohesion_cooldown, "stop_cohesion_cooldown"
        )

    def prepare_to_fight(self):
        """Prepare every character to fight."""
        for char in self.chars.values():
            char.prepare_to_fight()

    def surrender(self):
        """Make the whole team surrender."""
        for char in self.chars.values():
            char.surrender()

    def _calc_cohesion(self, task):
        """Calculate the current team cohesion.

        Relations between all the characters are tracked.
        While characters are staying together, cohesion
        between them increases. Total cohesion is calculated
        as a sum of all relations relatively to the number
        of all relations in team. Different unit classes
        have different cohesion factors.
        """
        for char1 in self.chars.values():
            for char2 in self.chars.values():
                if char1.id == char2.id:
                    continue

                rel_id = tuple(sorted([char1.id, char2.id]))
                if rel_id in self._relations:
                    self._relations[rel_id] += COHESION_FACTORS[
                        (char1.class_, char2.class_)
                    ]
                else:
                    self._relations[rel_id] = COHESION_FACTORS[
                        (char1.class_, char2.class_)
                    ]

        rel_max = 100 / len(self._relations)
        cohesion = 0
        for relation in self._relations.values():
            cohesion += relation / 100 * rel_max

        self.cohesion = min(100, cohesion)
        base.res_interface.update_cohesion(self.cohesion)  # noqa: F821

        task.delayTime = 360
        return task.again

    def calc_cohesion_for_chars(self, chars):
        """Calculate cohesion for an outing party.

        Cohesion will be calculated only with relations
        between the given characters. If only one character
        given, all of his relations will be calculated.
        Resulting sum will be relative to 20 - maximum
        cohesion score in any outing.

        Args:
            chars (list): Characters to calculate cohesion for.

        Returns:
            float: Cohesion score for the given characters.
        """
        cohesion = 0
        rel_num = 0
        if len(chars) == 1:
            for key in self._relations.keys():
                if chars[0].id in key:
                    rel_num += 1
                    cohesion += self._relations[key] / 100
        else:
            used_rels = []
            for char1 in chars:
                for char2 in chars:
                    if char1.id == char2.id:
                        continue

                    rel_id = tuple(sorted([char1.id, char2.id]))
                    if rel_id in used_rels:
                        continue

                    rel_num += 1
                    used_rels.append(rel_id)
                    cohesion += self._relations[rel_id] / 100

        cohesion = round((cohesion / rel_num) * 20, 2)
        return cohesion
