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
        train = self.loader.loadModel("models/bam/locomotive.bam")
        train.reparentTo(self.render)

        # set Train node
        self._train = self.render.attachNewNode("Train")
        train.wrtReparentTo(self._train)

        # start moving
        self._move_along_next(train, is_start=True)

        self.cam.setPos(8, 12, 15)
        self.cam.lookAt(train)

    def _move_along_next(self, model, is_start=False):
        """Move model along the next motion path.

        Args:
            model (NodePath): Model to move.
            is_start (bool): True if this is the first rail block.
        """
        name = (
            "direct" if is_start else random.choice(("r90_turn", "direct", "l90_turn"))
        )
        print(name)

        # prepare model to move along next motion path
        model.wrtReparentTo(self.render)
        self._train.setPos(model.getPos())
        self._train.setHpr(model, 0)
        model.wrtReparentTo(self._train)

        path_int2 = MopathInterval(
            self._rail_blocks[name], model, duration=10, name="current_path"
        )
        seq = Sequence(path_int2, Func(self._move_along_next, model))
        seq.start()
        pos = self._train.getPos()
        pos.setZ(pos.getZ() + 10)
        pos.setX(pos.getX() + 18)

        self.cam.setPos(pos)
        self.cam.lookAt(self._train)

    def _load_rail_blocks(self):
        """Load all rail blocks into the inner index.

        Returns:
            dict: Index of rail blocks in form {name: RailBlock}.
        """
        paths = {}

        for key, file_name in {
            "direct": "models/bam/direct_path.bam",
            "l90_turn": "models/bam/l90_turn_path.bam",
            "r90_turn": "models/bam/r90_turn_path.bam",
        }.items():
            paths[key] = Mopath.Mopath(objectToLoad=file_name)
            paths[key].fFaceForward = True

        return paths


ForwardOnly().run()
