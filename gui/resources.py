"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Resources GUI.
"""
from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel, DirectWaitBar
from panda3d.core import TransparencyAttrib

from .interface import ICON_PATH, RUST_COL, SILVER_COL


class ResourcesInterface:
    """Interface to show the current amount of player resources."""

    def __init__(self):
        self._coh_desc_wids = []
        self._coh_desc_shown = False

        frame = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.075, 0.075, -0.025, 0.025),
            pos=(0.075, 0, -0.025),
            frameTexture=ICON_PATH + "metal1.png",
        )
        frame.setTransparency(TransparencyAttrib.MAlpha)
        DirectFrame(
            parent=frame,  # noqa: F821
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            pos=(-0.05, 0, 0),
            frameTexture=ICON_PATH + "icon_dollar.png",
        )
        self._dollars = DirectLabel(
            parent=frame,
            text="300",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.035, 0.035),
            text_fg=RUST_COL,
            pos=(0.01, 0, -0.008),
        )
        self._coh_frame = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.55, 0.55, -0.05, 0.05),
            pos=(2.95, 0, -0.05),
            frameTexture=ICON_PATH + "metal1.png",
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
            frameTexture=ICON_PATH + "ny_recall_icon.png",
            pos=(-0.27, 0, -0.02),
            relief="flat",
            command=base.team.cohesion_recall,  # noqa: F821
        )
        recall_ico.setTransparency(TransparencyAttrib.MAlpha)

        cover_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.035, 0.035, -0.035, 0.035),
            frameTexture=ICON_PATH + "ny_cover_icon.png",
            pos=(-0.09, 0, -0.01),
            relief="flat",
            command=base.team.cohesion_cover_fire,  # noqa: F821
        )
        cover_ico.setTransparency(TransparencyAttrib.MAlpha)

        heal_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            frameTexture=ICON_PATH + "ny_heal_icon.png",
            pos=(0.09, 0, -0.015),
            relief="flat",
            command=base.team.cohesion_heal_wounded,  # noqa: F821
        )
        heal_ico.setTransparency(TransparencyAttrib.MAlpha)

        rage_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.035, 0.035, -0.035, 0.035),
            frameTexture=ICON_PATH + "ny_rage_icon.png",
            pos=(0.27, 0, -0.015),
            relief="flat",
            command=base.team.cohesion_rage,  # noqa: F821
        )
        rage_ico.setTransparency(TransparencyAttrib.MAlpha)

        heart_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.035, 0.035, -0.035, 0.035),
            frameTexture=ICON_PATH + "ny_heart_icon.png",
            pos=(0.445, 0, -0.015),
            relief="flat",
            command=base.team.cohesion_hold_together,  # noqa: F821
        )
        heart_ico.setTransparency(TransparencyAttrib.MAlpha)

        self._coh_icons = (
            {"wid": recall_ico, "file": "recall_icon.png", "value": 20},
            {"wid": cover_ico, "file": "cover_icon.png", "value": 40},
            {"wid": heal_ico, "file": "heal_icon.png", "value": 60},
            {"wid": rage_ico, "file": "rage_icon.png", "value": 80},
            {"wid": heart_ico, "file": "heart_icon.png", "value": 100},
        )
        DirectButton(
            parent=self._coh_frame,
            text="?",
            frameSize=(-0.02, 0.02, -0.02, 0.02),
            frameColor=(0, 0, 0, 0),
            text_bg=(0, 0, 0, 0),
            text_fg=SILVER_COL,
            text_scale=0.03,
            pos=(-0.5, 0, -0.028),
            relief="flat",
            command=self._show_cohesion_abilities,
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
        self._coh_frame["frameSize"] = (-0.55, 0.55, -0.6, 0.05)
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.035, 0.035, -0.035, 0.035),
                frameTexture=ICON_PATH + "recall_icon.png",
                pos=(-0.45, 0, -0.11),
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
                pos=(-0.29, 0, -0.097),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Every character gets +15 energy. Cooldown: 15 min.",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.029, 0.029),
                text_fg=SILVER_COL,
                pos=(-0.055, 0, -0.135),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.045, 0.045, -0.045, 0.045),
                frameTexture=ICON_PATH + "cover_icon.png",
                pos=(-0.45, 0, -0.2),
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
                pos=(-0.325, 0, -0.197),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Every character gets +20 accuracy. Cooldown: 10 min.",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.029, 0.029),
                text_fg=SILVER_COL,
                pos=(-0.038, 0, -0.235),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.035, 0.035, -0.035, 0.035),
                frameTexture=ICON_PATH + "heal_icon.png",
                pos=(-0.45, 0, -0.31),
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
                pos=(-0.283, 0, -0.297),
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
                pos=(0.03, 0, -0.335),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.045, 0.045, -0.045, 0.045),
                frameTexture=ICON_PATH + "rage_icon.png",
                pos=(-0.45, 0, -0.41),
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
                pos=(-0.298, 0, -0.397),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Every character gets +30% to damage. Cooldown: 15 min.",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.029, 0.029),
                text_fg=SILVER_COL,
                pos=(-0.023, 0, -0.435),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.043, 0.043, -0.043, 0.043),
                frameTexture=ICON_PATH + "heart_icon.png",
                pos=(-0.45, 0, -0.51),
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
                pos=(-0.298, 0, -0.497),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="No characters will die in next 1.5 min. Cooldown: 20 min.",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.029, 0.029),
                text_fg=SILVER_COL,
                pos=(-0.029, 0, -0.535),
            )
        )

    def update_money(self, new_value):
        """Update money indicator with the given value.

        Args:
            new_value (int): New amount of money.
        """
        self._dollars["text"] = str(new_value)

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