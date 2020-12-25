"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Character state GUI.
"""
from direct.gui.DirectGui import (
    DGG,
    DirectButton,
    DirectFrame,
    DirectLabel,
    DirectWaitBar,
)
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TransparencyAttrib

from personage.character_data import TRAIT_DESC
from .widgets import ICON_PATH, RUST_COL, SILVER_COL

ABOUT_BUT_PARAMS = {
    "text": "?",
    "frameSize": (-0.03, 0.03, -0.03, 0.03),
    "frameColor": (0, 0, 0, 0),
    "text_bg": (0, 0, 0, 0),
    "text_fg": SILVER_COL,
    "text_scale": 0.03,
    "relief": "flat",
}


class CharacterInterface:
    """Widget with the chosen character info."""

    def __init__(self):
        self._char = None  # the chosen character
        self._rest_buttons = {}
        self._rest_list_active = False

        self._char_desc_wids = []
        self._char_desc_shown = False

        self._fr = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.31, 0.31, -0.1, 0.115),
            pos=(0.31, 0, -1.9),
            frameTexture=ICON_PATH + "metal1.png",
            state=DGG.NORMAL,
        )
        self._fr.setTransparency(TransparencyAttrib.MAlpha)

        self._char_desc_but = DirectButton(
            parent=self._fr,
            pos=(0.27, 0, 0.0675),
            command=self._show_char_desc,
            clickSound=base.main_menu.click_snd,  # noqa: F821
            **ABOUT_BUT_PARAMS,
        )
        DirectLabel(
            parent=self._fr,
            text="Name:",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.22, 0, 0.07),
        )
        self._char_name = DirectLabel(
            parent=self._fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=SILVER_COL,
            pos=(-0.09, 0, 0.069),
        )
        self._traits_list = DirectLabel(
            parent=self._fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.028, 0.028),
            text_fg=SILVER_COL,
            pos=(0, 0, 0.025),
        )
        DirectLabel(
            parent=self._fr,
            text="Type:",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(0.05, 0, 0.07),
        )
        self._char_class = DirectLabel(
            parent=self._fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=SILVER_COL,
            pos=(0.17, 0, 0.068),
        )
        DirectLabel(
            parent=self._fr,
            text="Health",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.22, 0, -0.015),
        )
        self._char_health = DirectWaitBar(
            parent=self._fr,
            frameSize=(-0.17, 0.17, -0.002, 0.002),
            value=0,
            barColor=(0.85, 0.2, 0.28, 1),
            pos=(0.07, 0, -0.008),
        )
        DirectLabel(
            parent=self._fr,
            text="Energy",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.216, 0, -0.06),
        )
        self._char_energy = DirectWaitBar(
            parent=self._fr,
            frameSize=(-0.17, 0.17, -0.002, 0.002),
            value=0,
            barColor=(0.46, 0.61, 0.53, 1),
            pos=(0.07, 0, -0.053),
        )
        self._tip = OnscreenText(
            parent=base.render2d,  # noqa: F821
            text="",
            scale=(0.021, 0.027),
            fg=SILVER_COL,
            bg=(0, 0, 0, 0.4),
        )
        self._tip.hide()

        self._disease = DirectFrame(
            parent=self._fr,
            frameSize=(-0.02, 0.02, -0.02, 0.02),
            pos=(0.27, 0, -0.008),
            frameTexture=ICON_PATH + "disease.png",
        )
        self._disease.setTransparency(TransparencyAttrib.MAlpha)
        self._disease.hide()

        self.clear_char_info()

    def show_char_info(self, character):
        """Show the given character parameters.

        Args:
            character (personage.character.Character):
                The chosen character object.
        """
        self._char_name["text"] = character.name
        self._char_class["text"] = character.class_.capitalize()
        self._traits_list["text"] = ", ".join(character.traits)

        self._char_health["range"] = character.class_data["health"]
        self._char_health["value"] = character.health
        self._char_energy["value"] = character.energy

        if character.is_diseased:
            self._disease.show()

        self._char = character

        self._char_name.show()
        self._char_class.show()
        self._char_health.show()
        self._char_energy.show()
        self._traits_list.show()
        self._char_desc_but.show()

        if self._char_desc_shown:
            self._show_char_desc()
            self._show_char_desc()

        taskMgr.doMethodLater(  # noqa: F821
            0.5, self._update_char_info, "track_char_info"
        )

    def clear_char_info(self):
        """Clear the character interface."""
        self._char_name.hide()
        self._char_class.hide()
        self._char_health.hide()
        self._char_energy.hide()
        self._traits_list.hide()
        self._char_desc_but.hide()
        self._disease.hide()

        if self._char_desc_shown:
            self._show_char_desc()

        taskMgr.remove("track_char_info")  # noqa: F821
        self._char = None

        for but in self._rest_buttons.values():
            but.destroy()

        self._rest_list_active = False

    def show_tooltip(self, text):
        """Show tooltip with the given text.

        Args:
            text (str): Text to show in the tooltip.
        """
        if not base.mouseWatcherNode.hasMouse():  # noqa: F821
            return

        if self._rest_list_active and text == "Rest zone":
            return

        self._tip.setText(text)
        self._tip.setX(base.mouseWatcherNode.getMouseX())  # noqa: F821
        self._tip.setY(base.mouseWatcherNode.getMouseY())  # noqa: F821
        self._tip.show()

    def hide_tip(self):
        """Hide the tooltip."""
        self._tip.hide()

    def show_resting_chars(self, part):
        """Show a list of the characters resting in this part.

        Args:
            part (Train.RestPart): Rest part of the Train.
        """
        if self._rest_list_active:
            return

        self._tip.hide()
        self._rest_list_active = True

        x = base.mouseWatcherNode.getMouseX()  # noqa: F821
        z = base.mouseWatcherNode.getMouseY()  # noqa: F821

        self._rest_buttons["title"] = DirectButton(
            pos=(x, 0, z),
            text="Resting:",
            text_fg=RUST_COL,
            frameColor=(0, 0, 0, 0.6),
            scale=(0.04, 0, 0.03),
        )
        shift = -0.039
        for char in part.chars:
            self._rest_buttons[char.id] = DirectButton(
                pos=(x, 0, z + shift),
                text=char.name,
                text_fg=SILVER_COL,
                frameColor=(0, 0, 0, 0.6),
                command=base.common_ctrl.choose_char,  # noqa: F821
                extraArgs=[char.id],
                scale=(0.04, 0, 0.03),
            )
            shift -= 0.033

    def destroy_char_button(self, char_id):
        """Hide the button related to the given character id.

        Args:
            char_id (str): Character id.
        """
        if char_id in self._rest_buttons.keys():
            self._rest_buttons[char_id].destroy()
            self._rest_buttons.pop(char_id)

    def _update_char_info(self, task):
        """Track the chosen character parameters in the GUI."""
        if self._char.is_dead:
            self.clear_char_info()
            return task.done

        self._char_health["value"] = self._char.health
        self._char_energy["value"] = self._char.energy
        self._traits_list["text"] = ", ".join(self._char.traits)

        if self._char.is_diseased:
            self._disease.show()
        else:
            self._disease.hide()

        if self._char_desc_shown:
            self._update_desc()

        return task.again

    def _update_desc(self):
        """Update the chosen character description."""
        to_del = []
        for wid in self._char_desc_wids:
            if wid["text"] not in ("Traits", "Status"):
                wid.destroy()
                to_del.append(wid)

        for del_wid in to_del:
            self._char_desc_wids.remove(del_wid)

        self._fill_status(self._fill_traits(0.64))

    def _fill_traits(self, shift):
        """Fill the chosen character traits.

        Args:
            shift (float): Z-coor for the new widgets.

        Returns:
            float: Z-coor including the new widgets shift.
        """
        shift -= 0.03
        for trait in self._char.traits + self._char.disabled_traits:
            self._char_desc_wids.append(
                DirectLabel(
                    parent=self._fr,
                    text=trait,
                    frameSize=(0.1, 0.1, 0.1, 0.1),
                    text_scale=0.03,
                    text_fg=SILVER_COL
                    if trait in self._char.traits
                    else (0.3, 0.3, 0.3, 1),
                    pos=(0, 0, shift),
                )
            )
            self._char_desc_wids.append(
                DirectLabel(
                    parent=self._fr,
                    text=TRAIT_DESC[trait],
                    frameSize=(0.1, 0.1, 0.1, 0.1),
                    text_scale=0.029,
                    text_fg=SILVER_COL
                    if trait in self._char.traits
                    else (0.3, 0.3, 0.3, 1),
                    pos=(0, 0, shift - 0.045),
                )
            )
            shift -= 0.1
        return shift

    def _fill_status(self, shift):
        """Fill the chosen character status.

        Args:
            shift (float): Z-coor for the new widgets.
        """
        shift -= 0.04
        for status in self._char.statuses:
            self._char_desc_wids.append(
                DirectLabel(
                    parent=self._fr,
                    text=status,
                    frameSize=(0.1, 0.1, 0.1, 0.1),
                    text_scale=0.029,
                    text_fg=SILVER_COL,
                    pos=(0, 0, shift),
                )
            )
            shift -= 0.045

    def _show_char_desc(self):
        """Show detailed character description.

        Includes description of every character's
        trait and his/her current status.
        """
        if self._char_desc_shown:
            self._fr["frameSize"] = (-0.31, 0.31, -0.1, 0.115)
            for wid in self._char_desc_wids:
                wid.destroy()

            self._char_desc_wids = []
        else:
            shift = 0.7
            self._fr["frameSize"] = (-0.31, 0.31, -0.1, shift)
            shift -= 0.06
            self._char_desc_wids.append(
                DirectLabel(
                    parent=self._fr,
                    text="Traits",
                    frameSize=(0.1, 0.1, 0.1, 0.1),
                    text_scale=0.03,
                    text_fg=RUST_COL,
                    pos=(-0.225, 0, shift),
                )
            )
            shift = self._fill_traits(shift)

            self._char_desc_wids.append(
                DirectLabel(
                    parent=self._fr,
                    text="Status",
                    frameSize=(0.1, 0.1, 0.1, 0.1),
                    text_scale=0.03,
                    text_fg=RUST_COL,
                    pos=(-0.221, 0, shift),
                )
            )
            self._fill_status(shift)

        self._char_desc_shown = not self._char_desc_shown
