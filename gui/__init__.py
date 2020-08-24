"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Game GUI interfaces.
"""
from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel

from .character import CharacterInterface  # noqa: F401
from .city import CityInterface  # noqa: F401
from .train import ICON_PATH, RUST_COL, TrainInterface  # noqa: F401
from .outings import OutingsInterface  # noqa: F401
from .resources import ResourcesInterface  # noqa: F401


class MainMenu:
    """Main game menu.

    Includes starting a game, loading, saving and exiting.
    """

    def __init__(self):
        self._main_fr = DirectFrame(frameSize=(-2, 2, -1, 1), frameColor=(0, 0, 0, 1))

        DirectButton(
            parent=self._main_fr,
            pos=(-1, 0, 0.5),
            text_scale=(0.05, 0.05),
            text_fg=RUST_COL,
            text="New game",
            relief=None,
            command=self._start_new_game,
        )
        DirectButton(
            parent=self._main_fr,
            pos=(-0.996, 0, 0.4),
            text_scale=(0.05, 0.05),
            text_fg=(0.5, 0.5, 0.5, 1),
            text="Load game",
            relief=None,
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
        self._game_load_msg = DirectLabel(
            parent=self._main_fr,
            text="Loading...",
            text_fg=RUST_COL,
            frameSize=(1, 1, 1, 1),
            text_scale=(0.04),
            pos=(0, 0, -0.63),
        )
        base.doMethodLater(0.25, base.start_new_game, "start_new_game")  # noqa: F821

    def hide(self):
        """Hide main menu."""
        self._main_fr.hide()
