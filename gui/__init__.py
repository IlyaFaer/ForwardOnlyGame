"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Game graphical interfaces.
"""
import sys

from direct.gui.DirectGui import DGG, DirectButton, DirectFrame, DirectLabel
from panda3d.core import TransparencyAttrib

from utils import save_exists
from .character import CharacterGUI  # noqa: F401
from .city import CityInterface  # noqa: F401
from .notes import TeachingNotes  # noqa: F401
from .outings import OutingsInterface  # noqa: F401
from .resources import ResourcesGUI  # noqa: F401
from .train import TrainGUI  # noqa: F401
from .traits import TraitsGui  # noqa: F401
from .widgets import ICON_PATH, RUST_COL, SILVER_COL  # noqa: F401


class MainMenu:
    """The main game menu.

    Includes starting a game, loading, saving and exiting functions.
    """

    def __init__(self):
        self._save_but = None
        self._chosen_team = None
        self._is_first_pause = True
        self._tactics_wids = []

        self._hover_snd = loader.loadSfx("sounds/menu1.ogg")  # noqa: F821
        self._hover_snd.setVolume(0.1)
        self.click_snd = loader.loadSfx("sounds/menu2.ogg")  # noqa: F821
        self.click_snd.setVolume(0.1)

        self._main_fr = DirectFrame(
            frameSize=(-2, 2, -1, 1), frameColor=(0.15, 0.15, 0.15, 1)
        )
        but_params = {
            "text_scale": (0.05, 0.05),
            "relief": None,
            "parent": self._main_fr,
            "clickSound": self.click_snd,
        }
        self._new_game_but = DirectButton(
            pos=(-1, 0, 0.5),
            text_fg=RUST_COL,
            text="New game",
            command=self._choose_tactics,
            **but_params,
        )
        self.bind_button(self._new_game_but)

        is_save_exists = save_exists()
        self._load_but = DirectButton(
            pos=(-0.996, 0, 0.4),
            text_fg=RUST_COL if is_save_exists else (0.5, 0.5, 0.5, 1),
            text="Load game",
            command=self._load_game if is_save_exists else None,
            **but_params,
        )
        self.bind_button(self._load_but)

        self.bind_button(
            DirectButton(
                pos=(-1.083, 0, 0),
                text_fg=RUST_COL,
                text="Exit",
                command=sys.exit,
                extraArgs=[1],
                **but_params,
            )
        )
        self._alpha_disclaimer = DirectLabel(
            parent=self._main_fr,
            pos=(0, 0, -0.9),
            text_scale=(0.03, 0.03),
            text_fg=SILVER_COL,
            frameColor=(0, 0, 0, 0),
            text=(
                "This is a game alpha build. It's not finally balanced and some"
                " features are in development yet."
                "\nThus, it's mostly a conceptual release, to demonstrate you the main "
                "game princips. Enjoy your play!"
            ),
        )

    def bind_button(self, button):
        """Bind the given button to visual effects.

        Args:
            button (panda3d.gui.DirectGui.DirectButton):
                Button to bind.
        """
        button.bind(DGG.ENTER, self._highlight_but, extraArgs=[button])
        button.bind(DGG.EXIT, self._dehighlight_but, extraArgs=[button])

    def _highlight_but(self, button, _):
        """Highlight the button pointed by mouse.

        Args:
            button (panda3d.gui.DirectGui.DirectButton):
                Button to highlight.
        """
        if button["command"] is not None:
            button["text_scale"] = (
                button["text_scale"][0] + 0.002,
                button["text_scale"][1] + 0.003,
            )
            self._hover_snd.play()

    def _dehighlight_but(self, button, _):
        """Dehighlight the button, when mouse pointer leaved it.

        Args:
            button (panda3d.gui.DirectGui.DirectButton):
                Button to dehighlight.
        """
        if button["command"] is not None:
            button["text_scale"] = (
                button["text_scale"][0] - 0.002,
                button["text_scale"][1] - 0.003,
            )

    def _choose_tactics(self):
        """Choose initial tactics before new game start."""
        if self._chosen_team:
            return

        self._tactics_wids.append(
            DirectLabel(
                parent=self._main_fr,
                text="Choose your team",
                text_fg=RUST_COL,
                text_scale=0.04,
                frameColor=(0, 0, 0, 0),
                pos=(0.7, 0, 0.75),
            )
        )
        self._team_preview = DirectFrame(
            parent=self._main_fr,
            frameSize=(-0.61, 0.61, -0.35, 0.35),
            pos=(0.7, 0, 0.3),
        )
        self._team_preview.setTransparency(TransparencyAttrib.MAlpha)
        self._tactics_wids.append(self._team_preview)

        but_params = {
            "parent": self._main_fr,
            "text_scale": 0.035,
            "text_fg": RUST_COL,
            "relief": None,
            "clickSound": self.click_snd,
            "command": self._show_team,
        }

        self._team_buts = {
            "soldiers": DirectButton(
                text="Soldiers",
                extraArgs=["soldiers"],
                pos=(0.5, 0, -0.15),
                **but_params,
            ),
            "raiders": DirectButton(
                text="Raiders",
                extraArgs=["raiders"],
                pos=(0.7, 0, -0.15),
                **but_params,
            ),
            "anarchists": DirectButton(
                text="Anarchists",
                extraArgs=["anarchists"],
                pos=(0.925, 0, -0.15),
                **but_params,
            ),
        }
        self._tactics_wids += self._team_buts.values()

        for but in self._team_buts.values():
            self.bind_button(but)

        self._team_description = DirectLabel(
            parent=self._main_fr,
            text="Team description",
            text_fg=SILVER_COL,
            text_scale=0.03,
            frameColor=(0, 0, 0, 0),
            pos=(0.7, 0, -0.26),
        )
        self._tactics_wids.append(self._team_description)

        start_but = DirectButton(
            parent=self._main_fr,
            text_scale=0.045,
            text_fg=RUST_COL,
            text="Start",
            relief=None,
            command=self._start_new_game,
            pos=(0.7, 0, -0.5),
            clickSound=self.click_snd,
        )
        self.bind_button(start_but)

        self._tactics_wids.append(start_but)
        self._show_team("soldiers")

    def _show_team(self, team):
        """Show the description of the chosen tactics.

        Args:
            team (str): The chosen tactics name.
        """
        self._chosen_team = team
        self._team_preview["frameTexture"] = "gui/tex/preview/{}.png".format(team)

        for key, but in self._team_buts.items():
            but["text_fg"] = SILVER_COL if key == team else RUST_COL

        descs = {
            "soldiers": (
                "Your Train - your fortress! Improve it, build its defense, "
                "hardness, and it'll bring you there.\nSoldiers are good shooters at "
                "medium distance and good fortification assaulters.\n\n"
                "You'll start with 3 soldier males."
            ),
            "raiders": (
                "You're accustomed to difficulties and can recover no matter how "
                "tough was the damage."
                "\nRaiders are good fighters at short distance and they know how to "
                "find resources.\n\n You'll start with 2 male and 1 "
                "female raiders."
            ),
            "anarchists": (
                "Your main value is solid collective! Build relations, and your "
                "party will survive anything.\nAnarchists build cohesion faster "
                "than others and getting higher factors from it.\n\n"
                "You'll start with 2 male and 1 female anarchists."
            ),
        }
        self._team_description["text"] = descs[team]

    def _clear_temp_wids(self, task):
        """Destroy widgets from the first game screen."""
        for wid in self._tactics_wids:
            wid.destroy()

        self._tactics_wids = []
        self._alpha_disclaimer.destroy()
        self._load_msg.destroy()
        return task.done

    def _start_new_game(self):
        """Start a new game."""
        taskMgr.doMethodLater(  # noqa: F821
            4, self._clear_temp_wids, "clear_main_menu_temp_wids"
        )
        self.show_loading()
        taskMgr.doMethodLater(  # noqa: F821
            0.25,
            base.start_new_game,  # noqa: F821
            "start_new_game",
            extraArgs=[self._chosen_team],
        )

    def _load_game(self):
        """Load previously saved game."""
        self.show_loading()
        base.doMethodLater(0.25, base.load_game, "load_game")  # noqa: F821

    def show_loading(self):
        """Show "Loading..." note on the screen."""
        self._load_msg = DirectLabel(
            parent=self._main_fr,
            text="Loading...",
            text_fg=RUST_COL,
            frameSize=(1, 1, 1, 1),
            text_scale=0.04,
            pos=(0, 0, -0.75),
        )

    def hide(self):
        """Hide the main menu."""
        self._main_fr.hide()
        base.accept("escape", self.show)  # noqa: F821

    def show(self, is_game_over=False):
        """Show the main menu.

        Args:
            is_game_over (bool):
                True, if the main menu is shown on game over.
        """
        self._main_fr.show()

        if is_game_over:
            self._new_game_but["command"] = None
            self._new_game_but["text_fg"] = SILVER_COL
            DirectLabel(
                parent=self._main_fr,
                pos=(0.7, 0, 0.3),
                frameColor=(0, 0, 0, 0),
                text_scale=0.055,
                text_fg=SILVER_COL,
                text=(
                    "Your locomotive is critically damaged!\n"
                    "You're not able to continue the road.\n\n"
                    "It's all over...",
                ),
            )
            base.ignore("escape")  # noqa: F821
        else:
            base.accept("escape", self.hide)  # noqa: F821

        can_save = not (
            base.train.ctrl.critical_damage  # noqa: F821
            or base.world.is_in_city  # noqa: F821
            or base.train.ctrl.on_et  # noqa: F821
            or base.world.current_block_number < 4  # noqa: F821
        )
        if not self._is_first_pause:
            if can_save:
                self._save_but["text_fg"] = RUST_COL
                self._save_but["command"] = base.save_game  # noqa: F821
            else:
                self._save_but["text_fg"] = SILVER_COL
                self._save_but["command"] = None
            return

        # it is the first pause
        self._main_fr["frameColor"] = (0, 0, 0, 0.6)

        self._new_game_but["text"] = "Resume"
        self._new_game_but.setPos(-1.028, 0, 0.4)
        if not is_game_over:
            self._new_game_but["command"] = self.hide

        self._load_but.destroy()

        self._save_but = DirectButton(
            parent=self._main_fr,
            pos=(-0.998, 0, 0.3),
            text_scale=(0.05, 0.05),
            text_fg=RUST_COL if can_save else SILVER_COL,
            text="Save game",
            relief=None,
            command=base.save_game if can_save else None,  # noqa: F821
            clickSound=self.click_snd,
        )
        self.bind_button(self._save_but)

        self.bind_button(
            DirectButton(
                parent=self._main_fr,
                pos=(-1, 0, 0.1),
                text_scale=0.05,
                text_fg=RUST_COL,
                text="Main menu",
                relief=None,
                command=base.restart_game,  # noqa: F821
                clickSound=self.click_snd,
            )
        )
        self._is_first_pause = False
