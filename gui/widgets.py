"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The game GUI primitives.
"""
import abc

from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel
from .train import SILVER_COL


class ItemChooser(metaclass=abc.ABCMeta):
    """The base class for choose-one-of widgets.

    Args:
        is_shadowed (bool):
            Optional. If True, a shadowed font
            color will be used for this widget.
    """

    def __init__(self, is_shadowed=False):
        font = (0, 0, 0, 0.3 if is_shadowed else 0)
        self._ind = 0

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
            command=self._next,
            scale=(0.075, 0, 0.075),
        )
        DirectButton(
            parent=self._fr,
            pos=(-0.15, 0, -0.015),
            text="<",
            text_fg=SILVER_COL,
            frameColor=font,
            command=self._prev,
            scale=(0.075, 0, 0.075),
        )
        self._fr.hide()

    def _next(self):
        """Choose the next item from the list."""
        self._ind += 1
        self._show_info()

    def _prev(self):
        """Choose the previous item from the list."""
        self._ind -= 1
        self._show_info()

    def destroy(self):
        """Clear this widget."""
        self._fr.destroy()
        self._ind = 0

    def prepare(self, parent, pos):
        """Set this widget's parent and position.

        Args:
            parent (panda3d.core.NodePath): Parent widget.
            pos (tuple): New widget position.
        """
        self._fr.reparentTo(parent)
        self._fr.setPos(pos)
        self._fr.show()
        self._show_info()

    @abc.abstractmethod
    def _show_info(self):
        """Show info about the chosen item."""
        raise NotImplementedError("Chooser class must have _show_info() method.")


class CharacterChooser(ItemChooser):
    """Widget to choose a single character.

    Args:
        is_shadowed (bool):
            Optional. If True, a shadowed font
            color will be used for this widget.
    """

    def __init__(self, is_shadowed=False):
        ItemChooser.__init__(self, is_shadowed)

        self._chosen_char = None
        self._chars = None

    @property
    def chosen_char(self):
        """Return the chosen character object.

        Returns:
            personage.character.Character:
                The character chosen by this widget.
        """
        return self._chosen_char

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
        base.char_gui.show_char_info(self._chosen_char)  # noqa: F821

    def prepare(self, parent, pos, chars):
        """Set this widget's parent and position.

        Args:
            parent (panda3d.core.NodePath): Parent widget.
            pos (tuple): New widget position.
            chars (dict): Chars to show in this widget.
        """
        self._chars = chars

        ItemChooser.prepare(self, parent, pos)

    def leave_unit(self, id_):
        """Take out the chosen unit from the widget.

        Args:
            id_ (str): Id of the unit to take out.
        """
        if id_ in self._chars.keys():
            self._chars.pop(id_)

        self._ind = 0
        self._show_info()

    def destroy(self):
        """Clear this widget."""
        ItemChooser.destroy(self)

        self._chosen_char = None
        self._chars = None


class UpgradeChooser(ItemChooser):
    """Widget to choose one Train upgrade.

    Args:
        desc_label (direct.gui.DirectGui.DirectLabel):
            Widget in which the description of the
            chosen upgrade should be shown.
        cost_label (direct.gui.DirectGui.DirectLabel):
            Widget in which the chosen upgrade
            cost should be shown.
    """

    def __init__(self, desc_label, cost_label):
        ItemChooser.__init__(self)

        self._chosen_up = None
        self._ups = None
        self._desc = desc_label
        self._cost = cost_label

    @property
    def chosen_upgrade(self):
        """Returns the chosen upgrade.

        Returns:
            dict: The chosen upgrade description.
        """
        return self._chosen_up

    def prepare(self, parent, pos, ups):
        """Set this widget's parent and position.

        Args:
            parent (panda3d.core.NodePath): Parent widget.
            pos (tuple): New widget position.
            ups (dict): Upgrades to show in this widget.
        """
        self._ups = ups

        ItemChooser.prepare(self, parent, pos)

    def _show_info(self):
        """Show the chosen upgrade info in the related widgets."""
        if len(self._ups) == 0:
            self._name["text"] = ""
            self._chosen_up = None
            self._desc["text"] = ""
            self._cost["text"] = ""
            return

        if self._ind == len(self._ups):
            self._ind = 0
        elif self._ind == -1:
            self._ind = len(self._ups) - 1

        key = list(self._ups.keys())[self._ind]
        self._chosen_up = self._ups[key]

        self._name["text"] = self._chosen_up["name"]
        self._desc["text"] = self._chosen_up["desc"]
        self._cost["text"] = self._chosen_up["cost"]

        base.train.preview_upgrade(self._chosen_up["model"])  # noqa: F821

    def destroy(self):
        """Clear this widget."""
        ItemChooser.destroy(self)
        self._chosen_up = None
        self._ups = None

        base.train.clear_upgrade_preview()  # noqa: F821

    def pop_upgrade(self, id_):
        """Drop upgrade with the given id from the chooser.

        Args:
            id_ (str): Id of the upgrade to drop.
        """
        if id_ in self._ups.keys():
            self._ups.pop(id_)

        self._ind = 0
        self._show_info()
