"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Game graphical interfaces module.
"""
import os
import shelve
import sys
import webbrowser

from direct.interval.LerpInterval import LerpPosInterval
from direct.gui.DirectGui import (
    DGG,
    DirectButton,
    DirectCheckButton,
    DirectFrame,
    DirectLabel,
)
from panda3d.core import TextNode, TransparencyAttrib

from utils import clear_wids, drown_snd, save_exists
from .character import CharacterGUI  # noqa: F401
from .city import CityGUI  # noqa: F401
from .journal import Journal  # noqa: F401
from .notes import TeachingNotes  # noqa: F401
from .outings import OutingsGUI  # noqa: F401
from .rails_scheme import RailsScheme  # noqa: F401
from .resources import ResourcesGUI  # noqa: F401
from .teaching import EnemyDesc, MechanicDesc  # noqa: F401
from .train import TrainGUI  # noqa: F401
from .traits import TraitsGUI  # noqa: F401
from .widgets import GUI_PIC, RUST_COL, SILVER_COL, ListChooser  # noqa: F401

LANGUAGES = ("EN", "RU")
FPS = ("30", "60", "120")
RESOLUTIONS = [
    "800x600",
    "1024x768",
    "1176x664",
    "1280x720",
    "1280x768",
    "1280x800",
    "1280x960",
    "1280x1024",
    "1360x768",
    "1366x768",
    "1440x900",
    "1600x900",
    "1768x992",
    "1920x1080",
    "2560x1440",
]


class MainMenu:
    """The main game menu.

    Includes starting a game, loading, saving and exiting GUI.
    """

    def __init__(self):
        self._save_but = None
        self._chosen_crew = None
        self._load_msg = None
        self._load_screen = None
        self._is_first_pause = True
        self._save_blocked_lab = None
        self._menu_music = loader.loadSfx(  # noqa: F821
            "sounds/music/Among Madness - Fever.mp3"
        )
        self._menu_music.setVolume(0.19)

        self.tactics_wids = []
        self.save_wids = []
        self.conf_wids = []
        self.cred_wids = []

        self._hover_snd = loader.loadSfx("sounds/GUI/menu1.ogg")  # noqa: F821
        self._hover_snd.setVolume(0.1)
        self.click_snd = loader.loadSfx("sounds/GUI/menu2.ogg")  # noqa: F821
        self.click_snd.setVolume(0.1)
        self.new_enemy_snd = loader.loadSfx("sounds/new_enemy.ogg")  # noqa: F821
        self.new_enemy_snd.setPlayRate(0.95)

        self._main_fr = DirectFrame(
            frameSize=(-2, 2, -1, 1),
            frameColor=(0.15, 0.15, 0.15, 1),
            state=DGG.NORMAL,
        )
        wids = self._show_authors_word()
        taskMgr.doMethodLater(  # noqa: F821
            5, self._hide_authors_word, "stop_splash_screens", extraArgs=[wids]
        )

    def _build(self):
        """Build the main menu."""
        but_params = {
            "text_scale": 0.05,
            "relief": None,
            "parent": self._main_fr,
            "clickSound": self.click_snd,
            "text_font": base.main_font,  # noqa: F821
        }
        self._new_game_but = DirectButton(  # New game
            pos=(-1.12, 0, 0.5),
            text_fg=RUST_COL,
            text=base.labels.MAIN_MENU[0],  # noqa: F821
            command=self._choose_tactics,
            text_align=TextNode.ALeft,
            **but_params,
        )
        self.bind_button(self._new_game_but)

        is_save_exists = save_exists(1) or save_exists(2) or save_exists(3)
        self._load_but = DirectButton(  # Load game
            pos=(-1.12, 0, 0.4),
            text_fg=RUST_COL if is_save_exists else (0.5, 0.5, 0.5, 1),
            text=base.labels.MAIN_MENU[1],  # noqa: F821
            command=self._show_slots if is_save_exists else None,
            extraArgs=[True],
            text_align=TextNode.ALeft,
            **but_params,
        )
        self.bind_button(self._load_but)

        self.bind_button(
            DirectButton(  # Options
                pos=(-1.12, 0, 0.2),
                text_fg=RUST_COL,
                text=base.labels.MAIN_MENU[2],  # noqa: F821
                text_align=TextNode.ALeft,
                command=self._show_conf,
                **but_params,
            )
        )
        self.bind_button(
            DirectButton(  # Credits
                pos=(-1.12, 0, 0.1),
                text_fg=RUST_COL,
                text=base.labels.MAIN_MENU[30],  # noqa: F821
                command=self._show_credits,
                text_align=TextNode.ALeft,
                **but_params,
            )
        )
        self.bind_button(
            DirectButton(  # Exit
                pos=(-1.12, 0, -0.1),
                text_fg=RUST_COL,
                text=base.labels.MAIN_MENU[3],  # noqa: F821
                command=sys.exit,
                extraArgs=[1],
                text_align=TextNode.ALeft,
                **but_params,
            )
        )
        self._alpha_disclaimer = DirectLabel(
            parent=self._main_fr,
            pos=(0, 0, -0.9),
            text_scale=0.03,
            text_fg=SILVER_COL,
            frameColor=(0, 0, 0, 0),
            text_font=base.main_font,  # noqa: F821
            text=base.labels.MAIN_MENU[4],  # noqa: F821
        )

    def _check_can_save(self, task):
        """Check if the game can be saved right now.

        If the game can't be saved, the cause will
        be shown under the "Save game" button.
        """
        if base.world.is_on_et:  # noqa: F821
            cause = base.labels.MAIN_MENU[16]  # noqa: F821
        elif base.world.is_in_city:  # noqa: F821
            cause = base.labels.MAIN_MENU[17]  # noqa: F821
        elif base.world.is_near_fork:  # noqa: F821
            cause = base.labels.MAIN_MENU[18]  # noqa: F821
        elif base.train.ctrl.critical_damage:  # noqa: F821
            cause = base.labels.MAIN_MENU[19]  # noqa: F821
        elif base.current_block.id < 4:  # noqa: F821
            cause = base.labels.MAIN_MENU[20]  # noqa: F821
        else:
            cause = None

        if cause:
            if self._save_blocked_lab is None:
                self._save_blocked_lab = DirectLabel(
                    parent=self._main_fr,
                    pos=(-1.12, 0, 0.26),
                    frameColor=(0, 0, 0, 0),
                    text_scale=0.026,
                    text_fg=SILVER_COL,
                    text=cause,
                    text_font=base.main_font,  # noqa: F821
                    text_align=TextNode.ALeft,
                )
            self._save_blocked_lab["text"] = cause
            self._save_but["text_fg"] = SILVER_COL
            self._save_but["command"] = None
            clear_wids(self.save_wids)
        else:
            self._save_but["text_fg"] = RUST_COL
            self._save_but["command"] = self._show_slots
            if self._save_blocked_lab is not None:
                self._save_blocked_lab.destroy()
                self._save_blocked_lab = None

        return task.again

    def _choose_tactics(self):
        """Choose initial tactics before new game start."""
        if self.tactics_wids:
            return

        clear_wids(self.save_wids)
        clear_wids(self.conf_wids)
        clear_wids(self.cred_wids)

        self.tactics_wids.append(
            DirectLabel(  # Choose your crew
                parent=self._main_fr,
                text=base.labels.MAIN_MENU[5],  # noqa: F821
                text_fg=RUST_COL,
                text_scale=0.04,
                text_font=base.main_font,  # noqa: F821
                frameColor=(0, 0, 0, 0),
                pos=(0.7, 0, 0.75),
            )
        )
        # an image with a crew representer
        self._crew_preview = DirectFrame(
            parent=self._main_fr,
            frameSize=(-0.61, 0.61, -0.35, 0.35),
            pos=(0.7, 0, 0.3),
        )
        self._crew_preview.setTransparency(TransparencyAttrib.MAlpha)
        self.tactics_wids.append(self._crew_preview)

        but_params = {
            "parent": self._main_fr,
            "text_scale": 0.035,
            "text_fg": RUST_COL,
            "text_font": base.main_font,  # noqa: F821
            "relief": None,
            "clickSound": self.click_snd,
            "command": self._show_crew,
        }
        self._crew_buts = {
            "soldiers": DirectButton(
                text=base.labels.MAIN_MENU[6],  # noqa: F821
                extraArgs=["soldiers"],
                pos=(0.5, 0, -0.15),
                **but_params,
            ),
            "raiders": DirectButton(
                text=base.labels.MAIN_MENU[7],  # noqa: F821
                extraArgs=["raiders"],
                pos=(0.7, 0, -0.15),
                **but_params,
            ),
            "anarchists": DirectButton(
                text=base.labels.MAIN_MENU[8],  # noqa: F821
                extraArgs=["anarchists"],
                pos=(0.925, 0, -0.15),
                **but_params,
            ),
        }
        self.tactics_wids += self._crew_buts.values()

        for but in self._crew_buts.values():
            self.bind_button(but)

        self._team_description = DirectLabel(  # Crew description
            parent=self._main_fr,
            text=base.labels.MAIN_MENU[9],  # noqa: F821
            text_fg=SILVER_COL,
            text_scale=0.03,
            text_font=base.main_font,  # noqa: F821
            frameColor=(0, 0, 0, 0),
            pos=(0.7, 0, -0.26),
        )
        self.tactics_wids.append(self._team_description)

        start_but = DirectButton(  # Start
            parent=self._main_fr,
            text_scale=0.045,
            text_fg=RUST_COL,
            text=base.labels.MAIN_MENU[10],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            relief=None,
            command=self._start_new_game,
            pos=(0.7, 0, -0.5),
            clickSound=self.click_snd,
        )
        self.bind_button(start_but)
        self.tactics_wids.append(start_but)

        self._show_crew("soldiers")

    def _clear_temp_wids(self, task):
        """Destroy widgets from the first game screen."""
        clear_wids(self.tactics_wids)
        self._alpha_disclaimer.destroy()
        return task.done

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

    def _hide_authors_word(self, wids):
        """Hide author's word splashscreen and build the main menu.

        Args:
            wids (list): Widgets to destroy.
        """
        for wid in wids:
            wid.destroy()

        self._menu_music.play()
        self._build()

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

    def _load_game(self, num):
        """Load previously saved game.

        Args:
            num (int): The slot number.
        """
        save_file = "saves/save{}.dat".format(num)
        if not os.path.exists(save_file):
            return

        self.show_loading()
        taskMgr.doMethodLater(  # noqa: F821
            4, self._clear_temp_wids, "clear_main_menu_temp_wids"
        )
        base.doMethodLater(  # noqa: F821
            0.25, base.load_game, "load_game", extraArgs=[num]  # noqa: F821
        )

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

    def _save_conf_and_restart(
        self,
        res_chooser,
        tutorial_check,
        lang_chooser,
        fps_chooser,
        fps_meter,
        multi_threading,
    ):
        """Save configurations and restart the game program.

        Args:
            res_chooser (GUI.widgets.ListChooser):
                Widget to choose a screen resolution.
            tutorial_check (direct.gui.DirectCheckButton):
                Tutorial enabling check button.
            lang_chooser (GUI.widgets.ListChooser):
                Widget to choose GUI language.
            fps_chooser (GUI.widgets.ListChooser):
                Framerate chooser.
            fps_meter (direct.gui.DirectCheckButton):
                FPS meter enabling check button.
            multi_threading (direct.gui.DirectCheckButton):
                Multi threading mode enabling check button.
        """
        base.game_config.update(  # noqa: F821
            res_chooser.chosen_item,
            lang_chooser.chosen_item,
            str(bool(tutorial_check["indicatorValue"])),
            fps_chooser.chosen_item,
            str(bool(fps_meter["indicatorValue"])),
            str(bool(multi_threading["indicatorValue"])),
        )
        base.restart_game()  # noqa: F821

    def _show_authors_word(self):
        """Show author's word splashscreen.

        Returns:
            list: Splash screen widgets.
        """
        title = DirectLabel(
            pos=(0, 0, 0.2),
            text_scale=0.045,
            text_fg=SILVER_COL,
            frameColor=(0, 0, 0, 0),
            text=base.labels.SPLASHES[0],  # noqa: F821
            state=DGG.NORMAL,
            text_font=base.main_font,  # noqa: F821
        )
        msg = DirectLabel(
            pos=(0, 0, 0.05),
            text_scale=0.035,
            text_fg=SILVER_COL,
            frameColor=(0, 0, 0, 0),
            text=base.labels.SPLASHES[1],  # noqa: F821,
            state=DGG.NORMAL,
            text_font=base.main_font,  # noqa: F821
        )
        return [title, msg]

    def _show_conf(self):
        """Show game configurations GUI."""
        clear_wids(self.save_wids)
        clear_wids(self.tactics_wids)
        clear_wids(self.cred_wids)

        self.conf_wids.append(
            DirectLabel(  # Resolution:
                parent=self._main_fr,
                text=base.labels.MAIN_MENU[22],  # noqa: F821,
                text_fg=RUST_COL,
                text_scale=0.04,
                text_font=base.main_font,  # noqa: F821
                pos=(-0.3, 0, 0.5),
                frameColor=(0, 0, 0, 0),
            )
        )

        if base.game_config.resolution in RESOLUTIONS:  # noqa: F821
            res_ind = RESOLUTIONS.index(base.game_config.resolution)  # noqa: F821
        else:
            res_ind = len(RESOLUTIONS)
            RESOLUTIONS.append(base.game_config.resolution)  # noqa: F821

        res_chooser = ListChooser()
        res_chooser.prepare(self._main_fr, (0.1, 0, 0.51), RESOLUTIONS, res_ind)
        self.conf_wids.append(res_chooser)

        self.conf_wids.append(
            DirectLabel(  # Tutorial:
                parent=self._main_fr,
                text=base.labels.MAIN_MENU[23],  # noqa: F821,
                text_fg=RUST_COL,
                text_scale=0.04,
                text_font=base.main_font,  # noqa: F821
                pos=(-0.3, 0, 0.4),
                frameColor=(0, 0, 0, 0),
            )
        )
        tutorial_check = DirectCheckButton(
            parent=self._main_fr,
            indicatorValue=base.game_config.tutorial_enabled,  # noqa: F821
            clickSound=self.click_snd,
            scale=0.02,
            pos=(0.12, 0, 0.41),
            boxBorder=0,
            boxImage=(GUI_PIC + "no_check.png", GUI_PIC + "check.png", None),
            boxRelief=None,
            relief="flat",
            frameColor=RUST_COL,
        )
        tutorial_check.setTransparency(TransparencyAttrib.MAlpha)
        self.conf_wids.append(tutorial_check)

        self.conf_wids.append(
            DirectLabel(  # Language
                parent=self._main_fr,
                text=base.labels.MAIN_MENU[24],  # noqa: F821,
                text_fg=RUST_COL,
                text_scale=0.04,
                text_font=base.main_font,  # noqa: F821
                pos=(-0.3, 0, 0.3),
                frameColor=(0, 0, 0, 0),
            )
        )

        lang_chooser = ListChooser()
        lang_chooser.prepare(
            self._main_fr,
            (0.1, 0, 0.31),
            LANGUAGES,
            LANGUAGES.index(base.game_config.language),  # noqa: F821,
        )
        self.conf_wids.append(lang_chooser)

        self.conf_wids.append(
            DirectLabel(  # Framerate limit
                parent=self._main_fr,
                text=base.labels.MAIN_MENU[29],  # noqa: F821,
                text_fg=RUST_COL,
                text_scale=0.04,
                text_font=base.main_font,  # noqa: F821
                pos=(-0.3, 0, 0.21),
                frameColor=(0, 0, 0, 0),
            )
        )

        fps_chooser = ListChooser()
        fps_chooser.prepare(
            self._main_fr,
            (0.1, 0, 0.22),
            FPS,
            FPS.index(str(base.game_config.fps_limit)),  # noqa: F821
        )
        self.conf_wids.append(fps_chooser)

        self.conf_wids.append(
            DirectLabel(  # FPS meter:
                parent=self._main_fr,
                text=base.labels.MAIN_MENU[36],  # noqa: F821,
                text_fg=RUST_COL,
                text_scale=0.04,
                text_font=base.main_font,  # noqa: F821
                pos=(-0.3, 0, 0.11),
                frameColor=(0, 0, 0, 0),
            )
        )

        fps_meter = DirectCheckButton(
            parent=self._main_fr,
            indicatorValue=base.game_config.fps_meter,  # noqa: F821
            clickSound=self.click_snd,
            scale=0.02,
            pos=(0.12, 0, 0.12),
            boxBorder=0,
            boxImage=(GUI_PIC + "no_check.png", GUI_PIC + "check.png", None),
            boxRelief=None,
            relief="flat",
            frameColor=RUST_COL,
        )
        fps_meter.setTransparency(TransparencyAttrib.MAlpha)
        self.conf_wids.append(fps_meter)

        self.conf_wids.append(
            DirectLabel(  # Multi threading:
                parent=self._main_fr,
                text=base.labels.MAIN_MENU[37],  # noqa: F821,
                text_fg=RUST_COL,
                text_scale=0.04,
                text_font=base.main_font,  # noqa: F821
                pos=(-0.3, 0, 0.01),
                frameColor=(0, 0, 0, 0),
            )
        )

        multi_threading = DirectCheckButton(
            parent=self._main_fr,
            indicatorValue=base.game_config.multi_threading,  # noqa: F821
            clickSound=self.click_snd,
            scale=0.02,
            pos=(0.12, 0, 0.02),
            boxBorder=0,
            boxImage=(GUI_PIC + "no_check.png", GUI_PIC + "check.png", None),
            boxRelief=None,
            relief="flat",
            frameColor=RUST_COL,
        )
        multi_threading.setTransparency(TransparencyAttrib.MAlpha)
        self.conf_wids.append(multi_threading)

        self.conf_wids.append(
            DirectLabel(  # Multi threading:
                parent=self._main_fr,
                text=base.labels.MAIN_MENU[38],  # noqa: F821,
                text_fg=SILVER_COL,
                text_scale=0.025,
                text_font=base.main_font,  # noqa: F821
                pos=(-0.3, 0, -0.03),
                frameColor=(0, 0, 0, 0),
            )
        )

        but = DirectButton(  # Save and restart
            parent=self._main_fr,
            text_scale=0.045,
            text_fg=RUST_COL,
            text=base.labels.MAIN_MENU[25],  # noqa: F821,
            text_font=base.main_font,  # noqa: F821
            relief=None,
            command=self._save_conf_and_restart,
            extraArgs=[
                res_chooser,
                tutorial_check,
                lang_chooser,
                fps_chooser,
                fps_meter,
                multi_threading,
            ],
            pos=(0.1, 0, -0.2),
            clickSound=self.click_snd,
        )
        self.bind_button(but)
        self.conf_wids.append(but)

    def _show_credits(self):
        """Show the game credits."""
        clear_wids(self.save_wids)
        clear_wids(self.conf_wids)
        clear_wids(self.tactics_wids)

        center = 0.25

        self.cred_wids.append(
            DirectLabel(
                parent=self._main_fr,
                pos=(center, 0, 0.6),
                text_scale=0.04,
                text_fg=SILVER_COL,
                text_font=base.main_font,  # noqa: F821
                frameColor=(0, 0, 0, 0),
                text=base.labels.MAIN_MENU[31],  # noqa: F821
            )
        )
        self.cred_wids.append(
            DirectLabel(  # Project source code
                parent=self._main_fr,
                pos=(center, 0, 0.5),
                text_scale=0.04,
                text_fg=SILVER_COL,
                text_font=base.main_font,  # noqa: F821
                frameColor=(0, 0, 0, 0),
                text=base.labels.MAIN_MENU[32],  # noqa: F821
            )
        )
        self.cred_wids.append(
            DirectButton(
                parent=self._main_fr,
                pos=(center, 0, 0.45),
                frameColor=(0, 0, 0, 0),
                text_scale=0.04,
                text_fg=RUST_COL,
                text="github.com/IlyaFaer/ForwardOnlyGame",
                text_font=base.main_font,  # noqa: F821
                relief=None,
                command=webbrowser.open,
                extraArgs=["https://github.com/IlyaFaer/ForwardOnlyGame"],
                clickSound=self.click_snd,
            )
        )
        self.cred_wids.append(
            DirectLabel(  # Subscribe
                parent=self._main_fr,
                pos=(center, 0, 0.35),
                text_scale=0.04,
                text_fg=SILVER_COL,
                text_font=base.main_font,  # noqa: F821
                frameColor=(0, 0, 0, 0),
                text=base.labels.MAIN_MENU[33],  # noqa: F821
            )
        )
        self.cred_wids.append(
            DirectButton(
                parent=self._main_fr,
                pos=(0.11, 0, 0.29),
                frameTexture="credits/youtube.png",
                frameSize=(-0.056, 0.056, -0.029, 0.029),
                relief="flat",
                command=webbrowser.open,
                extraArgs=["https://www.youtube.com/channel/UCKmtk9K6VkcQdOMiE7H-W9w"],
                clickSound=self.click_snd,
            )
        )
        self.cred_wids.append(
            DirectButton(
                parent=self._main_fr,
                pos=(center, 0, 0.29),
                frameTexture="credits/indie_db.png",
                frameSize=(-0.058, 0.058, -0.029, 0.029),
                relief="flat",
                command=webbrowser.open,
                extraArgs=["https://www.indiedb.com/games/forward-only"],
                clickSound=self.click_snd,
            )
        )
        but = DirectButton(
            parent=self._main_fr,
            pos=(0.38, 0, 0.29),
            frameTexture="credits/discord.png",
            frameSize=(-0.045, 0.045, -0.045, 0.045),
            relief="flat",
            command=webbrowser.open,
            extraArgs=["https://discord.gg/8UgFJAWsFx"],
            clickSound=self.click_snd,
        )
        but.setTransparency(TransparencyAttrib.MAlpha)
        self.cred_wids.append(but)
        self.cred_wids.append(
            DirectLabel(  # Stack
                parent=self._main_fr,
                pos=(center, 0, 0.18),
                text_scale=0.04,
                text_fg=SILVER_COL,
                text_font=base.main_font,  # noqa: F821
                frameColor=(0, 0, 0, 0),
                text=base.labels.MAIN_MENU[34],  # noqa: F821
            )
        )
        but = DirectButton(
            parent=self._main_fr,
            pos=(0.05, 0, 0.11),
            frameTexture="credits/python.png",
            frameSize=(-0.05, 0.05, -0.05, 0.05),
            relief="flat",
            command=webbrowser.open,
            extraArgs=["https://www.python.org/"],
            clickSound=self.click_snd,
        )
        but.setTransparency(TransparencyAttrib.MAlpha)
        self.cred_wids.append(but)

        but = DirectButton(
            parent=self._main_fr,
            pos=(0.185, 0, 0.11),
            frameTexture="credits/panda3d.png",
            frameSize=(-0.05, 0.05, -0.05, 0.05),
            relief="flat",
            command=webbrowser.open,
            extraArgs=["https://www.panda3d.org/"],
            clickSound=self.click_snd,
        )
        but.setTransparency(TransparencyAttrib.MAlpha)
        self.cred_wids.append(but)

        but = DirectButton(
            parent=self._main_fr,
            pos=(0.315, 0, 0.11),
            frameTexture="credits/blender.png",
            frameSize=(-0.05, 0.05, -0.05, 0.05),
            relief="flat",
            command=webbrowser.open,
            extraArgs=["https://www.blender.org/"],
            clickSound=self.click_snd,
        )
        but.setTransparency(TransparencyAttrib.MAlpha)
        self.cred_wids.append(but)

        but = DirectButton(
            parent=self._main_fr,
            pos=(0.45, 0, 0.11),
            frameTexture="credits/make_human.png",
            frameSize=(-0.05, 0.05, -0.05, 0.05),
            relief="flat",
            command=webbrowser.open,
            extraArgs=["http://www.makehumancommunity.org/"],
            clickSound=self.click_snd,
        )
        but.setTransparency(TransparencyAttrib.MAlpha)
        self.cred_wids.append(but)

        self.cred_wids.append(
            DirectLabel(  # Tools
                parent=self._main_fr,
                pos=(center, 0, -0.02),
                text_scale=0.04,
                text_fg=SILVER_COL,
                text_font=base.main_font,  # noqa: F821
                frameColor=(0, 0, 0, 0),
                text=base.labels.MAIN_MENU[35],  # noqa: F821
            )
        )
        but = DirectButton(
            parent=self._main_fr,
            pos=(center - 0.12, 0, -0.09),
            frameTexture="credits/free_sound.png",
            frameSize=(-0.057, 0.057, -0.029, 0.029),
            relief="flat",
            command=webbrowser.open,
            extraArgs=["https://freesound.org/"],
            clickSound=self.click_snd,
        )
        but.setTransparency(TransparencyAttrib.MAlpha)
        self.cred_wids.append(but)

        but = DirectButton(
            parent=self._main_fr,
            pos=(center, 0, -0.09),
            frameTexture="credits/photopea.png",
            frameSize=(-0.03, 0.03, -0.03, 0.03),
            relief="flat",
            command=webbrowser.open,
            extraArgs=["https://www.photopea.com/"],
            clickSound=self.click_snd,
        )
        but.setTransparency(TransparencyAttrib.MAlpha)
        self.cred_wids.append(but)

        but = DirectButton(
            parent=self._main_fr,
            pos=(center + 0.09, 0, -0.09),
            frameTexture="credits/online_convert.png",
            frameSize=(-0.03, 0.03, -0.03, 0.03),
            relief="flat",
            command=webbrowser.open,
            extraArgs=["https://audio.online-convert.com/"],
            clickSound=self.click_snd,
        )
        but.setTransparency(TransparencyAttrib.MAlpha)
        self.cred_wids.append(but)

        self.cred_wids.append(
            DirectLabel(  # Music
                parent=self._main_fr,
                pos=(center, 0, -0.24),
                text_scale=0.042,
                text_fg=SILVER_COL,
                text_font=base.main_font,  # noqa: F821
                frameColor=(0, 0, 0, 0),
                text=base.labels.MAIN_MENU[39],  # noqa: F821
            )
        )
        but = DirectButton(
            parent=self._main_fr,
            pos=(-0.15, 0, -0.45),
            frameTexture="credits/among_madness_logo.png",
            frameSize=(-0.15, 0.15, -0.15, 0.15),
            relief="flat",
            command=webbrowser.open,
            extraArgs=["https://open.spotify.com/artist/3uy4tvaLvBAsKdV52Kc2TI"],
            clickSound=self.click_snd,
        )
        but.setTransparency(TransparencyAttrib.MAlpha)
        self.cred_wids.append(but)

        self.cred_wids.append(
            DirectLabel(
                parent=self._main_fr,
                pos=(-0.15, 0, -0.65),
                text_scale=0.033,
                text_fg=SILVER_COL,
                text_font=base.main_font,  # noqa: F821
                frameColor=(0, 0, 0, 0),
                text="Among Madness",
            )
        )

        but = DirectButton(
            parent=self._main_fr,
            pos=(0.25, 0, -0.45),
            frameTexture="credits/qualia_logo.png",
            frameSize=(-0.15, 0.15, -0.15, 0.15),
            relief="flat",
            command=webbrowser.open,
            extraArgs=["https://open.spotify.com/artist/1LAJZmgQeOryYUV8qoF9tF"],
            clickSound=self.click_snd,
        )
        but.setTransparency(TransparencyAttrib.MAlpha)
        self.cred_wids.append(but)

        self.cred_wids.append(
            DirectLabel(
                parent=self._main_fr,
                pos=(0.25, 0, -0.65),
                text_scale=0.033,
                text_fg=SILVER_COL,
                text_font=base.main_font,  # noqa: F821
                frameColor=(0, 0, 0, 0),
                text="Квалиа",
            )
        )

        but = DirectButton(
            parent=self._main_fr,
            pos=(0.65, 0, -0.45),
            frameTexture="credits/moloken_logo.png",
            frameSize=(-0.15, 0.15, -0.15, 0.15),
            relief="flat",
            command=webbrowser.open,
            extraArgs=["https://open.spotify.com/artist/3LZzdqKCEcBwhh6vd6y6Q5"],
            clickSound=self.click_snd,
        )
        but.setTransparency(TransparencyAttrib.MAlpha)
        self.cred_wids.append(but)

        self.cred_wids.append(
            DirectLabel(
                parent=self._main_fr,
                pos=(0.65, 0, -0.65),
                text_scale=0.033,
                text_fg=SILVER_COL,
                text_font=base.main_font,  # noqa: F821
                frameColor=(0, 0, 0, 0),
                text="Moloken",
            )
        )

    def _show_crew(self, crew):
        """Show the description of the chosen tactics.

        Args:
            crew (str): The chosen tactics name.
        """
        self._chosen_crew = crew
        self._crew_preview["frameTexture"] = "gui/tex/preview/{}.png".format(crew)

        for key, but in self._crew_buts.items():
            but["text_fg"] = SILVER_COL if key == crew else RUST_COL

        descs = {
            "soldiers": base.labels.MAIN_MENU[11],  # noqa: F821
            "raiders": base.labels.MAIN_MENU[12],  # noqa: F821
            "anarchists": base.labels.MAIN_MENU[13],  # noqa: F821
        }
        self._team_description["text"] = descs[crew]

    def _show_slots(self, for_loading=False):
        """Show save slots GUI.

        Args:
            for_loading (bool):
                Optional. True if slots must be shown for loading.
        """
        if self.save_wids:
            return

        clear_wids(self.tactics_wids)
        clear_wids(self.conf_wids)
        clear_wids(self.cred_wids)

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

        z_shift = 0.5
        x_shift = -0.2
        for num in range(1, 4):
            but = DirectButton(
                parent=self._main_fr,
                text="Slot {}".format(str(num)),
                pos=(x_shift - 0.103, 0, z_shift),
                text_scale=0.04,
                text_fg=RUST_COL,
                relief=None,
                command=command if is_active else None,
                extraArgs=[num],
                clickSound=self.click_snd,
            )
            self.bind_button(but)
            self.save_wids.append(but)

            self.save_wids.append(
                DirectLabel(
                    parent=self._main_fr,
                    pos=(x_shift, 0, z_shift - 0.05),
                    text_scale=0.03,
                    text_fg=SILVER_COL,
                    frameColor=(0, 0, 0, 0),
                    text=saves[num - 1].get("save_time", "-"),
                )
            )
            self.save_wids.append(
                DirectLabel(
                    parent=self._main_fr,
                    pos=(x_shift - 0.1, 0, z_shift - 0.1),
                    text_scale=0.03,
                    text_fg=SILVER_COL,
                    frameColor=(0, 0, 0, 0),
                    text=(str(saves[num - 1].get("miles") or "- ")) + " mi",
                )
            )
            self.save_wids.append(
                DirectLabel(
                    parent=self._main_fr,
                    pos=(x_shift + 0.35, 0, z_shift - 0.1),
                    text_scale=0.03,
                    text_fg=SILVER_COL,
                    frameColor=(0, 0, 0, 0),
                    text="{0} soldiers, {1} raiders, {2} anarchists".format(
                        *saves[num - 1].get("chars", ("-", "-", "-"))
                    ),
                )
            )
            z_shift -= 0.2

    def _start_new_game(self):
        """Start a new game."""
        taskMgr.doMethodLater(  # noqa: F821
            4, self._clear_temp_wids, "clear_main_menu_temp_wids"
        )
        self.show_loading(is_game_start=True)
        taskMgr.doMethodLater(  # noqa: F821
            0.25,
            base.start_new_game,  # noqa: F821
            "start_new_game",
            extraArgs=[self._chosen_crew],
        )

    def bind_button(self, button):
        """Bind the given button to visual effects.

        Args:
            button (panda3d.gui.DirectGui.DirectButton): Button to bind.
        """
        button.bind(DGG.ENTER, self._highlight_but, extraArgs=[button])
        button.bind(DGG.EXIT, self._dehighlight_but, extraArgs=[button])

    def hide(self):
        """Hide the main menu."""
        self._main_fr.hide()
        clear_wids(self.save_wids)
        clear_wids(self.conf_wids)
        clear_wids(self.cred_wids)

        if self._load_screen is not None:
            self._load_screen.destroy()
            self._load_screen = None

        base.accept("escape", self.show)  # noqa: F821
        taskMgr.remove("check_can_save")  # noqa: F821

    def hide_loading_msg(self):
        """Hide the "Loading..." message widget."""
        self._load_msg.destroy()

    def show_credits(self, task):
        """Show the game end credits."""

        mus = loader.loadSfx("sounds/music/Moloken - 11''12.mp3")  # noqa: F821
        mus.setVolume(0.2)
        mus.play()

        goodness = 0

        inserts = {}
        for key, value in base.decisions.items():  # noqa: F821
            inserts[key] = value["decision"]
            goodness += value["goodness"]

        if goodness <= 15:
            inserts["leader_desc"] = base.labels.ROUGH_LEADER  # noqa: F821
        elif goodness <= 30:
            inserts["leader_desc"] = base.labels.OPPORTUNIST_LEADER  # noqa: F821
        else:
            inserts["leader_desc"] = base.labels.EMPATHIC_LEADER  # noqa: F821

        frame = DirectFrame(
            frameSize=(-2, 2, -1, 1),
            frameColor=(0.15, 0.15, 0.15, 1),
            state=DGG.NORMAL,
        )
        lab = DirectLabel(
            parent=frame,
            text=base.labels.CREDITS.format(**inserts),  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            text_scale=0.042,
            text_fg=SILVER_COL,
            frameColor=(0, 0, 0, 0),
            text_align=TextNode.ACenter,
            pos=(0, 0, -1.5),
        )
        LerpPosInterval(lab, 100, (0, 0, 10)).start()
        return task.done

    def show_loading(self, is_game_start=False):
        """Show game loading screen.

        Args:
            is_game_start (bool):
                Flag, indicating if the player just started a new game.
        """
        if is_game_start:
            self.hide()
            self._load_screen = DirectFrame(
                frameSize=(-2, 2, -1, 1),
                frameColor=(0.15, 0.15, 0.15, 1),
                state=DGG.NORMAL,
            )
            DirectLabel(
                parent=self._load_screen,
                text=base.labels.SCENARIO_LABELS[2],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                text_scale=0.056,
                text_fg=RUST_COL,
                frameColor=(0, 0, 0, 0),
                text_align=TextNode.ALeft,
                pos=(-1, 0, 0.5),
            )
            DirectLabel(
                parent=self._load_screen,
                text=base.labels.PREAMBULA,  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                text_scale=0.033,
                text_fg=SILVER_COL,
                frameColor=(0, 0, 0, 0),
                text_align=TextNode.ALeft,
                pos=(-1, 0, 0.4),
            )

        self._load_msg = DirectLabel(  # Loading...
            parent=self._load_screen or self._main_fr,
            text=base.labels.MAIN_MENU[26],  # noqa: F821,
            text_font=base.main_font,  # noqa: F821
            text_fg=RUST_COL,
            frameSize=(1, 1, 1, 1),
            text_scale=0.04,
            pos=(0, 0, -0.75),
        )

    def show(self, is_game_over=False):
        """Show the main menu.

        Args:
            is_game_over (bool):
                True, if the main menu is shown on game over.
        """
        if not getattr(base, "traits_gui", None):  # noqa: F821
            return

        if base.world.rails_scheme.is_shown:  # noqa: F821
            base.world.rails_scheme.show()  # noqa: F821

        if base.traits_gui.is_shown:  # noqa: F821
            base.traits_gui.hide()  # noqa: F821

        self._main_fr.show()

        if is_game_over:
            self._new_game_but["command"] = None
            self._new_game_but["text_fg"] = SILVER_COL
            DirectLabel(
                parent=self._main_fr,
                pos=(0.85, 0, 0.3),
                frameColor=(0, 0, 0, 0),
                text_scale=0.055,
                text_fg=SILVER_COL,
                text_font=base.main_font,  # noqa: F821
                text=base.labels.MAIN_MENU[28],  # noqa: F821
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

        self._new_game_but["text"] = base.labels.MAIN_MENU[21]  # noqa: F821
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
            pos=(-1.12, 0, 0.3),
            text_scale=0.05,
            text_fg=RUST_COL if can_save else SILVER_COL,
            text=base.labels.MAIN_MENU[15],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            relief=None,
            text_align=TextNode.ALeft,
            command=self._show_slots if can_save else None,  # noqa: F821
            clickSound=self.click_snd,
        )
        self.bind_button(self._save_but)

        self.bind_button(
            DirectButton(  # Main menu
                parent=self._main_fr,
                pos=(-1.12, 0, 0),
                text_scale=0.05,
                text_fg=RUST_COL,
                text=base.labels.MAIN_MENU[14],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                relief=None,
                command=base.restart_game,  # noqa: F821
                text_align=TextNode.ALeft,
                clickSound=self.click_snd,
            )
        )
        self._is_first_pause = False

    def show_start_button(self):
        """Show a button to start a game on the loading screen."""
        parent = self._load_msg.getParent()
        self._load_msg.destroy()

        self._load_msg = DirectButton(
            parent=parent,
            text=base.labels.MAIN_MENU[27],  # noqa: F821,
            text_font=base.main_font,  # noqa: F821
            text_fg=RUST_COL,
            text_scale=0.04,
            pos=(0, 0, -0.75),
            relief=None,
            clickSound=self.click_snd,
            command=base.start_game,  # noqa: F821
        )
        self.bind_button(self._load_msg)

    def stop_music(self):
        """Stop the main menu music."""
        taskMgr.doMethodLater(  # noqa: F821
            0.3,
            drown_snd,
            "drown_menu_music",
            extraArgs=[self._menu_music],
            appendTask=True,
        )
        taskMgr.doMethodLater(  # noqa: F821
            3,
            loader.unloadSfx,  # noqa: F821
            "unload_menu_music",
            extraArgs=[self._menu_music],
            appendTask=False,
        )
