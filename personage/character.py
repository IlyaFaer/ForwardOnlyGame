"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Characters (player units) API.
"""
import random

from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import LerpAnimInterval, Sequence
from panda3d.core import CollisionCapsule

from const import MOUSE_MASK, NO_MASK
from utils import address, chance

from .character_data import NAMES, CLASSES
from .shooter import Shooter
from .unit import Unit


class Character(Shooter, Unit):
    """Game character.

    Args:
        id_ (int): Character unique id.
        name (str): Character name.
        class_ (str): Unit class.
        sex (str): Character gender.
        team (team.Team): Team object.
    """

    def __init__(self, id_, name, class_, sex, team):
        Unit.__init__(
            self, "character_" + str(id_), class_, CLASSES[sex + "_" + class_]
        )
        Shooter.__init__(self)

        self._team = team

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

    @property
    def description(self):
        """This character saveable parameters.

        Used for saving the character.

        Returns:
            dict: This character description.
        """
        desc = {
            "id": int(self.id.split("_")[1]),
            "name": self.name,
            "sex": self.sex,
            "class": self.class_,
            "health": self.health,
            "energy": self.energy,
            "place": self.current_part.name,
        }
        return desc

    def prepare(self):
        """Load the character model and positionate it.

        Tweak collision solid as well.
        """
        self.model = Actor(
            address(self.sex + "_" + self.class_),
            {
                "die": address(self.class_ + "-die"),
                "gun_up": address(self.class_ + "-gun_up"),
                "incline1": address(self.class_ + "-incline1"),
                "release_gun": address(self.class_ + "-release_gun"),
                "stand_and_aim": address(self.class_ + "-stand_and_aim"),
                "stand": address(self.class_ + "-stand"),
                "surrender": address(self.class_ + "-surrender"),
                "tread1": address(self.class_ + "-tread1"),
                "turn_head1": address(self.class_ + "-turn_head1"),
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
        self.shot_snd = self._set_shoot_snd(self.class_data["shot_snd"])

        if self.class_ == "soldier":
            z = 0.064 if self.sex == "male" else 0.062
        elif self.class_ == "raider":
            z = 0.047

        self._shoot_anim = self._set_shoot_anim(
            (0.004, 0.045, z), 97, self.class_data["shots_num"]
        )
        base.taskMgr.doMethodLater(  # noqa: F821
            self.class_data["energy_spend"],
            self._reduce_energy,
            self.id + "_reduce_energy",
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
                self.stop_rest()

        if part.name.startswith("part_rest_"):
            self.rest()

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

    def rest(self):
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

    def stop_rest(self):
        """Stop this character rest."""
        self.model.show()
        self._col_node.unstash()
        base.char_interface.destroy_char_button(self.id)  # noqa: F821

        base.taskMgr.remove(self.id + "_gain_energy")  # noqa: F821
        base.taskMgr.remove(self.id + "_heal")  # noqa: F821
        base.taskMgr.doMethodLater(  # noqa: F821
            self.class_data["energy_spend"],
            self._reduce_energy,
            self.id + "_reduce_energy",
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
            task.delayTime = self.class_data["energy_spend"]

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

    def leave(self):
        """Make this character leave, plan clearing.

        Used only when sending a character away in a city.
        """
        base.taskMgr.remove(self.id + "_calm_down")  # noqa: F821
        base.taskMgr.remove(self.id + "_gain_energy")  # noqa: F821
        base.taskMgr.remove(self.id + "_heal")  # noqa: F821
        base.taskMgr.doMethodLater(0.05, self.clear, self.id + "_clear")  # noqa: F821

    def clear(self, task):
        """Clear this character.

        Release models and sounds memory, release the part
        cell and delete the character from the team list.
        """
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
        elif self.class_ == "raider":
            if (
                abs(self._target.node.getX()) > 0.5
                and abs(self._target.node.getY()) > 0.95
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
        character.Character: Ready-to-go character object.
    """
    char = Character(desc["id"], desc["name"], desc["class"], desc["sex"], team)
    char.health = desc["health"]
    char.energy = desc["energy"]

    char.prepare()
    char.move_to(parts[desc["place"]])
    return char
