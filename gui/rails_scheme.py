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

from utils import clear_wids


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

        DirectLabel(  # Silewer Railways Scheme
            parent=self._list,
            text=base.labels.SCHEME[0],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            frameSize=(0.2, 0.2, 0.2, 0.2),
            text_scale=0.035,
            pos=(0, 0, 0.5),
        )
        self._scheme = DirectFrame(
            parent=self._list,
            frameSize=(-1.1, 1.1, -0.3, 0.3),
            frameTexture="gui/tex/world_scheme.png",
        )
        self._scheme.setTransparency(TransparencyAttrib.MAlpha)

        self._arrow = DirectFrame(
            parent=self._scheme,
            frameSize=(-0.02, 0.02, -0.02, 0.02),
            frameTexture="gui/tex/train_dir.png",
            pos=(-0.96, 0, 0.07),
        )
        self._build_legend()

    def _build_legend(self):
        """Build the scheme legend GUI."""
        lab_opts = {
            "parent": self._list,
            "text_scale": 0.033,
            "frameColor": (0, 0, 0, 0),
            "frameSize": (-0.1, 0.1, -0.1, 0.1),
        }
        DirectLabel(  # Legend
            text=base.labels.SCHEME[1],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
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
        DirectLabel(  # city
            text=base.labels.SCHEME[2],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            pos=(-0.3, 0, -0.42),
            **lab_opts,
        )
        DirectFrame(
            parent=self._scheme,
            frameTexture="gui/tex/dash.png",
            frameSize=(-0.004, 0.004, -0.06, 0.06),
            frameColor=(0, 0, 0, 0.2),
            pos=(0.09, 0, -0.37),
        ).setR(90)

        DirectLabel(
            text=base.labels.SCHEME[3],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            pos=(0.29, 0, -0.38),
            **lab_opts,
        )
        DirectFrame(
            parent=self._scheme,
            frameColor=(0.71, 0.25, 0.05, 0.2),
            frameSize=(-0.06, 0.06, -0.02, 0.02),
            pos=(0.09, 0, -0.45),
        )
        DirectLabel(
            text=base.labels.SCHEME[4],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            pos=(0.26, 0, -0.46),
            **lab_opts,
        )

    def _fill_branches(self):
        """Paint railway branches on the railways scheme."""
        for branch in base.world.branches:  # noqa: F821
            start = -0.96 + self._world_map[branch["start"]].id * 0.00385
            self._temp_wids.append(
                DirectFrame(
                    parent=self._scheme,
                    frameTexture="gui/tex/dash.png",
                    frameSize=(-0.004, 0.004, -0.1, 0.1),
                    frameColor=(0, 0, 0, 0.2),
                    pos=(start, 0, 0.1 if branch["side"] == "l" else -0.1),
                )
            )
            end = -0.96 + self._world_map[branch["end"]].id * 0.00385
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

                if block.is_station:
                    outs += "i"

            if outs:
                outs = outs.lower()
                self._temp_wids.append(
                    DirectLabel(
                        parent=self._scheme,
                        text=outs,
                        text_scale=0.035,
                        text_bg=(0, 0, 0, 0),
                        text_fg=(0, 0, 0, 0.5),
                        frameColor=(0, 0, 0, 0),
                        pos=(x_coor, 0, 0.25 if branch["side"] == "l" else -0.27),
                    )
                )

    def _fill_scheme(self):
        """Fill the railways scheme with the world data.

        Shows cities, outings and railway branches on the scheme.
        """
        self._fill_branches()

        outs = None
        cities = 0
        for block in self._world_map[:501]:
            if block.id % 100 == 0:
                if outs:
                    self._temp_wids.append(
                        DirectLabel(
                            parent=self._scheme,
                            text=outs,
                            text_scale=0.035,
                            text_bg=(0, 0, 0, 0),
                            frameColor=(0, 0, 0, 0),
                            pos=(-0.96 + (block.id - 50) * 0.00385, 0, -0.1),
                        )
                    )
                outs = ""

            if block.outing_available:
                outs += block.outing_available[0].lower()

            if block.is_station:
                outs += "i"

            if block.is_city:
                self._temp_wids.append(
                    DirectFrame(
                        parent=self._scheme,
                        frameTexture="gui/tex/city.png",
                        frameSize=(-0.04, 0.04, -0.04, 0.04),
                        pos=(-0.96 + block.id * 0.00385, 0, 0),
                    )
                )
                self._temp_wids.append(
                    DirectLabel(
                        parent=self._scheme,
                        text=base.labels.CITY_NAMES[cities],  # noqa: F821
                        text_font=base.main_font,  # noqa: F821
                        text_scale=0.032,
                        text_bg=(0, 0, 0, 0),
                        frameColor=(0, 0, 0, 0),
                        pos=(-0.96 + block.id * 0.00385, 0, 0.1),
                    )
                )
                cities += 1

        self._temp_wids.append(
            DirectFrame(
                parent=self._scheme,
                frameColor=(0.71, 0.25, 0.05, 0.2),
                frameSize=(
                    0,
                    base.world.stench_step * 0.00385,  # noqa: F821
                    -0.22,
                    0.22,
                ),
                pos=(-0.96, 0, 0),
            )
        )

    def _update_arrow(self, task):
        """Update the Train position on the scheme."""
        blocks = base.world.current_blocks  # noqa: F821
        if blocks and blocks[0] != -1:

            z_shift = 0
            if not base.world.is_near_fork:  # noqa: F821
                if base.world.current_block.branch == "l":  # noqa: F821
                    z_shift = 0.155
                elif base.world.current_block.branch == "r":  # noqa: F821
                    z_shift = -0.295

            if blocks[0] < 500:
                x = -0.96 + blocks[0] * 0.00385
            else:
                x = self._arrow.getX()

            self._arrow.setPos(x, 0, 0.07 + z_shift)

            if blocks[0] < blocks[1]:
                self._arrow["frameTexture"] = "gui/tex/train_dir.png"
            else:
                self._arrow["frameTexture"] = "gui/tex/train_dir_op.png"

        task.delayTime = 3
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

            clear_wids(self._temp_wids)
        else:
            if base.world.is_on_et:  # noqa: F821
                return

            self._open_snd.play()
            taskMgr.doMethodLater(  # noqa: F821
                0.2, self._update_arrow, "update_scheme_arrow"
            )
            self._fill_scheme()
            self._list.show()
            base.char_gui.clear_char_info(True)  # noqa: F821

        self.is_shown = not self.is_shown
