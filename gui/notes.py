"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

In-game teaching notes GUI.
"""
import random

from direct.gui.DirectGui import DirectFrame, DirectLabel
from panda3d.core import TransparencyAttrib

from .widgets import GUI_PIC, SILVER_COL

NOTES = (
    """Don't forget to save your
game progress!""",
    # traits
    """Single character can have up
to three different traits""",
    """Characters with strong cohesion
can randomly adopt traits
from each other""",
    # enemy
    """Skinheads activity is at
maximum during evening""",
    """Skinheads activity is at
minimum during morning""",
    """The slower the Train is moving
the easier for enemies to
hit it with throwing weapon""",
    """Some enemies are shooting, some
are slowing you down, some
are deafening your people.
Study their tactics!""",
    """Enemy territory is not
considered on the railways
scheme""",
    """City governments will reward
you with money for destroying
skinheads nearby""",
    # cohesion
    """Increasing team cohesion unlocks
crew skills. These are powerful
temporary effects, which can
help you to survive.""",
    """Raiders and soldiers don't like
each other. It's hard to build
cohesion between them.""",
    """To build stronger cohesion
between particular characters
keep them closer to
each other""",
    """Good way to increase cohesion
between particular characters
is to send them for outing""",
    # outings
    """Different types of outings
are offering different
kinds of trophies""",
    """Outing can turn dangerous, it's
better to send people who are
familiar with each other to
get better chances""",
    """You can not command your people
while they are on outing. You
only can choose right people
to send.""",
    """Some outings can turn very
dangerous, while other are
sure case. Take your risks!""",
    """Press M to see the railways
scheme and choose an
optimal route""",
    """Railway branches always merge
back to the main
railway line""",
    # Train
    """You can turn around in a city.
Consider it, while choosing
an optimal route.""",
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
    """Locomotive active weapons
can only be used
on enemy territory""",
    # characters and classes
    """Women are nice and social, they
reduce stress at any collective""",
    """Women have less health points,
but they are much more
energetic""",
    """People tired faster while in
dark and during fight""",
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
    """If you want to hit an enemy
fortification, soldiers are
your choice""",
    # anarchists
    """Anarchists are companionable,
they build cohesion much
faster than others""",
    """Anarchists get damage factor
x2 from cohesion""",
    """Anarchists are people from
crowd. They value mutual
assistance with those
life has brought them.""",
    # accuracy
    """Shooting accuracy is affected
by lighting, distance,
character class and his
energy level""",
    """Send your character into a Train
rest zone. Rest helps to regain
energy and heal wounds.""",
    # diseases
    """Disease lowers character energy
maximum down to 80 and disables
all the positive traits until
getting well""",
    """Try to reduce diseased character
contacts to avoid spreading
the infection""",
    """Wounded and tired characters are
more vulnerable for diseases""",
    # the Stench
    """The Stench orange clouds are
highly poisonous""",
    # resources
    """Stimulator temporarily disables
the character's negative
traits. It also gives
immunity from deafening.""",
)


class TeachingNotes:
    """GUI that shows teaching notes from time to time."""

    def __init__(self):
        self._note_text = "Press F1 key to open game\ncontrols help"

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
            frameSize=(1, 1, 1, 1),
            text_scale=0.03,
            pos=(0, 0, 0.04),
        )
        self._fr.hide()

    def _hide_note(self, task):
        """Hire the current note and choose the next one."""
        self._fr.hide()
        self._note_text = random.choice(NOTES)
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
        self._note_text = random.choice(NOTES)
        taskMgr.doMethodLater(200, self._show_note, "show_teaching_note")  # noqa: F821

    def start(self):
        """Start showing teaching notes in period."""
        taskMgr.doMethodLater(60, self._show_note, "show_teaching_note")  # noqa: F821

    def stop(self):
        """Stop showing teaching notes."""
        self._fr.hide()
        taskMgr.remove("show_teaching_note")  # noqa: F821
        taskMgr.remove("hide_teaching_note")  # noqa: F821
