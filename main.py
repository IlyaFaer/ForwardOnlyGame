"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Main game file. Starts the game itself
and maintains the major systems.
"""
from direct.showbase import Audio3DManager
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, loadPrcFileData

from character import Character
from controls import CameraController, CommonController
from train import Train
from world import World

loadPrcFileData("", "threading-model Cull/Draw")
loadPrcFileData("", "audio-library-name p3fmod_audio")


class ForwardOnly(ShowBase):
    """Object, which represents the game itself.

    Includes the major game systems. The main mechanism
    represents infinite Train movement along World
    blocks, which are loaded and unloaded on a fly.
    """

    def __init__(self):
        ShowBase.__init__(self)
        self._configure_window()

        self.sound_mgr = Audio3DManager.Audio3DManager(
            base.sfxManagerList[0], self.cam  # noqa: F821
        )
        self.sound_mgr.setDropOffFactor(5)

        self._char_id = 0  # variable to count character ids
        self.train = Train(self)

        common_ctrl = CommonController(self.train.parts)
        common_ctrl.set_controls(self)

        # build game world
        self._world = World(self, self.train)
        self._world.generate_location("Plains", 300)
        self._current_block = self._world.prepare_next_block()

        CameraController().set_controls(self, self.cam, self.train)

        # prepare default characters
        for part in (
            self.train.parts["part_arrow_locomotive_right"],
            self.train.parts["part_arrow_locomotive_right"],
            self.train.parts["part_arrow_locomotive_front"],
        ):
            self._char_id += 1

            char = Character(self._char_id)
            char.generate("male")
            char.prepare(self.taskMgr)
            char.move_to(part)

            common_ctrl.chars[char.id] = char

        self._move_along_block()

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

    def _move_along_block(self):
        """Move Train along the current world block.

        While Train is moving along the current block,
        the game prepares the next one.
        """
        self.train.switch_to_current_block()

        # load next world block and clear penult
        next_block = self._world.prepare_next_block()
        self._world.clear_prev_block()

        # move along the current world block
        self.train.move_along_block(self._current_block)
        self.acceptOnce("block_finished", self._move_along_block)
        self._current_block = next_block


ForwardOnly().run()
