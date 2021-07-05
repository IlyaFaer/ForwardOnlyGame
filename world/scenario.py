"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The main game scenario.
"""
import random

from direct.gui.DirectGui import (
    DGG,
    DirectButton,
    DirectFrame,
    DirectLabel,
)
from panda3d.core import TransparencyAttrib

from gui.widgets import RUST_COL

SCENARIO = [
    {  # 1
        "intro": """Kenneth - the Adjutant mechanic approaches your table and sits to
the right of you. "Captain, we probably have a trouble." You're
uppering a spoon full of dry porridge to your mouth: "Yeah?!"
"Yeah. Come see me after you snaсk is over." He gets up and
leaves the deckhouse. Finishing the awfully tasteless portion,
you're walking to the lower level of the Adjutant. Before you
pronounce the first word, Kenneth rises his finger up, asking
you to stay silent and listen. You're concentrating on the noises...
"Hear that?" - the mechanic points to the left side of the room,
and you understand what he's trying to say. Some metal screeching
can be heard from the wall. "That's an axle box, something's
acting up." - Kenneth explains silently. - "We need to check
it, and it'll take some time." You're trying to remember how far
was the Stench frontier, when you last heard about it. "Our
options?" Looking at you, Kenneth calculates something in his
mind and then tells: "We need five hours long stop to deal with
the axle box." It's much. "Other options?" The mechanic seems
to be not very pleasant to say it, but he does: "We can try
to do it on move. But that's dangerous, and will required two
men - me here and someone on the other side of the locomotive.
The second guy can get injured I warn you. Anyway I think not
dealing with it can cause us troubles as well. Your call, Captain." """,
        "variants": {
            "Stop the Adjutant for a revision": {
                "desc": """You're making a decision to stop for, as planned, five hours. The
crew starts to work without delays. Dismantling the axle box,
you see that a couple of details do not fit each other, and
rub hard. Your people start to deal with the problem, leaded
by Kenneth. Seeing that they are okay to fix the trouble
without you, you return to the deckhouse and turn on radio.
"The Stench clouds were noticed in Stuttgart! On the south
of the city several people already found dead, others leaving
their homes, trying to get out of the city. Stay on this
station, we'll keep you posted!" Stuttgart. Looks like the
Stench frontier moves from south-east direction. It should
be considered while planning the further route... Four hours
passed, and the crew reports you that the axle box is good
to go. Calling everyone back on board, you're commanding to
continue the road in the same moment. Four hours is not five,
but it's still long, very long. Better keep your pace high now.

The Stench frontier came 20 miles closer to you,
but the Adjutant is in a good shape for now.""",
                "effect": ("make_stench_steps", [20]),
            },
            "Try to deal with the axle box on move": {
                "desc": """You're giving Kenneth command to choose one of your team mates
and try to deal with the axle box on move. You see that the
mechanic doesn't like your decision, but he still accepts
the order, promising to think who fits the task better.
You're returning back to the deckhouse, and some time later
see Kenneth taking one of the fighters with him to the
lower level of the Adjutant. For several long hours they
slip out of your radars... Exiting on the fresh air, you
incline above the railings and see a blood spot on one of
the wheels, blinking on every turnover. Without delays you
go to find the mechanic. Kenneth, seeing you concerned,
uppers his hands in the same moment: "It's okay, it's okay!
Small wound, but the axle box is fine now. Nothing serious!"
Making a deep breath, you nod your head, trying to calm
down. You knew the risks from the beginning, but it's still
about your people safety. It's good that the helper didn't
get serious wounds. You better find him or her later to
say your thanks.

One of your fighters getting -20 health""",
                "effect": ("do_charaters_effect", [{"health": -20}, True]),
            },
            "Ignore the problem": {
                "desc": """It's better not to stop for such long period. Asking Kenneth
to wait for some time, you return back to the deckhouse. It
is better to double check. The Stench frontier is far back
for now, but three hours later... Looking at the map, you
understand that you can't afford even three hours. Too risky,
in these days it's better to keep some spare time. Returning
back to Kenneth, you tell him to ignore the noises for now.
He doesn't like your decision very much, you can see it on
his face, but your common past outweighs everything. You
helped him and his family more times than you both can count,
so he's not going to argue with you...

Some time later you'll understand that the problem was not
one of those to be ignored. The axle box will be damaged.

The Adjutant loses 50 Durability""",
                "effect": ("do_locomotive_damage", [50]),
            },
        },
    },
]


