"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The Train indicators GUI.
"""
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectWaitBar
from panda3d.core import TransparencyAttrib

from .widgets import GUI_PIC, RUST_COL, SILVER_COL


class TrainGUI:
    """The Train state GUI."""

    def __init__(self):
        frame = DirectFrame(
            parent=base.a2dBottomRight,  # noqa: F821
            frameSize=(-0.09, 0.09, -0.28, 0.28),
            pos=(-0.09, 0, 0.28),
            frameTexture=GUI_PIC + "metal1.png",
        )
        frame.setTransparency(TransparencyAttrib.MAlpha)
        DirectFrame(
            parent=frame,
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            pos=(0.05, 0, 0.24),
            frameTexture=GUI_PIC + "train.png",
        ).setTransparency(TransparencyAttrib.MAlpha)

        DirectFrame(
            parent=frame,
            frameSize=(-0.028, 0.028, -0.023, 0.023),
            pos=(-0.012, 0, 0.24),
            frameTexture=GUI_PIC + "speed.png",
        ).setTransparency(TransparencyAttrib.MAlpha)

        self._durability = DirectWaitBar(
            parent=frame,
            frameSize=(-0.225, 0.225, -0.002, 0.002),
            frameColor=(0.35, 0.35, 0.35, 1),
            range=1000,
            value=1000,
            barColor=(0.42, 0.42, 0.8, 1),
            pos=(0.05, 0, -0.025),
        )
        self._durability.setR(-90)
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
            pos=(0, 0, -0.97),
            frameTexture=GUI_PIC + "metal1.png",
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
            0.25, self._update_speed, "update_speed_indicator"
        )
        self._fork_lab = None

    def _turn_on_fork(self, fork):
        """Turn the Train on the next fork.

        Args:
            fork (world.block.Block): Fork block to turn on.
        """
        base.train.do_turn = 1  # noqa: F821
        base.ignore("t")  # noqa: F821
        fork.load_additional_surface()
        self.hide_turning_ability()

    def _update_speed(self, task):
        """Update the Train speed GUI indicator."""
        self._speed["value"] = base.train.ctrl.current_speed  # noqa: F821
        return task.again

    def hide_turning_ability(self):
        """Hide turning GUI."""
        if self._fork_lab is None:
            return

        self._fork_lab.destroy()
        self._fork_lab = None

    def show_turning_ability(self, fork, branch, invert):
        """Show a notification about turning ability.

        If there is a fork in the next 2 miles, the player can
        use an ability to turn, or ignore the fork and move in
        the default direction.

        Args:
            fork (world.block.Block):
                Fork block to which the player is approaching.
            branch (str): Branch side indicator: "l" or "r".
            invert (bool):
                True, if the player is approaching the fork
                from opposite direction of the world.
        """
        base.train.do_turn = 0  # noqa: F821
        text = ""

        if fork.name == "l_fork":
            if invert or branch == "l":
                text = "Approaching a fork:\npress T to turn right\nignore to proceed"
            else:
                text = "Approaching a fork:\npress T to turn left\nignore to proceed"
        elif fork.name == "r_fork":
            if invert or branch == "r":
                text = "Approaching a fork:\npress T to turn left\nignore to proceed"
            else:
                text = "Approaching a fork:\npress T to turn right\nignore to proceed"

        base.accept("t", self._turn_on_fork, [fork])  # noqa: F821

        self._fork_lab = DirectLabel(
            pos=(0, 0, -0.8),
            text_scale=0.04,
            text_fg=SILVER_COL,
            frameColor=(0, 0, 0, 0.4),
            text=text,
        )

    def update_indicators(self, **params):
        """Update the Train GUI with the given parameters.

        Args:
            params (dict): New parameters values.
        """
        if "durability" in params.keys():
            self._durability["value"] = params["durability"]

    def update_miles(self, new_miles):
        """Update the miles meter widget.

        Args:
            new_miles (int): New milesmeter value.
        """
        self._miles_meter["text"] = str(new_miles).rjust(7, "0") + " mi"
