"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Cities GUI.
"""
from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel
from panda3d.core import TransparencyAttrib

from .interface import ICON_PATH, RUST_COL, SILVER_COL, CharacterChooser


class CityInterface:
    """City GUI interface.

    Includes healing and regaining energy for the player
    units. Every service requires some money to be spent.
    """

    def __init__(self):
        self._city_fr = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.35, 0.35, -0.7, 0.7),
            pos=(0.75, 0, -1),
            frameTexture=ICON_PATH + "metal1.png",
        )
        self._city_fr.setTransparency(TransparencyAttrib.MAlpha)
        self._city_fr.hide()

        DirectLabel(
            parent=self._city_fr,
            text="Services",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.045, 0.045),
            text_fg=RUST_COL,
            pos=(0, 0, 0.62),
        )
        DirectLabel(
            parent=self._city_fr,
            text="Team",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.035, 0.035),
            text_fg=RUST_COL,
            pos=(-0.27, 0, 0.57),
        )

        self._char_chooser = CharacterChooser(
            [char.id for char in base.team.chars.values()]  # noqa: F821
        )
        self._char_chooser.setPos(self._city_fr, (0, 0, 0.52))

        DirectLabel(
            parent=self._city_fr,
            frameColor=(0, 0, 0, 0.3),
            text_fg=SILVER_COL,
            text="Health",
            text_scale=(0.03, 0.03),
            pos=(-0.2, 0, 0.43),
        )
        DirectButton(
            parent=self._city_fr,
            pos=(-0.05, 0, 0.45),
            text_fg=SILVER_COL,
            text="+10\n10$",
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=(0.45, 0.45),
            command=self._heal,
            extraArgs=[10],
        )
        DirectButton(
            parent=self._city_fr,
            pos=(0.05, 0, 0.45),
            text_fg=SILVER_COL,
            text="+50\n50$",
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=(0.45, 0.45),
            command=self._heal,
            extraArgs=[50],
        )
        DirectLabel(
            parent=self._city_fr,
            frameColor=(0, 0, 0, 0.3),
            text_fg=SILVER_COL,
            text="Energy",
            text_scale=(0.03, 0.03),
            pos=(-0.2, 0, 0.33),
        )
        DirectButton(
            parent=self._city_fr,
            pos=(-0.05, 0, 0.35),
            text_fg=SILVER_COL,
            text="+10\n5$",
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=(0.45, 0.45),
            command=self._rest,
            extraArgs=[10],
        )
        DirectButton(
            parent=self._city_fr,
            pos=(0.05, 0, 0.35),
            text_fg=SILVER_COL,
            text="+50\n25$",
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=(0.45, 0.45),
            command=self._rest,
            extraArgs=[50],
        )
        DirectButton(
            parent=self._city_fr,
            pos=(0.2, 0, 0.25),
            text_fg=SILVER_COL,
            text="Leave unit",
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=(0.45, 0.45),
            command=self._send_away,
        )

    def _send_away(self):
        """Send the chosen unit away."""
        if len(base.team.chars) == 1:  # noqa: F821
            return

        char = self._char_chooser.chosen_char
        base.taskMgr.doMethodLater(0.25, char.clear, char.id + "_clear")  # noqa: F821
        self._char_chooser.leave_unit(char.id)

    def _heal(self, value):
        """Heal the chosen character.

        Spends money.

        Args:
            value (int): Points to heal.
        """
        if base.dollars - value < 0:  # noqa: F821
            return

        self._char_chooser.chosen_char.health += value
        base.dollars -= value  # noqa: F821
        base.res_interface.update_money(base.dollars)  # noqa: F821

    def _rest(self, value):
        """Regain energy of the chosen character.

        Spends money.

        Args:
            value (int): Points to regain.
        """
        spent = 5 if value == 10 else 25
        if base.dollars - spent < 0:  # noqa: F821
            return

        self._char_chooser.chosen_char.energy += value
        base.dollars -= spent  # noqa: F821
        base.res_interface.update_money(base.dollars)  # noqa: F821

    def show(self):
        """Show city GUI."""
        self._city_fr.show()
