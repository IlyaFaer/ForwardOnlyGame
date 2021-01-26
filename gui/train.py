"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The Train indicators GUI.
"""
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectWaitBar
from panda3d.core import TransparencyAttrib

from .widgets import ICON_PATH, RUST_COL, SILVER_COL


class TrainGUI:
    """The Train state GUI."""

    def __init__(self):
        frame = DirectFrame(
            parent=base.a2dBottomRight,  # noqa: F821
            frameSize=(-0.09, 0.09, -0.28, 0.28),
            pos=(-0.09, 0, 0.28),
            frameTexture=ICON_PATH + "metal1.png",
        )
        frame.setTransparency(TransparencyAttrib.MAlpha)
        DirectFrame(
            parent=frame,  # noqa: F821
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            pos=(0.05, 0, 0.24),
            frameTexture=ICON_PATH + "train.png",
        ).setTransparency(TransparencyAttrib.MAlpha)

        DirectFrame(
            parent=frame,  # noqa: F821
            frameSize=(-0.028, 0.028, -0.023, 0.023),
            pos=(-0.012, 0, 0.24),
            frameTexture=ICON_PATH + "speed.png",
        ).setTransparency(TransparencyAttrib.MAlpha)

        self._damnability = DirectWaitBar(
            parent=frame,
            frameSize=(-0.225, 0.225, -0.002, 0.002),
            frameColor=(0.35, 0.35, 0.35, 1),
            range=1000,
            value=1000,
            barColor=(0.42, 0.42, 0.8, 1),
            pos=(0.05, 0, -0.025),
        )
        self._damnability.setR(-90)
        self._speed = DirectWaitBar(
            parent=frame,
            frameSize=(-0.225, 0.225, -0.002, 0.002),
            frameColor=(0.35, 0.35, 0.35, 1),
            range=1,
            value=1,
            barColor=(1, 0.63, 0, 0.6),
            pos=(-0.012, 0, -0.025),
        )
        self._speed.setR(-90)

        DirectLabel(
            parent=frame,
            pos=(-0.05, 0, 0.19),
            frameSize=(-0.25, 0.25, -0.01, 0.01),
            frameColor=(0, 0, 0, 0),
            text="40-\n\n-\n\n-\n\n-\n\n20-\n\n-\n\n-\n\n-\n\n0-",
            text_scale=0.028,
            text_fg=SILVER_COL,
        )

        frame_miles = DirectFrame(
            frameSize=(-0.115, 0.115, -0.03, 0.03),
            pos=(0.0, 0, -0.97),
            frameTexture=ICON_PATH + "metal1.png",
        )
        self._miles_meter = DirectLabel(
            parent=frame_miles,
            text="0000000",
            frameSize=(0.1, 0.1, 0.15, 0.15),
            text_scale=(0.033, 0.038),
            text_fg=RUST_COL,
            pos=(0, 0, -0.01),
        )
        taskMgr.doMethodLater(  # noqa: F821
            0.3, self._update_speed, "update_speed_indicator"
        )

    def _update_speed(self, task):
        """Update the Train speed GUI indicator."""
        self._speed["value"] = base.train.ctrl.current_speed  # noqa: F821
        return task.again

    def update_indicators(self, **params):
        """Update the Train GUI with the given parameters.

        Args:
            params (dict): New parameters values.
        """
        if "damnability" in params.keys():
            self._damnability["value"] = params["damnability"]

    def update_miles(self, new_miles):
        """Update the miles meter widget.

        Args:
            new_miles (int): New milesmeter value.
        """
        self._miles_meter["text"] = str(new_miles).rjust(7, "0") + " mi"
