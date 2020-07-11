"""Game graphical interface API."""
from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel, DirectWaitBar
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TransparencyAttrib

RUST_COL = (0.71, 0.25, 0.05, 1)
SILVER_COL = (0.51, 0.54, 0.59, 1)


class CharacterInterface:
    """Widget with character info."""

    def __init__(self):
        self._char = None  # chosen character
        self._rest_buttons = {}
        self._rest_list_active = False

        char_int_fr = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.3, 0.3, -0.1, 0.1),
            pos=(0.3, 0, -1.9),
            frameTexture="gui/tex/metal1.png",
        )
        char_int_fr.setTransparency(TransparencyAttrib.MAlpha)

        DirectLabel(
            parent=char_int_fr,
            text="Name:",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.23, 0, 0.04),
        )
        self._char_name = DirectLabel(
            parent=char_int_fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=SILVER_COL,
            pos=(-0.11, 0, 0.038),
        )
        DirectLabel(
            parent=char_int_fr,
            text="Type:",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(0.03, 0, 0.04),
        )
        self._char_class = DirectLabel(
            parent=char_int_fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=SILVER_COL,
            pos=(0.15, 0, 0.038),
        )
        DirectLabel(
            parent=char_int_fr,
            text="Health",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.23, 0, -0.015),
        )
        self._char_health = DirectWaitBar(
            parent=char_int_fr,
            frameSize=(-0.17, 0.17, -0.002, 0.002),
            value=0,
            barColor=(0.85, 0.2, 0.28, 1),
            pos=(0.06, 0, -0.008),
        )
        DirectLabel(
            parent=char_int_fr,
            text="Energy",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.226, 0, -0.06),
        )
        self._char_energy = DirectWaitBar(
            parent=char_int_fr,
            frameSize=(-0.17, 0.17, -0.002, 0.002),
            value=0,
            barColor=(0.46, 0.61, 0.53, 1),
            pos=(0.06, 0, -0.053),
        )
        self._tip = OnscreenText(
            parent=base.render2d,  # noqa: F821
            text="",
            scale=(0.021, 0.027),
            fg=SILVER_COL,
            bg=(0, 0, 0, 0.4),
        )
        self._tip.hide()

        self.clear_char_info()

    def show_char_info(self, character):
        """Show character parameters.

        Args:
            character (personage.character.Character):
                Chosen character object.
        """
        self._char_name["text"] = character.name
        self._char_class["text"] = character.class_.capitalize()

        self._char_health["range"] = character.class_data["health"]
        self._char_health["value"] = character.health
        self._char_energy["value"] = character.energy

        self._char_name.show()
        self._char_class.show()
        self._char_health.show()
        self._char_energy.show()

        self._char = character
        base.taskMgr.doMethodLater(  # noqa: F821
            0.5, self._update_char_info, "track_char_info"
        )

    def clear_char_info(self):
        """Clear the interface."""
        self._char_name.hide()
        self._char_class.hide()
        self._char_health.hide()
        self._char_energy.hide()

        base.taskMgr.remove("track_char_info")  # noqa: F821
        self._char = None

        for but in self._rest_buttons.values():
            but.destroy()

        self._rest_list_active = False

    def show_unit_tip(self, unit):
        """Show personage tooltip.

        Args:
            unit (Union[
                    personage.character.Character,
                    personage.enemy.EnemyUnit
                ]):
                Pointed unit object.
        """
        self._tip.setText(unit.tooltip)
        self._tip.setX(base.mouseWatcherNode.getMouseX())  # noqa: F821
        self._tip.setY(base.mouseWatcherNode.getMouseY())  # noqa: F821
        self._tip.show()

    def hide_unit_tip(self):
        """Hide unit tooltip."""
        self._tip.hide()

    def show_resting_chars(self, part):
        """Show a list of the characters resting in this part.

        Args:
            part (Train.RestPart): Rest part of Train.
        """
        if self._rest_list_active:
            return

        self._rest_list_active = True

        x = base.mouseWatcherNode.getMouseX()  # noqa: F821
        z = base.mouseWatcherNode.getMouseY()  # noqa: F821

        self._rest_buttons["title"] = DirectButton(
            pos=(x, 0, z),
            text="Resting:",
            text_fg=RUST_COL,
            frameColor=(0, 0, 0, 0.6),
            scale=(0.04, 0, 0.03),
        )
        shift = -0.039
        for char in part.chars:
            self._rest_buttons[char.id] = DirectButton(
                pos=(x, 0, z + shift),
                text=char.name,
                text_fg=SILVER_COL,
                frameColor=(0, 0, 0, 0.6),
                command=base.common_ctrl.choose_resting_char,  # noqa: F821
                extraArgs=[char.id],
                scale=(0.04, 0, 0.03),
            )
            shift -= 0.033

    def destroy_char_button(self, char_id):
        """Hide the button related to the given character id.

        Args:
            char_id (str): Character id.
        """
        if char_id in self._rest_buttons.keys():
            self._rest_buttons[char_id].destroy()
            self._rest_buttons.pop(char_id)

    def _update_char_info(self, task):
        """Track character parameters on the interface."""
        if self._char.is_dead:
            self.clear_char_info()
            return task.done

        self._char_health["value"] = self._char.health
        self._char_energy["value"] = self._char.energy
        return task.again


