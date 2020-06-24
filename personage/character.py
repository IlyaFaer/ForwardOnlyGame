"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Characters (player units) API.
"""
import random
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import LerpAnimInterval, Sequence
from panda3d.core import CollisionCapsule, CollisionNode

from const import MOUSE_MASK, NO_MASK
from .shooter import Shooter
from utils import address

NAMES = {
    "male": (
        "Aaron",
        "Alex",
        "Alexis",
        "Arnold",
        "Ben",
        "Bruce",
        "Chris",
        "Cody",
        "Cory",
        "Craig",
        "Donnie",
        "Ed",
        "Elijah",
        "Eric",
        "Frank",
        "James",
        "Jerome",
        "Josh",
        "Justin",
        "Max",
        "Mike",
        "Nathan",
        "Paul",
        "Peter",
        "Roy",
        "Shawn",
        "Sid",
        "Steven",
        "Tim",
        "Thomas",
        "Tyler",
    )
}
MODELS = {"male": ("character1",)}


class Team:
    """All characters (player units) object."""

    def __init__(self):
        self._char_id = 0  # variable to count character ids
        self.chars = {}

    def gen_default(self, train_parts):
        """Generate default team.

        Args:
            train_pargs (dict):
                Train parts to set characters on.
        """
        for part in (
            train_parts["part_locomotive_right"],
            train_parts["part_locomotive_right"],
            train_parts["part_locomotive_front"],
        ):
            self._char_id += 1

            char = Character(self._char_id, self)
            char.generate("male")
            char.prepare()
            char.move_to(part)

            self.chars[char.id] = char

    def prepare_to_fight(self, attacking_enemies):
        """Prepare every character to fight.

        Args:
            attacking_enemies (dict): Attacking units index.
        """
        for char in self.chars.values():
            char.prepare_to_fight(attacking_enemies)


class Character(Shooter):
    """Game character.

    Character can be generated for the given type.

    Args:
        id_ (int): Character unique id.
        team (Team): Team object.
    """

    def __init__(self, id_, team):
        super().__init__()
        self._team = team

        self._current_pos = None
        self._current_anim = None
        self._idle_seq = None
        self._attacking_enemies = None

        self.name = None
        self.type = None
        self.mod_name = None
        self.model = None

        self.damage = (3, 5)
        self.id = "character_" + str(id_)

    def generate(self, type_):
        """Generate a character of the given type.

        Args:
            type_ (str):
                Character type name. Describes names and
                models to be used while character generation.
        """
        self.name = random.choice(NAMES[type_])
        self.type = "Soldier"
        self.mod_name = address(random.choice(MODELS[type_]))

    def prepare(self):
        """Load the character model and positionate it.

        Tweak collision solid as well.
        """
        self.model = Actor(self.mod_name)
        self.model.enableBlend()
        self.model.setControlEffect("stand", 1)

        self.model.setPlayRate(0.8, "stand_and_aim")
        self.model.setPlayRate(0.6, "stand")

        self.model.loop("stand")

        base.taskMgr.doMethodLater(  # noqa: F821
            random.randint(40, 60),
            self._idle_animation,
            "{id_}_idle_anim".format(id_=self.id),
        )
        # set character collisions
        col_node = CollisionNode(self.id)
        col_node.setFromCollideMask(NO_MASK)
        col_node.setIntoCollideMask(MOUSE_MASK)
        col_node.addSolid(CollisionCapsule(0, 0, 0, 0, 0, 0.035, 0.035))
        self._col_node = self.model.attachNewNode(col_node)

        self.shot_snd = self._set_shoot_snd("rifle_shot1")
        self._shoot_anim = self._set_shoot_anim((0.004, 0.045, 0.064), 97)

    def move_to(self, part):
        """Move this Character to the given train part.

        Args:
            part (train.TrainPart):
                Train part to move this Character to.
        """
        pos = part.give_cell(self)
        if not pos:  # no free cells on the chosen part
            return

        if self.current_part is not None:
            self.current_part.release_cell(self._current_pos, self)

        self.model.wrtReparentTo(part.parent)
        self.model.setPos(pos["pos"])
        self.model.setH(pos["angle"])

        self.current_part = part
        self._current_pos = pos

    def prepare_to_fight(self, enemies):
        """Prepare the character to fight.

        Switch animations and run a task to choose a target.

        Args:
            enemies (dict): Attacking enemies index.
        """
        self._attacking_enemies = enemies

        base.taskMgr.remove(self.id + "_idle_anim")  # noqa: F821
        if self._idle_seq is not None:
            self._idle_seq.finish()

        self.model.loop("stand_and_aim")
        LerpAnimInterval(self.model, 0.8, self._current_anim, "stand_and_aim").start()
        LerpAnimInterval(self.model, 0.8, "stand", "stand_and_aim").start()

        base.taskMgr.doMethodLater(  # noqa: F821
            0.5, self._choose_target, self.id + "_choose_target"
        )

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
        if not self._attacking_enemies:
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

        if self._attacking_enemies:
            base.taskMgr.doMethodLater(  # noqa: F821
                0.5, self._choose_target, self.id + "_choose_target"
            )
            return task.done

        self._target = None
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
            random.randint(40, 60),
            self._idle_animation,
            "{id_}_idle_anim".format(id_=self.id),
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
        if not self.is_dead:
            self.is_dead = True

            base.taskMgr.remove(self.id + "_aim")  # noqa: F821
            base.taskMgr.remove(self.id + "_shoot")  # noqa: F821
            base.taskMgr.remove(self.id + "_choose_target")  # noqa: F821
            self._col_node.removeNode()

            self._shoot_anim.finish()
            LerpAnimInterval(self.model, 0.3, "stand_and_aim", "die").start()
            self.model.hprInterval(1, (self._current_pos["angle"], 0, 0)).start()
            self.model.play("die")

            base.taskMgr.doMethodLater(3, self._hide, self.id + "_hide")  # noqa: F821
            base.taskMgr.doMethodLater(  # noqa: F821
                3.5, self._clear, self.id + "_clear"
            )

    def _hide(self, task):
        """Hide the main model."""
        self.model.hide()
        return task.done

    def _clear(self, task):
        """Clear this character."""
        self.model.cleanup()
        self.model.removeNode()
        base.sound_mgr.detach_sound(self.shot_snd)  # noqa: F821

        self._team.chars.pop(self.id)
        self.current_part.release_cell(self._current_pos, self)
        self.current_part = None

        return task.done
