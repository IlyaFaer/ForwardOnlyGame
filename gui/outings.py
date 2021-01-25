"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Outings GUI.
"""

from direct.gui.DirectGui import (
    DGG,
    DirectButton,
    DirectFrame,
    DirectLabel,
    DirectWaitBar,
)
from panda3d.core import TransparencyAttrib

from personage.character_data import TRAIT_DESC
from .widgets import RUST_COL, SILVER_COL, CharacterChooser

OUTINGS_ICONS = {
    "looting": "gui/tex/looting.png",
    "enemy camp": "gui/tex/enemy_camp.png",
    "meet": "gui/tex/meet.png",
}


class OutingsInterface:
    """Outing dialogs GUI."""

    def __init__(self):
        self._char_chooser = None
        self._outing_widgets = []
        self._assignees = []
        self._char_buttons = {}

        self._blink_step = 0
        self._upcome_ico = DirectFrame(
            frameSize=(-0.1, 0.1, -0.1, 0.1),
            pos=(0, 0, 0.8),
            frameTexture="gui/tex/looting.png",
        )
        self._upcome_ico.setTransparency(TransparencyAttrib.MAlpha)
        self._upcome_ico.hide()

        self._upcome_text = DirectLabel(
            text="",
            frameSize=(0.4, 0.4, 0.4, 0.4),
            text_scale=0.04,
            text_fg=SILVER_COL,
            text_bg=(0, 0, 0, 0.5),
            pos=(0, 0, 0.65),
        )
        self._upcome_text.hide()

        self._list = DirectFrame(
            frameSize=(-0.73, 0.73, -0.9, 0.9),
            frameTexture="gui/tex/paper1.png",
            state=DGG.NORMAL,
        )
        self._list.setDepthTest(False)
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

    def _assign_for_outing(self, to_send_wid, assignees):
        """Assign the chosen character for the outing.

        Args:
            to_send_wid (direct.gui.DirectLabel.DirectLabel):
                Widget with number of assigned characters.
            assignees (int): Assignees limit.
        """
        char = base.common_ctrl.chosen_char  # noqa: F821
        if char is None or char in self._assignees or len(self._assignees) == assignees:
            return

        self._assignees.append(char)
        self._char_buttons[char.id].setX(0.35)

        to_send_wid["text"] = "People to send ({cur_as}/{max_as}):".format(
            cur_as=str(len(self._assignees)), max_as=str(assignees)
        )

    def _unassign_for_outing(self, to_send_wid, assignees):
        """Exclude the chosen character from the outing.

        Args:
            to_send_wid (direct.gui.DirectLabel.DirectLabel):
                Widget with number of assigned characters.
            assignees (int): Assignees limit.
        """
        char = base.common_ctrl.chosen_char  # noqa: F821
        if char not in self._assignees:
            return

        self._assignees.remove(char)
        self._char_buttons[char.id].setX(-0.35)

        to_send_wid["text"] = "People to send ({cur_as}/{max_as}):".format(
            cur_as=str(len(self._assignees)), max_as=str(assignees)
        )

    def _blink_upcome_icon(self, task):
        """Blink upcoming outing icon to attract attention."""
        self._blink_step += 1
        if self._blink_step in (2, 4, 6):
            self._upcome_ico.show()
            if self._blink_step == 6:
                self._blink_step = 0
                return task.done

            return task.again

        self._upcome_ico.hide()
        return task.again

    def _animate_bars(self, bars, score, selected_effect, recruit_effect, task):
        """Animate filling the bars.

        Args:
            bars (list): Widget to fill.
            score (int): Total outing score.
            selected_effect (dict):
                Effect which requires to choose a target.
            recruit_effect (int): Cost of a possible recruit
        """
        all_filled = True
        for bar in bars:
            bar_wid = bar[0]
            if bar_wid["value"] >= bar[1]:
                continue

            bar_wid["value"] = bar_wid["value"] + bar_wid["range"] / 100
            all_filled = False

        if all_filled:
            shift = -0.07

            for num in range(4):
                self._outing_widgets.append(
                    DirectLabel(
                        parent=self._list,
                        text=str(bars[num][1]) + "/" + str(bars[num][2]),
                        frameSize=(0.6, 0.6, 0.6, 0.6),
                        text_scale=(0.035),
                        pos=(0.168, 0, shift),
                    )
                )
                shift -= 0.12

            self._outing_widgets.append(
                DirectLabel(
                    parent=self._list,
                    text="Total outing score:\n" + str(score) + "/100",
                    frameSize=(0.6, 0.6, 0.6, 0.6),
                    text_scale=(0.045),
                    pos=(0, 0, -0.58),
                )
            )
            self._outing_widgets.append(
                DirectButton(
                    pos=(0, 0, -0.75),
                    text="Done",
                    text_fg=RUST_COL,
                    frameColor=(0, 0, 0, 0.4),
                    command=self._finish_outing,
                    extraArgs=[selected_effect, recruit_effect],
                    scale=(0.05, 0, 0.05),
                    clickSound=base.main_menu.click_snd,  # noqa: F821
                )
            )
            return task.done

        return task.again

    def _dont_hire_unit(self):
        """Finish an outing without recruiting."""
        self.hide_outing()
        base.common_ctrl.deselect()  # noqa: F821

    def _hire_unit(self, char, cost):
        """Hire unit from the outing.

        Args:
            char (personage.character.Character):
                Character to recruit.
            cost (int): Cost of the recruitement.
        """
        if base.dollars < cost:  # noqa: F821
            return

        if not base.train.has_cell():  # noqa: F821
            return

        base.dollars -= cost  # noqa: F821

        base.world.city_gui.write_snd.play()  # noqa: F821
        base.team.chars[char.id] = char  # noqa: F821

        char.prepare()
        base.train.place_recruit(char)  # noqa: F821

        self.hide_outing()
        base.common_ctrl.deselect()  # noqa: F821

    def _finish_outing(self, selected_effect, recruit_effect):
        """Show effect selector if needed and finish the outing.

        Args:
            selected_effect (dict):
                Effect which requires to choose a target.
            recruit_effect (int):
                Cost of a possible recruit.
        """
        self._clear_temporary_widgets()

        if not (selected_effect or recruit_effect):
            self.hide_outing()
            return

        if recruit_effect:
            char = base.team.generate_recruit()  # noqa: F821
            base.char_gui.show_char_info(char)  # noqa: F821

            self._outing_widgets.append(
                DirectLabel(
                    parent=self._list,
                    pos=(0, 0, 0),
                    text="You can recruit {name} for {cost}$".format(
                        name=char.name, cost=recruit_effect
                    ),
                    frameSize=(0.6, 0.6, 0.6, 0.6),
                    text_scale=0.045,
                )
            )
            self._outing_widgets.append(
                DirectButton(
                    pos=(-0.2, 0, -0.75),
                    text="Recruit",
                    text_fg=RUST_COL,
                    frameColor=(0, 0, 0, 0.3),
                    command=self._hire_unit,
                    extraArgs=[char, recruit_effect],
                    scale=(0.05, 0, 0.05),
                )
            )
            self._outing_widgets.append(
                DirectButton(
                    pos=(0.2, 0, -0.75),
                    text="Don't recruit",
                    text_fg=RUST_COL,
                    frameColor=(0, 0, 0, 0.3),
                    command=self._dont_hire_unit,
                    scale=(0.05, 0, 0.05),
                )
            )
            return

        # there are effects to select a target for
        effect_str = ""
        for key, value in selected_effect.items():
            if key == "add_trait":
                effect_str = "Get {trait} trait\n ({desc})".format(
                    trait=value, desc=TRAIT_DESC[value]
                )
            else:
                effect_str += (
                    key + " " + ("+" if value > 0 else "-") + str(value) + "\n"
                )

        self._outing_widgets.append(
            DirectLabel(
                parent=self._list,
                text="""Select one character as a target for the effect:
{effect}""".format(
                    effect=effect_str
                ),
                frameSize=(0.6, 0.6, 0.6, 0.6),
                text_scale=0.045,
            )
        )
        self._char_chooser = CharacterChooser(is_shadowed=True)
        self._char_chooser.prepare(
            self._list, (0, 0, -0.15), base.team.chars  # noqa: F821
        )
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
        """
        Do effects for the selected character
        and finish the outing.

        Args:
            effect (dict): Effect to do.
        """
        self._char_chooser.chosen_item.do_effects(effect)
        self._char_chooser.destroy()
        self.hide_outing()

    def _clear_temporary_widgets(self):
        """Destroy all the one-time widgets."""
        for wid in self._outing_widgets:
            wid.destroy()
        self._outing_widgets.clear()

    def show_upcoming(self, text, icon):
        """Show the upcoming event notification.

        Args:
            text (str): Event text.
            icon (str): Event icon.
        """
        self._upcome_text["text"] = text
        self._upcome_ico["frameTexture"] = icon

        self._upcome_text.show()
        self._upcome_ico.show()

        taskMgr.doMethodLater(  # noqa: F821
            0.3, self._blink_upcome_icon, "blink_outing_icon"
        )

    def show_upcoming_outing(self, type_):
        """Show upcoming outing notification.

        Args:
            type_ (str): Outing type.
        """
        self.show_upcoming(
            '"{}" outing available in 2 miles'.format(type_.capitalize()),
            OUTINGS_ICONS[type_],
        )

    def show_city(self):
        """Show upcoming city notification."""
        self.show_upcoming("Approaching a city", "gui/tex/city.png")

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
        self._upcome_ico.hide()

        self._assignees.clear()

        self._list.hide()
        self._clear_temporary_widgets()

    def start(self, outing):
        """Start the outing scenario.

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
                command=base.common_ctrl.choose_char,  # noqa: F821
                extraArgs=[char.id],
                scale=(0.04, 0, 0.03),
            )
            self._char_buttons[id_] = but
            self._outing_widgets.append(but)

            shift -= 0.04

        to_send = DirectLabel(
            parent=self._list,
            text="People to send (0/{}):".format(outing["assignees"]),
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
                extraArgs=[to_send, outing["assignees"]],
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
                extraArgs=[to_send, outing["assignees"]],
                scale=(0.075, 0, 0.075),
            )
        )
        self._outing_widgets.append(
            DirectButton(
                pos=(-0.15, 0, -0.75),
                text="Don't send",
                text_fg=RUST_COL,
                frameColor=(0, 0, 0, 0.4),
                command=self.hide_outing,  # noqa: F821
                scale=(0.05, 0, 0.05),
                clickSound=base.main_menu.click_snd,  # noqa: F821
            )
        )
        self._outing_widgets.append(
            DirectButton(
                pos=(0.15, 0, -0.75),
                text="Send",
                text_fg=RUST_COL,
                frameColor=(0, 0, 0, 0.4),
                command=base.world.outings_mgr.go_for_outing,  # noqa: F821
                extraArgs=[outing, self._assignees],
                clickSound=base.main_menu.click_snd,  # noqa: F821
                scale=(0.05, 0, 0.05),
            )
        )

    def show_result(
        self,
        desc,
        score,
        cond_score,
        class_score,
        cohesion_score,
        day_part_score,
        selected_effect,
        recruit_effect,
    ):
        """Show outing results GUI.

        Args:
            desc (str): Result description.
            score (int): Total outing score.
            cond_score (float):
                Score from characters condition.
            class_score (int):
                Score from characters classes.
            cohesion_score (float):
                Characters cohesion score.
            day_part_score (int):
                Day part bonus and special skills score.
            selected_effect (dict):
                Effect which requires to choose a target.
            recruit_effect (int):
                Cost of a possible recruit.
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
            ("Character classes fit:", 45, (0.46, 0.61, 0.53, 1), class_score),
            ("Characters condition:", 25, RUST_COL, cond_score),
            ("Characters cohesion:", 20, SILVER_COL, cohesion_score),
            ("Day part and traits:", 10, (0.42, 0.42, 0.8, 1), day_part_score),
        ):
            self._outing_widgets.append(
                DirectLabel(
                    parent=self._list,
                    text=name,
                    frameSize=(0.6, 0.6, 0.6, 0.6),
                    text_scale=(0.035),
                    pos=(-0.08, 0, shift),
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
            bars.append((bar, value, maximum))
            self._outing_widgets.append(bar)

            shift -= 0.08

        taskMgr.doMethodLater(  # noqa: F821
            0.035,
            self._animate_bars,
            "animate_outing_bars",
            extraArgs=[bars, score, selected_effect, recruit_effect],
            appendTask=True,
        )
