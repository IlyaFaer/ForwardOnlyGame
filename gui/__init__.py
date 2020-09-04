"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Game GUI interfaces.
"""
from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel

from utils import save_exists
from .character import CharacterInterface  # noqa: F401
from .city import CityInterface  # noqa: F401
from .notes import TeachingNotes  # noqa: F401
from .outings import OutingsInterface  # noqa: F401
from .resources import ResourcesInterface  # noqa: F401
from .train import ICON_PATH, RUST_COL, TrainInterface  # noqa: F401


class MainMenu:
    """Main game menu.

    Includes starting a game, loading, saving and exiting.
    """

    def __init__(self):
        self._is_first_pause = True
        self._main_fr = DirectFrame(frameSize=(-2, 2, -1, 1), frameColor=(0, 0, 0, 1))

        self._new_game_but = DirectButton(
            parent=self._main_fr,
            pos=(-1, 0, 0.5),
            text_scale=(0.05, 0.05),
            text_fg=RUST_COL,
            text="New game",
            relief=None,
            command=self._start_new_game,
        )
        is_save_exists = save_exists()
        self._load_game_but = DirectButton(
            parent=self._main_fr,
            pos=(-0.996, 0, 0.4),
            text_scale=(0.05, 0.05),
            text_fg=RUST_COL if is_save_exists else (0.5, 0.5, 0.5, 1),
            text="Load game",
            relief=None,
            command=self._load_game if is_save_exists else None,
        )
        DirectButton(
            parent=self._main_fr,
            pos=(-1.083, 0, 0),
            text_scale=(0.05, 0.05),
            text_fg=RUST_COL,
            text="Exit",
            relief=None,
            command=exit,
        )

    def _start_new_game(self):
        """Start a new game."""
        self.show_loading()
        base.doMethodLater(0.25, base.start_new_game, "start_new_game")  # noqa: F821

    def _load_game(self):
        """Load previously saved game."""
        self.show_loading()
        base.doMethodLater(0.25, base.load_game, "load_game")  # noqa: F821

    def show_loading(self):
        self._game_load_msg = DirectLabel(
            parent=self._main_fr,
            text="Loading...",
            text_fg=RUST_COL,
            frameSize=(1, 1, 1, 1),
            text_scale=(0.04),
            pos=(0, 0, -0.63),
        )

    def hide(self):
        """Hide main menu."""
        self._main_fr.hide()
        base.accept("escape", self.show)  # noqa: F821

    def show(self):
        """Show main menu."""
        self._main_fr.show()
        base.accept("escape", self.hide)  # noqa: F821
        if not self._is_first_pause:
            return

        self._main_fr["frameColor"] = (0, 0, 0, 0.6)
        self._game_load_msg.hide()
        self._new_game_but["text"] = "Resume"
        self._new_game_but["command"] = self.hide
        self._new_game_but.setPos(-1.028, 0, 0.4),

        self._load_game_but.destroy()

        DirectButton(
            parent=self._main_fr,
            pos=(-0.998, 0, 0.3),
            text_scale=(0.05, 0.05),
            text_fg=RUST_COL,
            text="Save game",
            relief=None,
            command=base.save_game,  # noqa: F821
        )
        self._is_first_pause = False
