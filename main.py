"""Main game file. Starts the game itself and maintains the main systems."""
from direct.directutil import Mopath
from direct.interval.MopathInterval import MopathInterval
from direct.interval.IntervalGlobal import Sequence, Func
from direct.showbase.ShowBase import ShowBase

from railway_generator import RailwayGenerator
from world import World

MOD_DIR = "models/bam/"


class ForwardOnly(ShowBase):
    """Object, which represents the game itself.

    Includes the main game systems.
    """

    def __init__(self):
        ShowBase.__init__(self)

        self._world = World(self.render)

        self._path_map = RailwayGenerator().generate_path(300)
        self._paths, self._rails = self._load_rail_blocks()

        # set Train node
        self._train = self.render.attachNewNode("Train")
        train_mod = self.loader.loadModel(MOD_DIR + "locomotive.bam")
        train_mod.reparentTo(self._train)

        # set first path block
        self._last_block = self.loader.loadModel(self._rails["direct"])
        self._last_block.reparentTo(self.render)

        # start moving
        self._move_along_block(train_mod, 0)

        self.cam.reparentTo(train_mod)
        self.cam.setPos(0, -2, 3)
        self.cam.lookAt(train_mod)

    def _move_along_block(self, train_mod, block_num):
        """Move Train model along the next motion path.

        Args:
            train_mod (NodePath): Train model to move.
            block_num (int): Current path block number.
        """
        # prepare model to move along next motion path
        train_mod.wrtReparentTo(self.render)
        pos = train_mod.getPos()
        hpr = train_mod.getHpr()

        # round Train position to avoid increasing position error
        train_mod.setPos(round(pos.getX()), round(pos.getY()), round(pos.getZ()))
        train_mod.setHpr(round(hpr.getX()), round(hpr.getY()), round(hpr.getZ()))

        self._train.setPos(train_mod.getPos(self.render))
        self._train.setHpr(train_mod, 0)
        train_mod.wrtReparentTo(self._train)

        # move camera
        # cam_pos = self._train.getPos()
        # cam_pos.setY(cam_pos.getY() + 4)
        # cam_pos.setZ(cam_pos.getZ() + 3)
        # self.cam.setPos(cam_pos)
        # self.cam.lookAt(self._train)

        # load next path block
        next_rails = self.loader.loadModel(self._rails[self._path_map[block_num + 1]])
        next_rails.reparentTo(self._last_block)

        name = self._path_map[block_num]
        final_pos = self._paths[name].getFinalState()[0]
        next_rails.setPos(final_pos)

        if name == "r90_turn":
            next_rails.setH(-90)
        elif name == "l90_turn":
            next_rails.setH(90)

        self._last_block = next_rails

        Sequence(
            MopathInterval(
                self._paths[name], train_mod, duration=5, name="current_path"
            ),
            Func(self._move_along_block, train_mod, block_num + 1),
        ).start()

    def _load_rail_blocks(self):
        """Load all rail blocks.

        Returns:
            (dict, dict): Index of paths, index of rails models.
        """
        paths = {}
        rails = {}

        for key, path, model in {
            ("direct", "direct_path.bam", "direct_rails.bam"),
            ("l90_turn", "l90_turn_path.bam", "l90_turn_rails.bam"),
            ("r90_turn", "r90_turn_path.bam", "r90_turn_rails.bam"),
        }:
            paths[key] = Mopath.Mopath(objectToLoad=MOD_DIR + path)
            paths[key].fFaceForward = True
            rails[key] = MOD_DIR + model

        return paths, rails


ForwardOnly().run()
