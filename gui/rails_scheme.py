"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The game world scheme GUI.
"""
from direct.gui.DirectGui import (
    DGG,
    DirectFrame,
    DirectLabel,
)
from panda3d.core import TransparencyAttrib


class RailsScheme:
    """Rails scheme GUI.

    Represents the railways map, which can be used by
    players to choose the right way across the game world.
    """

    def __init__(self):
        self.is_shown = False

        self._list = DirectFrame(
            frameSize=(-1.2, 1.2, -0.6, 0.6),
            frameTexture="gui/tex/paper2.png",
            state=DGG.NORMAL,
        )
        self._list.setDepthTest(False)
        self._list.setTransparency(TransparencyAttrib.MAlpha)
        self._list.hide()

        DirectLabel(
            parent=self._list,
            text="Railways scheme",
            frameSize=(0.2, 0.2, 0.2, 0.2),
            text_scale=0.035,
            pos=(0, 0, 0.5),
        )

        scheme = DirectFrame(
            parent=self._list,
            frameSize=(-1.1, 1.1, -0.3, 0.3),
            frameTexture="gui/tex/world_scheme.png",
            pos=(0, 0, 0),
        )
        scheme.setTransparency(TransparencyAttrib.MAlpha)

        self._arrow = DirectFrame(
            parent=scheme,
            frameSize=(-0.02, 0.02, -0.03, 0.03),
            frameTexture="gui/tex/scheme_arrow.png",
            pos=(-0.967, 0, 0.1),
        )

    def _update_arrow(self, task):
        """Update the Train position on the scheme."""
        blocks = base.world.current_blocks  # noqa: F821
        if blocks and blocks[0] != -1 and blocks[0] < 900:
            self._arrow.setPos(-0.967 + blocks[0] * 0.00216, 0, 0.1)

        task.delayTime = 7
        return task.again

    def show(self):
        """Show/hide railways scheme GUI."""
        if self.is_shown:
            self._list.hide()
            taskMgr.remove("update_scheme_arrow")  # noqa: F821
        else:
            taskMgr.doMethodLater(  # noqa: F821
                0.2, self._update_arrow, "update_scheme_arrow"
            )
            self._list.show()

        self.is_shown = not self.is_shown
