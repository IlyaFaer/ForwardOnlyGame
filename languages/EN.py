"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The game text labels wirrten in English language.
"""

MAIN_MENU = (
    "New game",
    "Load game",
    "Options",
    "Exit",
    (
        "This is a game alpha build. It's not finally balanced and some"
        " features are in development yet."
        "\nThus, it's mostly a conceptual release, to demonstrate you the main "
        "game princips. Enjoy your play!"
    ),
    "Choose your crew",
    "Soldiers",
    "Raiders",
    "Anarchists",
    "Crew description",
    "Start",  # 10
    (
        "Soldiers are people of a tough discipline. They are good "
        "shooters at medium\ndistance and good fortification assaulters. "
        "Their tactic is based mostly on a good\ndefence and locomotive "
        "upgrading, which can make the Train a real fortress.\n\n"
        "You'll start with 3 soldier males."
    ),
    (
        "Raiders are accustomed to difficulties and can recover from "
        "anything. They are\ngood fighters at short distance and they "
        "know how to find resources. Their tactic\nis based on getting "
        "and using expendable resources and fast recovering.\n\n"
        "You'll start with 2 male and 1 female raiders."
    ),
    (
        "Anarchists are the force of nature! They build cohesion "
        "faster than others and\nalways value those, who life brought "
        "them with. The tactic is based on\ngetting more people, "
        "tweaking their traits and using team skills.\n\n"
        "You'll start with 2 male and 1 female anarchists."
    ),
    "Main menu",
    "Save game",
    "(blocked during fight)",
    "(blocked near a city)",
    "(blocked near a fork)",
    "(blocked on game over)",
    "(blocked on game start)",  # 20
    "Resume",
    "Resolution:",
    "Tutorial:",
    "Language:",
    "Save and restart",
    "Loading...",
    "Take command",
)

KEYS_INFO = u"""
Game controls:

Mouse Left Button - choose character/rest zone
Mouse Right Button - move character/set target
R - show the character's cohesion with others

W - hold to accelerate
S - hold to slow down
F - toggle flood lights
M - see railways scheme

Camera:
\u2190\u2191\u2193\u2192 or push screen edge with mouse - move
Alt + \u2190\u2191\u2193\u2192 or hold mouse wheel - rotate
"+", "-" or scroll mouse wheel - zoom
C - toggle centered view
"""

RESOURCES = (
    "Expendable resources:",
    "Medicine",
    "Cure sick/wounded character",
    "Smoke filter",
    "Reduce attack chance (5 min)",
    "Stimulator",
    "Disable negative traits (5 min)",
)

CHARACTERS = ("Name:", "Class:", "Health", "Energy")
CITY = (
    "Services",
    "Party",
    "Train",
    "Exit city",
    "Turn around and exit",
    "Locomotive",
    "Repair",
    "Upgrades",
    "Purchase",
    "Crew",
    "Recruits",  # 10
    "Resources",
    "Leave unit",
    "Hire unit",
    "Sell",
    "Buy",
)

NOTES = (
    # controls
    """Don't forget to save your
game progress!""",
    """Choose a character and press
right mouse button on
another one to exchange
their positions""",
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
    """Governments of Silewer cities
will reward you with
money for destroying
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
    """Even bad outing result can
be very useful -
characters will
increase cohesion""",
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

DEFAULT_NOTE = "Press F1 key to open game\ncontrols help"

TIPS = ("Resting:", "Rest zone", "Approaching a city")

COHESION = (
    "Cohesion skills",
    "Recall the past",
    "Every character gets +25 energy. Cooldown: 10 min.",
    "Cover fire",
    "Every character gets +20% accuracy. Cooldown: 5 min.",
    "Not leaving ours",
    "Characters with health < 30 getting +20 health. Cooldown: 10 min.",
    "Common rage",
    "Every character gets +30% to damage. Cooldown: 10 min.",
    "Hold together",
    "No characters will die in next 1.5 min. Cooldown: 15 min.",
)

DISTINGUISHED = (
    "List of distinguished",
    (
        "Here you can praise your people or scold them "
        "to change their traits.\nPointing to a person is "
        "usually harmful for collective relations,\nso every "
        "praise/scold will reduce common team cohesion a bit.\n\n"
        "Choose one of the current character's traits (positive "
        "or negative) and\nscold the character to erase the trait. "
        "It'll cost you 4 cohesion points.\n\n"
        "If the character has less than 3 traits, you can praise "
        "him/her to\ngenerate 3 new traits and add one of them "
        "to the character's\ntraits list. It'll cost you 4 "
        "cohesion points."
    ),
    "Cohesion points:",
    "New traits:",
    "Praise",
    "Scold",
    "Done",
    "Current traits",
)
