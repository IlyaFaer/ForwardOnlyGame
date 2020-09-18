"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Character related GUI.
"""
from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel, DirectWaitBar
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TransparencyAttrib

from .train import ICON_PATH, RUST_COL, SILVER_COL


class CharacterInterface:
    """Widget with character info."""

    def __init__(self):
        self._char = None  # chosen character
        self._rest_buttons = {}
        self._rest_list_active = False

        char_int_fr = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.3, 0.3, -0.1, 0.1),
            pos=(0.3, 0, -1.9),
            frameTexture=ICON_PATH + "metal1.png",
        )
        char_int_fr.setTransparency(TransparencyAttrib.MAlpha)

        DirectLabel(
            parent=char_int_fr,
            text="Name:",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.23, 0, 0.04),
        )
        self._char_name = DirectLabel(
            parent=char_int_fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=SILVER_COL,
            pos=(-0.11, 0, 0.038),
        )
        DirectLabel(
            parent=char_int_fr,
            text="Type:",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(0.03, 0, 0.04),
        )
        self._char_class = DirectLabel(
            parent=char_int_fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=SILVER_COL,
            pos=(0.15, 0, 0.038),
        )
        DirectLabel(
            parent=char_int_fr,
            text="Health",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.23, 0, -0.015),
        )
        self._char_health = DirectWaitBar(
            parent=char_int_fr,
            frameSize=(-0.17, 0.17, -0.002, 0.002),
            value=0,
            barColor=(0.85, 0.2, 0.28, 1),
            pos=(0.06, 0, -0.008),
        )
        DirectLabel(
            parent=char_int_fr,
            text="Energy",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.226, 0, -0.06),
        )
        self._char_energy = DirectWaitBar(
            parent=char_int_fr,
            frameSize=(-0.17, 0.17, -0.002, 0.002),
            value=0,
            barColor=(0.46, 0.61, 0.53, 1),
            pos=(0.06, 0, -0.053),
        )
        self._tip = OnscreenText(
            parent=base.render2d,  # noqa: F821
            text="",
            scale=(0.021, 0.027),
            fg=SILVER_COL,
            bg=(0, 0, 0, 0.4),
        )
        self._tip.hide()

        self.clear_char_info()

    def show_char_info(self, character):
        """Show the given character parameters.

        Args:
            character (personage.character.Character):
                Chosen character object.
        """
        self._char_name["text"] = character.name
        self._char_class["text"] = character.class_.capitalize()

        self._char_health["range"] = character.class_data["health"]
        self._char_health["value"] = character.health
        self._char_energy["value"] = character.energy

        self._char_name.show()
        self._char_class.show()
        self._char_health.show()
        self._char_energy.show()

        self._char = character
        base.taskMgr.doMethodLater(  # noqa: F821
            0.5, self._update_char_info, "track_char_info"
        )

    def clear_char_info(self):
        """Clear the character interface."""
        self._char_name.hide()
        self._char_class.hide()
        self._char_health.hide()
        self._char_energy.hide()

        base.taskMgr.remove("track_char_info")  # noqa: F821
        self._char = None

        for but in self._rest_buttons.values():
            but.destroy()

        self._rest_list_active = False

    def show_tooltip(self, text):
        """Show tooltip with the given text.

        Args:
            unit (str): Text to show in the tooltip.
        """
        self._tip.setText(text)
        self._tip.setX(base.mouseWatcherNode.getMouseX())  # noqa: F821
        self._tip.setY(base.mouseWatcherNode.getMouseY())  # noqa: F821
        self._tip.show()

    def hide_unit_tip(self):
        """Hide unit tooltip."""
        self._tip.hide()

    def show_resting_chars(self, part):
        """Show a list of the characters resting in this part.

        Args:
            part (Train.RestPart): Rest part of Train.
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
                command=base.common_ctrl.choose_resting_char,  # noqa: F821
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
        """Track character parameters on the interface."""
        if self._char.is_dead:
            self.clear_char_info()
            return task.done

        self._char_health["value"] = self._char.health
        self._char_energy["value"] = self._char.energy
        return task.again


class CharacterChooser:
    """Widget to choose single one character.

    Args:
        is_shadowed (bool): Optional. If True, a shadowed
            font color will be used for this widget
    """

    def __init__(self, is_shadowed=False):
        self._ind = 0
        self._chosen_char = None
        self._chars = None

        font = (0, 0, 0, 0.3 if is_shadowed else 0)

        self._fr = DirectFrame(frameSize=(-0.11, 0.12, -0.025, 0.024), frameColor=font)
        self._name = DirectLabel(
            parent=self._fr,
            frameColor=(0, 0, 0, 0.3),
            text_fg=SILVER_COL,
            text="",
            text_scale=(0.03, 0.03),
            pos=(0, 0, -0.01),
        )
        DirectButton(
            parent=self._fr,
            pos=(0.15, 0, -0.015),
            text=">",
            text_fg=SILVER_COL,
            frameColor=font,
            command=self._next_char,
            scale=(0.075, 0, 0.075),
        )
        DirectButton(
            parent=self._fr,
            pos=(-0.15, 0, -0.015),
            text="<",
            text_fg=SILVER_COL,
            frameColor=font,
            command=self._prev_char,
            scale=(0.075, 0, 0.075),
        )
        self._fr.hide()

    @property
    def chosen_char(self):
        """Return the chosen character object.

        Returns:
            personage.character.Character:
                The character chosen by this widget.
        """
        return self._chosen_char

    def _next_char(self):
        """Choose the next character from the list."""
        self._ind += 1
        self._show_info()

    def _prev_char(self):
        """Choose the previous character from the list."""
        self._ind -= 1
        self._show_info()

    def _show_info(self):
        """Show the current character's info in the GUI."""
        if len(self._chars) == 0:
            self._name["text"] = ""
            self._chosen_char = None
            return

        if self._ind == len(self._chars):
            self._ind = 0
        elif self._ind == -1:
            self._ind = len(self._chars) - 1

        key = list(self._chars.keys())[self._ind]
        self._chosen_char = self._chars[key]

        self._name["text"] = self._chosen_char.name
        base.char_interface.show_char_info(self._chosen_char)  # noqa: F821

    def prepare(self, parent, pos, chars):
        """Set this widget's parent and position.

        Args:
            parent (panda3d.core.NodePath): Parent widget.
            pos (tuple): New widget position.
            chars (dict): Chars to show in this widget.
        """
        self._fr.reparentTo(parent)
        self._fr.setPos(pos)
        self._fr.show()
        self._chars = chars
        self._show_info()

    def leave_unit(self, id_):
        """Take out the chosen unit from the widget.

        Args:
            id_ (str): Id of the unit to take out.
        """
        if id_ in self._chars.keys():
            self._chars.pop(id_)

        self._ind = 0
        self._show_info()

    def clear(self):
        """Clear this widget."""
        self._fr.destroy()

        self._ind = 0
        self._chosen_char = None
        self._chars = None