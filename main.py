"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The main game file. Starts the game itself
and maintains the major systems.
"""
import dbm.dumb  # noqa: F401
import logging
import os
import shelve
import sys

from direct.showbase import Audio3DManager
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, WindowProperties

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
loadPrcFileData(
    "",
    "audio-library-name "
    + ("p3openal_audio" if sys.platform == "linux" else "p3fmod_audio"),
)

logging.basicConfig(
    filename="logs.txt",
    format="[%(levelname)s] %(asctime)s: %(message)s",
    level=logging.INFO,
)


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

        self.setBackgroundColor(0.1, 0.17, 0.1)

        self.sound_mgr = Audio3DManager.Audio3DManager(self.sfxManagerList[0], self.cam)
        self.sound_mgr.setDropOffFactor(5)

        self.enableParticles()
        self.effects_mgr = EffectsManager()

        self._dollars = 0
        self._medicine_boxes = 0
        self._smoke_filters = 0

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
        self.res_interface.update_resource("dollars", value)

    @property
    def smoke_filters(self):
        """Smoke filters amount.

        Returns:
            int: Current player smoke filters amount.
        """
        return self._smoke_filters

    @smoke_filters.setter
    def smoke_filters(self, value):
        """Smoke filter setter.

        Args:
            value (int): New smoke filters amount.
        """
        self._smoke_filters = value
        self.res_interface.update_resource("smoke_filters", value)

    @property
    def medicine_boxes(self):
        """Medicine boxes amount.

        Returns:
            int: Current player medicine boxes amount.
        """
        return self._medicine_boxes

    @medicine_boxes.setter
    def medicine_boxes(self, value):
        """Medicine boxes setter.

        Args:
            value (int): New medicine boxes amount value.
        """
        self._medicine_boxes = value
        self.res_interface.update_resource("medicine_boxes", value)

    def _configure_window(self):
        """Configure the game window.

        Set fullscreen mode, and resolution
        according to the player's screen size.
        """
        props = WindowProperties()
        props.setFullscreen(True)
        props.setSize(self.pipe.getDisplayWidth(), self.pipe.getDisplayHeight())
        self.openDefaultWindow(props=props)

    def _start_game(self, task):
        """Actually start the game process."""
        self.city_interface = CityInterface()
        self.notes = TeachingNotes()

        self.main_menu.hide()
        self.enableAllAudio()

        self.taskMgr.doMethodLater(60, self.world.disease_activity, "disease")

        self.accept("block_finished", self._move_along_block)
        self._move_along_block()
        return task.done

    def _move_along_block(self):
        """Move the Train along the current world block.

        While the Train is moving along the current block,
        the game prepares the next one and clears penalt.
        """
        self.train.switch_to_current_block()

        next_block = self.world.prepare_next_block()
        self.world.clear_prev_block()

        self.train.move_along_block(self._current_block)
        if self._current_block.is_stenchy:
            self.effects_mgr.stench_effect.play()
            self.world.stop_ambient_snd()
            self.train.ctrl.silence_move_snd()

            self.team.start_stench_activity()
        else:
            self.effects_mgr.stench_effect.stop()
            self.world.resume_ambient_snd()
            self.train.ctrl.unsilence_move_snd()
            if next_block.is_stenchy:
                self.effects_mgr.stench_effect.play_clouds()

            self.team.stop_stench_activity()

        self._current_block = next_block

    def start_new_game(self, chosen_team):
        """Start a new game, replacing the saved one.

        Args:
            chosen_team (str): The chosen main game tactics.
        """
        self.disableAllAudio()

        self.train = Train()

        self.camera_ctrl = CameraController()
        self.camera_ctrl.set_controls(self.train)

        self.team = Team()
        self.team.gen_default(chosen_team)

        self.common_ctrl = CommonController(self.train.parts, self.team.chars)
        self.common_ctrl.set_controls()

        # build game world
        self.world = World()
        self.world.generate_location("Plains", 600)
        self._current_block = self.world.prepare_next_block()

        self.char_gui = CharacterInterface()
        self.res_interface = ResourcesInterface()

        self.doMethodLater(3, self._start_game, "start_game")

        self.dollars = 300
        self.medicine_boxes = 0
        self.smoke_filters = 0

    def save_game(self):
        """Save the current game."""
        save = shelve.open("saves/save1")

        save["cur_block"] = self.world.current_block_number
        save["last_angle"] = self.world.last_cleared_block_angle
        save["enemy_score"] = self.world.enemy.score
        save["disease_threshold"] = self.world.disease_threshold

        save["train"] = self.train.description
        save["dollars"] = self.dollars
        save["medicine_boxes"] = self.medicine_boxes
        save["smoke_filters"] = self.smoke_filters
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
        self.world.load_location(
            "Plains", save["enemy_score"], save["disease_threshold"]
        )
        self._current_block = self.world.load_blocks(
            save["cur_block"], save["last_angle"]
        )

        self.char_gui = CharacterInterface()

        self.train.load_upgrades(save["train"]["upgrades"])

        self.doMethodLater(3, self._start_game, "start_game")
        self.doMethodLater(
            3.01,
            self.train.ctrl.load_speed,
            "load_speed",
            extraArgs=[save["train"]["speed"]],
        )
        self.dollars = save["dollars"]
        self.medicine_boxes = save["medicine_boxes"]
        self.smoke_filters = save["smoke_filters"]
        return task.done


try:
    ForwardOnly().run()
except Exception:
    logging.exception("Exception occured:")
