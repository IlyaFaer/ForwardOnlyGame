"""Main game file. Starts the game itself and maintains the main systems."""
from direct.directutil import Mopath
from direct.interval.IntervalGlobal import Sequence, Parallel, Func
from direct.interval.MopathInterval import MopathInterval
from direct.showbase.ShowBase import ShowBase

from camera_controller import CameraController
from railway_generator import RailwayGenerator
from world import World

MOD_DIR = "models/bam/"
PATH_SPEED = 4


class ForwardOnly(ShowBase):
    """Object, which represents the game itself.

    Includes the main game systems.
    """

    def __init__(self):
        ShowBase.__init__(self)

        World(self.render)

        self._path_map = RailwayGenerator().generate_path(300)
        self._paths, self._rails = self._load_rail_blocks()

        # set Train node
        self._train = self.render.attachNewNode("Train")
        train_mod = self.loader.loadModel(MOD_DIR + "locomotive.bam")
        train_mod.reparentTo(self._train)

        # set first path block
        self._last_block = self.loader.loadModel(self._rails["direct"])
        self._last_block.reparentTo(self.render)

        base.disableMouse()  # noqa: F821
        cam_node = CameraController().set_camera_controls(
            self, self.cam, self._train, train_mod
        )

        # start moving
        self._move_along_block(train_mod, cam_node, 0)

    def _move_along_block(self, train_mod, cam_node, block_num):
        """Move Train model along the next motion path.

        Args:
            train_mod (panda3d.core.NodePath): Train model to move.
            cam_node (panda3d.core.NodePath): Camera node.
            block_num (int): Current path block number.
        """
        # prepare model to move along next motion path
        train_mod.wrtReparentTo(self.render)
        cam_node.wrtReparentTo(self.render)

        # round Train position to avoid increasing
        # position/rotation errors
        mod_pos = (
            round(train_mod.getX()),
            round(train_mod.getY()),
            round(train_mod.getZ()),
        )
        mod_hpr = (
            round(train_mod.getH()),
            round(train_mod.getP()),
            round(train_mod.getR()),
        )

        train_mod.setPos(mod_pos)
        train_mod.setHpr(mod_hpr)

        cam_node.setPos(mod_pos)

        self._train.setPos(mod_pos)
        self._train.setHpr(train_mod, 0)

        train_mod.wrtReparentTo(self._train)
        cam_node.wrtReparentTo(self._train)

        # load next path block
        next_rails = self.loader.loadModel(self._rails[self._path_map[block_num + 1]])
        next_rails.reparentTo(self._last_block)

        name = self._path_map[block_num]
        final_pos = self._paths[name].getFinalState()[0]
        next_rails.setPos(
            round(final_pos.getX()), round(final_pos.getY()), round(final_pos.getZ())
        )

        if name == "r90_turn":
            next_rails.setH(-90)
        elif name == "l90_turn":
            next_rails.setH(90)

        self._last_block = next_rails

        Sequence(
            Parallel(
                MopathInterval(
                    self._paths[name],
                    train_mod,
                    duration=PATH_SPEED,
                    name="current_path",
                ),
                MopathInterval(
                    self._paths["cam_" + name],
                    cam_node,
                    duration=PATH_SPEED,
                    name="current_camera_path",
                ),
            ),
            Func(self._move_along_block, train_mod, cam_node, block_num + 1),
        ).start()

    def _load_rail_blocks(self):
        """Load all rail blocks.

        Returns:
            (dict, dict): Index of paths, index of rails models.
        """
        paths = {}
        rails = {}

        for name, path, model in {
            ("direct", "direct_path.bam", "direct_rails.bam"),
            ("l90_turn", "l90_turn_path.bam", "l90_turn_rails.bam"),
            ("r90_turn", "r90_turn_path.bam", "r90_turn_rails.bam"),
        }:
            path_mod = self.loader.loadModel(MOD_DIR + path)

            paths[name] = Mopath.Mopath(objectToLoad=path_mod)
            paths[name].fFaceForward = True

            paths["cam_" + name] = Mopath.Mopath(objectToLoad=path_mod)
            rails[name] = MOD_DIR + model

        return paths, rails


ForwardOnly().run()
