"""Characters and enemies API."""
import random
from direct.actor.Actor import Actor
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

    def prepare(self, loader):
        """Load character model and positionate it.

        Tweak collision solid.

        Args:
            loader (direct.showbase.Loader.Loader): Panda3D models loader.
        """
        self.model = Actor(self.mod_name)
        self.model.setPlayRate(0.8, "stand_and_aim")
        self.model.loop("stand_and_aim")

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
