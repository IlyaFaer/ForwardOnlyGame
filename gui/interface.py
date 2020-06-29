"""Game graphical interface API."""
from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel, DirectWaitBar
from direct.gui.OnscreenText import OnscreenText

RUST_COL = (0.71, 0.25, 0.05, 1)


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
            frameTexture="gui/tex/metal1.jpg",
        )
        DirectLabel(
            parent=char_int_fr,
            text="Name:",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.24, 0, 0.04),
        )
        self._char_name = DirectLabel(
            parent=char_int_fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=(0.51, 0.54, 0.59, 1),
            pos=(-0.12, 0, 0.038),
        )
        DirectLabel(
            parent=char_int_fr,
            text="Type:",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(0.02, 0, 0.04),
        )
        self._char_type = DirectLabel(
            parent=char_int_fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=(0.51, 0.54, 0.59, 1),
            pos=(0.14, 0, 0.038),
        )
        DirectLabel(
            parent=char_int_fr,
            text="Health",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.24, 0, -0.015),
        )
        self._char_health = DirectWaitBar(
            parent=char_int_fr,
            frameSize=(-0.17, 0.17, -0.002, 0.002),
            value=0,
            barColor=(0.85, 0.2, 0.28, 1),
            pos=(0.05, 0, -0.008),
        )
        DirectLabel(
            parent=char_int_fr,
            text="Energy",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.236, 0, -0.06),
        )
        self._char_energy = DirectWaitBar(
            parent=char_int_fr,
            frameSize=(-0.17, 0.17, -0.002, 0.002),
            value=0,
            barColor=(0.46, 0.61, 0.53, 1),
            pos=(0.05, 0, -0.053),
        )
        self._tip = OnscreenText(
            parent=base.render2d,  # noqa: F821
            text="",
            scale=(0.021, 0.027),
            fg=(0.51, 0.54, 0.59, 1),
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
        self._char_type["text"] = character.type
        self._char_health["value"] = character.health
        self._char_energy["value"] = character.energy

        self._char_name.show()
        self._char_type.show()
        self._char_health.show()
        self._char_energy.show()

        self._char = character
        base.taskMgr.doMethodLater(  # noqa: F821
            0.5, self._update_char_info, "track_char_info"
        )

    def clear_char_info(self):
        """Clear the interface."""
        self._char_name.hide()
        self._char_type.hide()
        self._char_health.hide()
        self._char_energy.hide()

        base.taskMgr.remove("track_char_info")  # noqa: F821
        self._char = None

        for but in self._rest_buttons.values():
            but.destroy()

        self._rest_list_active = False

    def show_pers_tip(self, pers, is_enemy=False):
        """Show personage tooltip.

        If mouse points on a character, his/her name will
        be shown. If on enemy unit, his/her fraction and
        type will be shown.

        Args:
            pers (Union[
                    personage.character.Character,
                    personage.enemy.Enemy
                ]):
                Pointed character or enemy unit object.
            is_enemy (bool): True, if enemy pointed, False otherwise.
        """
        self._tip.setText(pers.name + (" - " + pers.type if is_enemy else ""))
        self._tip.setX(base.mouseWatcherNode.getMouseX())  # noqa: F821
        self._tip.setY(base.mouseWatcherNode.getMouseY())  # noqa: F821
        self._tip.show()

    def hide_pers_tip(self):
        """Hide personage tooltip."""
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
                text_fg=(0.51, 0.54, 0.59, 1),
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
        train_int_fr = DirectFrame(
            parent=base.a2dBottomRight,  # noqa: F821
            frameSize=(-0.03, 0.03, -0.3, 0.3),
            pos=(-0.03, 0, 0.3),
            frameTexture="gui/tex/metal1.jpg",
        )
        DirectFrame(
            parent=train_int_fr,  # noqa: F821
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            pos=(0, 0, 0.265),
            frameTexture="gui/tex/icon_train.png",
        )
        self._train_damnability = DirectWaitBar(
            parent=train_int_fr,
            frameSize=(-0.25, 0.25, -0.002, 0.002),
            range=1000,
            value=1000,
            barColor=(0.42, 0.42, 0.8, 1),
            pos=(0, 0, -0.023),
        )
        self._train_damnability.setR(-90)

    def update_indicators(self, **params):
        """Update Train interface with given parameters.

        Args:
            params (dict): New parameters values.
        """
        if "damnability" in params.keys():
            self._train_damnability["value"] = params["damnability"]
