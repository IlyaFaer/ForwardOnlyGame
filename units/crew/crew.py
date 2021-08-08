"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Player characters as a single crew object.
"""
import copy
import random

from utils import chance, take_random
from .character import generate_char, load_char

# cohesion factors, which are used on every cohesion increasing step
COHESION_FACTORS = {
    ("anarchist", "anarchist"): 0.77,
    ("soldier", "soldier"): 0.57,
    ("raider", "raider"): 0.57,
    ("soldier", "raider"): 0.43,
    ("raider", "soldier"): 0.43,
    ("raider", "anarchist"): 0.61,
    ("anarchist", "raider"): 0.61,
    ("anarchist", "soldier"): 0.58,
    ("soldier", "anarchist"): 0.58,
}


class Crew:
    """All the player's characters together object."""

    def __init__(self):
        self._char_id = 0  # variable to count character ids
        self._relations = {}  # cohesion relations between characters
        self._is_in_stench = False

        self.chars = {}
        self.cover_fire = False
        self.cohesion_cooldown = False
        self.cohesion = 0
        self.hold_together = False

        taskMgr.doMethodLater(5, self._calc_cohesion, "calc_cohesion")  # noqa: F821
        self._medicine_snd = loader.loadSfx("sounds/GUI/medicine.ogg")  # noqa: F821
        self._stimulator_snd = loader.loadSfx("sounds/GUI/stimulator.ogg")  # noqa: F821

        self._victory_snd = base.sound_mgr.loadSfx("sounds/victory.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(  # noqa: F821
            self._victory_snd, base.train.model  # noqa: F821
        )

    @property
    def current_cohesion(self):
        """Current crew cohesion values.

        Returns:
            float, dict:
                Total crew cohesion, relations index.
        """
        return self.cohesion, self._relations

    @property
    def description(self):
        """Saveable crew description.

        Returns:
            list: Saveable description of every unit.
        """
        return [char.description for char in self.chars.values()]

    def _plan_cohesion_cooldown(self, delay):
        """Start cohesion abilities cooldown.

        If cohesion skill was used, all the cohesion
        skills become non-active for some time.

        Args:
            delay (int): Cooldown length in seconds.
        """
        self.cohesion_cooldown = True
        base.res_gui.disable_cohesion()  # noqa: F821

        taskMgr.doMethodLater(  # noqa: F821
            delay, self._stop_cohesion_cooldown, "stop_cohesion_cooldown"
        )
        for m in range(int(delay / 60)):
            taskMgr.doMethodLater(  # noqa: F821
                m * 60,
                base.res_gui.show_reload_min,  # noqa: F821
                "show_reloading_eta",
                extraArgs=[(int(delay / 60) - m)],
            )

    def gen_default(self, chosen_crew):
        """Generate a default crew.

        There are three default crew types:
        Soldiers, Raiders and Anarchists.

        Args:
            chosen_crew (str): The crew type to generate.
        """
        default_crews = {
            "soldiers": {"class": "soldier", "sexes": ("male", "male", "male")},
            "raiders": {"class": "raider", "sexes": ("male", "male", "female")},
            "anarchists": {"class": "anarchist", "sexes": ("male", "male", "female")},
        }
        for sex in default_crews[chosen_crew]["sexes"]:
            self._char_id += 1

            char = generate_char(
                self._char_id, default_crews[chosen_crew]["class"], sex, self
            )
            char.prepare()

            base.train.place_recruit(char)  # noqa: F821
            self.chars[char.id] = char

    def generate_recruit(self):
        """Generate a single random recruit.

        Returns:
            units.character.Character: The generated character.
        """
        self._char_id += 1

        return generate_char(
            self._char_id,
            random.choice(("soldier", "raider", "anarchist")),
            random.choice(("male", "female")),
            self,
        )

    def gen_recruits(self):
        """Generate several recruits.

        Used in cities.

        Returns:
            dict: Recruits index.
        """
        chars = {}
        for _ in range(random.randint(6, 11)):
            chars["character_" + str(self._char_id)] = self.generate_recruit()

        return chars

    def load(self, char_desc, parts, cohesion_desc):
        """Load the crew according to the given description.

        Args:
            char_desc (list): Characters descriptions.
            parts (dict): Train parts index.
            cohesion_desc (tuple): Crew relations description.
        """
        for char_desc in char_desc:
            char = load_char(char_desc, self, parts)
            self.chars[char.id] = char
            self._char_id = max(self._char_id, int(char.id.split("_")[1]))

        self.cohesion = cohesion_desc[0]
        self._relations = cohesion_desc[1]

        base.res_gui.update_cohesion(self.cohesion)  # noqa: F821
        base.res_gui.update_chars()  # noqa: F821

    def cohesion_recall(self):
        """Do cohesion ability "Recall the past"."""
        if self.cohesion_cooldown or self.cohesion < 20:
            return

        for char in self.chars.values():
            char.energy += 25
            char.play_cohesion_effect("recall_the_past")

        self._plan_cohesion_cooldown(600)

    def cohesion_cover_fire(self):
        """Do cohesion ability "Cover fire"."""
        if self.cohesion_cooldown or self.cohesion < 40:
            return

        self.cover_fire = True

        for char in self.chars.values():
            char.play_cohesion_aura("cover_fire")

        taskMgr.doMethodLater(  # noqa: F821
            90, self._stop_cover_fire, "stop_cover_fire"
        )
        self._plan_cohesion_cooldown(300)

    def cohesion_heal_wounded(self):
        """Do cohesion ability "Not leaving ours"."""
        if self.cohesion_cooldown or self.cohesion < 60:
            return

        for char in self.chars.values():
            if char.health <= 30:
                char.health += 20
                char.play_cohesion_effect("not_leaving_ours")

        self._plan_cohesion_cooldown(600)

    def cohesion_rage(self):
        """Do cohesion ability "Common rage"."""
        if self.cohesion_cooldown or self.cohesion < 80:
            return

        for char in self.chars.values():
            char.clear_damage = copy.copy(char.damage_range)
            char.damage_range[0] *= 1.3
            char.damage_range[1] *= 1.3

        taskMgr.doMethodLater(90, self._stop_rage, "stop_rage")  # noqa: F821
        self._plan_cohesion_cooldown(600)

    def cohesion_hold_together(self):
        """Do cohesion ability "Hold together"."""
        if self.cohesion_cooldown or self.cohesion < 100:
            return

        self.hold_together = True
        taskMgr.doMethodLater(  # noqa: F821
            90, self._stop_hold_together, "stop_hold_together"
        )
        self._plan_cohesion_cooldown(900)

    def rest_all(self):
        """Make all the characters rest."""
        for char in self.chars.values():
            if not char.current_part.name == "part_rest":
                char.rest()

    def stop_rest_all(self):
        """Stop the team rest."""
        for char in self.chars.values():
            if not char.current_part.name == "part_rest":
                char.stop_rest()

    def _stop_cover_fire(self, task):
        """Stop "Cover fire" cohesion ability."""
        self.cover_fire = False
        for char in self.chars.values():
            char.stop_aura_effect("cover_fire")

        return task.done

    def _stop_rage(self, task):
        """Stop "Common rage" cohesion ability."""
        for char in self.chars.values():
            char.damage_range = copy.copy(char.clear_damage)

        return task.done

    def _stop_hold_together(self, task):
        """Stop "Hold together" cohesion ability."""
        self.hold_together = False
        return task.done

    def _stop_cohesion_cooldown(self, task):
        """End cohesion abilities cooldown."""
        self.cohesion_cooldown = False
        base.res_gui.finish_reload()  # noqa: F821
        base.res_gui.update_cohesion(self.cohesion)  # noqa: F821
        return task.done

    def celebrate(self):
        """Run victory celebration sequence."""
        if len(self.chars) > 2:
            taskMgr.doMethodLater(  # noqa: F821
                0.6, self._victory_snd.play, "play_victory_sound", extraArgs=[]
            )

            for char in self.chars.values():
                taskMgr.doMethodLater(  # noqa: F821
                    random.uniform(0.1, 0.5), char.celebrate, "celebrate_victory"
                )

    def prepare_to_fight(self):
        """Prepare every character for a fight."""
        for char in self.chars.values():
            if char.current_part.name == "part_rest":
                continue
            char.prepare_to_fight()

        taskMgr.doMethodLater(0.7, self._check_enemies, "check_enemies")  # noqa: F821

    def _check_enemies(self, task):
        """Check if all enemies are defeated."""
        if base.world.enemy.active_units:  # noqa: F821
            return task.again

        self.celebrate()
        return task.done

    def surrender(self):
        """Make the whole crew surrender."""
        for char in self.chars.values():
            char.surrender()

    def _calc_cohesion(self, task):
        """Calculate the current crew cohesion.

        Relations between all the characters are tracked.
        While characters are staying together, cohesion
        between them increases. Total cohesion is calculated
        as a sum of all relations relatively to the number
        of all relations in the crew. Different unit classes
        have different cohesion factors.
        """
        for char1 in self.chars.values():
            for char2 in self.chars.values():
                if char1.id == char2.id:
                    continue

                rel_id = tuple(sorted([char1.id, char2.id]))
                factor = 1.35 if char1.current_part == char2.current_part else 1

                if (
                    base.labels.TRAITS[4][0]  # noqa: F821
                    in char1.traits + char2.traits
                    and char1.class_ != char2.class_
                ):
                    # Liberal
                    factor *= 1.15

                if rel_id in self._relations:
                    plus = COHESION_FACTORS[(char1.class_, char2.class_)] * factor
                    self._relations[rel_id] = min(100, plus + self._relations[rel_id])

                    # propagate traits from one character to another
                    if self._relations[rel_id] > 80 and chance(50):
                        pair = [char1, char2]
                        from_char = take_random(pair)
                        if from_char.traits:
                            trait = random.choice(from_char.traits)
                            if trait not in pair[0].traits and len(pair[0].traits) < 3:
                                pair[0].traits.append(trait)
                else:
                    self._relations[rel_id] = (
                        COHESION_FACTORS[(char1.class_, char2.class_)] * factor
                    )

        self._calc_total_cohesion()
        task.delayTime = 185
        return task.again

    def init_relations(self, new_char):
        """Initialize new character's relations with other characters.

        Args:
            new_char (units.character.Character):
                A new character in the crew.
        """
        for char in self.chars.values():
            if char.id == new_char.id:
                continue
            self._relations[tuple(sorted([new_char.id, char.id]))] = 0

    def _calc_total_cohesion(self):
        """Calculate total cohesion score considering all the relations."""
        if not self._relations:
            return

        rel_max = 100 / len(self._relations)
        cohesion = 0
        for relation in self._relations.values():
            cohesion += relation / 100 * rel_max

        self.cohesion = min(100, cohesion)
        base.res_gui.update_cohesion(self.cohesion)  # noqa: F821

    def calc_cohesion_for_chars(self, chars):
        """Calculate cohesion for the given characters.

        Cohesion will be calculated only with relations
        between the given characters. If only one character
        given, all of his relations will be calculated.
        Resulting sum will be relative to 25 - maximum
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

        cohesion = round((cohesion / rel_num) * 25, 2)
        return cohesion

    def calc_cohesion_factor(self, chars, for_char):
        """Calculate the damage factor for the given characters.

        The stronger cohesion the given characters
        have the higher will be the damage factor.

        Args:
            chars (list):
                Characters, for whom a damage factor must
                be calculated.
            for_char (units.Character):
                Unit for whom the factor must be calculated.

        Returns:
            float: The damage factor.
        """
        if len(chars) < 2:
            return 1

        rel_id = tuple(sorted([chars[0].id, chars[1].id]))
        try:
            cohesion = self._relations[rel_id] / 100
        except KeyError:
            # character was killed during calculations
            cohesion = 0
        return 1 + cohesion * 0.5 * (2 if for_char.class_ == "anarchist" else 1)

    def delete_relations(self, char_id):
        """Delete all the relations of the given character.

        Args:
            char_id (str): Character whose relations should be erased.
        """
        to_del = []
        for rel_id in self._relations.keys():
            if char_id in rel_id:
                to_del.append(rel_id)

        for id_ in to_del:
            self._relations.pop(id_)

    def increase_cohesion_for_chars(self, chars, outing_score):
        """Increase cohesion for those who went for an outing.

        Increase factor depends on outing score: the higher
        it is - the higher will be cohesion increase.

        Args:
            chars (list): Chars who went for an outing.
            outing_score (float): Total outing score.
        """
        for char1 in chars:
            for char2 in chars:
                if char1.id == char2.id:
                    continue

                rel_id = tuple(sorted([char1.id, char2.id]))
                factor = 1 + outing_score // 25 * 0.3

                if rel_id in self._relations:
                    self._relations[rel_id] += (
                        COHESION_FACTORS[(char1.class_, char2.class_)] * factor
                    )
                else:
                    self._relations[rel_id] = (
                        COHESION_FACTORS[(char1.class_, char2.class_)] * factor
                    )
        self._calc_total_cohesion()

    def show_relations(self, char):
        """Show the given character relations GUI.

        Highlights cohesion between the given character
        and other characters with color balls above all
        characters except the chosen.

        Args:
            char (units.crew.character.Character):
                The character, whose relations must be shown.
        """
        char.hide_relations_ball()

        for rel_id, relation in self._relations.items():
            if char.id in rel_id:
                to_id = rel_id[1] if char.id == rel_id[0] else rel_id[0]
                self.chars[to_id].show_relation(relation)

    def hide_relations(self):
        """Hide all the relations GUI."""
        for char in self.chars.values():
            char.hide_relations_ball()

    def use_medicine(self):
        """Use a medicine on the chosen character.

        Will help the character to get well.
        Uses single Medicine resource.
        """
        if not base.resource("medicine_boxes"):  # noqa: F821
            return

        char = base.common_ctrl.chosen_char  # noqa: F821
        if char:
            char.get_well_score = 20
            char.health += 35
            base.plus_resource("medicine_boxes", -1)  # noqa: F821
            self._medicine_snd.play()

    def use_stimulator(self):
        """Use stimulator on the chosen character.

        Disables all the negative traits of the
        chosen character for the next 5 minutes.
        """
        if not base.resource("stimulators"):  # noqa: F821
            return

        char = base.common_ctrl.chosen_char  # noqa: F821
        if char:
            char.get_stimulated()
            base.plus_resource("stimulators", -1)  # noqa: F821
            self._stimulator_snd.play()

    def spend_cohesion(self, value):
        """Spend the given number of cohesion points.

        Args:
            value (int): Cohesion points to spend.
        """
        if not self._relations:
            return

        factor = (self.cohesion - value) / self.cohesion

        rel_max = 100 / len(self._relations)
        cohesion = 0

        for rel_id in self._relations.keys():
            self._relations[rel_id] *= factor
            cohesion += self._relations[rel_id] / 100 * rel_max

        self.cohesion = min(100, cohesion)
        base.res_gui.update_cohesion(self.cohesion)  # noqa: F821

    def start_stench_activity(self):
        """Start dealing the Stench damage to characters."""
        if not self._is_in_stench:
            taskMgr.doMethodLater(  # noqa: F821
                4.2, self.stench_activity, "stench_activity"
            )
            self._is_in_stench = True

    def stop_stench_activity(self):
        """Stop dealing the Stench damage to characters."""
        if self._is_in_stench:
            taskMgr.remove("stench_activity")  # noqa: F821
            self._is_in_stench = False

            for char in self.chars.values():
                char.inhale = 15

    def stench_activity(self, task):
        """Deal the Stench damage to every character."""
        for char in self.chars.values():
            char.get_stench_damage()

        return task.again
