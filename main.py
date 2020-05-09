"""
Main game file. Starts the game itself
and maintains the major systems.
"""
from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, loadPrcFileData

from controls import CameraController, CommonController, TrainController
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

        CommonController().set_controls(self)

        # configurate Train
        self._train = self.render.attachNewNode("train_root")
        train_np = self._train.attachNewNode("train")

        train_mod = Actor(MOD_DIR + "locomotive.bam")
        train_mod.reparentTo(self._train)

        self._train_ctrl = TrainController(self, train_mod)
        self._train_ctrl.set_controls()

        # build game world
        self._world = World(self, train_np, train_mod)
        self._world.generate_location(300)

        self._current_block = self._world.prepare_block(0)

        base.disableMouse()  # noqa: F821
        CameraController().set_controls(self, self.cam, train_np, train_mod)

        # start moving
        self._move_along_block(train_mod, train_np, 0)

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

    def _move_along_block(self, train_mod, train_np, block_num):
        """Move Train along the current world block.

        While Train is moving along the current block,
        game prepares the next one.

        Args:
            train_mod (panda3d.core.NodePath): Train model to move.
            cam_np (panda3d.core.NodePath): Camera node.
            block_num (int): Current path block number.
        """
        # prepare model to move along the next motion path
        train_mod.wrtReparentTo(self.render)
        train_np.wrtReparentTo(self.render)

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

        train_np.setPos(mod_pos)

        self._train.setPos(mod_pos)
        self._train.setHpr(train_mod, 0)

        train_mod.wrtReparentTo(self._train)
        train_np.wrtReparentTo(self._train)

        # load next world block and clear penult
        next_block = self._world.prepare_block(block_num + 1)
        self._world.clear_block(block_num - 2)

        # move along the current world block
        self._train_ctrl.move_along_block(self._current_block, train_np)
        self.acceptOnce(
            "block_finished",
            self._move_along_block,
            [train_mod, train_np, block_num + 1],
        )
        self._current_block = next_block


ForwardOnly().run()
