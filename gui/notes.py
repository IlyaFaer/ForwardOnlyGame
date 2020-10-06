"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Teaching notes GUI.
"""
import random

from direct.gui.DirectGui import DirectFrame, DirectLabel
from panda3d.core import TransparencyAttrib

from .train import ICON_PATH, SILVER_COL

NOTES = (
    # enemy
    """Skinheads activity is at
maximum during evening""",
    """Skinheads activity is at
minimum during morning""",
    # cohesion
    """Increasing team cohesion unlocks
team skills. These are powerful
temporary effects, which can
help you to survive.""",
    """Raiders and soldiers don't like
each other. It's hard to build
cohesion between them.""",
    """To build stronger cohesion
between particular characters
keep them closer to
each other""",
    # outings
    """On "Looting" outings you can find
resources to repair Train, heal
characters, regain energy""",
    """Outing can turn dangerous, it's
better to send people who are
familiar with each other to
get better chances""",
    """You can not command your people
while they are on outing. You
only can choose right people
to send.""",
    # Train
    """It's reckless to stop while
on enemy territory""",
    """Switching on lights helps to save
characters energy and to increase
their accuracy, but also attracts
enemy attention""",
    """Deteriorated rusty rails
can damage your Train wheels.
Slow down when you hear a
metal creak.""",
    # characters and classes
    """Women are nice and social, they
reduce stress at any collective""",
    """Women have less health points,
but they are much more
energetic""",
    # raiders
    """Raider's life is mostly about
looting. They know how to find
useful things.""",
    """Raiders are good shooters at
short distance""",
    """Raiders are spending energy
faster, but they also rest
faster than others""",
    # soldiers
    """Soldiers are good shooters at
medium distance""",
    # accuracy
    """Shooting accuracy is affected
by lighting, distance,
character class and his
energy level""",
    """Send your character into a Train
rest zone. Rest helps to regain
energy and heal wounds.""",
)


class TeachingNotes:
    """GUI that shows teaching notes from time to time."""

    def __init__(self):
        self._note_text = "Press F1 key to open game\ncontrols help"

        self._notes_fr = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.25, 0.25, -0.07, 0.07),
            pos=(0.25, 0, -0.2),
            frameTexture=ICON_PATH + "metal1.png",
        )
        self._notes_fr.setTransparency(TransparencyAttrib.MAlpha)

        self._note = DirectLabel(
            parent=self._notes_fr,
            text="",
            text_fg=SILVER_COL,
            frameSize=(1, 1, 1, 1),
            text_scale=(0.03),
            pos=(0, 0, 0.04),
        )
        self._notes_fr.hide()

        base.taskMgr.doMethodLater(  # noqa: F821
            20, self._show_note, "show_teaching_note"
        )

    def _show_note(self, task):
        """Shot next teaching note."""
        self._note["text"] = self._note_text
        self._notes_fr.show()

        base.taskMgr.doMethodLater(  # noqa: F821
            10, self._hide_note, "hide_teaching_note"
        )
        task.delayTime = 180
        return task.again

    def _hide_note(self, task):
        """Hire the current note and choose the next one."""
        self._notes_fr.hide()
        self._note_text = random.choice(NOTES)
        return task.done

    def stop(self):
        """Stop showing teaching notes."""
        self._notes_fr.hide()
        base.taskMgr.remove("show_teaching_note")  # noqa: F821
        base.taskMgr.remove("hide_teaching_note")  # noqa: F821

    def resume(self):
        """Resume showing teaching notes."""
        self._note_text = random.choice(NOTES)
        base.taskMgr.doMethodLater(  # noqa: F821
            180, self._show_note, "show_teaching_note"
        )
