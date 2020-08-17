"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Main game file. Starts the game itself
and maintains the major systems.
"""
from direct.showbase import Audio3DManager
from direct.showbase.ShowBase import ShowBase
from direct.showbase.Transitions import Transitions
from panda3d.core import WindowProperties, loadPrcFileData

from controls import CameraController, CommonController
from effects import EffectsManager
from gui import CharacterInterface, CityInterface, ResourcesInterface
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

        self.transition = Transitions(self.loader)
        self.transition.setFadeColor(0, 0, 0)

        self.enableParticles()
        self.effects_mgr = EffectsManager()

        self.train = Train()

        self.camera_ctrl = CameraController()
        self.camera_ctrl.set_controls(self.train)

        self.team = Team()
        self.team.gen_default(self.train.parts)

        self.common_ctrl = CommonController(self.train.parts, self.team.chars)
        self.common_ctrl.set_controls()

        # build game world
        self.world = World()
        self.world.generate_location("Plains", 500)
        self._current_block = self.world.prepare_next_block()

        self.char_interface = CharacterInterface()
        self.res_interface = ResourcesInterface()
        self.city_interface = CityInterface()

        self.enableAllAudio()

        self._move_along_block()
        self.accept("block_finished", self._move_along_block)

        self.dollars = 300

    def _configure_window(self):
        """Configure the game window.

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
        the game prepares the next one and clears penalt.
        """
        self.train.switch_to_current_block()

        next_block = self.world.prepare_next_block()
        self.world.clear_prev_block()

        self.train.move_along_block(self._current_block)
        self._current_block = next_block

    def fade_out_screen(self, task):
        """Smoothly fill the screen with black color."""
        self.transition.fadeOut(3)
        return task.done

    def fade_in_screen(self, task):
        """Smoothly fill the screen with natural colors."""
        self.transition.fadeIn(3)
        return task.done


ForwardOnly().run()
