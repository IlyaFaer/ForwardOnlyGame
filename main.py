"""Main game file. Starts the game itself and maintains the main systems."""
from direct.directutil import Mopath
from direct.interval.MopathInterval import MopathInterval
from direct.interval.IntervalGlobal import Sequence, Func
from direct.showbase.ShowBase import ShowBase

from railway_generator import RailwayGenerator


class ForwardOnly(ShowBase):
    """Object, which represents the game itself.

    Includes the main game systems.
    """

    def __init__(self):
        ShowBase.__init__(self)

        self._last_block = None

        self._path = RailwayGenerator().generate_path(300)
        self._rail_blocks, self._rails = self._load_rail_blocks()

        # set Train node
        self._train = self.render.attachNewNode("Train")
        train = self.loader.loadModel("models/bam/locomotive.bam")
        train.reparentTo(self._train)

        # start moving
        self._move_along_block(train)

        self.cam.setPos(10, -14, 17)
        self.cam.lookAt(train)

    # TODO: calibrate movement, as after some time passed
    # Train diverges from railways.
    def _move_along_block(self, model, block_num=0):
        """Move model along the next motion path.

        Args:
            model (NodePath): Model to move.
            block_num (int): Number of current path block.
        """
        name = self._path[block_num]

        # prepare model to move along next motion path
        model.wrtReparentTo(self.render)
        self._train.setPos(model.getPos())
        self._train.setHpr(model, 0)

        if block_num == 0:
            self._last_block = self.loader.loadModel(self._rails[name])
            self._last_block.reparentTo(self.render)
            self._last_block.setPos(model.getPos())
            self._last_block.setHpr(self._train, 0)

        model.wrtReparentTo(self._train)

        path_int2 = MopathInterval(
            self._rail_blocks[name], model, duration=2, name="current_path"
        )
        Sequence(path_int2, Func(self._move_along_block, model, block_num + 1)).start()

        pos = self._train.getPos()
        pos.setZ(pos.getZ() + 17)
        pos.setX(pos.getX() + 10)
        pos.setY(pos.getY() - 14)

        self.cam.setPos(pos)
        self.cam.lookAt(self._train)

        next_name = self._path[block_num + 1]
        next_rails = self.loader.loadModel(self._rails[next_name])
        next_rails.reparentTo(self._last_block)

        final_pos = self._rail_blocks[name].getFinalState()[0]
        next_rails.setPos(final_pos)

        if name == "r90_turn":
            next_rails.setHpr(-90, 0, 0)

        if name == "l90_turn":
            next_rails.setHpr(90, 0, 0)

        self._last_block = next_rails

    def _load_rail_blocks(self):
        """Load all rail blocks into the inner index.

        Returns:
            dict: Index of rail blocks in form {name: RailBlock}.
        """
        paths = {}
        rails = {}

        for key, path, model in {
            ("direct", "models/bam/direct_path.bam", "models/bam/direct_rails.bam"),
            (
                "l90_turn",
                "models/bam/l90_turn_path.bam",
                "models/bam/l90_turn_rails.bam",
            ),
            (
                "r90_turn",
                "models/bam/r90_turn_path.bam",
                "models/bam/r90_turn_rails.bam",
            ),
        }:
            paths[key] = Mopath.Mopath(objectToLoad=path)
            paths[key].fFaceForward = True
            rails[key] = model

        return paths, rails


ForwardOnly().run()
