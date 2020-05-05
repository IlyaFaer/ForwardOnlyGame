"""
Main game file. Starts the game itself
and maintains the major systems.
"""
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence, Parallel, Func
from direct.interval.MopathInterval import MopathInterval
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, loadPrcFileData

from camera_controller import CameraController
from world import World

loadPrcFileData("", "threading-model Cull/Draw")

MOD_DIR = "models/bam/"


class ForwardOnly(ShowBase):
    """Object, which represents the game itself.

    Includes the main game systems.
    """

    def __init__(self):
        ShowBase.__init__(self)
        self._configure_window()

        # build game world
        self._world = World(self)
        self._world.generate_location(300)

        self._current_block = self._world.prepare_block(0)

        # configurate Train
        self._speed = 4  # seconds to pass single block

        self._train = self.render.attachNewNode("Train")
        train_mod = Actor(MOD_DIR + "locomotive.bam")
        train_mod.reparentTo(self._train)

        self._move_forward_int = train_mod.actorInterval("move_forward", playRate=10)
        self._move_forward_int.loop()

        base.disableMouse()  # noqa: F821
        cam_node = CameraController().set_camera_controls(
            self, self.cam, self._train, train_mod
        )
        # start moving
        self._move_along_block(train_mod, cam_node, 0)

    def _configure_window(self):
        """Configure game window.

        Set fullscreen mode, and resolution
        according to player's screen size.
        """
        props = WindowProperties()
        props.setFullscreen(True)

        props.setSize(
            base.pipe.getDisplayWidth(), base.pipe.getDisplayHeight()  # noqa: F821
        )
        base.openDefaultWindow(props=props)  # noqa: F821

    def _move_along_block(self, train_mod, cam_node, block_num):
        """Move Train along the current world block.

        Args:
            train_mod (panda3d.core.NodePath): Train model to move.
            cam_node (panda3d.core.NodePath): Camera node.
            block_num (int): Current path block number.
        """
        # prepare model to move along the next motion path
        train_mod.wrtReparentTo(self.render)
        cam_node.wrtReparentTo(self.render)

        # round coordinates to avoid position/rotation errors
        mod_pos = (
            round(train_mod.getX()),
            round(train_mod.getY()),
            round(train_mod.getZ()),
        )
        train_mod.setPos(mod_pos)
        train_mod.setHpr(
            (round(train_mod.getH()), round(train_mod.getP()), round(train_mod.getR()),)
        )

        cam_node.setPos(mod_pos)

        self._train.setPos(mod_pos)
        self._train.setHpr(train_mod, 0)

        train_mod.wrtReparentTo(self._train)
        cam_node.wrtReparentTo(self._train)

        # load next world block and clear penult
        next_block = self._world.prepare_block(block_num + 1)
        self._world.clear_block(block_num - 2)

        # move along the current world block
        Sequence(
            Parallel(
                MopathInterval(  # Train movement
                    self._current_block.path,
                    train_mod,
                    duration=self._speed,
                    name="current_path",
                ),
                MopathInterval(  # camera movement
                    self._current_block.cam_path,
                    cam_node,
                    duration=self._speed,
                    name="current_camera_path",
                ),
            ),
            Func(self._move_along_block, train_mod, cam_node, block_num + 1),
        ).start()

        self._current_block = next_block


ForwardOnly().run()
