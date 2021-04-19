"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Common game GUI primitives.
"""
import abc

from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel

RUST_COL = (0.71, 0.25, 0.05, 1)
SILVER_COL = (0.51, 0.54, 0.59, 1)
GUI_PIC = "gui/tex/"


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
        self._items = None
        self._chosen_item = None

        self._fr = DirectFrame(frameSize=(-0.11, 0.12, -0.025, 0.024), frameColor=font)
        self._name = DirectLabel(
            parent=self._fr,
            frameColor=(0, 0, 0, 0.3),
            text_fg=SILVER_COL,
            text="",
            text_scale=0.03,
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

    @abc.abstractmethod
    def _show_info(self):
        """Show the chosen item info."""
        raise NotImplementedError("Chooser class must have _show_info() method.")

    @property
    def chosen_item(self):
        """The item chosen with this widget.

        Returns:
            object: The chosen object.
        """
        return self._chosen_item

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
        self._chosen_item = None
        self._items = None

    def prepare(self, parent, pos, items, init_ind=None):
        """Set this widget's parent and position.

        Args:
            parent (panda3d.core.NodePath): Parent widget.
            pos (tuple): New widget position.
            items (dict): Items to iterate through.
            init_ind (int): Index of the initial value.
        """
        self._items = items

        self._fr.reparentTo(parent)
        self._fr.setPos(pos)
        self._fr.show()

        if init_ind is not None:
            self._ind = init_ind

        self._show_info()


class CharacterChooser(ItemChooser):
    """Widget to choose a single character.

    Args:
        is_shadowed (bool):
            Optional. If True, a shadowed font
            color will be used for this widget.
    """

    def _show_info(self):
        """Show the current character's info in the GUI."""
        if len(self._items) == 0:
            self._name["text"] = ""
            self._chosen_item = None
            return

        if self._ind == len(self._items):
            self._ind = 0
        elif self._ind == -1:
            self._ind = len(self._items) - 1

        key = list(self._items.keys())[self._ind]
        self._chosen_item = self._items[key]

        self._name["text"] = self._chosen_item.name
        base.char_gui.show_char_info(self._chosen_item)  # noqa: F821

    def leave_unit(self, id_):
        """Take out the chosen unit from the widget.

        Args:
            id_ (str): Id of the unit to take out.
        """
        if id_ in self._items.keys():
            self._items.pop(id_)

        self._ind = 0
        self._show_info()


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

        self._desc = desc_label
        self._cost = cost_label

    def _show_info(self):
        """Show the chosen upgrade info in the related widgets."""
        if len(self._items) == 0:
            self._name["text"] = ""
            self._chosen_item = None
            self._desc["text"] = ""
            self._cost["text"] = ""
            base.train.clear_upgrade_preview()  # noqa: F821
            return

        if self._ind == len(self._items):
            self._ind = 0
        elif self._ind == -1:
            self._ind = len(self._items) - 1

        key = list(self._items.keys())[self._ind]
        self._chosen_item = self._items[key]

        self._name["text"] = self._chosen_item["name"]
        self._desc["text"] = self._chosen_item["desc"]
        self._cost["text"] = self._chosen_item["cost"]

        base.train.preview_upgrade(self._chosen_item["model"])  # noqa: F821

    def destroy(self):
        """Clear this widget."""
        ItemChooser.destroy(self)

        base.train.clear_upgrade_preview()  # noqa: F821

    def pop_upgrade(self, id_):
        """Drop upgrade with the given id from the chooser.

        Args:
            id_ (str): Id of the upgrade to drop.
        """
        if id_ in self._items.keys():
            self._items.pop(id_)

        self._ind = 0
        self._show_info()


class ResolutionChooser(ItemChooser):
    """A widget to choose screen resolution."""

    def _show_info(self):
        """Show the chosen resolution."""
        if self._ind == len(self._items):
            self._ind = 0
        elif self._ind == -1:
            self._ind = len(self._items) - 1

        key = list(self._items.keys())[self._ind]
        self._chosen_item = self._items[key]

        self._name["text"] = self._chosen_item
