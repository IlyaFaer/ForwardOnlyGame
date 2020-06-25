"""Game graphical interface API."""
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectWaitBar

RUST_COL = (0.71, 0.25, 0.05, 1)


class CharacterInterface:
    """Widget with character info."""

    def __init__(self):
        self._char = None  # chosen character

        char_int_fr = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.3, 0.3, -0.075, 0.075),
            pos=(0.3, 0, -1.925),
            frameTexture="gui/tex/metal1.jpg",
        )
        DirectLabel(
            parent=char_int_fr,
            text="Name:",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.24, 0, 0.03),
        )
        self._char_name = DirectLabel(
            parent=char_int_fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=(0.51, 0.54, 0.59, 1),
            pos=(-0.12, 0, 0.028),
        )
        DirectLabel(
            parent=char_int_fr,
            text="Type:",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(0.02, 0, 0.03),
        )
        self._char_type = DirectLabel(
            parent=char_int_fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=(0.51, 0.54, 0.59, 1),
            pos=(0.14, 0, 0.028),
        )
        DirectLabel(
            parent=char_int_fr,
            text="Health",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.24, 0, -0.03),
        )
        self._char_health = DirectWaitBar(
            parent=char_int_fr,
            frameSize=(-0.17, 0.17, -0.002, 0.002),
            value=0,
            barColor=(0.85, 0.2, 0.28, 1),
            pos=(0.05, 0, -0.023),
        )

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

        self._char_name.show()
        self._char_type.show()
        self._char_health.show()

        self._char = character
        base.taskMgr.doMethodLater(  # noqa: F821
            0.5, self._update_char_info, "track_char_info"
        )

    def clear_char_info(self):
        """Clear the interface."""
        self._char_name.hide()
        self._char_type.hide()
        self._char_health.hide()

        base.taskMgr.remove("track_char_info")  # noqa: F821
        self._char = None

    def _update_char_info(self, task):
        """Track character parameters on the interface."""
        if self._char.is_dead:
            self.clear_char_info()
            return task.done

        self._char_health["value"] = self._char.health
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
