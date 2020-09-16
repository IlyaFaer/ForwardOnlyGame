"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Main game file. Starts the game itself
and maintains the major systems.
"""
import os
import shelve

from direct.showbase import Audio3DManager
from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties, loadPrcFileData

from controls import CameraController, CommonController
from effects import EffectsManager
from gui import (
    CharacterInterface,
    CityInterface,
    MainMenu,
    ResourcesInterface,
    TeachingNotes,
)
from personage.team import Team
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

        if not os.path.exists("saves"):
            os.mkdir("saves")

        self.sound_mgr = Audio3DManager.Audio3DManager(self.sfxManagerList[0], self.cam)
        self.sound_mgr.setDropOffFactor(5)

        self.enableParticles()
        self.effects_mgr = EffectsManager()

        self.main_menu = MainMenu()

    @property
    def dollars(self):
        """Game money amount.

        Returns:
            int: Current player money amount.
        """
        return self._dollars

    @dollars.setter
    def dollars(self, value):
        """Money setter.

        Tracks money on the resources GUI.

        Args:
            value (int): New money amount value.
        """
        self._dollars = max(0, value)
        self.res_interface.update_money(self._dollars)

    def start_new_game(self, task):
        self.disableAllAudio()

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
        self.notes = TeachingNotes()

        self.accept("block_finished", self._move_along_block)

        self.main_menu.hide()
        self.doMethodLater(3, self._start_to_move, "start_to_move")

        self.dollars = 300
        return task.done

    def _configure_window(self):
        """Configure the game window.

        Set fullscreen mode, and resolution
        according to player's screen size.
        """
        props = WindowProperties()
        props.setFullscreen(True)
        props.setSize(self.pipe.getDisplayWidth(), self.pipe.getDisplayHeight())
        self.openDefaultWindow(props=props)

    def _start_to_move(self, task):
        """Actually start the game process."""
        self.enableAllAudio()
        self._move_along_block()
        return task.done

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

    def save_game(self):
        """Save the current game."""
        save = shelve.open("saves/save1")

        save["cur_block"] = self.world.current_block_number
        save["last_angle"] = self.world.last_cleared_block_angle
        save["enemy_score"] = self.world.enemy.score

        save["train"] = self.train.condition
        save["dollars"] = self.dollars
        save["cohesion"] = self.team.current_cohesion
        save["day_part"] = {
            "name": self.world.sun.day_part,
            "time": self.world.sun.day_part_time,
        }
        save["team"] = self.team.description

        save.close()

    def load_game(self, task):
        """Load the previously saved game."""
        save = shelve.open("saves/save1")

        self.disableAllAudio()

        self.train = Train(save["train"])

        self.camera_ctrl = CameraController()
        self.camera_ctrl.set_controls(self.train)

        self.team = Team()
        self.res_interface = ResourcesInterface()
        self.team.load(save["team"], self.train.parts, save["cohesion"])

        self.common_ctrl = CommonController(self.train.parts, self.team.chars)
        self.common_ctrl.set_controls()

        # build game world
        self.world = World(save["day_part"])
        self.world.load_location("Plains", save["enemy_score"])
        self._current_block = self.world.load_blocks(
            save["cur_block"], save["last_angle"]
        )

        self.char_interface = CharacterInterface()
        self.city_interface = CityInterface()
        TeachingNotes()

        self.accept("block_finished", self._move_along_block)

        self.main_menu.hide()
        self.doMethodLater(3, self._start_to_move, "start_to_move")
        self.doMethodLater(
            3.01,
            self.train.ctrl.load_speed,
            "load_speed",
            extraArgs=[save["train"]["speed"]],
            appendTask=True,
        )
        self.dollars = save["dollars"]
        return task.done


ForwardOnly().run()
