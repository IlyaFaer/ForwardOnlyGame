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
from panda3d.core import TextNode, TransparencyAttrib


class RailsScheme:
    """Rails scheme GUI.

    Represents the railways map, which can be used by
    players to choose the right way across the game world.

    Args:
        world_map (list): All the world blocks.
    """

    def __init__(self, world_map):
        self.is_shown = False
        self._temp_wids = []

        self._open_snd = loader.loadSfx("sounds/GUI/paper1.ogg")  # noqa: F821
        self._close_snd = loader.loadSfx("sounds/GUI/paper2.ogg")  # noqa: F821
        self._world_map = world_map

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
        self._scheme = DirectFrame(
            parent=self._list,
            frameSize=(-1.1, 1.1, -0.3, 0.3),
            frameTexture="gui/tex/world_scheme.png",
            pos=(0, 0, 0),
        )
        self._scheme.setTransparency(TransparencyAttrib.MAlpha)

        self._arrow = DirectFrame(
            parent=self._scheme,
            frameSize=(-0.02, 0.02, -0.03, 0.03),
            frameTexture="gui/tex/scheme_arrow.png",
            pos=(-0.967, 0, 0.1),
        )

        self._build_legend()

    def _build_legend(self):
        """Build the scheme legend GUI."""
        lab_opts = {
            "parent": self._list,
            "text_scale": 0.035,
            "frameColor": (0, 0, 0, 0),
            "frameSize": (-0.1, 0.1, -0.1, 0.1),
        }
        DirectLabel(
            text=("Legend:\nm - Meet\n" "e - Enemy Camp\n" "l - Looting"),
            text_align=TextNode.ALeft,
            pos=(-1, 0, -0.35),
            **lab_opts,
        )
        DirectFrame(
            parent=self._scheme,
            frameTexture="gui/tex/city.png",
            frameSize=(-0.04, 0.04, -0.04, 0.04),
            pos=(-0.39, 0, -0.41),
        )
        DirectLabel(
            text="- city", pos=(-0.3, 0, -0.42), **lab_opts,
        )
        DirectFrame(
            parent=self._scheme,
            frameTexture="gui/tex/dash.png",
            frameSize=(-0.004, 0.004, -0.06, 0.06),
            frameColor=(0, 0, 0, 0.2),
            pos=(0.09, 0, -0.37),
        ).setR(90)

        DirectLabel(
            text="- railway branch", pos=(0.29, 0, -0.38), **lab_opts,
        )

        DirectFrame(
            parent=self._scheme,
            frameColor=(0.71, 0.25, 0.05, 0.2),
            frameSize=(-0.06, 0.06, -0.02, 0.02),
            pos=(0.09, 0, -0.45),
        )
        DirectLabel(
            text="- the Stench", pos=(0.26, 0, -0.46), **lab_opts,
        )

    def _fill_branches(self):
        """Paint railway branches on the railways scheme."""
        for branch in base.world.branches:  # noqa: F821
            start = -0.967 + self._world_map[branch["start"]].id * 0.00216
            self._temp_wids.append(
                DirectFrame(
                    parent=self._scheme,
                    frameTexture="gui/tex/dash.png",
                    frameSize=(-0.004, 0.004, -0.1, 0.1),
                    frameColor=(0, 0, 0, 0.2),
                    pos=(start, 0, 0.1 if branch["side"] == "l" else -0.1),
                )
            )
            end = -0.967 + self._world_map[branch["end"]].id * 0.00216
            self._temp_wids.append(
                DirectFrame(
                    parent=self._scheme,
                    frameTexture="gui/tex/dash.png",
                    frameSize=(-0.004, 0.004, -0.1, 0.1),
                    frameColor=(0, 0, 0, 0.2),
                    pos=(end, 0, 0.1 if branch["side"] == "l" else -0.1),
                )
            )

            x_coor = (start + end) / 2

            horiz = DirectFrame(
                parent=self._scheme,
                frameTexture="gui/tex/dash.png",
                frameSize=(-0.004, 0.004, -(x_coor - start), end - x_coor),
                frameColor=(0, 0, 0, 0.2),
                pos=(x_coor, 0, 0.2 if branch["side"] == "l" else -0.2),
            )
            horiz.setR(90)
            self._temp_wids.append(horiz)

            outs = ""
            for block in branch["blocks"][1:-1]:
                if block.outing_available:
                    outs += block.outing_available[0]

            if outs:
                self._temp_wids.append(
                    DirectLabel(
                        parent=self._scheme,
                        text=outs,
                        text_scale=0.035,
                        text_bg=(0, 0, 0, 0),
                        text_fg=(0, 0, 0, 0.5),
                        frameColor=(0, 0, 0, 0),
                        pos=(x_coor, 0, 0.25 if branch["side"] == "l" else -0.25),
                    )
                )

    def _fill_scheme(self):
        """Fill the railways scheme with the world data.

        Shows cities, outings and railway branches on the scheme.
        """
        self._fill_branches()

        outs = None
        for block in self._world_map[:901]:
            if block.id % 100 == 0:
                if outs:
                    self._temp_wids.append(
                        DirectLabel(
                            parent=self._scheme,
                            text=outs,
                            text_scale=0.035,
                            text_bg=(0, 0, 0, 0),
                            frameColor=(0, 0, 0, 0),
                            pos=(-0.967 + (block.id - 50) * 0.00216, 0, -0.1),
                        )
                    )
                outs = ""

            if block.outing_available:
                outs += block.outing_available[0]

            if block.is_city:
                self._temp_wids.append(
                    DirectFrame(
                        parent=self._scheme,
                        frameTexture="gui/tex/city.png",
                        frameSize=(-0.04, 0.04, -0.04, 0.04),
                        pos=(-0.967 + block.id * 0.00216, 0, 0),
                    )
                )

        self._temp_wids.append(
            DirectFrame(
                parent=self._scheme,
                frameColor=(0.71, 0.25, 0.05, 0.2),
                frameSize=(
                    0,
                    base.world.stench_step * 0.00216,  # noqa: F821
                    -0.22,
                    0.22,
                ),
                pos=(-0.967, 0, 0),
            )
        )

    def _update_arrow(self, task):
        """Update the Train position on the scheme."""
        blocks = base.world.current_blocks  # noqa: F821
        if blocks and blocks[0] != -1 and blocks[0] < 900:
            self._arrow.setPos(-0.967 + blocks[0] * 0.00216, 0, 0.1)

        task.delayTime = 6
        return task.again

    def show(self):
        """Show/hide railways scheme GUI."""
        if (
            self.is_shown
            or base.world.outings_mgr.gui_is_shown  # noqa: F821
            or base.traits_gui.is_shown  # noqa: F821
        ):
            self._close_snd.play()
            self._list.hide()
            taskMgr.remove("update_scheme_arrow")  # noqa: F821

            for wid in self._temp_wids:
                wid.destroy()
            self._temps_wids = []
        else:
            self._open_snd.play()
            taskMgr.doMethodLater(  # noqa: F821
                0.2, self._update_arrow, "update_scheme_arrow"
            )
            self._fill_scheme()
            self._list.show()

        self.is_shown = not self.is_shown
