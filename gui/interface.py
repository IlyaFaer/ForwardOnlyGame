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
        self.char_name = DirectLabel(
            parent=char_int_fr,
            text="Char",
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
            pos=(0, 0, 0.03),
        )
        self.char_type = DirectLabel(
            parent=char_int_fr,
            text="Char_type",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=(0.51, 0.54, 0.59, 1),
            pos=(0.15, 0, 0.028),
        )
        DirectLabel(
            parent=char_int_fr,
            text="Health",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.24, 0, -0.03),
        )
        self.char_health = DirectWaitBar(
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
        self.char_name["text"] = character.name
        self.char_type["text"] = character.type
        self.char_health["value"] = character.health

        self.char_name.show()
        self.char_type.show()
        self.char_health.show()

        self._char = character
        base.taskMgr.doMethodLater(  # noqa: F821
            0.5, self._update_char_info, "track_char_info"
        )

    def clear_char_info(self):
        """Clear the interface."""
        self.char_name.hide()
        self.char_type.hide()
        self.char_health.hide()

        base.taskMgr.remove("track_char_info")  # noqa: F821
        self._char = None

    def _update_char_info(self, task):
        """Track character parameters on the interface."""
        if self._char.is_dead:
            self.clear_char_info()
            return task.done

        self.char_health["value"] = self._char.health
        return task.again
