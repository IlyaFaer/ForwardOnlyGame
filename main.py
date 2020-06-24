"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Main game file. Starts the game itself
and maintains the major systems.
"""
from direct.showbase import Audio3DManager
from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, WindowProperties, loadPrcFileData

from controls import CameraController, CommonController
from gui.interface import CharacterInterface
from personage.character import Team
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

        self.disableAllAudio()
        self.sound_mgr = Audio3DManager.Audio3DManager(self.sfxManagerList[0], self.cam)
        self.sound_mgr.setDropOffFactor(5)

        self.traverser = CollisionTraverser("traverser")

        self.train = Train()

        CameraController().set_controls(self.train)

        team = Team()
        team.gen_default(self.train.parts)

        common_ctrl = CommonController(self.train.parts, team.chars)
        common_ctrl.set_controls()

        # build game world
        self.world = World(self, self.train, team)
        self.world.generate_location("Plains", 300)
        self._current_block = self.world.prepare_next_block()

        self.enableParticles()

        self.interface = CharacterInterface()

        self.enableAllAudio()
        self._move_along_block()

    def _configure_window(self):
        """Configure game window.

        Set fullscreen mode, and resolution
        according to player's screen size.
        """
        props = WindowProperties()
        props.setFullscreen(True)
        props.setSize(self.pipe.getDisplayWidth(), self.pipe.getDisplayHeight())
        self.openDefaultWindow(props=props)

    def _move_along_block(self):
        """Move Train along the current world block.

        While Train is moving along the current block,
        the game prepares the next one.
        """
        self.train.switch_to_current_block()

        # load next world block and clear penult
        next_block = self.world.prepare_next_block()
        self.world.clear_prev_block()

        # move along the current world block
        self.train.move_along_block(self._current_block)
        self.acceptOnce("block_finished", self._move_along_block)
        self._current_block = next_block


ForwardOnly().run()
