"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

In-game teaching notes GUI.
"""
import random

from direct.gui.DirectGui import DirectFrame, DirectLabel
from panda3d.core import TransparencyAttrib

from .widgets import GUI_PIC, SILVER_COL


class TeachingNotes:
    """GUI that shows teaching notes from time to time."""

    def __init__(self):
        self._note_text = base.labels.DEFAULT_NOTE  # noqa: F821

        self._fr = DirectFrame(
            parent=base.a2dBottomRight,  # noqa: F821
            frameSize=(-0.25, 0.25, -0.07, 0.07),
            pos=(-0.25, 0, 0.65),
            frameTexture=GUI_PIC + "metal1.png",
        )
        self._fr.setTransparency(TransparencyAttrib.MAlpha)

        self._note = DirectLabel(
            parent=self._fr,
            text="",
            text_fg=SILVER_COL,
            text_font=base.main_font,  # noqa: F821
            frameSize=(1, 1, 1, 1),
            text_scale=0.028,
            pos=(0, 0, 0.04),
        )
        self._fr.hide()

    def _hide_note(self, task):
        """Hide the current note and choose the next one."""
        self._fr.hide()
        self._note_text = random.choice(base.labels.NOTES)  # noqa: F821
        return task.done

    def _show_note(self, task):
        """Show the next teaching note."""
        self._note["text"] = self._note_text
        self._fr.show()

        taskMgr.doMethodLater(10, self._hide_note, "hide_teaching_note")  # noqa: F821
        task.delayTime = 150
        return task.again

    def resume(self):
        """Resume showing teaching notes."""
        self._note_text = random.choice(base.labels.NOTES)  # noqa: F821
        taskMgr.doMethodLater(200, self._show_note, "show_teaching_note")  # noqa: F821

    def start(self):
        """Start showing teaching notes in period."""
        taskMgr.doMethodLater(60, self._show_note, "show_teaching_note")  # noqa: F821

    def stop(self):
        """Stop showing teaching notes."""
        self._fr.hide()
        taskMgr.remove("show_teaching_note")  # noqa: F821
        taskMgr.remove("hide_teaching_note")  # noqa: F821
