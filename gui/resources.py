"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Resources GUI.
"""
from direct.gui.DirectGui import (
    DGG,
    DirectButton,
    DirectFrame,
    DirectLabel,
    DirectWaitBar,
)
from panda3d.core import TransparencyAttrib

from .character import ABOUT_BUT_PARAMS
from .train import ICON_PATH, RUST_COL, SILVER_COL


class ResourcesInterface:
    """GUI to track player's resources.

    Includes money and cohesion.
    """

    def __init__(self):
        self._coh_desc_wids = []
        self._coh_desc_shown = False
        self._res_desc_wids = []
        self._res_desc_shown = False

        self._resources = {}

        self._res_frame = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.21, 0.21, -0.03, 0.028),
            pos=(0.21, 0, -0.028),
            frameTexture=ICON_PATH + "metal1.png",
        )
        self._res_frame.setTransparency(TransparencyAttrib.MAlpha)

        DirectFrame(
            parent=self._res_frame,  # noqa: F821
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            pos=(-0.18, 0, 0),
            frameTexture=ICON_PATH + "dollar.png",
        )
        self._resources["dollars"] = DirectLabel(
            parent=self._res_frame,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.035, 0.035),
            text_fg=RUST_COL,
            pos=(-0.11, 0, -0.008),
        )
        DirectButton(
            parent=self._res_frame,
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            relief="flat",
            pos=(-0.02, 0, 0),
            frameTexture=ICON_PATH + "medicine.png",
            command=base.team.use_medicine,  # noqa: F821
        )
        self._resources["medicine_boxes"] = DirectLabel(
            parent=self._res_frame,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.035, 0.035),
            text_fg=RUST_COL,
            pos=(0.02, 0, -0.008),
        )
        DirectButton(
            parent=self._res_frame,
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            relief="flat",
            pos=(0.08, 0, 0),
            frameTexture=ICON_PATH + "smoke_filter.png",
            command=base.train.use_smoke_filter,  # noqa: F821
        )
        self._resources["smoke_filters"] = DirectLabel(
            parent=self._res_frame,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.035, 0.035),
            text_fg=RUST_COL,
            pos=(0.125, 0, -0.008),
        )
        DirectButton(
            parent=self._res_frame,
            pos=(0.18, 0, -0.013),
            command=self._show_expendable_resources,
            clickSound=base.main_menu.click_snd,  # noqa: F821
            **ABOUT_BUT_PARAMS,
        ).setTransparency(TransparencyAttrib.MAlpha)

        self._coh_frame = DirectFrame(
            parent=base.a2dBottomRight,  # noqa: F821
            frameSize=(-0.55, 0.55, -0.05, 0.05),
            pos=(-0.6, 0, 1.95),
            frameTexture=ICON_PATH + "metal1.png",
            state=DGG.NORMAL,
        )
        self._coh_frame.setTransparency(TransparencyAttrib.MAlpha)

        self._cohesion = DirectWaitBar(
            parent=self._coh_frame,
            frameSize=(-0.45, 0.45, -0.002, 0.002),
            value=0,
            barColor=SILVER_COL,
            pos=(0, 0, 0.02),
        )
        recall_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            frameTexture=ICON_PATH + "ny_recall.png",
            pos=(-0.27, 0, -0.02),
            relief="flat",
            command=base.team.cohesion_recall,  # noqa: F821
        )
        recall_ico.setTransparency(TransparencyAttrib.MAlpha)

        cover_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.035, 0.035, -0.035, 0.035),
            frameTexture=ICON_PATH + "ny_cover.png",
            pos=(-0.09, 0, -0.01),
            relief="flat",
            command=base.team.cohesion_cover_fire,  # noqa: F821
        )
        cover_ico.setTransparency(TransparencyAttrib.MAlpha)

        heal_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            frameTexture=ICON_PATH + "ny_heal.png",
            pos=(0.09, 0, -0.015),
            relief="flat",
            command=base.team.cohesion_heal_wounded,  # noqa: F821
        )
        heal_ico.setTransparency(TransparencyAttrib.MAlpha)

        rage_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.035, 0.035, -0.035, 0.035),
            frameTexture=ICON_PATH + "ny_rage.png",
            pos=(0.27, 0, -0.015),
            relief="flat",
            command=base.team.cohesion_rage,  # noqa: F821
        )
        rage_ico.setTransparency(TransparencyAttrib.MAlpha)

        heart_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.035, 0.035, -0.035, 0.035),
            frameTexture=ICON_PATH + "ny_heart.png",
            pos=(0.445, 0, -0.015),
            relief="flat",
            command=base.team.cohesion_hold_together,  # noqa: F821
        )
        heart_ico.setTransparency(TransparencyAttrib.MAlpha)

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
                text_scale=(0.033, 0.033),
                text_fg=SILVER_COL,
                pos=(0, 0, -0.08),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.035, 0.035, -0.035, 0.035),
                frameTexture=ICON_PATH + "recall.png",
                pos=(-0.45, 0, -0.13),
                relief="flat",
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Recall the past",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.03, 0.03),
                text_fg=SILVER_COL,
                pos=(-0.29, 0, -0.117),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Every character gets +15 energy. Cooldown: 15 min.",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.029, 0.029),
                text_fg=SILVER_COL,
                pos=(-0.055, 0, -0.155),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.045, 0.045, -0.045, 0.045),
                frameTexture=ICON_PATH + "cover.png",
                pos=(-0.45, 0, -0.22),
                relief="flat",
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Cover fire",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.03, 0.03),
                text_fg=SILVER_COL,
                pos=(-0.325, 0, -0.217),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Every character gets +20% accuracy. Cooldown: 10 min.",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.029, 0.029),
                text_fg=SILVER_COL,
                pos=(-0.032, 0, -0.255),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.035, 0.035, -0.035, 0.035),
                frameTexture=ICON_PATH + "heal.png",
                pos=(-0.45, 0, -0.33),
                relief="flat",
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Not leaving ours",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.03, 0.03),
                text_fg=SILVER_COL,
                pos=(-0.283, 0, -0.317),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text=(
                    "Characters with health < 30 "
                    "getting +20 health. Cooldown: 15 min."
                ),
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.029, 0.029),
                text_fg=SILVER_COL,
                pos=(0.03, 0, -0.355),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.045, 0.045, -0.045, 0.045),
                frameTexture=ICON_PATH + "rage.png",
                pos=(-0.45, 0, -0.43),
                relief="flat",
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Common rage",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.03, 0.03),
                text_fg=SILVER_COL,
                pos=(-0.298, 0, -0.417),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Every character gets +30% to damage. Cooldown: 15 min.",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.029, 0.029),
                text_fg=SILVER_COL,
                pos=(-0.023, 0, -0.455),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.043, 0.043, -0.043, 0.043),
                frameTexture=ICON_PATH + "heart.png",
                pos=(-0.45, 0, -0.53),
                relief="flat",
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Hold together",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.03, 0.03),
                text_fg=SILVER_COL,
                pos=(-0.298, 0, -0.517),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="No characters will die in next 1.5 min. Cooldown: 20 min.",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.029, 0.029),
                text_fg=SILVER_COL,
                pos=(-0.029, 0, -0.555),
            )
        )

    def _show_expendable_resources(self):
        """Show/hide expendable resources description."""
        if self._res_desc_shown:
            self._res_frame["frameSize"] = (-0.21, 0.21, -0.03, 0.028)

            for wid in self._res_desc_wids:
                wid.destroy()

            self._res_desc_wids.clear()
            self._res_desc_shown = False
            return

        self._res_desc_shown = True
        self._res_frame["frameSize"] = (-0.21, 0.21, -0.32, 0.028)
        self._res_desc_wids.append(
            DirectLabel(
                parent=self._res_frame,
                text="Expendable resources:",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.033, 0.033),
                text_fg=SILVER_COL,
                pos=(0, 0, -0.08),
            )
        )
        self._res_desc_wids.append(
            DirectButton(
                parent=self._res_frame,
                frameSize=(-0.03, 0.03, -0.03, 0.03),
                frameTexture=ICON_PATH + "medicine.png",
                pos=(-0.15, 0, -0.16),
                relief="flat",
            )
        )
        self._res_desc_wids.append(
            DirectLabel(
                parent=self._res_frame,
                text="Medicine box",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.03, 0.03),
                text_fg=SILVER_COL,
                pos=(0.035, 0, -0.147),
            )
        )
        self._res_desc_wids.append(
            DirectLabel(
                parent=self._res_frame,
                text="Cure the disease",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.029, 0.029),
                text_fg=SILVER_COL,
                pos=(0.035, 0, -0.185),
            )
        )
        self._res_desc_wids.append(
            DirectButton(
                parent=self._res_frame,
                frameSize=(-0.03, 0.03, -0.03, 0.03),
                frameTexture=ICON_PATH + "smoke_filter.png",
                pos=(-0.15, 0, -0.25),
                relief="flat",
            )
        )
        self._res_desc_wids.append(
            DirectLabel(
                parent=self._res_frame,
                text="Smoke filter",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.03, 0.03),
                text_fg=SILVER_COL,
                pos=(0.035, 0, -0.243),
            )
        )
        self._res_desc_wids.append(
            DirectLabel(
                parent=self._res_frame,
                text="Reduce attack chance",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.029, 0.029),
                text_fg=SILVER_COL,
                pos=(0.035, 0, -0.275),
            )
        )

    def update_resource(self, name, value):
        """Update the indicator with the given value.

        Args:
            name (str): The indicator name.
            value (Any): The new indicator value.
        """
        self._resources[name]["text"] = str(value)

    def update_cohesion(self, new_value):
        """Update cohesion indicator with the given value.

        Args:
            new_value (int): New amount of the cohesion points.
        """
        self._cohesion["value"] = new_value

        if base.team.cohesion_cooldown:  # noqa: F821
            return

        for icon in self._coh_icons:
            if new_value >= icon["value"]:
                icon["wid"]["frameTexture"] = ICON_PATH + icon["file"]
            else:
                icon["wid"]["frameTexture"] = ICON_PATH + "ny_" + icon["file"]

    def disable_cohesion(self):
        """Disable all the cohesion abilities."""
        for icon in self._coh_icons:
            icon["wid"]["frameTexture"] = ICON_PATH + "ny_" + icon["file"]
