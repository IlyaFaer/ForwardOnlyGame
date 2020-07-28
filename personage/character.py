"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Characters (player units) API.
"""
import copy
import random

from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import LerpAnimInterval, Sequence
from panda3d.core import CollisionCapsule

from const import MOUSE_MASK, NO_MASK
from utils import address, chance

from .personage_data import NAMES, CLASSES
from .shooter import Shooter
from .unit import Unit

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


class Character(Shooter, Unit):
    """Game character.

    Args:
        id_ (int): Character unique id.
        name (str): Character name.
        class_ (str): Unit class.
        mod_name (str): Character model name.
        sex (str): Character gender.
        team (Team): Team object.
    """

    def __init__(self, id_, name, class_, mod_name, sex, team):
        Unit.__init__(
            self, "character_" + str(id_), class_, CLASSES[sex + "_" + class_]
        )
        Shooter.__init__(self)

        self._team = team
        self._mod_name = mod_name

        self._current_pos = None
        self._current_anim = None
        self._idle_seq = None
        self._energy = 100

        self.name = name
        self.sex = sex
        self.heshe = "he" if sex == "male" else "she"
        self.hisher = "his" if sex == "male" else "her"
        self.himher = "him" if sex == "male" else "her"
        self.damage = [3, 5]
        self.clear_damage = [3, 5]

    @property
    def energy(self):
        """This character energy.

        Returns:
            int: This character energy points.
        """
        return self._energy

    @energy.setter
    def energy(self, value):
        """This character energy setter.

        Args:
            value (int): New energy value.
        """
        self._energy = min(max(value, 0), 100)

    @property
    def tooltip(self):
        """Tooltip to show on mouse pointing to this character.

        Returns:
            str: This character name.
        """
        return self.name

    @property
    def clear_delay(self):
        """Delay between this character's death and clearing.

        Returns:
            float: Seconds to hold the character before delete.
        """
        return 3.5

    def prepare(self):
        """Load the character model and positionate it.

        Tweak collision solid as well.
        """
        self.model = Actor(
            self._mod_name,
            {
                "die": address("soldier-die"),
                "gun_up": address("soldier-gun_up"),
                "incline1": address("soldier-incline1"),
                "release_gun": address("soldier-release_gun"),
                "stand_and_aim": address("soldier-stand_and_aim"),
                "stand": address("soldier-stand"),
                "surrender": address("soldier-surrender"),
                "tread1": address("soldier-tread1"),
                "turn_head1": address("soldier-turn_head1"),
            },
        )
        self.model.enableBlend()
        self.model.setControlEffect("stand", 1)

        self.model.setPlayRate(0.8, "stand_and_aim")
        self.model.setPlayRate(0.6, "stand")

        self.model.loop("stand")

        base.taskMgr.doMethodLater(  # noqa: F821
            random.randint(40, 60), self._idle_animation, self.id + "_idle_anim"
        )
        self._col_node = self._init_col_node(
            NO_MASK, MOUSE_MASK, CollisionCapsule(0, 0, 0, 0, 0, 0.035, 0.035)
        )
        self.shot_snd = self._set_shoot_snd("rifle_shot1")
        self._shoot_anim = self._set_shoot_anim(
            (0.004, 0.045, 0.064 if self.sex == "male" else 0.062), 97
        )
        base.taskMgr.doMethodLater(  # noqa: F821
            30, self._reduce_energy, self.id + "_reduce_energy"
        )

    def move_to(self, part):
        """Move this Character to the given Train part.

        Args:
            part (train.TrainPart):
                Train part to move this Character to.
        """
        pos = part.give_cell(self)
        if not pos:  # no free cells on the chosen part
            return

        if self.current_part is not None:
            self.current_part.release_cell(self._current_pos, self)

            if self.current_part.name.startswith("part_rest_"):
                self._stop_rest()

        if part.name.startswith("part_rest_"):
            self._rest()

        self.model.wrtReparentTo(part.parent)
        self.model.setPos(pos["pos"])
        self.model.setH(pos["angle"])

        self.current_part = part
        self._current_pos = pos

    def attack(self, enemy_unit):
        """Make the given enemy unit this character's target.

        Args:
            enemy_unit (personage.enemy.EnemyUnit):
                Enemy unit to attack.
        """
        if enemy_unit in self.current_part.enemies:
            self._target = enemy_unit

    def prepare_to_fight(self):
        """Prepare the character to fight.

        Switch animations and run a task to choose a target.
        """
        base.taskMgr.remove(self.id + "_idle_anim")  # noqa: F821
        if self._idle_seq is not None:
            self._idle_seq.finish()

        self.model.loop("stand_and_aim")
        LerpAnimInterval(self.model, 0.8, self._current_anim, "stand_and_aim").start()
        LerpAnimInterval(self.model, 0.8, "stand", "stand_and_aim").start()

        base.taskMgr.doMethodLater(  # noqa: F821
            0.5, self._choose_target, self.id + "_choose_target"
        )

    def surrender(self):
        """Stop fighting, surrender."""
        base.taskMgr.remove(self.id + "_shoot")  # noqa: F821
        base.taskMgr.remove(self.id + "_aim")  # noqa: F821
        base.taskMgr.remove(self.id + "_choose_target")  # noqa: F821

        self._col_node.removeNode()
        self._shoot_anim.finish()

        LerpAnimInterval(self.model, 0.5, "stand_and_aim", "surrender").start()
        self.model.play("surrender")

    def _rest(self):
        """Make this character rest.

        Stops all the active tasks and starts
        energy regaining.
        """
        for task in (
            "_reduce_energy",
            "_shoot",
            "_aim",
            "_choose_target",
            "_idle_anim",
        ):
            base.taskMgr.remove(self.id + task)  # noqa: F821

        self.model.hide()
        self._col_node.stash()

        base.taskMgr.doMethodLater(  # noqa: F821
            0.05, self._calm_down, self.id + "_calm_down"
        )
        base.taskMgr.doMethodLater(  # noqa: F821
            self.class_data["energy_gain"], self._gain_energy, self.id + "_gain_energy"
        )
        if self.health < self.class_data["health"]:
            base.taskMgr.doMethodLater(30, self._heal, self.id + "_heal")  # noqa: F821

    def do_effects(self, effects):
        """Do outing effects to this character.

        Args:
            effects (dict): Effects and their values.
        """
        if effects is None:
            return

        for key, value in effects.items():
            if hasattr(self, key):
                setattr(self, key, getattr(self, key) + value)

    def _stop_rest(self):
        """Stop this character rest."""
        self.model.show()
        self._col_node.unstash()
        base.char_interface.destroy_char_button(self.id)  # noqa: F821

        base.taskMgr.remove(self.id + "_gain_energy")  # noqa: F821
        base.taskMgr.remove(self.id + "_heal")  # noqa: F821
        base.taskMgr.doMethodLater(  # noqa: F821
            30, self._reduce_energy, self.id + "_reduce_energy"
        )
        if base.world.enemy.active_units:  # noqa: F821
            self.prepare_to_fight()

    def _reduce_energy(self, task):
        """
        Reduce the character energy according to day part
        and status: fighting or not.
        """
        if self._target:
            task.delayTime = 20
        elif base.world.sun.is_dark:  # noqa: F821
            if base.train.lights_on:  # noqa: F821
                task.delayTime = 20
            else:
                task.delayTime = 15
        else:
            task.delayTime = 30

        self.energy -= 1
        return task.again

    def _gain_energy(self, task):
        """Regain this character energy."""
        self.energy += 3

        for char in self.current_part.chars:
            if char.sex == "female" and self.id != char.id:
                task.delayTime = self.class_data["energy_gain"] - 5
                return task.again

        return task.again

    def _heal(self, task):
        """Regain this character health."""
        if self.health < self.class_data["health"]:
            self.health += 1
            return task.again

        return task.done

    def _choose_target(self, task):
        """Choose an enemy to shoot.

        Only an enemy from the Train part shooting
        range can be chosen as a target.
        """
        if self.current_part.enemies:
            self._target = random.choice(self.current_part.enemies)
            base.taskMgr.doMethodLater(0.1, self._aim, self.id + "_aim")  # noqa: F821
            base.taskMgr.doMethodLater(1, self._shoot, self.id + "_shoot")  # noqa: F821
            return task.done

        # enemies retreated - return to passive state
        if not base.world.enemy.active_units:  # noqa: F821
            base.taskMgr.doMethodLater(  # noqa: F821
                3, self._calm_down, self.id + "_calm_down"
            )
            return task.done

        return task.again

    def _aim(self, task):
        """Rotate the character to aim on enemy."""
        if self._target in self.current_part.enemies:
            self.model.headsUp(self._target.model)
            return task.again

        base.taskMgr.remove(self.id + "_shoot")  # noqa: F821
        self._target = None

        if base.world.enemy.active_units:  # noqa: F821
            base.taskMgr.doMethodLater(  # noqa: F821
                0.5, self._choose_target, self.id + "_choose_target"
            )
            return task.done

        base.taskMgr.doMethodLater(  # noqa: F821
            3, self._calm_down, self.id + "_calm_down"
        )
        return task.done

    def _calm_down(self, task):
        """Return to passive state."""
        base.taskMgr.remove(self.id + "_shoot")  # noqa: F821
        self.model.hprInterval(2, (self._current_pos["angle"], 0, 0)).start()

        LerpAnimInterval(self.model, 2, "stand_and_aim", "stand").start()
        base.taskMgr.doMethodLater(  # noqa: F821
            random.randint(40, 60), self._idle_animation, self.id + "_idle_anim"
        )
        return task.done

    def _idle_animation(self, task):
        """Play one of the idle animations.

        Args:
            task (panda3d.core.PythonTask): Task object.
        """
        self._current_anim = random.choice(
            ("incline1", "gun_up", "release_gun", "tread1", "turn_head1")
        )
        LerpAnimInterval(self.model, 0.3, "stand", self._current_anim).start()

        self._idle_seq = Sequence(
            self.model.actorInterval(self._current_anim, playRate=0.75),
            LerpAnimInterval(self.model, 0.3, self._current_anim, "stand"),
        )
        self._idle_seq.start()

        task.delayTime = random.randint(40, 60)
        return task.again

    def _die(self):
        """Character death code.

        Stop all the character's tasks, play death
        animation and plan character clearing.
        """
        if self._team.hold_together:
            self.health = 1
            return False

        if not Shooter._die(self):
            return False

        Unit._die(self)

        base.taskMgr.remove(self.id + "_reduce_energy")  # noqa: F821

        LerpAnimInterval(self.model, 0.3, "stand_and_aim", "die").start()
        self.model.hprInterval(1, (self._current_pos["angle"], 0, 0)).start()
        self.model.play("die")

        base.taskMgr.doMethodLater(3, self._hide, self.id + "_hide")  # noqa: F821

    def _hide(self, task):
        """Hide the main model."""
        self.model.hide()
        return task.done

    def clear(self, task):
        """Clear this character."""
        self.model.cleanup()
        self.model.removeNode()
        base.sound_mgr.detach_sound(self.shot_snd)  # noqa: F821

        self._team.chars.pop(self.id)
        self.current_part.release_cell(self._current_pos, self)
        self.current_part = None

        return task.done

    def _missed_shot(self):
        """Calculate if character missed the current shot.

        Returns:
            bool: True if character missed, False otherwise.
        """
        miss_chance = 0
        if self.class_ == "soldier":
            if (
                abs(self._target.node.getX()) < 0.5
                and abs(self._target.node.getY()) < 0.95
            ):
                miss_chance += 20

        if base.world.sun.is_dark:  # noqa: F821
            miss_chance += 20

        miss_chance += (100 - self.energy) // 5
        if self._team.cover_fire:
            miss_chance = max(0, miss_chance - 25)

        return chance(miss_chance)


def generate_char(id_, class_, sex, team=None):
    """Generate character with the given parameters.

    Args:
        id_ (str): Character id.
        class_ (str): Character class.
        sex (str): Character gender.
        team (Team): Optional. Team to add new character into.

    Returns:
        Character: The generated character.
    """
    return Character(
        id_, random.choice(NAMES[sex]), class_, address(sex + "_" + class_), sex, team
    )