class Scenario:
    """The game scenario orchestrator.

    Tracks on which part of the scenario the player is, controls
    the next scenario steps and performs choice consequences effects.

    One scenario chapter includes a situation in which the player
    has to make a decision. Decision will have consequences, positive
    or negative, but in any case the player will become one step
    closer to figuring out the way to survive the Stench. After
    every chapter the player will also get a note written in a
    diary fashion. The note will give the player more info about
    the Stench, Captain, the Adjutant and how the cataclysm
    started to destroy the World.
    """

    def __init__(self):
        self.current_chapter = -1

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
            text_scale=0.05,
            pos=(-0.4, 0, 0.7),
        )
        self._type = DirectLabel(
            parent=self._list,
            text="Scenario",
            frameSize=(0.4, 0.4, 0.4, 0.4),
            text_scale=0.035,
            pos=(-0.13, 0, 0.699),
        )
        self._desc = DirectLabel(
            parent=self._list,
            text="",
            frameSize=(0.6, 0.6, 0.6, 0.6),
            text_scale=0.04,
            pos=(0, 0, 0.55),
        )

        self._buts = []
        z_coor = -0.5
        for _ in range(3):
            self._buts.append(
                DirectButton(
                    parent=self._list,
                    text="Text",
                    text_fg=RUST_COL,
                    text_shadow=(0, 0, 0, 1),
                    frameColor=(0, 0, 0, 0),
                    frameSize=(-9, 9, -0.3, 0.7),
                    scale=(0.05, 0, 0.05),
                    clickSound=base.main_menu.click_snd,  # noqa: F821
                    pos=(0, 0, z_coor),
                )
            )
            z_coor -= 0.1

        self._done_but = DirectButton(
            parent=self._list,
            text="Done",
            text_fg=RUST_COL,
            text_shadow=(0, 0, 0, 1),
            frameColor=(0, 0, 0, 0),
            frameSize=(-9, 9, -0.3, 0.7),
            scale=(0.05, 0, 0.05),
            clickSound=base.main_menu.click_snd,  # noqa: F821
            pos=(0, 0, -0.8),
            command=self.hide_chapter,
        )

    def _choose_variant(self, var):
        """Process the player's choice and do consequences.

        Args:
            var (str): Variant id.
        """
        consequences = SCENARIO[self.current_chapter]["variants"][var]
        for but in self._buts:
            but.hide()

        self._desc["text"] = consequences["desc"]
        taskMgr.doMethodLater(  # noqa: F821
            0.05,
            getattr(self, consequences["effect"][0]),
            "do_choice_consequences",
            extraArgs=consequences["effect"][1],
        )
        self._done_but.show()

    def do_character_effect(self, char, effect):
        """Do choice consequences effect to the given character.

        Args:
            char (units.crew.character.Character):
                The character to do effect to.
            effect (dict): The effect description.
        """
        for key, value in effect.items():
            setattr(char, key, getattr(char, key) + value)

    def do_charaters_effect(self, effect, to_one=False):
        """Do choice consequences effects to the crew.

        Args:
            effect (dict): Effect description.
            to_one (bool): Effect targets only one random character.
        """
        if to_one:
            self.do_character_effect(
                random.choice(list(base.team.chars.values())), effect  # noqa: F821
            )

    def do_locomotive_damage(self, damage):
        """Do some damage to the Adjutant.

        Args:
            damage (int): Amount of damage to do.
        """
        base.train.get_damage(damage)  # noqa: F821

    def hide_chapter(self):
        """Hide the scenario GUI."""
        self._list.hide()

    def make_stench_steps(self, steps):
        """Move the Stench frontier several miles deeper into the Silewer.

        Args:
            steps (int): Number of miles to cover with the Stench.
        """
        for _ in range(steps):
            base.world.make_stench_step()  # noqa: F821

    def start_chapter(self, task):
        """Start a new scenario chapter."""
        self.current_chapter += 1

        base.train.ctrl.set_controls(base.train)  # noqa: F821
        base.camera_ctrl.enable_ctrl_keys()  # noqa: F821

        base.world.outings_mgr.hide_outing()  # noqa: F821
        base.traits_gui.hide()  # noqa: F821

        if self.current_chapter == 0:
            self.show_chapter_situation()  # noqa: F821

        return task.done

    def show_chapter_situation(self):
        """Show the situation description and the possible variants."""
        self._done_but.hide()
        self._name["text"] = "Chapter " + str(self.current_chapter + 1)
        self._desc["text"] = SCENARIO[self.current_chapter]["intro"]

        for index, var in enumerate(SCENARIO[self.current_chapter]["variants"]):
            self._buts[index]["text"] = var
            self._buts[index]["extraArgs"] = [var]
            self._buts[index]["command"] = self._choose_variant
            self._buts[index].show()

        self._list.show()
