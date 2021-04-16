"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Game graphical interfaces module.
"""
import shelve
import sys

from direct.gui.DirectGui import DGG, DirectButton, DirectFrame, DirectLabel
from panda3d.core import TextNode, TransparencyAttrib

from utils import save_exists
from .character import CharacterGUI  # noqa: F401
from .city import CityGUI  # noqa: F401
from .notes import TeachingNotes  # noqa: F401
from .outings import OutingsGUI  # noqa: F401
from .rails_scheme import RailsScheme  # noqa: F401
from .resources import ResourcesGUI  # noqa: F401
from .teaching import EnemyDesc  # noqa: F401
from .train import TrainGUI  # noqa: F401
from .traits import TraitsGUI  # noqa: F401
from .widgets import GUI_PIC, RUST_COL, SILVER_COL  # noqa: F401


class MainMenu:
    """The main game menu.

    Includes starting a game, loading, saving and exiting GUI.
    """

    def __init__(self):
        self._save_but = None
        self._chosen_team = None
        self._is_first_pause = True
        self._tactics_wids = []
        self._save_wids = []
        self._save_blocked_lab = None

        self._hover_snd = loader.loadSfx("sounds/GUI/menu1.ogg")  # noqa: F821
        self._hover_snd.setVolume(0.1)
        self.click_snd = loader.loadSfx("sounds/GUI/menu2.ogg")  # noqa: F821
        self.click_snd.setVolume(0.1)

        self._main_fr = DirectFrame(
            frameSize=(-2, 2, -1, 1),
            frameColor=(0.15, 0.15, 0.15, 1),
            state=DGG.NORMAL,
        )
        but_params = {
            "text_scale": 0.05,
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

        is_save_exists = save_exists(1) or save_exists(2) or save_exists(3)
        self._load_but = DirectButton(
            pos=(-0.996, 0, 0.4),
            text_fg=RUST_COL if is_save_exists else (0.5, 0.5, 0.5, 1),
            text="Load game",
            command=self._show_slots if is_save_exists else None,
            extraArgs=[True],
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
            text_scale=0.03,
            text_fg=SILVER_COL,
            frameColor=(0, 0, 0, 0),
            text=(
                "This is a game alpha build. It's not finally balanced and some"
                " features are in development yet."
                "\nThus, it's mostly a conceptual release, to demonstrate you the main "
                "game princips. Enjoy your play!"
            ),
        )

    def _check_can_save(self, task):
        """Check if the game can be saved.

        If the game can't be saved, the cause will
        be shown under the "Save game" button.
        """
        if base.world.is_on_et:  # noqa: F821
            cause = "(blocked during fight)"
        elif base.world.is_in_city:  # noqa: F821
            cause = "(blocked near a city)"
        elif base.world.is_near_fork:  # noqa: F821
            cause = "(blocked near a fork)"
        elif base.train.ctrl.critical_damage:  # noqa: F821
            cause = "(blocked on game over)"
        elif base.current_block.id < 4:  # noqa: F821
            cause = "(blocked on game start)"
        else:
            cause = None

        if cause:
            if self._save_blocked_lab is None:
                self._save_blocked_lab = DirectLabel(
                    parent=self._main_fr,
                    pos=(-1.12, 0, 0.26),
                    text_scale=0.026,
                    text_fg=SILVER_COL,
                    frameColor=(0, 0, 0, 0),
                    text=cause,
                    text_align=TextNode.ALeft,
                )
            self._save_blocked_lab["text"] = cause
            self._save_but["text_fg"] = SILVER_COL
            self._save_but["command"] = None
            self.hide_slots()
        else:
            self._save_but["text_fg"] = RUST_COL
            self._save_but["command"] = self._show_slots
            if self._save_blocked_lab is not None:
                self._save_blocked_lab.destroy()
                self._save_blocked_lab = None

        return task.again

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
        if self._tactics_wids:
            return

        self.hide_slots()

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
                "Soldiers are people of a tough discipline. They are good "
                "shooters at medium\ndistance and good fortification assaulters. "
                "Their tactic is based mostly on a good\ndefence and locomotive "
                "upgrading, which can make the Train a real fortress.\n\n"
                "You'll start with 3 soldier males."
            ),
            "raiders": (
                "Raiders are accustomed to difficulties and can recover from "
                "anything. They are\ngood fighters at short distance and they "
                "know how to find resources. Their tactic\nis based on getting "
                "and using expendable resources and fast recovering.\n\n"
                "You'll start with 2 male and 1 female raiders."
            ),
            "anarchists": (
                "Anarchists are the force of nature! They build cohesion "
                "faster than others and\nalways value those, who life brought "
                "them with. The tactic is based on\ngetting more people, "
                "tweaking their traits and using team skills.\n\n"
                "You'll start with 2 male and 1 female anarchists."
            ),
        }
        self._team_description["text"] = descs[team]

    def _clear_temp_wids(self, task):
        """Destroy widgets from the first game screen."""
        for wid in self._tactics_wids:
            wid.destroy()

        self._tactics_wids.clear()
        self._alpha_disclaimer.destroy()
        self._load_msg.destroy()
        return task.done

    def _read_saves(self):
        """Read all the game save slots.

        Returns:
            list: Dicts, each of which describes a save.
        """
        saves = []
        for num in range(1, 4):
            if save_exists(num):
                save = shelve.open("saves/save{}".format(str(num)))
                classes = [char["class"] for char in save["team"]]

                saves.append(
                    {
                        "save_time": save["save_time"],
                        "miles": save["train"]["miles"],
                        "chars": (
                            classes.count("soldier"),
                            classes.count("raider"),
                            classes.count("anarchist"),
                        ),
                    }
                )
                save.close()
            else:
                saves.append({})

        return saves

    def _show_slots(self, for_loading=False):
        """Show save slots GUI.

        Args:
            for_loading (bool):
                Optional. True if slots must be shown for loading.
        """
        if self._save_wids:
            return

        for wid in self._tactics_wids:
            wid.destroy()

        self._tactics_wids.clear()

        if for_loading:
            is_active = True
            command = self._load_game
        else:
            is_active = not (
                base.train.ctrl.critical_damage  # noqa: F821
                or base.world.is_in_city  # noqa: F821
                or base.world.is_on_et  # noqa: F821
                or base.current_block.id < 4  # noqa: F821
                or base.world.is_near_fork  # noqa: F821
            )
            command = base.save_game  # noqa: F821

        saves = self._read_saves()

        shift = 0.4
        for num in range(1, 4):
            but = DirectButton(
                parent=self._main_fr,
                text="Slot {}".format(str(num)),
                pos=(-0.553, 0, shift),
                text_scale=0.04,
                text_fg=RUST_COL,
                relief=None,
                command=command if is_active else None,
                extraArgs=[num],
                clickSound=self.click_snd,
            )
            self.bind_button(but)
            self._save_wids.append(but)

            self._save_wids.append(
                DirectLabel(
                    parent=self._main_fr,
                    pos=(-0.45, 0, shift - 0.05),
                    text_scale=0.03,
                    text_fg=SILVER_COL,
                    frameColor=(0, 0, 0, 0),
                    text=saves[num - 1].get("save_time", "-"),
                )
            )
            self._save_wids.append(
                DirectLabel(
                    parent=self._main_fr,
                    pos=(-0.55, 0, shift - 0.1),
                    text_scale=0.03,
                    text_fg=SILVER_COL,
                    frameColor=(0, 0, 0, 0),
                    text=(str(saves[num - 1].get("miles") or "- ")) + " mi",
                )
            )
            self._save_wids.append(
                DirectLabel(
                    parent=self._main_fr,
                    pos=(-0.1, 0, shift - 0.1),
                    text_scale=0.03,
                    text_fg=SILVER_COL,
                    frameColor=(0, 0, 0, 0),
                    text="{0} soldiers, {1} raiders, {2} anarchists".format(
                        *saves[num - 1].get("chars", ("-", "-", "-"))
                    ),
                )
            )
            shift -= 0.2

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

    def _load_game(self, num):
        """Load previously saved game.

        Args:
            num (int): The slot number.
        """
        self.show_loading()
        taskMgr.doMethodLater(  # noqa: F821
            4, self._clear_temp_wids, "clear_main_menu_temp_wids"
        )
        base.doMethodLater(  # noqa: F821
            0.25, base.load_game, "load_game", extraArgs=[num]  # noqa: F821
        )

    def bind_button(self, button):
        """Bind the given button to visual effects.

        Args:
            button (panda3d.gui.DirectGui.DirectButton): Button to bind.
        """
        button.bind(DGG.ENTER, self._highlight_but, extraArgs=[button])
        button.bind(DGG.EXIT, self._dehighlight_but, extraArgs=[button])

    def hide_slots(self):
        """Hide save slots GUI."""
        for wid in self._save_wids:
            wid.destroy()

        self._save_wids.clear()

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
        self.hide_slots()

        base.accept("escape", self.show)  # noqa: F821
        taskMgr.remove("check_can_save")  # noqa: F821

    def show(self, is_game_over=False):
        """Show the main menu.

        Args:
            is_game_over (bool):
                True, if the main menu is shown on game over.
        """
        if base.world.rails_scheme.is_shown:  # noqa: F821
            base.world.rails_scheme.show()  # noqa: F821

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
                    "You're not able to continue the road, and\n"
                    "the Stench will not keep you waiting long.\n\n"
                    "It's all over...",
                ),
            )
            base.ignore("escape")  # noqa: F821
        else:
            base.accept("escape", self.hide)  # noqa: F821

        taskMgr.doMethodLater(  # noqa: F821
            0.25, self._check_can_save, "check_can_save"
        )
        if not self._is_first_pause:
            return

        # it is the first pause
        self._main_fr["frameColor"] = (0, 0, 0, 0.6)

        self._new_game_but["text"] = "Resume"
        self._new_game_but.setPos(-1.028, 0, 0.4)
        if not is_game_over:
            self._new_game_but["command"] = self.hide

        self._load_but.destroy()

        can_save = not (
            base.train.ctrl.critical_damage  # noqa: F821
            or base.world.is_in_city  # noqa: F821
            or base.world.is_on_et  # noqa: F821
            or base.current_block.id < 4  # noqa: F821
            or base.world.is_near_fork  # noqa: F821
        )
        self._save_but = DirectButton(
            parent=self._main_fr,
            pos=(-0.998, 0, 0.3),
            text_scale=0.05,
            text_fg=RUST_COL if can_save else SILVER_COL,
            text="Save game",
            relief=None,
            command=self._show_slots if can_save else None,  # noqa: F821
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
