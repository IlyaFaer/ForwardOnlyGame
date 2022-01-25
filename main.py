"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The main game file. Starts the game itself and maintains major systems.
"""
import dbm.dumb  # noqa: F401
import languages.EN  # noqa: F401
import languages.RU  # noqa: F401
import logging
import os
import shelve
import sys
import time

from direct.showbase import Audio3DManager
from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, ClockObject, Filename, WindowProperties

from controls import CameraController, CommonController
from effects import EffectsManager
from game_config import Config
from gui import (
    CharacterGUI,
    Journal,
    MainMenu,
    MechanicDesc,
    ResourcesGUI,
    TeachingNotes,
    TraitsGUI,
)
from train import Train
from world import Scenario, World
from units.crew.crew import Crew
from utils import clear_wids

# build hack: import languages module to add it into the build,
# delete the module later not to keep both languages in game
del languages

loadPrcFileData(
    "",
    "audio-library-name "
    + ("p3openal_audio" if sys.platform == "linux" else "p3fmod_audio"),
)
loadPrcFileData("", "notify-level error")

logging.basicConfig(
    filename="logs.txt",
    format="[%(levelname)s] %(asctime)s: %(message)s",
    level=logging.INFO,
)


class ForwardOnly(ShowBase):
    """Object, which represents the game itself.

    Includes the major game systems: starting, loading and saving a game;
    holds the game resources, orchestrates GUIs and the high level game
    instances. The main mechanism represents infinite locomotive movement
    along the World blocks, which are loaded and unloaded on a fly.
    """

    def __init__(self):
        ShowBase.__init__(self)
        self.game_config = Config()

        self.labels = getattr(
            __import__("languages." + self.game_config.language),
            self.game_config.language,
        )
        self._win_prors = self._configure_window()

        if not os.path.exists("saves"):
            os.mkdir("saves")

        self.main_font = self.loader.loadFont("arial.ttf")
        self.setBackgroundColor(0.1, 0.17, 0.1)

        self.sound_mgr = Audio3DManager.Audio3DManager(self.sfxManagerList[0], self.cam)
        self.sound_mgr.setDropOffFactor(5)

        self.effects_mgr = EffectsManager()

        self._dollars = 0
        self._resources = {
            "medicine_boxes": 0,
            "smoke_filters": 0,
            "stimulators": 0,
        }
        self._heads = {}
        self._cur_mouse_pointer = "normal"
        self.helped_children = False

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

    @property
    def heads(self):
        """
        The enemies, for whose death player
        didn't yet get a money reward.

        Returns:
            dict: Index of the destroyed enemies.
        """
        return self._heads

    def _configure_window(self):
        """Configure the game window.

        Set title, fullscreen mode and the given resolution.

        Returns:
            panda3d.core.WindowProperties: The main window properties object.
        """
        props = WindowProperties()

        props.setTitle("Forward Only Game")
        props.setFullscreen(True)

        x, z = self.game_config.resolution.split("x")
        props.setSize(int(x), int(z))
        props.setCursorFilename(Filename.binaryFilename("GUI/pointers/normal.ico"))

        globalClock.setMode(ClockObject.MLimited)  # noqa: F82
        globalClock.setFrameRate(self.game_config.fps_limit)  # noqa: F82

        self.openDefaultWindow(props=props)
        if self.game_config.fps_meter:
            self.setFrameRateMeter(True)

        return props

    def _move_along_block(self):
        """Move the locomotive along the current world block.

        While the locomotive is moving along the current block,
        the game prepares the next one and clears penalt.
        """
        self.train.switch_to_current_block()

        next_block = self.world.prepare_next_block()
        self.world.clear_prev_block()

        self.train.move_along_block(self.current_block)
        self._track_stench(next_block)

        if self.game_config.tutorial_enabled:
            self._track_tutorial(self.current_block.id)

        self.current_block = next_block

    def _track_stench(self, next_block):
        """Track the Stench.

        Start the Stench effect and activity, if needed.

        Args:
            next_block (world.block.Block): The next World block.
        """
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

    def _track_tutorial(self, block_id):
        """Check if a tutorial page should be shown on this block.

        Args:
            block_id (int): The current block id.
        """
        tutorial_name = {
            1: self.labels.MECHANIC_NAMES[0],
            3: self.labels.MECHANIC_NAMES[1],
            6: self.labels.MECHANIC_NAMES[2],
            10: self.labels.MECHANIC_NAMES[3],
            13: self.labels.MECHANIC_NAMES[4],
            16: self.labels.MECHANIC_NAMES[5],
            19: self.labels.MECHANIC_NAMES[6],
        }.get(block_id)

        if not tutorial_name:
            return

        MechanicDesc(tutorial_name)

        # start showing teaching notes and the Stench
        # spreading only when the tutorial ended
        if block_id == 19 and self.game_config.tutorial_enabled:
            self.notes.start()
            self.doMethodLater(24, self.world.make_stench_step, "stench_step")

    def add_head(self, enemy):
        """Make a record about the destroyed enemy.

        Args:
            enemy (str): The destroyed enemy class name.
        """
        if enemy not in self._heads:
            self._heads[enemy] = 0

        self._heads[enemy] += 1

    def clear_heads(self):
        """Clear all the records about previously destroyed enemies."""
        self._heads.clear()

    def start_game(self, task=None, loaded_game=False):
        """Actually start the game process.

        Args:
            loaded_game (bool):
                True if the game started after loading
                a previously saved session.
        """
        self.notes = TeachingNotes()
        self.traits_gui = TraitsGUI()

        self.main_menu.hide()
        self.enableAllAudio()

        if not self.game_config.tutorial_enabled or (
            self.game_config.tutorial_enabled and self.current_block.id > 18
        ):
            self.notes.start()
            self.doMethodLater(24, self.world.make_stench_step, "stench_step")

        self.doMethodLater(60, self.world.disease_activity, "disease")
        self.accept("block_finished", self._move_along_block)
        self._move_along_block()

        if task is not None:
            return task.done
        elif self.game_config.tutorial_enabled and not loaded_game:
            self.doMethodLater(
                0.1, self.train.ctrl.load_speed, "load_speed", extraArgs=[0.5],
            )

    def change_mouse_pointer(self, state):
        """Change mouse pointer icon.

        Shows an ability of action.

        Args:
            state (str): New pointer state.
        """
        if state == self._cur_mouse_pointer:
            return

        self._cur_mouse_pointer = state
        self._win_prors.setCursorFilename(
            Filename.binaryFilename("GUI/pointers/" + state + ".ico")
        )
        self.win.requestProperties(self._win_prors)

    def load_game(self, num):
        """Load the previously saved game.

        Args:
            num (int): The save slot number.
        """
        clear_wids(self.main_menu.save_wids)
        save = shelve.open("saves/save{}".format(num))

        self.disableAllAudio()

        self.train = Train(save["train"])

        self.camera_ctrl = CameraController()
        self.camera_ctrl.set_controls(self.train)

        self.team = Crew()
        self.res_gui = ResourcesGUI()

        self.journal = Journal(save["winned"])
        self.common_ctrl = CommonController(self.train.parts, self.team.chars)

        # build game world
        self.world = World(save["day_part"])
        self.world.load_location(
            num, save["enemy_score"], save["disease_threshold"], save["stench_step"],
        )
        self.world.city_gui.visit_num = save["city_visit_num"]

        self.current_block = self.world.load_blocks(
            save["cur_blocks"], save["last_angle"]
        )
        self.common_ctrl.set_controls()

        self.train.load_upgrades(save["train"]["upgrades"])
        self.char_gui = CharacterGUI()
        self.team.load(save["team"], self.train.parts, save["cohesion"])

        self.doMethodLater(3, self.start_game, "start_game", extraArgs=[None, True])
        self.doMethodLater(
            3.15,
            self.train.ctrl.load_speed,
            "load_speed",
            extraArgs=[save["train"]["speed"]],
        )
        self.dollars = save["dollars"]
        self._heads = save["heads"]
        self.plus_resource("medicine_boxes", save["medicine_boxes"])
        self.plus_resource("smoke_filters", save["smoke_filters"])
        self.plus_resource("stimulators", save["stimulators"])
        self.helped_children = save["helped_children"]

        self.res_gui.update_resource(
            "places_of_interest", str(save["chapter"] + 1) + "/10"
        )

        self.scenario = Scenario(save["chapter"])
        for num in range(save["chapter"] + 1):
            self.journal.add_page(num)

        save.close()
        self.main_menu.hide_loading_msg()

    def plus_resource(self, name, value):
        """Increase the amount of the given resource.

        Updates the corresponding GUI indicator.

        Args:
            name (str): Name of the resource.
            value (int): Amount to plus.
        """
        self._resources[name] += value
        self.res_gui.update_resource(name, self._resources[name])

    def resource(self, name):
        """Return the current amount of the given resource.

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
        """Save the current game description into a file.

        Args:
            num (int): The save slot number.
        """
        clear_wids(self.main_menu.save_wids)
        self.world.save_map(num)

        save = shelve.open("saves/save{}".format(num))

        save["save_time"] = time.strftime("%a, %d %b %Y %H:%M", time.localtime())
        save["cur_blocks"] = self.world.current_blocks
        save["last_angle"] = self.world.last_cleared_block_angle
        save["enemy_score"] = self.world.enemy.score
        save["disease_threshold"] = self.world.disease_threshold
        save["stench_step"] = self.world.stench_step
        save["heads"] = self.heads

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
        save["chapter"] = self.scenario.current_chapter
        save["city_visit_num"] = self.world.city_gui.visit_num
        save["winned"] = self.journal.winned
        save["helped_children"] = self.helped_children

        save.close()

    def start_new_game(self, chosen_crew):
        """Start new game.

        Args:
            chosen_crew (str): The chosen initial crew.
        """
        self.disableAllAudio()

        self.train = Train()

        self.camera_ctrl = CameraController()
        self.camera_ctrl.set_controls(self.train)

        self.journal = Journal()

        self.team = Crew()
        self.team.gen_default(chosen_crew)

        self.common_ctrl = CommonController(self.train.parts, self.team.chars)

        # build game world
        self.world = World()
        self.world.generate_location(800, chosen_crew)
        self.current_block = self.world.prepare_next_block()

        self.common_ctrl.set_controls()

        self.char_gui = CharacterGUI()
        self.res_gui = ResourcesGUI()
        self.main_menu.show_start_button()
        self.dollars = 300

        self.scenario = Scenario()


def configure_cull_draw():
    """
    Check the game configurations and enable multithreading if
    needed. Must be done before ShowBase__init__(), otherwise
    the configuration will not be applied.
    """
    if not os.path.exists(Config.opts_file) or open(Config.opts_file).read().endswith(
        "True"
    ):
        loadPrcFileData("", "threading-model Cull/Draw")


try:
    configure_cull_draw()
    ForwardOnly().run()
except Exception:
    logging.exception("Exception occured:")
