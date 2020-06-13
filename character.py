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
        "Eric",
        "Frank",
        "James",
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

            char = Character(self._char_id)
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


class Character:
    """Game character.

    Character can be generated for the given type.

    Args:
        id_ (int): Character unique id.
    """

    def __init__(self, id_):
        self._current_part = None
        self._current_pos = None
        self._current_anim = None
        self._idle_seq = None
        self._target = None  # target enemy id
        self._attacking_enemies = None

        self.name = None
        self.mod_name = None
        self.model = None
        self.id = "character_" + str(id_)

    def generate(self, type_):
        """Generate a character of the given type.

        Args:
            type_ (str):
                Character type name. Describes names and
                models to be used while character generation.
        """
        self.name = random.choice(NAMES[type_])
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
        self.model.attachNewNode(col_node)

    def move_to(self, part):
        """Move this Character to the given train part.

        Args:
            part (train.TrainPart):
                Train part to move this Character to.
        """
        pos = part.give_cell()
        if not pos:  # no free cells on the chosen part
            return

        if self._current_part is not None:
            self._current_part.release_cell(self._current_pos)

        self.model.wrtReparentTo(part.parent)
        self.model.setPos(pos["pos"])
        self.model.setH(pos["angle"])

        self._current_part = part
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
        if self._current_part.enemies_in_range:
            self._target = random.choice(self._current_part.enemies_in_range)
            base.taskMgr.doMethodLater(0.1, self._aim, self.id + "_aim")  # noqa: F821
            return task.done

        # enemies retreated - return to passive state
        if not self._attacking_enemies:
            self._calm_down()
            return task.done

        return task.again

    def _aim(self, task):
        """Rotate the character to aim on enemy."""
        if self._target in self._current_part.enemies_in_range:
            self.model.headsUp(self._attacking_enemies[self._target].model)
            return task.again

        if self._attacking_enemies:
            base.taskMgr.doMethodLater(  # noqa: F821
                0.5, self._choose_target, self.id + "_choose_target"
            )
            return task.done

        self._target = None
        self._calm_down()
        return task.done

    def _calm_down(self):
        """Return to passive state."""
        self.model.hprInterval(2, (self._current_pos["angle"], 0, 0)).start()

        LerpAnimInterval(self.model, 0.8, "stand_and_aim", "stand").start()
        base.taskMgr.doMethodLater(  # noqa: F821
            random.randint(40, 60),
            self._idle_animation,
            "{id_}_idle_anim".format(id_=self.id),
        )

    def _idle_animation(self, task):
        """Play one of the idle animations.

        Args:
            task (panda3d.core.PythonTask): Task object.
        """
        self._current_anim = random.choice(("turn_head1", "release_gun"))
        LerpAnimInterval(self.model, 0.3, "stand", self._current_anim).start()

        self._idle_seq = Sequence(
            self.model.actorInterval(self._current_anim, playRate=0.75),
            LerpAnimInterval(self.model, 0.3, self._current_anim, "stand"),
        )
        self._idle_seq.start()

        task.delayTime = random.randint(40, 60)
        return task.again
