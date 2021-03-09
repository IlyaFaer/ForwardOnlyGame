"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The main game file. Starts the game itself
and maintains the major systems.
"""
import dbm.dumb  # noqa: F401
import logging
import os
import shelve
import sys
import time

from direct.showbase import Audio3DManager
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, WindowProperties

from controls import CameraController, CommonController
from effects import EffectsManager
from gui import (
    CharacterGUI,
    MainMenu,
    ResourcesGUI,
    TeachingNotes,
    TraitsGUI,
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

    Includes the major game systems. The main mechanism represents
    infinite Train movement along World blocks, which are loaded
    and unloaded on a fly.
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

        self._resources = {
            "medicine_boxes": 0,
            "smoke_filters": 0,
            "stimulators": 0,
        }
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
        self.res_gui.update_resource("dollars", value)

    def _configure_window(self):
        """Configure the game window.

        Set title, fullscreen mode and resolution
        according to the player's screen size.
        """
        props = WindowProperties()

        props.setTitle("Forward Only Game")
        props.setFullscreen(True)
        props.setSize(self.pipe.getDisplayWidth(), self.pipe.getDisplayHeight())

        self.openDefaultWindow(props=props)

    def _move_along_block(self):
        """Move the Train along the current world block.

        While the Train is moving along the current block,
        the game prepares the next one and clears penalt.
        """
        self.train.switch_to_current_block()

        next_block = self.world.prepare_next_block()
        self.world.clear_prev_block()

        self.train.move_along_block(self.current_block)

        # track the Stench
        if self.current_block.is_stenchy:
            self.effects_mgr.stench_effect.play()
            self.world.stop_ambient_snd()
            self.train.ctrl.drown_move_snd()

            self.team.start_stench_activity()
        else:
            self.effects_mgr.stench_effect.stop()
            self.world.resume_ambient_snd()
            self.train.ctrl.raise_move_snd()
            if next_block.is_stenchy:
                self.effects_mgr.stench_effect.play_clouds()

            self.team.stop_stench_activity()

        self.current_block = next_block

    def _start_game(self, task):
        """Actually start the game process."""
        self.notes = TeachingNotes()
        self.traits_gui = TraitsGUI()

        self.main_menu.hide()
        self.enableAllAudio()

        self.taskMgr.doMethodLater(60, self.world.disease_activity, "disease")

        self.accept("block_finished", self._move_along_block)
        self._move_along_block()
        return task.done

    def load_game(self, num):
        """Load the previously saved game.

        Args:
            num (int): The save slot number.
        """
        self.main_menu.hide_slots()
        save = shelve.open("saves/save{}".format(str(num)))

        self.disableAllAudio()

        self.train = Train(save["train"])

        self.camera_ctrl = CameraController()
        self.camera_ctrl.set_controls(self.train)

        self.team = Team()
        self.res_gui = ResourcesGUI()
        self.team.load(save["team"], self.train.parts, save["cohesion"])

        self.common_ctrl = CommonController(self.train.parts, self.team.chars)
        self.common_ctrl.set_controls()

        # build game world
        self.world = World(save["day_part"])
        self.world.load_location(
            "Plains",
            num,
            save["enemy_score"],
            save["disease_threshold"],
            save["stench_step"],
        )
        self.current_block = self.world.load_blocks(
            save["cur_blocks"], save["last_angle"]
        )

        self.char_gui = CharacterGUI()

        self.train.load_upgrades(save["train"]["upgrades"])

        self.doMethodLater(3, self._start_game, "start_game")
        self.doMethodLater(
            3.01,
            self.train.ctrl.load_speed,
            "load_speed",
            extraArgs=[save["train"]["speed"]],
        )
        self.dollars = save["dollars"]
        self.plus_resource("medicine_boxes", save["medicine_boxes"])
        self.plus_resource("smoke_filters", save["smoke_filters"])
        self.plus_resource("stimulators", save["stimulators"])

        save.close()

    def resource(self, name):
        """Return the amount of the given resource.

        Args:
            name (str): Resource name.

        Returns:
            int: The amount of the resource.
        """
        return self._resources[name]

    def restart_game(self):
        """Completely restart the game program."""
        self.destroy()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def save_game(self, num):
        """Save the current game.

        Args:
            num (int): The save slot number.
        """
        self.main_menu.hide_slots()
        self.world.save_map(num)

        save = shelve.open("saves/save{}".format(str(num)))

        save["save_time"] = time.strftime("%a, %d %b %Y %H:%M", time.localtime())
        save["cur_blocks"] = self.world.current_blocks
        save["last_angle"] = self.world.last_cleared_block_angle
        save["enemy_score"] = self.world.enemy.score
        save["disease_threshold"] = self.world.disease_threshold
        save["stench_step"] = self.world.stench_step

        save["train"] = self.train.description
        save["dollars"] = self.dollars
        save["medicine_boxes"] = self.resource("medicine_boxes")
        save["smoke_filters"] = self.resource("smoke_filters")
        save["stimulators"] = self.resource("stimulators")
        save["cohesion"] = self.team.current_cohesion
        save["day_part"] = {
            "name": self.world.sun.day_part,
            "time": self.world.sun.day_part_time,
        }
        save["team"] = self.team.description

        save.close()

    def plus_resource(self, name, value):
        """Increase the amount of the given resource.

        Updates the corresponding GUI indicator.

        Args:
            name (str): Name of the resource.
            value (int): Amount to please.
        """
        self._resources[name] += value
        self.res_gui.update_resource(name, self._resources[name])

    def start_new_game(self, chosen_team):
        """Start new game.

        Args:
            chosen_team (str): The chosen initial team.
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
        self.world.generate_location("Plains", 900)
        self.current_block = self.world.prepare_next_block()

        self.char_gui = CharacterGUI()
        self.res_gui = ResourcesGUI()

        self.doMethodLater(3, self._start_game, "start_game")

        self.dollars = 300


try:
    ForwardOnly().run()
except Exception:
    logging.exception("Exception occured:")
