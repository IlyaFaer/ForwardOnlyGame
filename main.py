"""Main game file. Starts the game itself and maintains the main systems."""
from direct.interval.IntervalGlobal import Sequence, Parallel, Func
from direct.interval.MopathInterval import MopathInterval
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, loadPrcFileData

from camera_controller import CameraController
from world import World

MOD_DIR = "models/bam/"
PATH_SPEED = 4

loadPrcFileData("", "threading-model Cull/Draw")


class ForwardOnly(ShowBase):
    """Object, which represents the game itself.

    Includes the main game systems.
    """

    def __init__(self):
        ShowBase.__init__(self)
        self._configurate_window()

        self._world = World(self)
        self._world.generate_location("Plains", 300)

        # set first world block
        self._current_block = self._world.prepare_block(0)
        self._current_block.rails_mod.reparentTo(self.render)

        # set Train
        self._train = self.render.attachNewNode("Train")
        train_mod = self.loader.loadModel(MOD_DIR + "locomotive.bam")
        train_mod.reparentTo(self._train)

        base.disableMouse()  # noqa: F821
        cam_node = CameraController().set_camera_controls(
            self, self.cam, self._train, train_mod
        )
        # start moving
        self._move_along_block(train_mod, cam_node, 0)

    def _configurate_window(self):
        """Configurate game window.

        Set fullscreen mode. Set resolution
        according to player's screen size.
        """
        props = WindowProperties()
        props.setFullscreen(True)

        props.setSize(
            base.pipe.getDisplayWidth(), base.pipe.getDisplayHeight()  # noqa: F821
        )
        base.openDefaultWindow(props=props)  # noqa: F821

    def _move_along_block(self, train_mod, cam_node, block_num):
        """Move Train model along the next world block.

        Args:
            train_mod (panda3d.core.NodePath): Train model to move.
            cam_node (panda3d.core.NodePath): Camera node.
            block_num (int): Current path block number.
        """
        # prepare model to move along the next motion path
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

        # load next world block
        next_block = self._world.prepare_block(block_num + 1)

        # move along the current world block
        Sequence(
            Parallel(
                MopathInterval(  # Train movement
                    self._current_block.path,
                    train_mod,
                    duration=PATH_SPEED,
                    name="current_path",
                ),
                MopathInterval(  # camera movement
                    self._current_block.cam_path,
                    cam_node,
                    duration=PATH_SPEED,
                    name="current_camera_path",
                ),
            ),
            Func(self._move_along_block, train_mod, cam_node, block_num + 1),
        ).start()

        self._current_block = next_block


ForwardOnly().run()
