"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Character status GUI.
"""
from direct.gui.DirectGui import (
    DGG,
    DirectButton,
    DirectFrame,
    DirectLabel,
    DirectWaitBar,
)
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import CardMaker, NodePath, TransparencyAttrib

from utils import clear_wids
from .widgets import GUI_PIC, RUST_COL, SILVER_COL

ABOUT_BUT_PARAMS = {
    "text": "?",
    "frameSize": (-0.03, 0.03, -0.03, 0.03),
    "frameColor": (0, 0, 0, 0),
    "text_bg": (0, 0, 0, 0),
    "text_fg": SILVER_COL,
    "text_scale": 0.03,
    "relief": "flat",
}


class CharacterGUI:
    """Widget with the selected character info."""

    def __init__(self):
        self.char = None  # the chosen character
        self.rest_list_shown = False
        self._status_lab = None
        self._rest_buttons = {}
        self._char_desc_wids = []
        self._char_desc_shown = False

        self._fr = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.31, 0.31, -0.1, 0.115),
            pos=(0.31, 0, -1.9),
            frameTexture=GUI_PIC + "metal1.png",
            state=DGG.NORMAL,
        )
        self._fr.setTransparency(TransparencyAttrib.MAlpha)

        # a "?" button to open a detailed description of the character
        self._char_desc_but = DirectButton(
            parent=self._fr,
            pos=(0.27, 0, 0.0675),
            command=self._show_char_desc,
            clickSound=base.main_menu.click_snd,  # noqa: F821
            **ABOUT_BUT_PARAMS,
        )
        DirectLabel(  # Name:
            parent=self._fr,
            text=base.labels.CHARACTERS[0],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.03,
            text_fg=RUST_COL,
            pos=(-0.22, 0, 0.07),
        )
        self._char_name = DirectLabel(
            parent=self._fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.03,
            text_fg=SILVER_COL,
            pos=(-0.09, 0, 0.069),
        )
        self._traits = DirectLabel(
            parent=self._fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.028, 0.028),
            text_fg=SILVER_COL,
            text_font=base.main_font,  # noqa: F821
            pos=(0, 0, 0.025),
        )
        DirectLabel(  # Class:
            parent=self._fr,
            text=base.labels.CHARACTERS[1],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.03,
            text_fg=RUST_COL,
            pos=(0.05, 0, 0.07),
        )
        self._char_class = DirectLabel(
            parent=self._fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.03,
            text_fg=SILVER_COL,
            pos=(0.17, 0, 0.068),
        )
        DirectLabel(  # Health
            parent=self._fr,
            text=base.labels.CHARACTERS[2],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.03,
            text_fg=RUST_COL,
            pos=(-0.22, 0, -0.015),
        )
        self._char_health = DirectWaitBar(
            parent=self._fr,
            frameSize=(-0.17, 0.17, -0.002, 0.002),
            frameColor=(0.35, 0.35, 0.35, 1),
            value=0,
            barColor=(0.85, 0.2, 0.28, 1),
            pos=(0.07, 0, -0.008),
        )
        DirectLabel(  # Energy
            parent=self._fr,
            text=base.labels.CHARACTERS[3],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.03,
            text_fg=RUST_COL,
            pos=(-0.216, 0, -0.06),
        )
        self._char_energy = DirectWaitBar(
            parent=self._fr,
            frameSize=(-0.17, 0.17, -0.002, 0.002),
            frameColor=(0.35, 0.35, 0.35, 1),
            value=0,
            barColor=(0.46, 0.61, 0.53, 1),
            pos=(0.07, 0, -0.053),
        )
        self._tip = OnscreenText(
            parent=base.render2d,  # noqa: F821
            text="",
            font=base.main_font,  # noqa: F821
            scale=(0.021, 0.027),
            fg=SILVER_COL,
            bg=(0, 0, 0, 0.4),
        )
        self._tip.hide()

        self._disease = DirectFrame(
            parent=self._fr,
            frameSize=(-0.02, 0.02, -0.02, 0.02),
            pos=(0.27, 0, -0.008),
            frameTexture=GUI_PIC + "disease.png",
        )
        self._disease.setTransparency(TransparencyAttrib.MAlpha)

        self.clear_char_info()

    def _update_char_info(self, task):
        """Track the chosen character parameters in the GUI."""
        if self.char.is_dead:
            self.clear_char_info()
            return task.done

        self._char_health["value"] = self.char.health
        self._char_energy["value"] = self.char.energy
        self._traits["text"] = ", ".join(self.char.traits)

        if self.char.is_diseased:
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
            if wid["text"] not in ("Traits", "Status", ""):
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
        for trait in self.char.traits + self.char.disabled_traits:
            self._char_desc_wids.append(
                DirectLabel(
                    parent=self._fr,
                    text=trait,
                    frameSize=(0.1, 0.1, 0.1, 0.1),
                    text_scale=0.03,
                    text_font=base.main_font,  # noqa: F821
                    text_fg=SILVER_COL
                    if trait in self.char.traits
                    else (0.3, 0.3, 0.3, 1),
                    pos=(0, 0, shift),
                )
            )
            self._char_desc_wids.append(
                DirectLabel(
                    parent=self._fr,
                    text=base.labels.TRAIT_DESC[trait],  # noqa: F821
                    text_font=base.main_font,  # noqa: F821
                    frameSize=(0.1, 0.1, 0.1, 0.1),
                    text_scale=0.029,
                    text_fg=SILVER_COL
                    if trait in self.char.traits
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
        for status in self.char.statuses:
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
            clear_wids(self._char_desc_wids)
            self._status_lab = None
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
            if self.char.id in base.team.chars.keys():  # noqa: F821
                traits_but = DirectButton(
                    parent=self._fr,
                    text="",
                    frameSize=(-0.025, 0.025, -0.025, 0.025),
                    frameTexture=GUI_PIC + "like.png",
                    relief="flat",
                    pos=(0.265, 0, shift + 0.013),
                    command=base.traits_gui.show,  # noqa: F821
                )
                traits_but.bind(
                    DGG.ENTER, self._highlight_traits_but, extraArgs=[traits_but]
                )
                traits_but.bind(
                    DGG.EXIT, self._dehighlight_traits_but, extraArgs=[traits_but]
                )

                self._char_desc_wids.append(traits_but)

            shift = self._fill_traits(shift)

            self._status_lab = DirectLabel(
                parent=self._fr,
                text="Status",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.03,
                text_fg=RUST_COL,
                pos=(-0.221, 0, shift),
            )
            self._char_desc_wids.append(self._status_lab)
            self._fill_status(shift)

        self._char_desc_shown = not self._char_desc_shown

    def _highlight_traits_but(self, button, _):
        """Hightlight traits tweaking button.

        Args:
            button (panda3d.gui.DirectGui.DirectButton):
                Button to highlight.
        """
        button["frameTexture"] = GUI_PIC + "hover_like.png"

    def _dehighlight_traits_but(self, button, _):
        """Dehighlight traits tweaking button.

        Args:
            button (panda3d.gui.DirectGui.DirectButton):
                Button to dehighlight.
        """
        button["frameTexture"] = GUI_PIC + "like.png"

    def clear_char_info(self, clear_resting=True):
        """Clear the character GUI.

        Args:
            clear_resting (bool):
                Optional. A flag indicating if the list of the
                resting characters should also be closed.
        """
        for wid in (
            self._char_name,
            self._char_class,
            self._char_health,
            self._char_energy,
            self._traits,
            self._char_desc_but,
            self._disease,
        ):
            wid.hide()

        if self._char_desc_shown:
            self._show_char_desc()

        taskMgr.remove("track_char_info")  # noqa: F821
        self.char = None

        if clear_resting:
            for but in self._rest_buttons.values():
                but.destroy()

        self.rest_list_shown = False

    def destroy_char_button(self, char_id):
        """Hide the given character button from the resting characters list.

        Args:
            char_id (str): Character id.
        """
        if char_id in self._rest_buttons.keys():
            self._rest_buttons[char_id].destroy()
            self._rest_buttons.pop(char_id)

    def hide_tip(self):
        """Hide the tooltip."""
        self._tip.hide()

    def show_char_info(self, char):
        """Show the given character status.

        Args:
            char (units.crew.character.Character):
                The chosen character object.
        """
        self._char_name["text"] = char.name
        self._char_class["text"] = char.class_.capitalize()
        self._traits["text"] = ", ".join(char.traits)

        self._char_health["range"] = char.class_data["health"]
        self._char_health["value"] = char.health
        self._char_energy["value"] = char.energy

        if char.is_diseased:
            self._disease.show()
        else:
            self._disease.hide()

        self.char = char
        self._char_name.show()
        self._char_class.show()
        self._char_health.show()
        self._char_energy.show()
        self._traits.show()
        self._char_desc_but.show()

        if self._char_desc_shown:
            self._show_char_desc()
            self._show_char_desc()

        taskMgr.doMethodLater(  # noqa: F821
            0.5, self._update_char_info, "track_char_info"
        )

    def show_tooltip(self, text):
        """Show tooltip with the given text.

        Args:
            text (str): Text to show in the tooltip.
        """
        if not base.mouseWatcherNode.hasMouse():  # noqa: F821
            return

        if self.rest_list_shown and text == "Rest zone":
            return

        self._tip.setText(text)
        self._tip.setX(base.mouseWatcherNode.getMouseX())  # noqa: F821
        self._tip.setY(base.mouseWatcherNode.getMouseY())  # noqa: F821
        self._tip.show()

    def show_resting_chars(self, part):
        """Show a list of the characters resting in this part.

        Args:
            part (Train.RestPart): Rest part of the Train.
        """
        if self.rest_list_shown:
            return

        self._tip.hide()
        self.rest_list_shown = True

        x = base.mouseWatcherNode.getMouseX()  # noqa: F821
        z = base.mouseWatcherNode.getMouseY()  # noqa: F821

        self._rest_buttons["title"] = DirectButton(
            pos=(x, 0, z),
            text=base.labels.TIPS[0],  # noqa: F821
            text_fg=RUST_COL,
            text_font=base.main_font,  # noqa: F821
            frameColor=(0, 0, 0, 0.6),
            scale=(0.04, 0, 0.03),
        )
        shift = -0.039
        for char in part.chars:
            if char.is_dead:
                continue

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

    def update_resting_chars(self, part):
        """Update the list of the resting characters.

        Args:
            part (train.part.TrainPart): Rest train part.
        """
        for key, but in self._rest_buttons.items():
            if key != "title":
                but.destroy()
                self._rest_buttons[key] = None

        x, _, z = self._rest_buttons["title"].getPos()

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

    def move_status_label(self, place):
        """Move the status label widget.

        Args:
            place (int): Place to shift the widget.
        """
        if self._status_lab is not None:
            self._status_lab.setZ(self._status_lab.getZ() + place / 10)


class HealthBar(NodePath):
    """Widget to show character's health.

    Is shown only during fights.

    Args:
        char (units.crew.character.Character):
            Character, whos health must be shown.
    """

    def __init__(self, char):
        NodePath.__init__(self, "health_bar_" + char.id)

        self._char = char

        self.hide()
        self.reparentTo(char.model)
        self.setLightOff()
        self.setZ(0.1)
        self.setBillboardPointEye()

        cmfg = CardMaker("fg")
        cmfg.setFrame(0, 0.05, -0.002, 0.002)
        self._fg = self.attachNewNode(cmfg.generate())
        self._fg.setX(-0.026)

        cmbg = CardMaker("bg")
        cmbg.setFrame(-0.05, 0, -0.002, 0.002)
        self._bg = self.attachNewNode(cmbg.generate())
        self._bg.setPos(0.024, 0.001, 0)

        self._fg.setColor(0.55, 0, 0, 1)
        self._bg.setColor(0.5, 0.5, 0.5, 1)

    def _set_health(self, task):
        """Show the current character health on the widget."""
        value = self._char.health / self._char.class_data["health"]
        self._fg.setScale(value or 0.001, 1, 1)
        self._bg.setScale((1 - value) or 0.001, 1, 1)
        return task.again

    def hide_health(self):
        """Hide the widget."""
        taskMgr.remove(self._char.id + "_show_health")  # noqa: F821
        self.hide()

    def show_health(self):
        """Show the widget and start tracking the character's health on it."""
        self.show()

        taskMgr.doMethodLater(  # noqa: F821
            0.3, self._set_health, self._char.id + "_show_health"
        )
