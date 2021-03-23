"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

GUI used for teaching players.
"""
from direct.gui.DirectGui import DGG, DirectButton, DirectFrame, DirectLabel
from panda3d.core import TransparencyAttrib

from personage.enemy_unit import (
    BrakeThrower,
    DodgeShooter,
    MotoShooter,
    StunBombThrower,
)
from .widgets import RUST_COL, SILVER_COL

CLASS_DESCS = {
    MotoShooter: {
        "desc": (
            "Moto shooter will try to shoot at you and\n"
            "your locomotive as much as he can. Most of\n"
            "the skinheads prefer such a way of\n"
            "communication with foreigners, so stay\n"
            "sharp - there will be a lot of them."
        ),
        "preview": "shooter",
        "but_text": "We're ready!",
        "title": "Some skinheads searching for you!",
    },
    BrakeThrower: {
        "desc": (
            "Brake thrower will try to overtake you and\n"
            "throw a brake shoe under your wheels to slow\n"
            "you down. Such guys are not tough themselves,\n"
            "but they can make other skinhead attacks more\n"
            "successful. Try to deal with them fast!"
        ),
        "preview": "brake_thrower",
        "but_text": "Bring'em on!",
        "title": "Skinheads rumoring about dare newbies!",
    },
    StunBombThrower: {
        "desc": (
            "Such a guy uses stun bombs to make your fighters\n"
            "non-operational for several seconds. It's hard for\n"
            "a thrower to get right into a fast moving target,\n"
            "but if you'll lose some of your speed, throw\n"
            "efficiency will significantly increase."
        ),
        "preview": "bomb_thrower",
        "but_text": "We'll deal with them!",
        "title": "Skinheads start to take you seriously!",
    },
    DodgeShooter: {
        "desc": (
            "Dodge with a machine gun is a strong enemy! It can\n"
            "do a lot of damage to your locomotive, but the\n"
            "machine gun overheat fast and requires time to\n"
            "cool down. Armor Plate train upgrade recommended\n"
            "to be used for protection against this enemy."
        ),
        "preview": "dodge",
        "but_text": "They won't stop us!",
        "title": "Skinheads gather vehicles to deal with you!",
    },
}


class EnemyClassDesc:
    """Enemy class description.

    A teaching note about enemy type. Is shown on player's
    screen, when a new enemy type is added into the
    list of attacking enemy units.
    """

    def __init__(self, class_):
        self._fr = DirectFrame(
            frameSize=(-0.5, 0.5, -0.5, 0.5),
            frameColor=(0.18, 0.18, 0.18, 0.82),
            state=DGG.NORMAL,
        )
        DirectLabel(
            parent=self._fr,
            text=CLASS_DESCS[class_]["title"],
            text_fg=RUST_COL,
            text_scale=0.038,
            pos=(0, 0, 0.44),
            frameColor=(0, 0, 0, 0),
        )
        DirectFrame(
            parent=self._fr,
            frameTexture="teach_shots/{}.png".format(CLASS_DESCS[class_]["preview"]),
            pos=(0, 0, 0.15),
            frameSize=(-0.39, 0.39, -0.24, 0.24),
        ).setTransparency(TransparencyAttrib.MAlpha)
        DirectLabel(
            parent=self._fr,
            pos=(0, 0, -0.18),
            frameColor=(0, 0, 0, 0),
            text_fg=SILVER_COL,
            text_scale=0.035,
            text=CLASS_DESCS[class_]["desc"],
        )
        base.main_menu.bind_button(  # noqa: F821
            DirectButton(
                parent=self._fr,
                text=CLASS_DESCS[class_]["but_text"],
                text_scale=0.04,
                relief=None,
                pos=(0, 0, -0.45),
                text_fg=RUST_COL,
                command=self._hide,
                clickSound=base.main_menu.click_snd,  # noqa: F821
            )
        )

    def _hide(self):
        """Destroy the teaching note."""
        self._fr.destroy()
