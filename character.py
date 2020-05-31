"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Characters and enemies API.
"""
import random
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import LerpAnimInterval, Sequence
from panda3d.core import CollisionCapsule, CollisionNode

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


class Character:
    """Game character.

    Character can be generated for the given type.

    Args:
        id_ (int): Character unique id.
    """

    def __init__(self, id_):
        self._current_part = None
        self._current_pos = None

        self.name = None
        self.mod_name = None
        self.model = None
        self.id = "character_" + str(id_)

    def generate(self, type_):
        """Generate character of the given type.

        Args:
            type_ (str):
                Character type name. Describes names and
                models to be used while character generation.
        """
        self.name = random.choice(NAMES[type_])
        self.mod_name = address(random.choice(MODELS[type_]))

    def prepare(self, loader, taskMgr):
        """Load character model and positionate it.

        Tweak collision solid.

        Args:
            loader (direct.showbase.Loader.Loader): Panda3D models loader.
            taskMgr (direct.task.Task.TaskManager): Task manager.
        """
        self.model = Actor(self.mod_name)
        self.model.enableBlend()
        self.model.setControlEffect("stand", 1)

        self.model.setPlayRate(0.8, "stand_and_aim")
        self.model.setPlayRate(0.6, "stand")

        self.model.loop("stand")

        taskMgr.doMethodLater(
            random.randint(40, 60),
            self._idle_animation,
            "{id_}_idle_anim".format(id_=self.id),
        )
        col_solid = CollisionCapsule(0, 0, 0, 0, 0, 0.035, 0.035)
        col_node = self.model.attachNewNode(CollisionNode(str(self.id)))
        col_node.node().addSolid(col_solid)

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

    def _idle_animation(self, task):
        """Play one of the idle animations.

        Args:
            task (panda3d.core.PythonTask): Task object.
        """
        new_anim = random.choice(("turn_head1", "release_gun"))
        LerpAnimInterval(self.model, 0.3, "stand", new_anim).start()

        Sequence(
            self.model.actorInterval(new_anim, playRate=0.75),
            LerpAnimInterval(self.model, 0.3, new_anim, "stand"),
        ).start()

        task.delayTime = random.randint(40, 60)
        return task.again