class TrainInterface:
    """Train parameters interface."""

    def __init__(self):
        frame = DirectFrame(
            parent=base.a2dBottomRight,  # noqa: F821
            frameSize=(-0.03, 0.03, -0.3, 0.3),
            pos=(-0.03, 0, 0.3),
            frameTexture="gui/tex/metal1.png",
        )
        frame.setTransparency(TransparencyAttrib.MAlpha)
        DirectFrame(
            parent=frame,  # noqa: F821
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            pos=(0, 0, 0.265),
            frameTexture="gui/tex/icon_train.png",
        )
        self._damnability = DirectWaitBar(
            parent=frame,
            frameSize=(-0.25, 0.25, -0.002, 0.002),
            range=1000,
            value=1000,
            barColor=(0.42, 0.42, 0.8, 1),
            pos=(0, 0, -0.023),
        )
        self._damnability.setR(-90)

    def update_indicators(self, **params):
        """Update Train interface with the given parameters.

        Args:
            params (dict): New parameters values.
        """
        if "damnability" in params.keys():
            self._damnability["value"] = params["damnability"]


class ResourcesInterface:
    """Interface to show the current amount of player resources."""

    def __init__(self):
        frame = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.075, 0.075, -0.025, 0.025),
            pos=(0.075, 0, -0.025),
            frameTexture="gui/tex/metal1.png",
        )
        frame.setTransparency(TransparencyAttrib.MAlpha)
        DirectFrame(
            parent=frame,  # noqa: F821
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            pos=(-0.05, 0, 0),
            frameTexture="gui/tex/icon_dollar.png",
        )
        self._dollars = DirectLabel(
            parent=frame,
            text="300",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.035, 0.035),
            text_fg=RUST_COL,
            pos=(0.01, 0, -0.008),
        )


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

    def _assign_for_outing(self):
        """Assign the chosen character for the outing."""
        char = base.common_ctrl.chosen_char  # noqa: F821
        if char in self._going_for_outing:
            return

        self._going_for_outing.append(char)
        self._char_buttons[char.id].setX(0.35)

    def _unassign_for_outing(self):
        """Exclude the chosen character from the outing."""
        char = base.common_ctrl.chosen_char  # noqa: F821
        if char not in self._going_for_outing:
            return

        self._going_for_outing.remove(char)
        self._char_buttons[char.id].setX(-0.35)

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

        self._list.hide()
        for wid in self._outing_widgets:
            wid.destroy()

        self._outing_widgets.clear()

    def start(self, outing):
        """Start outing scenario.

        Draw an interface with outing description.

        Args:
            outing (dict): Outing description.
        """
        self.hide_outing()
        self._list.show()

        self._outing_widgets.append(
            DirectLabel(
                parent=self._list,
                text=outing["name"],
                frameSize=(0.4, 0.4, 0.4, 0.4),
                text_scale=(0.05),
                pos=(-0.4, 0, 0.7),
            )
        )
        self._outing_widgets.append(
            DirectLabel(
                parent=self._list,
                text=outing["type"],
                frameSize=(0.4, 0.4, 0.4, 0.4),
                text_scale=(0.035),
                pos=(-0.13, 0, 0.699),
            )
        )
        self._outing_widgets.append(
            DirectLabel(
                parent=self._list,
                text=outing["desc"],
                frameSize=(0.6, 0.6, 0.6, 0.6),
                text_scale=(0.04),
                pos=(0, 0, 0.4),
            )
        )
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

        self._outing_widgets.append(
            DirectLabel(
                parent=self._list,
                text="People to send:",
                frameSize=(0.6, 0.6, 0.6, 0.6),
                text_scale=(0.035),
                pos=(0.35, 0, 0),
            )
        )
        self._outing_widgets.append(
            DirectButton(
                pos=(0, 0, -0.15),
                text=">",
                text_fg=SILVER_COL,
                frameColor=(0, 0, 0, 0.3),
                command=self._assign_for_outing,  # noqa: F821
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
                extraArgs=[outing],
                scale=(0.05, 0, 0.05),
            )
        )
