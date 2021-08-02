"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

GUI used for teaching players.
"""
from direct.gui.DirectGui import DGG, DirectButton, DirectFrame, DirectLabel
from panda3d.core import TransparencyAttrib

from .widgets import RUST_COL, SILVER_COL


class EnemyDesc:
    """Enemy class/object description.

    A teaching note about enemy class/object. Is shown on
    player's screen, when a new enemy class/object is added
    into the list of attacking enemy units.
    """

    def __init__(self, class_):
        self._fr = DirectFrame(
            frameSize=(-0.5, 0.5, -0.5, 0.5),
            frameColor=(0.14, 0.14, 0.14, 0.82),
            state=DGG.NORMAL,
        )
        DirectLabel(  # the note title
            parent=self._fr,
            text=base.labels.CLASS_DESCS[class_]["title"],  # noqa: F821
            text_font=base.main_font, # noqa: F821
            text_fg=RUST_COL,
            text_scale=0.038,
            pos=(0, 0, 0.44),
            frameColor=(0, 0, 0, 0),
        )
        # an image on the note (usually demonstrates
        # the new enemy class/object representer)
        DirectFrame(
            parent=self._fr,
            frameTexture="teach_shots/{}.png".format(
                base.labels.CLASS_DESCS[class_]["preview"]  # noqa: F821
            ),
            pos=(0, 0, 0.15),
            frameSize=(-0.39, 0.39, -0.24, 0.24),
        ).setTransparency(TransparencyAttrib.MAlpha)

        DirectLabel(  # the enemy class/object description
            parent=self._fr,
            pos=(0, 0, -0.18),
            frameColor=(0, 0, 0, 0),
            text_fg=SILVER_COL,
            text_scale=0.035,
            text=base.labels.CLASS_DESCS[class_]["desc"],  # noqa: F821
            text_font=base.main_font, # noqa: F821
        )
        base.main_menu.bind_button(  # noqa: F821
            DirectButton(
                parent=self._fr,
                text=base.labels.CLASS_DESCS[class_]["but_text"],  # noqa: F821
                text_font=base.main_font, # noqa: F821
                text_scale=0.04,
                relief=None,
                pos=(0, 0, -0.45),
                text_fg=RUST_COL,
                command=self._hide,
                clickSound=base.main_menu.click_snd,  # noqa: F821
            )
        )
        base.main_menu.new_enemy_snd.play()  # noqa: F821

    def _hide(self):
        """Destroy the teaching note."""
        self._fr.destroy()


class MechanicDesc:
    """Teaching description of a game mechanic.

    Are shown on particular world blocks on the game start.

    Args:
        mechanic (str): The name of the game mechanic to be explained.
    """

    def __init__(self, mechanic):
        self._page = 0

        self._fr = DirectFrame(
            frameSize=(-0.5, 0.5, -0.5, 0.5),
            frameColor=(0.14, 0.14, 0.14, 0.82),
            state=DGG.NORMAL,
        )
        DirectLabel(
            parent=self._fr,
            text=base.labels.MAIN_MENU[23] + " " + mechanic,  # noqa: F821
            text_fg=RUST_COL,
            text_font=base.main_font,  # noqa: F821
            text_scale=0.038,
            pos=(0, 0, 0.44),
            frameColor=(0, 0, 0, 0),
        )
        self._preview = DirectFrame(  # an image describing the mechanic
            parent=self._fr,
            frameTexture="teach_shots/{}.png".format(
                base.labels.MECHANIC_DESC[mechanic]["previews"][  # noqa: F821
                    self._page
                ]
            ),
            pos=(0, 0, 0.15),
            frameSize=(-0.39, 0.39, -0.24, 0.24),
        )
        self._preview.setTransparency(TransparencyAttrib.MAlpha)

        self._desc = DirectLabel(  # the mechanic description
            parent=self._fr,
            pos=(0, 0, -0.18),
            frameColor=(0, 0, 0, 0),
            text_fg=SILVER_COL,
            text_scale=0.035,
            text=base.labels.MECHANIC_DESC[mechanic]["descs"][self._page],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
        )
        is_last_page = self._page + 1 == len(
            base.labels.MECHANIC_DESC[mechanic]["descs"]  # noqa: F821
        )

        self._but = DirectButton(
            parent=self._fr,
            text=base.labels.MECHANIC_BUTS[1]  # noqa: F821
            if is_last_page
            else base.labels.MECHANIC_BUTS[0],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            text_scale=0.04,
            relief=None,
            pos=(0, 0, -0.45),
            text_fg=RUST_COL,
            command=self._hide if is_last_page else self._next_page,
            extraArgs=[] if is_last_page else [mechanic],
            clickSound=base.main_menu.click_snd,  # noqa: F821
        )
        base.main_menu.bind_button(self._but)  # noqa: F821

        base.train.ctrl.pause_movement()  # noqa: F821

    def _hide(self):
        """Destroy the teaching note."""
        self._fr.destroy()
        base.train.ctrl.start_move()  # noqa: F821

    def _next_page(self, mechanic):
        """Show the next page of the mechanic tutorial.

        Args:
            mechanic (str): The explained mechanic name.
        """
        self._page += 1

        is_last_page = self._page + 1 == len(
            base.labels.MECHANIC_DESC[mechanic]["descs"]  # noqa: F821
        )

        if is_last_page:
            self._but["text"] = base.labels.MECHANIC_BUTS[1]  # noqa: F821
            self._but["command"] = self._hide
            self._but["extraArgs"] = []

        self._preview["frameTexture"] = "teach_shots/{}.png".format(
            base.labels.MECHANIC_DESC[mechanic]["previews"][self._page]  # noqa: F821
        )
        self._desc["text"] = base.labels.MECHANIC_DESC[mechanic]["descs"][  # noqa: F821
            self._page
        ]
