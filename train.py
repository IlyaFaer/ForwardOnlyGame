"""Train - the main game object, API."""
import random
from direct.actor.Actor import Actor
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

        self.parts = (
            TrainPart(  # left side
                [
                    {"pos": (-0.07, -0.02, 0.147), "angle": -90},
                    {"pos": (-0.07, 0.15, 0.147), "angle": -90},
                ]
            ),
            TrainPart(  # right side
                [
                    {"pos": (0.07, -0.02, 0.147), "angle": 90},
                    {"pos": (0.07, 0.15, 0.147), "angle": 90},
                ]
            ),
            # front side
            TrainPart([{"pos": (0, 0.42, 0.147), "angle": 180}]),
        )

    def move_along_block(self, block):
        """Move Train along the given world block.

        Args:
            block (world.block.Block): world block to move along.
        """
        self._ctrl.move_along_block(block, self.node)


class TrainPart:
    """Train part where characters can be set.

    Args:
        positions (list):
            Dicts describing possible positions and
            rotations on this TrainPart.
    """

    def __init__(self, positions):
        self._free = positions
        self._taken = []

    def give_cell(self):
        """Choose non taken cell.

        Returns:
            dict: Position and rotation to set character.
        """
        if not self._free:
            return None

        position = random.choice(self._free)
        self._free.remove(position)
        self._taken.append(position)
        return position
