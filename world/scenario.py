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
                "effects": (("do_stench_moves_effect", [20]),),
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
                "effects": (("do_charaters_effect", [{"health": -20}, True]),),
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
                "effects": (("do_locomotive_damage", [50]),),
            },
        },
    },
    {  # 2
        "intro": """Taking a closer look at the bunch of people walking through the
meadow, you understand that there are mostly children. Weird!
Asking a couple of teammates to follow you, you get closer
to the crowd, seeing a woman moving towards your party. In
a few words she tells that they are workers and children
from an orphan shelter. Understanding that the Stench moves
fast to the place, and the governors are too busy saving
themselves, adults, who worked there, gathered all the
children and decided to move to Silewer on foot. Looking at
pale and tired children, you silently think that it was really
tough idea. But probably the decision saved their lives...
Complaining about walking for six hours without a stop, the
woman asks you to help them build a field camp. You understand
that it'll take a lot of time, as there are about sixty
children. On the other hand, it doesn't look right to just
leave them here, in the foreign country, tired and
shelterless. Maybe there is some time to help them a little?""",
        "variants": {
            "Help them to build a camp": {
                "desc": """Feeling some qualm inside, you give your people order to help
the children. Losing time is not okay... Still, twenty minutes
later, seeing your people and children smiling while setting
up big tents, igniting bonfires and boiling pottage in big
cauldrons, you forget these heavy thoughts. This small break
will be useful for the crew as well... It takes you about two
hours to finish preparing the camp. Getting a lot of thanks
from the children and their teachers, you gather again on the
Adjutant. Everyone seems to be enlivened, still, the road calls.
Giving an order to start engine, you approach a couple of your
teammates, who are looking some kind of an article on a
martphone. "Hey, Captain, you need to see this! Some of those
children visited kinda research center a month ago and took
an interview there. The woman speaks about interesting things."
Telling them that you're going to take a closer look at the
article later, you go to the deckhouse to plan the route,
considering the recent delay.

The Stench frontier came 20 miles closer to you""",
                "effects": (
                    ("do_build_camp_effect", []),
                    ("do_stench_moves_effect", [20]),
                ),
            },
            "Agree in words, but steal from them": {
                "desc": """Calling the crew to speak aside, you're trying to convince
them to use an ability to replenish resources. "The situation
is getting tougher day after day, it's becoming about us or
them." Your teammates lower their eyes. Everybody know that
sooner or later it'll come to this, still, no one wants to take
responsibility. "It's hard to admit, but those children are not
going to make it. They are not fighters nor survivors. The first
meet with skinheads, and..." The crew continue to keep silence,
bit you feel them accepting the situation, so you're giving an
order: "Build the camp hastily, and take useful stuff in case you
see it!" Your teammates, avoiding to look at each other, go out
of the deckhouse... About an hour and half passed, and all of
your people gather together on the Adjutant. They still doesn't
want to look at each other, but they put an aid kit and a energy
drinks on the table. "Okay, let's move on!" - you command.

You're getting 1 medicine and 1 stimulator
Soon people of Silewer will know that you've stolen from kids.
This will bring more fighters under the skinhead banners.""",
                "effects": (
                    ("do_enemy_inc_effect", []),
                    ("do_plus_resource", ["medicine_boxes", 1]),
                    ("do_plus_resource", ["stimulators", 1]),
                ),
            },
            "Don't help them and continue the road": {
                "desc": """You go back to the deckhouse and negotiate with the crew. It
appears most of them would like to stop and help orphans, but
all understand that it'll take at least several hours. Clouds
of the Stench will not let you wait, so it makes sense to move
faster. People know nothing about the cataclysm behavior, in
theory it can accelerate or appear somewhere far from the
supposed source in Germany. Overthinking it again, again and
again, you decide to ignore the teachers plea. The crew don't
like the decision very much, but everyone mind the situation.
A hard silence forms in the air. No one wants to go there and
say those orphans that you're going to leave. "So, what?" - you
ask quietly. - "Should we continue the road without the last
word? What's the point in it?" Your teammates lower their
eyes and nod their heads. Taking this as an answer, you give
a command to go...

Some time later you see a paper on your table. Running through
it with your eyes, you find out it's an interview log. Those
orphans visited kind of a research center some time ago and
took an interview from one of the scientists. Most likely one
of your people got it from the children somehow. No thoughts
why it was left on your table, but it should be read.""",
                "effects": (("do_no_effect", []),),
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
        for effect in consequences["effects"]:
            getattr(self, effect[0])(*effect[1])

        self._done_but.show()

    def do_build_camp_effect(self):
        """Do effects for building a camp for orphans choice."""
        base.helped_children = True  # noqa: F821

    def do_plus_resource(self, name, value):
        """Change the given resource amount.

        Args:
            name (str): Resource name.
            value (int): Amount delta.
        """
        base.plus_resource(name, value)  # noqa: F821

    def do_enemy_inc_effect(self):
        """Make enemy stronger effect."""
        base.world.enemy.score += 3  # noqa: F821

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

    def do_no_effect(self):
        """No choice consequences method."""
        pass

    def hide_chapter(self):
        """Hide the scenario GUI."""
        self._list.hide()

    def do_stench_moves_effect(self, steps):
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

        if self.current_chapter <= 1:
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
