"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The game expendable resources GUI.
"""
from direct.gui.DirectGui import (
    DGG,
    DirectButton,
    DirectFrame,
    DirectLabel,
    DirectWaitBar,
)
from panda3d.core import TextNode, TransparencyAttrib

from .character import ABOUT_BUT_PARAMS
from .widgets import GUI_PIC, RUST_COL, SILVER_COL


class ResourcesGUI:
    """GUI to track player's resources.

    Includes money, expendable resources and cohesion.
    """

    def __init__(self):
        self._coh_desc_wids = []
        self._coh_desc_shown = False
        self._res_desc_wids = []
        self._res_desc_shown = False
        self._resources = {}
        self._blink_step = 0

        self._err_snd = loader.loadSfx("sounds/GUI/error.ogg")  # noqa: F821

        self._res_frame = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.3, 0.3, -0.03, 0.028),
            pos=(0.3, 0, -0.028),
            frameTexture=GUI_PIC + "metal1.png",
        )
        self._res_frame.setTransparency(TransparencyAttrib.MAlpha)

        DirectFrame(
            parent=self._res_frame,  # noqa: F821
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            pos=(-0.27, 0, 0),
            frameTexture=GUI_PIC + "dollar.png",
        )
        self._resources["dollars"] = DirectLabel(
            parent=self._res_frame,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.035,
            text_fg=RUST_COL,
            pos=(-0.2, 0, -0.008),
        )
        DirectFrame(
            parent=self._res_frame,  # noqa: F821
            frameSize=(-0.018, 0.018, -0.018, 0.018),
            pos=(-0.11, 0, 0),
            frameTexture=GUI_PIC + "chars.png",
        )
        self._resources["chars"] = DirectLabel(
            parent=self._res_frame,
            text="{}/{}".format(len(base.team.chars), base.train.cells),  # noqa: F821
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.035,
            text_fg=RUST_COL,
            pos=(-0.05, 0, -0.008),
        )
        but = DirectButton(
            parent=self._res_frame,
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            relief="flat",
            pos=(0.01, 0, 0),
            frameTexture=GUI_PIC + "medicine.png",
            command=base.team.use_medicine,  # noqa: F821
        )
        but.bind(DGG.ENTER, self._highlight_res_but, extraArgs=[but, "medicine_boxes"])
        but.bind(DGG.EXIT, self._dehighlight_but, extraArgs=[but])

        self._resources["medicine_boxes"] = DirectLabel(
            parent=self._res_frame,
            text="0",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.035,
            text_fg=RUST_COL,
            pos=(0.05, 0, -0.008),
        )
        but = DirectButton(
            parent=self._res_frame,
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            relief="flat",
            pos=(0.105, 0, 0),
            frameTexture=GUI_PIC + "smoke_filter.png",
            command=base.train.use_smoke_filter,  # noqa: F821
        )
        but.bind(DGG.ENTER, self._highlight_res_but, extraArgs=[but, "smoke_filters"])
        but.bind(DGG.EXIT, self._dehighlight_but, extraArgs=[but])

        self._resources["smoke_filters"] = DirectLabel(
            parent=self._res_frame,
            text="0",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.035,
            text_fg=RUST_COL,
            pos=(0.145, 0, -0.008),
        )
        but = DirectButton(
            parent=self._res_frame,
            frameSize=(-0.014, 0.014, -0.021, 0.021),
            relief="flat",
            pos=(0.19, 0, 0),
            frameTexture=GUI_PIC + "stimulator.png",
            command=base.team.use_stimulator,  # noqa: F821
        )
        but.bind(DGG.ENTER, self._highlight_res_but, extraArgs=[but, "stimulators"])
        but.bind(DGG.EXIT, self._dehighlight_but, extraArgs=[but])

        self._resources["stimulators"] = DirectLabel(
            parent=self._res_frame,
            text="0",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.035,
            text_fg=RUST_COL,
            pos=(0.23, 0, -0.008),
        )
        DirectButton(
            parent=self._res_frame,
            pos=(0.27, 0, -0.013),
            command=self._show_expendable_resources,
            clickSound=base.main_menu.click_snd,  # noqa: F821
            **ABOUT_BUT_PARAMS,
        ).setTransparency(TransparencyAttrib.MAlpha)

        self._coh_frame = DirectFrame(
            parent=base.a2dBottomRight,  # noqa: F821
            frameSize=(-0.55, 0.55, -0.05, 0.05),
            pos=(-0.6, 0, 1.95),
            frameTexture=GUI_PIC + "metal1.png",
            state=DGG.NORMAL,
        )
        self._coh_frame.setTransparency(TransparencyAttrib.MAlpha)

        self._cohesion = DirectWaitBar(
            parent=self._coh_frame,
            frameSize=(-0.45, 0.45, -0.002, 0.002),
            frameColor=(0.35, 0.35, 0.35, 1),
            value=0,
            barColor=SILVER_COL,
            pos=(0, 0, 0.02),
        )
        recall_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            frameTexture=GUI_PIC + "ny_recall.png",
            pos=(-0.27, 0, -0.02),
            relief="flat",
            command=base.team.cohesion_recall,  # noqa: F821
        )
        recall_ico.setTransparency(TransparencyAttrib.MAlpha)
        recall_ico.bind(DGG.ENTER, self._highlight_coh_but, extraArgs=[recall_ico])
        recall_ico.bind(DGG.EXIT, self._dehighlight_but, extraArgs=[recall_ico])

        cover_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.035, 0.035, -0.035, 0.035),
            frameTexture=GUI_PIC + "ny_cover.png",
            pos=(-0.09, 0, -0.01),
            relief="flat",
            command=base.team.cohesion_cover_fire,  # noqa: F821
        )
        cover_ico.setTransparency(TransparencyAttrib.MAlpha)
        cover_ico.bind(DGG.ENTER, self._highlight_coh_but, extraArgs=[cover_ico])
        cover_ico.bind(DGG.EXIT, self._dehighlight_but, extraArgs=[cover_ico])

        heal_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            frameTexture=GUI_PIC + "ny_heal.png",
            pos=(0.09, 0, -0.015),
            relief="flat",
            command=base.team.cohesion_heal_wounded,  # noqa: F821
        )
        heal_ico.setTransparency(TransparencyAttrib.MAlpha)
        heal_ico.bind(DGG.ENTER, self._highlight_coh_but, extraArgs=[heal_ico])
        heal_ico.bind(DGG.EXIT, self._dehighlight_but, extraArgs=[heal_ico])

        rage_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.035, 0.035, -0.035, 0.035),
            frameTexture=GUI_PIC + "ny_rage.png",
            pos=(0.27, 0, -0.015),
            relief="flat",
            command=base.team.cohesion_rage,  # noqa: F821
        )
        rage_ico.setTransparency(TransparencyAttrib.MAlpha)
        rage_ico.bind(DGG.ENTER, self._highlight_coh_but, extraArgs=[rage_ico])
        rage_ico.bind(DGG.EXIT, self._dehighlight_but, extraArgs=[rage_ico])

        heart_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.035, 0.035, -0.035, 0.035),
            frameTexture=GUI_PIC + "ny_heart.png",
            pos=(0.445, 0, -0.015),
            relief="flat",
            command=base.team.cohesion_hold_together,  # noqa: F821
        )
        heart_ico.setTransparency(TransparencyAttrib.MAlpha)
        heart_ico.bind(DGG.ENTER, self._highlight_coh_but, extraArgs=[heart_ico])
        heart_ico.bind(DGG.EXIT, self._dehighlight_but, extraArgs=[heart_ico])

        self._coh_icons = (
            {"wid": recall_ico, "file": "recall.png", "value": 20},
            {"wid": cover_ico, "file": "cover.png", "value": 40},
            {"wid": heal_ico, "file": "heal.png", "value": 60},
            {"wid": rage_ico, "file": "rage.png", "value": 80},
            {"wid": heart_ico, "file": "heart.png", "value": 100},
        )
        DirectButton(
            parent=self._coh_frame,
            pos=(-0.5, 0, -0.028),
            command=self._show_cohesion_abilities,
            clickSound=base.main_menu.click_snd,  # noqa: F821
            **ABOUT_BUT_PARAMS,
        ).setTransparency(TransparencyAttrib.MAlpha)

    def _highlight_coh_but(self, button, _):
        """Highlight cohesion skill button, if it can be used.

        Args:
            button (panda3d.gui.DirectGui.DirectButton):
                Button to highlight.
        """
        if "ny_" not in button["frameTexture"]:
            button["frameTexture"] = (
                GUI_PIC + "hover_" + button["frameTexture"].split("/")[-1]
            )

    def _dehighlight_but(self, button, _):
        """Dehighlight button.

        Args:
            button (panda3d.gui.DirectGui.DirectButton):
                Button to dehighlight.
        """
        if "hover_" in button["frameTexture"]:
            button["frameTexture"] = button["frameTexture"].replace("hover_", "")

    def _highlight_res_but(self, button, resource, _):
        """Highlight resource button, if it can be used.

        Args:
            button (panda3d.gui.DirectGui.DirectButton):
                Button to highlight.
            resource (str): Name of the resource.
        """
        if base.resource(resource):  # noqa: F821
            button["frameTexture"] = (
                GUI_PIC + "hover_" + button["frameTexture"].split("/")[-1]
            )

    def _show_cohesion_abilities(self):
        """Show/hide cohesion abilities description."""
        if self._coh_desc_shown:
            self._coh_frame["frameSize"] = (-0.55, 0.55, -0.05, 0.05)

            for wid in self._coh_desc_wids:
                wid.destroy()

            self._coh_desc_wids.clear()
            self._coh_desc_shown = False
            return

        self._coh_desc_shown = True
        self._coh_frame["frameSize"] = (-0.55, 0.55, -0.61, 0.05)
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Cohesion skills",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.033,
                text_fg=SILVER_COL,
                pos=(0, 0, -0.08),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.035, 0.035, -0.035, 0.035),
                frameTexture=GUI_PIC + "recall.png",
                pos=(-0.45, 0, -0.13),
                relief="flat",
            )
        )

        x_coor = -0.39
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Recall the past",
                text_align=TextNode.ALeft,
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.03,
                text_fg=SILVER_COL,
                pos=(x_coor, 0, -0.117),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Every character gets +25 energy. Cooldown: 10 min.",
                text_align=TextNode.ALeft,
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.029,
                text_fg=SILVER_COL,
                pos=(x_coor, 0, -0.155),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.045, 0.045, -0.045, 0.045),
                frameTexture=GUI_PIC + "cover.png",
                pos=(-0.45, 0, -0.22),
                relief="flat",
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Cover fire",
                text_align=TextNode.ALeft,
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.03,
                text_fg=SILVER_COL,
                pos=(x_coor, 0, -0.217),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Every character gets +20% accuracy. Cooldown: 5 min.",
                text_align=TextNode.ALeft,
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.029,
                text_fg=SILVER_COL,
                pos=(x_coor, 0, -0.255),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.035, 0.035, -0.035, 0.035),
                frameTexture=GUI_PIC + "heal.png",
                pos=(-0.45, 0, -0.33),
                relief="flat",
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Not leaving ours",
                text_align=TextNode.ALeft,
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.03,
                text_fg=SILVER_COL,
                pos=(x_coor, 0, -0.317),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text=(
                    "Characters with health < 30 "
                    "getting +20 health. Cooldown: 10 min."
                ),
                text_align=TextNode.ALeft,
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.029,
                text_fg=SILVER_COL,
                pos=(x_coor, 0, -0.355),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.045, 0.045, -0.045, 0.045),
                frameTexture=GUI_PIC + "rage.png",
                pos=(-0.45, 0, -0.43),
                relief="flat",
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Common rage",
                text_align=TextNode.ALeft,
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.03,
                text_fg=SILVER_COL,
                pos=(x_coor, 0, -0.417),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Every character gets +30% to damage. Cooldown: 10 min.",
                text_align=TextNode.ALeft,
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.029,
                text_fg=SILVER_COL,
                pos=(x_coor, 0, -0.455),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.043, 0.043, -0.043, 0.043),
                frameTexture=GUI_PIC + "heart.png",
                pos=(-0.45, 0, -0.53),
                relief="flat",
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Hold together",
                text_align=TextNode.ALeft,
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.03,
                text_fg=SILVER_COL,
                pos=(x_coor, 0, -0.517),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="No characters will die in next 1.5 min. Cooldown: 15 min.",
                text_align=TextNode.ALeft,
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.029,
                text_fg=SILVER_COL,
                pos=(x_coor, 0, -0.555),
            )
        )

    def _show_expendable_resources(self):
        """Show/hide expendable resources description."""
        if self._res_desc_shown:
            self._res_frame["frameSize"] = (-0.3, 0.3, -0.03, 0.028)

            for wid in self._res_desc_wids:
                wid.destroy()

            self._res_desc_wids.clear()
            self._res_desc_shown = False
            return

        self._res_desc_shown = True
        self._res_frame["frameSize"] = (-0.3, 0.3, -0.41, 0.028)
        self._res_desc_wids.append(
            DirectLabel(
                parent=self._res_frame,
                text=base.labels.RESOURCES[0],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.033,
                text_fg=SILVER_COL,
                pos=(0, 0, -0.08),
            )
        )
        self._res_desc_wids.append(
            DirectButton(
                parent=self._res_frame,
                frameSize=(-0.03, 0.03, -0.03, 0.03),
                frameTexture=GUI_PIC + "medicine.png",
                pos=(-0.22, 0, -0.16),
                relief="flat",
            )
        )
        self._res_desc_wids.append(
            DirectLabel(
                parent=self._res_frame,
                text=base.labels.RESOURCES[1],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.03,
                text_fg=SILVER_COL,
                pos=(0.035, 0, -0.147),
            )
        )
        self._res_desc_wids.append(
            DirectLabel(
                parent=self._res_frame,
                text=base.labels.RESOURCES[2],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.029,
                text_fg=SILVER_COL,
                pos=(0.035, 0, -0.185),
            )
        )
        self._res_desc_wids.append(
            DirectButton(
                parent=self._res_frame,
                frameSize=(-0.03, 0.03, -0.03, 0.03),
                frameTexture=GUI_PIC + "smoke_filter.png",
                pos=(-0.22, 0, -0.25),
                relief="flat",
            )
        )
        self._res_desc_wids.append(
            DirectLabel(
                parent=self._res_frame,
                text=base.labels.RESOURCES[3],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.03,
                text_fg=SILVER_COL,
                pos=(0.035, 0, -0.243),
            )
        )
        self._res_desc_wids.append(
            DirectLabel(
                parent=self._res_frame,
                text=base.labels.RESOURCES[4],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.029,
                text_fg=SILVER_COL,
                pos=(0.035, 0, -0.275),
            )
        )
        self._res_desc_wids.append(
            DirectButton(
                parent=self._res_frame,
                frameSize=(-0.018, 0.018, -0.028, 0.028),
                frameTexture=GUI_PIC + "stimulator.png",
                pos=(-0.22, 0, -0.349),
                relief="flat",
            )
        )
        self._res_desc_wids.append(
            DirectLabel(
                parent=self._res_frame,
                text=base.labels.RESOURCES[5],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.03,
                text_fg=SILVER_COL,
                pos=(0.035, 0, -0.337),
            )
        )
        self._res_desc_wids.append(
            DirectLabel(
                parent=self._res_frame,
                text=base.labels.RESOURCES[6],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.029,
                text_fg=SILVER_COL,
                pos=(0.035, 0, -0.375),
            )
        )

    def _blink_widget(self, widget, task):
        """Make the given widget blinking.

        Args:
            widget (str): Name of the widget to blink.
        """
        self._blink_step += 1

        if self._blink_step in (2, 4):
            self._resources[widget]["text_bg"] = (0, 0, 0, 0)
            self._resources[widget]["text_fg"] = RUST_COL
        else:
            self._resources[widget]["text_bg"] = (0.6, 0, 0, 1)
            self._resources[widget]["text_fg"] = (0, 0, 0, 1)

        if self._blink_step == 4:
            self._blink_step = 0
            return task.done

        return task.again

    def check_enough_money(self, ch_sum):
        """Ensure that player have enough money for a buy.

        Make the money widget blink if player doesn't have enough money.

        Args:
            ch_sum (int): Buy cost.

        Returns:
            bool: True, if player has enough money.
        """
        if ch_sum > base.dollars:  # noqa: F821
            taskMgr.doMethodLater(  # noqa: F821
                0.4,
                self._blink_widget,
                "blink_money_widget",
                extraArgs=["dollars"],
                appendTask=True,
            )
            self._err_snd.play()
            return False

        return True

    def check_has_cell(self):
        """Check that the Train has at least one cell.

        Make the characters number widget
        blink, if there are not free cells.
        """
        if not base.train.has_cell():  # noqa: F821
            taskMgr.doMethodLater(  # noqa: F821
                0.4,
                self._blink_widget,
                "blink_money_widget",
                extraArgs=["chars"],
                appendTask=True,
            )
            self._err_snd.play()
            return False

        return True

    def disable_cohesion(self):
        """Disable all the cohesion abilities."""
        for icon in self._coh_icons:
            icon["wid"]["frameTexture"] = GUI_PIC + "ny_" + icon["file"]

    def update_chars(self):
        """Update characters number widget."""
        self._resources["chars"]["text"] = "{current}/{maximum}".format(
            current=len(base.team.chars), maximum=base.train.cells  # noqa: F821
        )

    def update_cohesion(self, new_value):
        """Update cohesion indicator with the given value.

        Args:
            new_value (int): New amount of the cohesion points.
        """
        self._cohesion["value"] = new_value

        if base.team.cohesion_cooldown:  # noqa: F821
            return

        for icon in self._coh_icons:
            if "hover_" in icon["wid"]["frameTexture"]:
                continue

            if new_value >= icon["value"]:
                icon["wid"]["frameTexture"] = GUI_PIC + icon["file"]
            else:
                icon["wid"]["frameTexture"] = GUI_PIC + "ny_" + icon["file"]

    def update_resource(self, name, value):
        """Update the indicator with the given value.

        Args:
            name (str): The indicator name.
            value (Any): The new indicator value.
        """
        self._resources[name]["text"] = str(value)
