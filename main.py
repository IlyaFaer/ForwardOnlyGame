"""
Main game file. Starts the game itself
and maintains the major systems.
"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, loadPrcFileData

from character import Character
from controls import CameraController, CommonController
from train import Train
from world import World

loadPrcFileData("", "threading-model Cull/Draw")


class ForwardOnly(ShowBase):
    """Object, which represents the game itself.

    Includes the main game systems.
    """

    def __init__(self):
        ShowBase.__init__(self)
        self._configure_window()

        self._character_id = 0  # variable to count ids
        self._characters = {}  # characters under the player control

        CommonController(self._characters).set_controls(self)

        self._train = Train(self)

        # build game world
        self._world = World(self, self._train)
        self._world.generate_location(300)

        self._current_block = self._world.prepare_block(0)

        base.disableMouse()  # noqa: F821
        CameraController().set_controls(self, self.cam, self._train)

        # prepare default characters
        for part in (self._train.parts[1], self._train.parts[1], self._train.parts[2]):
            self._character_id += 1

            character = Character(self._character_id)
            character.generate("male")
            character.load(self.loader, self._train.model)
            character.move_to(part)

            self._characters[self._character_id] = character

        # start moving
        self._move_along_block(self._train.model, self._train.node, 0)

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
            train_np (panda3d.core.NodePath): Train node.
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

        self._train.root_node.setPos(mod_pos)
        self._train.root_node.setHpr(train_mod, 0)

        train_mod.wrtReparentTo(self._train.root_node)
        train_np.wrtReparentTo(self._train.root_node)

        # load next world block and clear penult
        next_block = self._world.prepare_block(block_num + 1)
        self._world.clear_block(block_num - 2)

        # move along the current world block
        self._train.move_along_block(self._current_block)
        self.acceptOnce(
            "block_finished",
            self._move_along_block,
            [train_mod, train_np, block_num + 1],
        )
        self._current_block = next_block


ForwardOnly().run()
