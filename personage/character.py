"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Characters (player units) API.
"""
import copy
import random

from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import LerpAnimInterval, Sequence
from panda3d.core import CollisionCapsule

from const import MOUSE_MASK, NO_MASK
from gui.character import HealthBar
from utils import address, chance, take_random

from .character_data import CLASSES, NAMES, TRAITS
from .shooter import Shooter
from .unit import Unit

# cohesion relation indicator colors
RELATION_COLORS = {
    0: (1, 0.01, 0.24, 1),  # red
    1: (1, 0.45, 0.09, 1),  # orange
    2: (1, 1, 0, 1),  # yellow
    3: (0.67, 0.97, 0.82, 1),  # light green
    4: (0.18, 0.97, 0.57, 1),  # green
    5: (0.18, 0.97, 0.57, 1),  # green
}


class Character(Shooter, Unit):
    """A game character.

    Represents a unit controlled by a player.

    Args:
        id_ (int): The character unique id.
        name (str): The character name.
        class_ (str): Unit class.
        sex (str): The character gender.
        team (team.Team): Team object.
        desc (dict): Optional. The character description.
    """

    def __init__(self, id_, name, class_, sex, team, desc=None):
        Unit.__init__(
            self, "character_" + str(id_), class_, CLASSES[sex + "_" + class_]
        )
        Shooter.__init__(self)

        self._team = team
        self._current_pos = None
        self._current_anim = None
        self._idle_seq = None
        self._cohesion_ball = None
        self._is_stunned = False
        self._is_stimulated = False
        self._health_bar = None
        self.inhale = 15

        self.name = name
        self.sex = sex
        self.heshe = "he" if sex == "male" else "she"
        self.hisher = "his" if sex == "male" else "her"
        self.himher = "him" if sex == "male" else "her"

        self.damage_range = [4, 6]
        self.clear_damage = [4, 6]

        if desc:
            self._energy = desc["energy"]
            self.is_diseased = desc["is_diseased"]
            self.get_well_score = desc["get_well_score"]

            self.traits = desc["traits"]
            self.disabled_traits = desc["disabled_traits"]
            if self.is_diseased:
                taskMgr.doMethodLater(  # noqa: F821
                    60, self.get_well, self.id + "_get_well"
                )
        else:
            self._energy = 100
            self.is_diseased = False
            self.get_well_score = 0

            self.disabled_traits = []
            self.traits = []
            traits = copy.copy(TRAITS)
            for _ in range(random.randint(0, 2)):
                self.traits.append(random.choice(take_random(traits)))

    @property
    def clear_delay(self):
        """
        Delay between this character death
        and clearing the character object.

        Returns:
            float: Seconds to wait before clearing.
        """
        return 3.5

    @property
    def damage(self):
        """This character one-time calculated damage.

        Returns:
            float: Damage one-time made by this character.
        """
        return random.uniform(*self.damage_range) * self.damage_factor

    @property
    def damage_factor(self):
        """This character damage factor.

        The damage factor depends on cohesion with another
        character on the same part of the Train.

        Returns:
            float: Damage one-time made by this character.
        """
        factor = self._team.calc_cohesion_factor(self.current_part.chars, self)
        if "Loner" in self.traits and len(self.current_part.chars) == 1:
            return factor * 1.3

        return factor

    @property
    def description(self):
        """This character saveable parameters.

        Used for saving the character.

        Returns:
            dict: This character description.
        """
        return {
            "id": int(self.id.split("_")[1]),
            "name": self.name,
            "sex": self.sex,
            "class": self.class_,
            "health": self.health,
            "energy": self.energy,
            "place": self.current_part.name,
            "traits": self.traits,
            "disabled_traits": self.disabled_traits,
            "is_diseased": self.is_diseased,
            "get_well_score": self.get_well_score,
        }

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
        self._energy = min(max(value, 0), 80 if self.is_diseased else 100)

    @property
    def shooting_speed(self):
        """Delay between shots of this unit.

        Returns:
            float: Delay between shots in seconds.
        """
        if "Fast hands" in self.traits:
            return 1.1 + random.uniform(0.1, 0.8)

        if "Snail" in self.traits:
            return 2 + random.uniform(0.1, 1.1)

        return 1.7 + random.uniform(0.1, 0.9)

    @property
    def statuses(self):
        """Return strings describing the current character status.

        Returns:
            list: Status description lines.
        """
        statuses = []
        if base.world.sun.is_dark:  # noqa: F821
            if "Cat eyes" in self.traits:
                statuses.append("Cat eyes: +5% accuracy")
            elif base.train.lights_on:  # noqa: F821
                if "Floodlights" not in base.train.upgrades:  # noqa: F821
                    statuses.append("Dark: -10% accuracy")
            else:
                statuses.append("Dark: -20% accuracy")

        if self.energy <= 95:
            statuses.append("Tired: -{}% accuracy".format((100 - self.energy) // 5))

        if not base.world.is_in_city and self.current_part is not None:  # noqa: F821
            factor = round(self.damage_factor, 2)
            if factor != 1:
                statuses.append("Damage factor: x{}".format(factor))

        if self.health < 50 and "Hemophobia" in self.traits:
            statuses.append("Hemophobia: +25% energy spend")

        if self.is_diseased:
            statuses.append("Diseased: -20 max energy")

        if (
            "Motion sickness" in self.traits
            and base.train.ctrl.current_speed > 0.75  # noqa: F821
        ):
            statuses.append("Motion sickness: doesn't restore")

        return statuses[:4]

    @property
    def tooltip(self):
        """Tooltip to show on mouse pointing to this character.

        Returns:
            str: This character name.
        """
        return self.name

    def prepare(self):
        """Load the character model and positionate it.

        Tweak collision solid and sounds.
        """
        animations = {
            name: address(self.class_ + "-" + name)
            for name in (
                "die",
                "gun_up",
                "incline1",
                "release_gun",
                "stand_and_aim",
                "stand",
                "surrender",
                "tread1",
                "turn_head1",
                "stunned",
                "cough",
            )
        }
        self.model = Actor(address(self.sex + "_" + self.class_), animations)
        self.model.enableBlend()
        self.model.setControlEffect("stand", 1)

        self.model.setPlayRate(0.8, "stand_and_aim")
        self.model.setPlayRate(0.6, "stand")

        self.model.loop("stand")
        self._health_bar = HealthBar(self)

        taskMgr.doMethodLater(  # noqa: F821
            random.randint(40, 60), self._idle_animation, self.id + "_idle_anim"
        )
        self._col_node = self._init_col_node(
            NO_MASK, MOUSE_MASK, CollisionCapsule(0, 0, 0, 0, 0, 0.035, 0.035)
        )
        self.shot_snd = self._set_shoot_snd(self.class_data["shot_snd"])
        self._cough_snd = base.sound_mgr.loadSfx(  # noqa: F821
            "sounds/{sex}_cough.ogg".format(sex=self.sex)
        )
        base.sound_mgr.attachSoundToObject(self._cough_snd, self.model)  # noqa: F821

        if self.class_ == "soldier":
            z = 0.064 if self.sex == "male" else 0.062
        elif self.class_ == "raider":
            z = 0.047
        elif self.class_ == "anarchist":
            z = 0.06 if self.sex == "male" else 0.057

        self._shoot_anim = self._set_shoot_anim(
            (0.004, 0.045, z), 97, self.class_data["shots_num"]
        )
        taskMgr.doMethodLater(  # noqa: F821
            self.class_data["energy_spend"],
            self._reduce_energy,
            self.id + "_reduce_energy",
        )

    def move_to(self, part, to_pos=None):
        """Move this Character to the given Train part.

        If the movement is done with a positions exchange
        between two characters, the method doesn't
        take or release characters cells, just replaces
        one character with another one.

        Args:
            part (train_part.TrainPart):
                Train part to move this Character to.
            to_pos (dict):
                Position to move this Character to.

        Returns:
            bool: True, if the character was moved.
        """
        if to_pos:
            part.chars.append(self)
            pos = to_pos
        else:
            pos = part.give_cell(self)

        if not pos:  # no free cells on the chosen part
            return

        if self.current_part is not None:
            if to_pos:
                self.current_part.chars.remove(self)
            else:
                self.current_part.release_cell(self._current_pos, self)

            if self.current_part.name.startswith("part_rest_"):
                self.stop_rest()

        if part.name.startswith("part_rest_"):
            self.rest()

        self.model.wrtReparentTo(part.parent)
        self.model.setPos(pos)
        self.model.setH(part.angle)

        self.current_part = part
        self._current_pos = pos

        if (
            part.name == "part_rest_locomotive"
            and base.char_gui.rest_list_shown  # noqa: F821
        ):
            base.char_gui.update_resting_chars(part)  # noqa: F821

        return True

    def attack(self, enemy_unit):
        """Make the given enemy unit this character's target.

        Args:
            enemy_unit (personage.enemy.EnemyUnit):
                Enemy unit to attack.
        """
        if enemy_unit in self.current_part.enemies:
            self._target = enemy_unit

    def do_effects(self, effects):
        """Do outing effects to this character.

        Args:
            effects (dict): Effects and their values.
        """
        if effects is None:
            return

        effects = copy.deepcopy(effects)
        self.get_damage(-effects.pop("health", 0))

        trait = effects.get("add_trait")
        if trait and trait not in self.traits + self.disabled_traits:
            self.traits.append(trait)
            base.char_gui.move_status_label(-1)  # noqa: F821
            effects.pop("add_trait")

        for key, value in effects.items():
            if hasattr(self, key):
                setattr(self, key, getattr(self, key) + value)

    def prepare_to_fight(self):
        """Prepare the character to fight.

        Switch animations and run a task to choose a target.
        """
        self._stop_tasks("_idle_anim")
        if self._idle_seq is not None:
            self._idle_seq.finish()

        self.model.loop("stand_and_aim")
        LerpAnimInterval(self.model, 0.8, self._current_anim, "stand_and_aim").start()
        LerpAnimInterval(self.model, 0.8, "stand", "stand_and_aim").start()

        taskMgr.doMethodLater(  # noqa: F821
            0.5, self._choose_target, self.id + "_choose_target"
        )
        self._health_bar.show_health()

    def rest(self):
        """Make this character rest.

        Stops all the active tasks and
        starts energy regaining/healing.
        """
        self._stop_tasks(
            "_reduce_energy", "_shoot", "_aim", "_choose_target", "_idle_anim"
        )
        self.model.hide()
        self._col_node.stash()

        taskMgr.doMethodLater(  # noqa: F821
            0.05, self._calm_down, self.id + "_calm_down"
        )
        taskMgr.doMethodLater(  # noqa: F821
            self.class_data["energy_gain"], self._gain_energy, self.id + "_gain_energy"
        )
        if self.health < self.class_data["health"]:
            taskMgr.doMethodLater(  # noqa: F821
                self.class_data["healing"], self._heal, self.id + "_heal"
            )

    def surrender(self):
        """Stop fighting, surrender."""
        self._stop_tasks("_shoot", "_aim", "_choose_target")
        self._col_node.removeNode()
        self._shoot_anim.finish()

        LerpAnimInterval(self.model, 0.5, "stand_and_aim", "surrender").start()
        self.model.play("surrender")

    def stop_rest(self):
        """Stop this character rest."""
        self.model.show()
        self._col_node.unstash()
        base.char_gui.destroy_char_button(self.id)  # noqa: F821

        self._stop_tasks("_gain_energy", "_heal")
        taskMgr.doMethodLater(  # noqa: F821
            self.class_data["energy_spend"],
            self._reduce_energy,
            self.id + "_reduce_energy",
        )
        if base.world.enemy.active_units:  # noqa: F821
            self.prepare_to_fight()

    def _reduce_energy(self, task):
        """
        Reduce the character energy according to
        day part and status: fighting or not.
        """
        if base.world.sun.is_dark:  # noqa: F821
            if not base.train.lights_on:  # noqa: F821
                task.delayTime = 15
            elif "Floodlights" in base.train.upgrades:  # noqa: F821
                task.delayTime = self.class_data["energy_spend"]
            else:
                task.delayTime = 20

            if "Fear of dark" in self.traits:
                task.delayTime /= 2

        elif self._target:
            task.delayTime = 15 if "Nervousness" in self.traits else 20
        else:
            task.delayTime = self.class_data["energy_spend"]

        if "Hemophobia" in self.traits and self.health < self.class_data["health"] / 2:
            task.delayTime *= 0.75

        self.energy -= 1
        if "Mechanic" in self.traits:
            base.train.get_damage(-3)  # noqa: F821

        return task.again

    def _gain_energy(self, task):
        """Regain this character energy."""
        if (
            "Motion sickness" in self.traits
            and base.train.ctrl.current_speed > 0.75  # noqa: F821
        ):
            return task.again

        self.energy += 3

        for char in self.current_part.chars:
            if char.sex == "female" and self.id != char.id:
                task.delayTime = self.class_data["energy_gain"] - 5
                return task.again

        return task.again

    def _heal(self, task):
        """Regain this character health."""
        if (
            "Motion sickness" in self.traits
            and base.train.ctrl.current_speed > 0.75  # noqa: F821
        ):
            return task.again

        if "Pharmacophobia" in self.traits and chance(40):
            return task.again

        if self.health < self.class_data["health"]:
            self.health += 1
            return task.again

        return task.done

    def _choose_target(self, task):
        """Choose an enemy to shoot.

        Only an enemy from the Train part shooting
        range can be chosen as a target.
        """
        if self.current_part and self.current_part.enemies:
            self._target = random.choice(self.current_part.enemies)
            taskMgr.doMethodLater(0.1, self._aim, self.id + "_aim")  # noqa: F821
            taskMgr.doMethodLater(1, self._shoot, self.id + "_shoot")  # noqa: F821
            return task.done

        # enemies retreated - return to passive state
        if not base.world.enemy.active_units:  # noqa: F821
            taskMgr.doMethodLater(  # noqa: F821
                3, self._calm_down, self.id + "_calm_down"
            )
            return task.done

        return task.again

    def _aim(self, task):
        """Rotate the character to aim on enemy."""
        if self._target.is_dead and "Bloodthirsty" in self.traits:
            self.health += 7

        if self.current_part and self._target in self.current_part.enemies:
            self.model.headsUp(self._target.model)
            return task.again

        self._stop_tasks("_shoot")
        self._target = None

        if base.world.enemy.active_units:  # noqa: F821
            taskMgr.doMethodLater(  # noqa: F821
                0.5, self._choose_target, self.id + "_choose_target"
            )
            return task.done

        taskMgr.doMethodLater(3, self._calm_down, self.id + "_calm_down")  # noqa: F821
        return task.done

    def _calm_down(self, task):
        """Return to passive state."""
        self._stop_tasks("_shoot")
        if self.current_part:
            self.model.hprInterval(2, (self.current_part.angle, 0, 0)).start()

        LerpAnimInterval(self.model, 2, "stand_and_aim", "stand").start()
        taskMgr.doMethodLater(  # noqa: F821
            random.randint(40, 60), self._idle_animation, self.id + "_idle_anim"
        )
        self._health_bar.hide_health()
        return task.done

    def _idle_animation(self, task):
        """Play one of the idle animations.

        Args:
            task (panda3d.core.PythonTask): Task object.
        """
        if self.is_diseased and chance(80):
            self._current_anim = "cough"
            self._cough_snd.play()
        else:
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
        animation and plan the character clearing.
        """
        if self._team.hold_together:
            self.health = 1
            return False

        if not Shooter._die(self):
            return False

        Unit._die(self)

        self._health_bar.hide_health()
        self._stop_tasks("_reduce_energy", "_get_well", "_infect", "_stop_stimul")

        self._team.delete_relations(self.id)
        LerpAnimInterval(self.model, 0.3, "stand_and_aim", "die").start()
        self.model.hprInterval(1, (self.current_part.angle, 0, 0)).start()
        self.model.play("die")

        taskMgr.doMethodLater(3, self._hide, self.id + "_hide")  # noqa: F821

    def _hide(self, task):
        """Hide the main model."""
        self.model.hide()
        return task.done

    def leave(self):
        """Make this character leave, plan clearing.

        Used only when sending a character away in a city.
        """
        self._stop_tasks("_calm_down", "_gain_energy", "_heal", "_infect", "_get_well")
        taskMgr.doMethodLater(0.05, self.clear, self.id + "_clear")  # noqa: F821

    def clear(self, task):
        """Clear this character.

        Release models and sounds memory, release the part
        cell and delete the character from the team list.
        """
        self.model.cleanup()
        self._health_bar.removeNode()
        self.model.removeNode()
        base.sound_mgr.detach_sound(self.shot_snd)  # noqa: F821
        base.sound_mgr.detach_sound(self._cough_snd)  # noqa: F821

        self._team.chars.pop(self.id)
        base.res_gui.update_chars()  # noqa: F821
        self.current_part.release_cell(self._current_pos, self)
        self.current_part = None

        return task.done

    def exchange_pos(self, char):
        """Exchange positions of this Character and the given one.

        Args:
            char (personage.character.Character):
                Character to exchange the positions with.
        """
        o_part, o_pos = self.current_part, self._current_pos
        self.move_to(char.current_part, char._current_pos)
        char.move_to(o_part, o_pos)

    def hide_relations_ball(self):
        """Hide the relations ball of this character."""
        if self._cohesion_ball is not None:
            self._cohesion_ball.removeNode()
            self._cohesion_ball = None

    def show_relation(self, cohesion):
        """Show a relations ball above this character.

        The color of the ball shows the strength of cohesion
        between the chosen character and this one.

        Args:
            cohesion (float):
                Value of the cohesion between the
                chosen character and this one.
        """
        if self._cohesion_ball is None:
            self._cohesion_ball = loader.loadModel(  # noqa: F821
                address("relation_ball")
            )
            self._cohesion_ball.clearLight()
            base.world.sun.ignore_shadows(self._cohesion_ball)  # noqa: F821

            self._cohesion_ball.reparentTo(self.model)
            self._cohesion_ball.setZ(0.14)

        self._cohesion_ball.setColorScale(*RELATION_COLORS[cohesion // 20])

    def _missed_shot(self):
        """Calculate if character missed the current shot.

        Returns:
            bool: True if character missed, False otherwise.
        """
        miss_chance = 0
        if self.class_ == "soldier":
            if (
                abs(self._target.node.getX()) < 0.56
                and abs(self._target.node.getY()) < 0.95
            ):
                miss_chance += 20
        elif self.class_ == "raider":
            if (
                abs(self._target.node.getX()) > 0.56
                and abs(self._target.node.getY()) > 0.95
            ):
                miss_chance += 20

        if base.world.sun.is_dark:  # noqa: F821
            if "Cat eyes" in self.traits:
                miss_chance -= 5
            elif base.train.lights_on:  # noqa: F821
                if "Floodlights" not in base.train.upgrades:  # noqa: F821
                    miss_chance += 10
            else:
                miss_chance += 20

        miss_chance += (100 - self.energy) // 5
        if self._team.cover_fire:
            miss_chance = min(100, max(0, miss_chance - 25))

        return chance(miss_chance)

    def get_stunned(self, duration):
        """Make this character stunned for some time.

        Stunned unit can't shoot.

        Args:
            duration (float): Stun duration in seconds.
        """
        if self._is_stunned or self._is_stimulated:
            return

        self._is_stunned = True
        self._stop_tasks("_aim", "_shoot")

        self._current_anim = "stunned"
        self.model.play("stunned")
        LerpAnimInterval(self.model, 0.05, "stand_and_aim", "stunned").start()

        taskMgr.doMethodLater(  # noqa: F821
            duration, self._stop_stunning, self.id + "_stop_stunning"
        )

    def get_sick(self, is_infect=False):
        """Calculations to get this character sick.

        The worse condition the character has the higher is the chance
        for him to get sick. Sick character has lower energy maximum,
        and all his positive traits are disabled until getting well.

        Args:
            is_infect (bool):
                True if the disease came from a
                character on the same Train part.
        """
        if self.is_diseased:
            return

        cond_percent = (self.energy + self.health) / (100 + self.class_data["health"])
        percent = (1 - cond_percent) * 30

        sick_chance = max(
            0,  # not less than zero
            (
                percent
                + (20 if is_infect else 0)
                - (40 if "Immunity" in self.traits else 0)
                + (20 if "Weak immunity" in self.traits else 0)
            ),
        )

        if chance(sick_chance):
            self.is_diseased = True
            self.get_well_score = 0

            for traits_pair in TRAITS:
                if traits_pair[0] in self.traits:

                    self.traits.remove(traits_pair[0])
                    self.disabled_traits.append(traits_pair[0])

            taskMgr.doMethodLater(  # noqa: F821
                60, self.get_well, self.id + "_get_well"
            )
            taskMgr.doMethodLater(240, self.infect, self.id + "_infect")  # noqa: F821
            self.energy = min(self.energy, 80)

    def get_stimulated(self):
        """Use a stimulator on this character.

        Disables all the negative traits for some time.
        """
        for traits_pair in TRAITS:
            if traits_pair[1] in self.traits:
                self.traits.remove(traits_pair[1])
                self.disabled_traits.append(traits_pair[1])

        self._is_stimulated = True
        taskMgr.doMethodLater(  # noqa: F821
            300, self._stop_stimul, self.id + "_stop_stimul"
        )

    def _stop_stimul(self, task):
        """Stop stimulation of this character.

        Returns back all the disabled negative traits.
        """
        for trait_pair in TRAITS:
            if trait_pair[1] in self.disabled_traits:
                self.traits.append(trait_pair[1])
                self.disabled_traits.remove(trait_pair[1])

        self._is_stimulated = False
        return task.done

    def get_well(self, task):
        """Get this character well.

        When the character got well, his energy maximum is restored to
        the default value, and his positive traits are back operational.
        """
        self.get_well_score += 1
        if self.get_well_score < 20:
            return task.again

        self.is_diseased = False
        for trait_pair in TRAITS:
            if trait_pair[0] in self.disabled_traits:
                self.traits.append(trait_pair[0])
                self.disabled_traits.remove(trait_pair[0])

        self._stop_tasks("_infect")
        return task.done

    def infect(self, task):
        """Infect other characters on the same Train part."""
        for char in self.current_part.chars:
            if char.id != self.id:
                char.get_sick(is_infect=True)

        return task.again

    def _shoot(self, task):
        """Play shooting animation and sound, make damage."""
        if self.current_part and not self.current_part.is_covered:
            return Shooter._shoot(self, task)

        return task.again

    def _stop_stunning(self, task):
        """Stop this character stun and continue fighting."""
        self._is_stunned = False

        LerpAnimInterval(self.model, 0.8, self._current_anim, "stand_and_aim").start()
        self._current_anim = "stand_and_aim"
        self.model.loop("stand_and_aim")

        taskMgr.doMethodLater(0.1, self._aim, self.id + "_aim")  # noqa: F821
        taskMgr.doMethodLater(1, self._shoot, self.id + "_shoot")  # noqa: F821

        return task.done

    def get_damage(self, damage):
        """Getting damage.

        Args:
            damage (int): Damage points to get.
        """
        if "Masochism" in self.traits:
            self.energy += 1

        Unit.get_damage(self, damage)

    def get_stench_damage(self):
        """Get damage from the Stench."""
        if "Deep breath" in self.traits and self.inhale > 0:
            self.inhale -= 1
            return

        self.get_damage(1)


def generate_char(id_, class_, sex, team=None):
    """Generate character with the given parameters.

    Args:
        id_ (str): Character id.
        class_ (str): Character class.
        sex (str): Character gender.
        team (team.Team): Optional. Team to add new character into.

    Returns:
        Character: The generated character.
    """
    return Character(id_, random.choice(NAMES[sex]), class_, sex, team)


def load_char(desc, team, parts):
    """Load a char using the given description.

    Load the model, state and move to the saved position.

    Args:
        desc (dict): Character description.
        team (team.Team): The team object.
        parts (dict): Train parts index.

    Returns:
        character.Character: A ready-to-go character object.
    """
    char = Character(desc["id"], desc["name"], desc["class"], desc["sex"], team, desc)
    char.health = desc["health"]
    char.prepare()
    char.move_to(parts[desc["place"]])
    return char
