"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Outings GUI.
"""

from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel, DirectWaitBar
from panda3d.core import TransparencyAttrib

from .interface import RUST_COL, SILVER_COL


class OutingsInterface:
    """Outing dialogs GUI."""

    def __init__(self):
        self._outing_widgets = []
        self._going_for_outing = []
        self._char_buttons = {}

        self._blink_step = 0
        self._upcome_icon = DirectFrame(
            frameSize=(-0.1, 0.1, -0.1, 0.1),
            pos=(0, 0, 0.8),
            frameTexture="gui/tex/icon_looting.png",
        )
        self._upcome_icon.setTransparency(TransparencyAttrib.MAlpha)
        self._upcome_icon.hide()

        self._upcome_text = DirectLabel(
            text="",
            frameSize=(0.4, 0.4, 0.4, 0.4),
            text_scale=(0.04, 0.04),
            text_fg=RUST_COL,
            pos=(0, 0, 0.65),
        )
        self._upcome_text.hide()

        self._list = DirectFrame(
            frameSize=(-0.73, 0.73, -0.9, 0.9), frameTexture="gui/tex/paper1.png"
        )
        self._list.setTransparency(TransparencyAttrib.MAlpha)
        self._list.hide()

        self._name = DirectLabel(
            parent=self._list,
            text="",
            frameSize=(0.4, 0.4, 0.4, 0.4),
            text_scale=(0.05),
            pos=(-0.4, 0, 0.7),
        )
        self._type = DirectLabel(
            parent=self._list,
            text="",
            frameSize=(0.4, 0.4, 0.4, 0.4),
            text_scale=(0.035),
            pos=(-0.13, 0, 0.699),
        )
        self._desc = DirectLabel(
            parent=self._list,
            text="",
            frameSize=(0.6, 0.6, 0.6, 0.6),
            text_scale=(0.04),
            pos=(0, 0, 0.55),
        )

    def _assign_for_outing(self, to_send_wid, max_assignees):
        """Assign the chosen character for the outing.

        Args:
            to_send_wid (direct.gui.DirectLabel.DirectLabel):
                Widget with number of assigned characters.
            max_assignees (int): Assignees limit.
        """
        char = base.common_ctrl.chosen_char  # noqa: F821
        if (
            char is None
            or char in self._going_for_outing
            or len(self._going_for_outing) == max_assignees
        ):
            return

        self._going_for_outing.append(char)
        self._char_buttons[char.id].setX(0.35)

        to_send_wid["text"] = "People to send ({cur_as}/{max_as}):".format(
            cur_as=str(len(self._going_for_outing)), max_as=str(max_assignees)
        )

    def _unassign_for_outing(self, to_send_wid, max_assignees):
        """Exclude the chosen character from the outing.

        Args:
            to_send_wid (direct.gui.DirectLabel.DirectLabel):
                Widget with number of assigned characters.
            max_assignees (int): Assignees limit.
        """
        char = base.common_ctrl.chosen_char  # noqa: F821
        if char not in self._going_for_outing:
            return

        self._going_for_outing.remove(char)
        self._char_buttons[char.id].setX(-0.35)

        to_send_wid["text"] = "People to send ({cur_as}/{max_as}):".format(
            cur_as=str(len(self._going_for_outing)), max_as=str(max_assignees)
        )

    def _blink_upcome_icon(self, task):
        """Blink upcoming outing icon to attract attention."""
        self._blink_step += 1
        if self._blink_step in (2, 4, 6):
            self._upcome_icon.show()
            if self._blink_step == 6:
                self._blink_step = 0
                return task.done

            return task.again

        self._upcome_icon.hide()
        return task.again

    def _animate_bars(self, bars, score, selected_effect, task):
        """Animate filling the bars.

        Args:
            bars (list): Widget to fill.
            score (int): Total outing score.
            selected_effect (dict):
                Effect which requires to choose a target.
        """
        all_filled = True
        for bar in bars:
            bar_wid = bar[0]
            if bar_wid["value"] >= bar[1]:
                continue

            bar_wid["value"] = bar_wid["value"] + bar_wid["range"] / 100
            all_filled = False

        if all_filled:
            self._outing_widgets.append(
                DirectLabel(
                    parent=self._list,
                    text=" + ".join(
                        (str(bars[0][1]), str(bars[1][1]), str(bars[2][1]))
                    ),
                    frameSize=(0.6, 0.6, 0.6, 0.6),
                    text_scale=(0.04),
                    pos=(0, 0, -0.4),
                )
            )
            self._outing_widgets.append(
                DirectLabel(
                    parent=self._list,
                    text=str(score) + "/100",
                    frameSize=(0.6, 0.6, 0.6, 0.6),
                    text_scale=(0.05),
                    pos=(0, 0, -0.52),
                )
            )
            self._outing_widgets.append(
                DirectButton(
                    pos=(0, 0, -0.75),
                    text="Done",
                    text_fg=RUST_COL,
                    frameColor=(0, 0, 0, 0.3),
                    command=self._finish_outing,  # noqa: F821
                    extraArgs=[selected_effect],
                    scale=(0.05, 0, 0.05),
                )
            )
            return task.done

        return task.again

    def _finish_outing(self, selected_effect):
        """Show effect selector if needed, and finish the outing.

        Args:
            selected_effect (dict):
                Effect which requires to choose a target.
        """
        self._clear_temporary_widgets()

        if not selected_effect:
            self.hide_outing()
            return

        effect_str = ""
        for key, value in selected_effect.items():
            effect_str += key + " " + ("+" if value > 0 else "-") + str(value) + "\n"

        self._outing_widgets.append(
            DirectLabel(
                parent=self._list,
                text="""Selected one character as a target for the effect:
{effect}""".format(
                    effect=effect_str
                ),
                frameSize=(0.6, 0.6, 0.6, 0.6),
                text_scale=(0.045),
                pos=(0, 0, 0.2),
            )
        )
        shift = 0.05
        for id_, char in base.team.chars.items():  # noqa: F821
            but = DirectButton(
                pos=(0, 0, shift),
                text=char.name,
                text_fg=SILVER_COL,
                frameColor=(0, 0, 0, 0.3),
                command=base.common_ctrl.choose_resting_char,  # noqa: F821
                extraArgs=[char.id],
                scale=(0.04, 0, 0.03),
            )
            self._char_buttons[id_] = but
            self._outing_widgets.append(but)

            shift -= 0.04

        self._outing_widgets.append(
            DirectButton(
                pos=(0, 0, -0.75),
                text="Done",
                text_fg=RUST_COL,
                frameColor=(0, 0, 0, 0.3),
                command=self._do_effect_and_finish,  # noqa: F821
                extraArgs=[selected_effect],
                scale=(0.05, 0, 0.05),
            )
        )

    def _do_effect_and_finish(self, effect):
        """Do effects for selected characters and finish the outing.

        Args:
            effect (dict): Effect to do.
        """
        base.common_ctrl.chosen_char.do_effects(effect)  # noqa: F821
        self.hide_outing()

    def _clear_temporary_widgets(self):
        """Destroy all the one-time widgets."""
        for wid in self._outing_widgets:
            wid.destroy()
        self._outing_widgets.clear()

    def show_upcoming(self, type_):
        """Show upcoming outing icon.

        Args:
            type_ (str): Outing type.
        """
        self._upcome_text[
            "text"
        ] = '"{type}" outing available\n in {miles} miles'.format(
            type=type_.capitalize(), miles=2
        )
        self._upcome_text.show()
        self._upcome_icon.show()

        base.taskMgr.doMethodLater(  # noqa: F821
            0.3, self._blink_upcome_icon, "blink_outing_icon"
        )

    def show_upcoming_closer(self):
        """Show that 1 mile left until available outing."""
        self._upcome_text["text"] = self._upcome_text["text"].replace(
            "2 miles", "1 mile"
        )

    def show_can_start(self):
        """Show that outing can be started."""
        self._upcome_text["text"] = "Stop to start outing"

    def hide_outing(self):
        """Hide all the outings gui."""
        self._upcome_text.hide()
        self._upcome_icon.hide()

        self._going_for_outing.clear()

        self._list.hide()
        self._clear_temporary_widgets()

    def start(self, outing):
        """Start outing scenario.

        Draw an interface with outing description.

        Args:
            outing (dict): Outing description.
        """
        self.hide_outing()
        self._list.show()

        self._name["text"] = outing["name"]
        self._type["text"] = outing["type"]
        self._desc["text"] = outing["desc"]

        self._outing_widgets.append(
            DirectLabel(
                parent=self._list,
                text="Team:",
                frameSize=(0.6, 0.6, 0.6, 0.6),
                text_scale=(0.035),
                pos=(-0.35, 0, 0),
            )
        )
        shift = -0.07
        for id_, char in base.team.chars.items():  # noqa: F821
            but = DirectButton(
                pos=(-0.35, 0, shift),
                text=char.name,
                text_fg=SILVER_COL,
                frameColor=(0, 0, 0, 0.3),
                command=base.common_ctrl.choose_resting_char,  # noqa: F821
                extraArgs=[char.id],
                scale=(0.04, 0, 0.03),
            )
            self._char_buttons[id_] = but
            self._outing_widgets.append(but)

            shift -= 0.04

        to_send = DirectLabel(
            parent=self._list,
            text="People to send (0/{max_as}):".format(max_as=outing["max_assignees"]),
            frameSize=(0.6, 0.6, 0.6, 0.6),
            text_scale=(0.035),
            pos=(0.35, 0, 0),
        )
        self._outing_widgets.append(to_send)

        self._outing_widgets.append(
            DirectButton(
                pos=(0, 0, -0.15),
                text=">",
                text_fg=SILVER_COL,
                frameColor=(0, 0, 0, 0.3),
                command=self._assign_for_outing,  # noqa: F821
                extraArgs=[to_send, outing["max_assignees"]],
                scale=(0.075, 0, 0.075),
            )
        )
        self._outing_widgets.append(
            DirectButton(
                pos=(0, 0, -0.21),
                text="<",
                text_fg=SILVER_COL,
                frameColor=(0, 0, 0, 0.3),
                command=self._unassign_for_outing,  # noqa: F821
                extraArgs=[to_send, outing["max_assignees"]],
                scale=(0.075, 0, 0.075),
            )
        )
        self._outing_widgets.append(
            DirectButton(
                pos=(-0.15, 0, -0.75),
                text="Don't send",
                text_fg=RUST_COL,
                frameColor=(0, 0, 0, 0.3),
                command=self.hide_outing,  # noqa: F821
                scale=(0.05, 0, 0.05),
            )
        )
        self._outing_widgets.append(
            DirectButton(
                pos=(0.15, 0, -0.75),
                text="Send",
                text_fg=RUST_COL,
                frameColor=(0, 0, 0, 0.3),
                command=base.world.outings_mgr.go_for_outing,  # noqa: F821
                extraArgs=[outing, self._going_for_outing],
                scale=(0.05, 0, 0.05),
            )
        )

    def show_result(
        self, desc, score, cond_score, class_score, day_part_score, selected_effect
    ):
        """Show outing results gui.

        Args:
            desc (str): Result description.
            score (int): Total outing score.
            cond_score (float):
                Score from characters condition.
            class_score (int):
                Score from characters classes.
            day_part_score (int):
                Day part bonus and special skills score.
            selected_effect (dict):
                Effect which requires to choose a target.
        """
        self._clear_temporary_widgets()

        self._desc["text"] = desc

        self._outing_widgets.append(
            DirectLabel(
                parent=self._list,
                text="Outing score:",
                frameSize=(0.6, 0.6, 0.6, 0.6),
                text_scale=(0.045),
            )
        )
        bars = []
        shift = -0.07
        for name, maximum, col, value in (
            ("Character classes fit", 50, (0.46, 0.61, 0.53, 1), class_score),
            ("Characters condition", 20, RUST_COL, cond_score),
            ("Day part and skills", 10, (0.42, 0.42, 0.8, 1), day_part_score),
        ):
            self._outing_widgets.append(
                DirectLabel(
                    parent=self._list,
                    text=name,
                    frameSize=(0.6, 0.6, 0.6, 0.6),
                    text_scale=(0.035),
                    pos=(0, 0, shift),
                )
            )
            shift -= 0.04
            bar = DirectWaitBar(
                parent=self._list,
                frameSize=(-0.17, 0.17, -0.005, 0.005),
                value=0,
                range=maximum,
                barColor=col,
                pos=(0, 0, shift),
            )

            bars.append((bar, value))
            self._outing_widgets.append(bar)

            shift -= 0.08

        base.taskMgr.doMethodLater(  # noqa: F821
            0.04,
            self._animate_bars,
            "animate_outing_bars",
            extraArgs=[bars, score, selected_effect],
            appendTask=True,
        )