"""Train - the main game object, API."""
import random
from direct.actor.Actor import Actor
from panda3d.core import CollisionNode, CollisionPolygon, Point3

from controls import TrainController

MOD_DIR = "models/bam/"


class Train:
    """Train object. The main game object.

    Args:
        game (ForwardOnly): Game object.
    """

    def __init__(self, game):
        # root Train node
        self.root_node = game.render.attachNewNode("train_root")
        # node to hold camera and Sun
        self.node = self.root_node.attachNewNode("train")

        self.model = Actor(MOD_DIR + "locomotive.bam")
        self.model.reparentTo(self.root_node)

        self._ctrl = TrainController(game, self.model)
        self._ctrl.set_controls()

        self.parts = {
            "part_arrow_locomotive_left": TrainPart(
                game.loader,
                self.model,
                "part_arrow_locomotive_left",
                positions=[
                    {"pos": (-0.07, -0.02, 0.147), "angle": -90},
                    {"pos": (-0.07, 0.15, 0.147), "angle": -90},
                ],
                arrow_pos={"pos": (-0.2, 0.09, 0.147), "angle": 90},
            ),
            "part_arrow_locomotive_right": TrainPart(
                game.loader,
                self.model,
                "part_arrow_locomotive_right",
                positions=[
                    {"pos": (0.07, -0.02, 0.147), "angle": 90},
                    {"pos": (0.07, 0.15, 0.147), "angle": 90},
                ],
                arrow_pos={"pos": (0.2, 0.09, 0.147), "angle": -90},
            ),
            "part_arrow_locomotive_front": TrainPart(
                game.loader,
                self.model,
                "part_arrow_locomotive_front",
                positions=[{"pos": (0, 0.42, 0.147), "angle": 180}],
                arrow_pos={"pos": (0, 0.55, 0.147), "angle": 0},
            ),
        }

    def move_along_block(self, block):
        """Move Train along the given world block.

        Args:
            block (world.block.Block): world block to move along.
        """
        self._ctrl.move_along_block(block, self.node)


class TrainPart:
    """Train part where characters can be set.

    Args:
        loader (direct.showbase.Loader.Loader): Panda3D models loader.
        parent (panda3d.core.NodePath):
                Model, to which arrow sprite of
                this part should be parented.
        id_ (str): Part id.
        positions (list):
            Dicts describing possible positions and
            rotations on this TrainPart.
        arrow_pos (dict): Arrow sprite position and rotation.
    """

    def __init__(self, loader, parent, id_, positions, arrow_pos):
        self.id = id_
        self._free = positions
        self._taken = []
        self._parent = parent

        # organize a manipulating arrow
        self._arrow = loader.loadModel(MOD_DIR + "train_part_arrow.bam")
        self._arrow.setPos(*arrow_pos["pos"])
        self._arrow.setH(arrow_pos["angle"])

        col_solid = CollisionPolygon(
            Point3(-0.06, -0.06, 0),
            Point3(-0.06, 0.06, 0),
            Point3(0.06, 0.06, 0),
            Point3(0.06, -0.06, 0),
        )
        col_solid.flip()
        col_node = self._arrow.attachNewNode(CollisionNode(self.id))
        col_node.node().addSolid(col_solid)

    def give_cell(self):
        """Choose non taken cell.

        Returns:
            dict: Position and rotation to set character.
        """
        if not self._free:
            return

        position = random.choice(self._free)
        self._free.remove(position)
        self._taken.append(position)
        return position

    def release_cell(self, position):
        """Release cell taken earlier.

        Args:
            position (dict):
                Position and rotation of the taken cell.
        """
        self._taken.remove(position)
        self._free.append(position)

    def show_arrow(self):
        """Show manipulating arrow if this TrainPart."""
        self._arrow.reparentTo(self._parent)

    def hide_arrow(self):
        """Hide manipulating arrow if this TrainPart."""
        self._arrow.detachNode()
