"""Main game file. Starts the game itself."""
import random

from direct.directutil import Mopath
from direct.interval.MopathInterval import MopathInterval
from direct.interval.IntervalGlobal import Sequence, Func
from direct.showbase.ShowBase import ShowBase


class ForwardOnly(ShowBase):
    """Object, which represents the game itself."""

    def __init__(self):
        ShowBase.__init__(self)

        self._rail_blocks = self._load_rail_blocks()

        # load dummy model
        box = self.loader.loadModel("models/bam/box.bam")
        box.reparentTo(self.render)

        # set Train node
        self._train = self.render.attachNewNode("Train")
        box.wrtReparentTo(self._train)

        # start moving
        self._move_along_next(box, is_start=True)

        self.cam.setPos(0, 0, 100)
        self.cam.lookAt(box)

    def _move_along_next(self, model, is_start=False):
        """Move model along the next motion path.

        Args:
            model (NodePath): Model to move.
            is_start (bool): True if this is the first rail block.
        """
        name = "direct" if is_start else random.choice(("l90_turn", "direct"))

        # prepare model to move along next motion path
        model.wrtReparentTo(self.render)
        self._train.setPos(model.getPos())
        self._train.setHpr(model, self._rail_blocks[name].angle)
        model.wrtReparentTo(self._train)

        path_int2 = MopathInterval(
            self._rail_blocks[name].mopath, model, duration=2, name="current_path"
        )
        seq = Sequence(path_int2, Func(self._move_along_next, model))
        seq.start()

    def _load_rail_blocks(self):
        """Load all rail blocks into the inner index.

        Returns:
            dict: Index of rail blocks in form {name: RailBlock}.
        """
        blocks = {}

        for key, file_name in {
            "direct": "models/bam/direct_path.bam",
            "l90_turn": "models/bam/l90_turn_path.bam",
        }.items():
            path = Mopath.Mopath(objectToLoad=file_name)
            path.fFaceForward = True

            blocks[key] = RailBlock(key, path)

        return blocks


class RailBlock:
    """Object which represents single railway block."""

    # angle to which model should be rotated
    # to switch to the next path correctly
    angles = {"direct": (90, 0, 0), "l90_turn": 0}

    def __init__(self, name, mopath):
        self.mopath = mopath
        self.angle = self.angles[name]


ForwardOnly().run()
