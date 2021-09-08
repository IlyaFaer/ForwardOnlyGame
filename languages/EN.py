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
        "game princips. Enjoy your play!\n"
        """(c) Created by Ilya "Faer" Gurov. All rights reserved."""
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
        "You'll start with 3 soldier males. "
        "Prefered outings type: Enemy Camp."
    ),
    (
        "Raiders are accustomed to difficulties and can recover from "
        "anything. They are\ngood fighters at short distance and they "
        "know how to find resources. Their tactic\nis based on getting "
        "and using expendable resources and fast recovering.\n\n"
        "You'll start with 2 male and 1 female raiders. "
        "Prefered outings type: Looting."
    ),
    (
        "Anarchists are the force of nature! They build cohesion "
        "faster than others and\nalways value those, who life brought "
        "them with. The tactic is based on\ngetting more people, "
        "tweaking their traits and using crew skills.\n\n"
        "You'll start with 2 male and 1 female anarchists. "
        "Prefered outings type: Meet."
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
    (
        "The Adjutant is critically damaged!\n"
        "You're not able to continue the road, and\n"
        "the Stench will not keep you waiting long.\n\n"
        "It's all over...",
    ),
    "Framerate limit:",
    "Credits",  # 30
    """Created by Ilya "Faer" Gurov""",
    "Project source code:",
    "Subscribe:",
    "Stack:",
    "Tools:",
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
J - open journal

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
    " mi",
)

CHARACTERS = ("Name:", "Class:", "Health", "Energy", "Status", "Traits")
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
    """The city government awards
you with money for
your help in clearing
the region of skinheads.

Heads you've taken:
""",
    "Total reward:\n",
    """This city dwellers heard that
you helped orphans to build
camp. They respect good
people and want to encourage
you - the Adjutant gets +250
Durability points free.""",
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
    """Recruits found on Meet outings
request less fee
than in cities""",
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
    """Don't forget to check units'
status on the character
detailed GUI""",
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
    """Anarchists get strength factor
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
highly poisonous. Cross
them as fast as you can.""",
    # resources
    """Stimulator temporarily disables
the character's negative
traits. It also gives
immunity from deafening.""",
)

DEFAULT_NOTE = "Press F1 key to open game\ncontrols help"

TIPS = ("Resting:", "Rest zone", "Approaching a city")

COHESION = (
    "Crew skills",
    "Recall the past",
    "Every character gets +10 energy. Cooldown: 4 min.",
    "Cover fire",
    "Every character gets +20% accuracy. Cooldown: 5 min.",
    "Not leaving ours",
    "Characters with health < 30 getting +25 health. Cooldown: 8 min.",
    "Common rage",
    "Every character gets +30% to damage. Cooldown: 10 min.",
    "Hold together",
    "No characters will die in next 1 min. Cooldown: 10 min.",
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

SPLASHES = (
    "Word from author",
    """Forward Only will strangle you gradually for your mistakes
instead of punishing at once. Calculate steps ahead!""",
)

MECHANIC_DESC = {
    "locomotive": {
        "descs": (
            (
                "This is the Adjutant - your locomotive. It moves fast\n"
                "enough to outrun death, so take care of it. If\n"
                "it'll not be able to ride, your hours are numbered.\n"
                "Its Durability is reflected in the right bottom\n"
                "corner of the GUI. Keep an eye for rusty rails, they\n"
                "damage your wheels - slow down if you hear creak."
            ),
            (
                "The Adjutant includes three parts and a rest\n"
                "zone, where you can arrange your teammates.\n"
                "A wise units rotation is the key to success.\n\n"
                "Train speed is reflected in the right bottom corner.\n"
                "Hold W and S keys to accelerate and decelerate."
            ),
        ),
        "previews": ("locomotive1", "locomotive2"),
    },
    "characters": {
        "descs": (
            (
                "Your crew consists of several unique fighters. Every\n"
                "unit has energy, which should be kept at a high\n"
                "level, as it influences character's shooting accuracy\n"
                "and efficiency on outings. The simplest way to\n"
                "restore unit's energy and health is to make him rest."
            ),
            (
                "Click LMB on a character to choose him; control\n"
                "arrows will appear - click RMB on one to move\n"
                "the character to the related locomotive part,\n"
                "or click RMB on the rest zone to make him rest.\n"
                "Number of unit cells on every part is limited."
            ),
        ),
        "previews": ("characters1", "characters2",),
    },
    "the Stench": {
        "descs": (
            (
                "The main threat is the Stench. Its poisonous clouds\n"
                "are spreading fast and chaotic, and most likely will\n"
                "cover the whole Silewer in a couple of weeks. If\n"
                "you got into it, you better accelerate to cross the\n"
                "cloud as fast as possible. You also should not\n"
                "stay long on the same place or ride in circles."
            ),
            (
                "You need to find a way to survive the Stench. There\n"
                "are several places of interest in Silewer - check\n"
                "them for useful information. Use the railways scheme\n"
                "(press M) to plan your route and visit as much places\n"
                "as you can. You can also see outing abilities and\n"
                "the Stench coverage on the railways scheme."
            ),
        ),
        "previews": ("the_stench1", "map"),
    },
    "cohesion": {
        "descs": (
            (
                "Your characters build cohesion with each other\n"
                "by time. Total crew cohesion is reflected at\n"
                "the right top corner of the screen. Increasing\n"
                "cohesion unlocks crew skills - powerful temporary\n"
                "effects, which influence your every character.\n"
            ),
            (
                "It's worth keeping units with high cohesion on\n"
                "the same locomotive part, as they'll get higher\n"
                "strength factor. Cohesion also increases faster\n"
                "between characters on the same part. To see\n"
                "cohesion level of the unit with others, press R."
            ),
        ),
        "previews": ("cohesion1", "cohesion2"),
    },
    "outings": {
        "descs": (
            (
                "Outings are the main source of money and other\n"
                "facilities. It's an event that requires you to\n"
                "stop and send units for it. There are three types\n"
                "of outings: Looting, Meet and Enemy Camp, each\n"
                "offers own type of trophies and prefers an\n"
                "exact unit class to be sent for it."
            ),
            (
                "An outing have five finals; the higher is your score,\n"
                "the better is final. Score includes four items:\n"
                "class fit - for the sent units class, condition - for\n"
                "their health and energy, cohesion - for total cohesion\n"
                "of the units, and a small random piece of score."
            ),
        ),
        "previews": ("outings1", "outings2"),
    },
    "resources": {
        "descs": (
            (
                "You can find resources on outings or buy in cities.\n"
                "To use a resource, choose a unit and then click\n"
                "the resource button. Money is the major resource\n"
                "among all, you can spend it in cities for repair,\n"
                "healing, recruiting and upgrading the Adjutant."
            ),
        ),
        "previews": ("resources1",),
    },
    "character status": {
        "descs": (
            (
                "Every character can have up to three traits (good\n"
                "and bad). Traits give (dis-)advantages and can\n"
                "be considered as perks. You can change character's\n"
                "traits in Distinguished List, but remember that\n"
                "it'll lower common crew cohesion for some time."
            ),
            (
                "The current effects influencing the unit can be\n"
                "seen in their Status GUI. Also keep an eye for\n"
                "the disease icon - a sick character can bring a\n"
                "lot of troubles for the crew. Try to isolate\n"
                "diseased and cure them as soon as possible."
            ),
        ),
        "previews": ("character_status1", "character_status2"),
    },
}

MECHANIC_NAMES = (
    "locomotive",
    "characters",
    "the Stench",
    "cohesion",
    "outings",
    "resources",
    "character status",
)

MECHANIC_BUTS = ("Next", "Got it!")

CLASS_DESCS = {
    "MotoShooter": {
        "desc": (
            "Moto shooter will try to shoot at you and\n"
            "your locomotive as much as he can. Most of\n"
            "the skinheads prefer such a way of\n"
            "communication with foreigners, so stay\n"
            "sharp - there will be a lot of them."
        ),
        "preview": "shooter",
        "but_text": "Got it!",
        "title": "Some skinheads searching for you!",
    },
    "BrakeThrower": {
        "desc": (
            "Brake thrower will try to outrun you and\n"
            "throw a brake shoe under your wheels to slow\n"
            "you down. Such guys are not tough themselves,\n"
            "but they can make other skinhead attacks more\n"
            "successful. Try to deal with them fast!"
        ),
        "preview": "brake_thrower",
        "but_text": "Understood!",
        "title": "Skinheads rumoring about dare newbies!",
    },
    "Barrier": {
        "desc": (
            "Now skinheads are using heavy barriers to get\n"
            "to you. A barrier can do a lot of damage to your\n"
            "locomotive on a clash. It's highly recommended to\n"
            "set the Ram train upgrade in the nearest city\n"
            "to get better protection from barriers."
        ),
        "preview": "barrier",
        "but_text": "We'll deal with it!",
        "title": "Skinheads start to use barriers!",
    },
    "StunBombThrower": {
        "desc": (
            "Such a guy uses stun bombs to make your fighters\n"
            "non-operational for several seconds. It's hard for\n"
            "a thrower to get right into a fast moving target,\n"
            "but if you'll lose some of your speed, throw\n"
            "efficiency will significantly increase."
        ),
        "preview": "bomb_thrower",
        "but_text": "We're ready!",
        "title": "Skinheads start to take you seriously!",
    },
    "DodgeShooter": {
        "desc": (
            "Dodge with a machine gun is a strong enemy! It can\n"
            "do a lot of damage to your locomotive, but its\n"
            "machine gun overheats fast and requires time to\n"
            "cool down. Armor Plate train upgrade recommended\n"
            "to be used for protection against this enemy."
        ),
        "preview": "dodge",
        "but_text": "Bring'em on!",
        "title": "Skinheads gather vehicles to deal with you!",
    },
    "Rocket": {
        "desc": (
            "Your progress is really pissing skinheads off.\n"
            "To stop you they bring more and more forces.\n"
            "Their new thought - telecontrolled rockets - can\n"
            "do a lot of damage to your locomotive. Use Armor\n"
            "Plate upgrade to cover a side targeted by a rocket."
        ),
        "preview": "rocket",
        "but_text": "They won't stop us!",
        "title": "Skinheads start to use rockets!",
    },
    "Kamikaze": {
        "desc": (
            "Skinhead kamikazes are after you! They can do\n"
            "a lot of damage to the Adjutant, use Armor Plate\n"
            "upgrade to protect the locomotive. You can also\n"
            "destroy those guys before they'll ignite the wick.\n"
            "If done in a right moment, they damage other enemies."
        ),
        "preview": "kamikaze",
        "but_text": "We'll defeat them!",
        "title": "All skinheads are chasing you!",
    },
}

SCHEME = (
    "Silewer Railways Scheme",
    "Legend:\nm - Meet\nl - Looting\ne - Enemy Camp\ni - Place of interest",
    "- city",
    "- railway branch",
    "- the Stench",
)

TRAITS = [
    ("Fast hands", "Snail"),  # 0
    ("Cat eyes", "Fear of dark"),  # 1
    ("Masochism", "Hemophobia"),  # 2
    ("Immunity", "Weak immunity"),  # 3
    ("Liberal", "Loner"),  # 4
    ("Bloodthirsty", "Nervousness"),  # 5
    ("Deep breath", "Motion sickness"),  # 6
    ("Mechanic", "Pharmacophobia"),  # 7
]

TRAIT_DESC = {
    "Fast hands": "+30% shooting speed",
    "Snail": "-20% shooting speed",
    "Cat eyes": "+25% accuracy in darkness",
    "Fear of dark": "+50% energy spend in darkness",
    "Masochism": "regain energy when getting damage",
    "Hemophobia": "+25% energy spend, if health < 50%",
    "Immunity": "-40% chance to get sick",
    "Weak immunity": "+20% chance to get sick",
    "Liberal": "+30% cohesion increase with other classes",
    "Loner": "x1.3 strength while alone on the Train part",
    "Bloodthirsty": "+7 health for a killed enemy unit",
    "Nervousness": "+25% energy spend while in fight",
    "Deep breath": "Avoid the Stench poison for the first 1 min",
    "Motion sickness": "Doesn't restore on high movement speed",
    "Mechanic": "Repairs the Train, while not resting",
    "Pharmacophobia": "Self-healing 40% slower",
}

UPGRADES_DESC = {
    "Ram": {
        "name": "Ram",
        "desc": """With this ram your locomotive
will be breaking road barriers
without getting damage""",
        "cost": "120$",
        "model": "ram1",
        "threshold": 1,
    },
    "Floodlights": {
        "name": "Floodlights",
        "desc": """All the negative darkness
factors are no more actual
with these floodlights on""",
        "cost": "190$",
        "model": "floodlights1",
        "threshold": 2,
    },
    "Armor Plate": {
        "name": "Armor Plate",
        "desc": """An active shield which can
cover one of the Train sides.
Press 4, 5, 6 keys to move it.""",
        "cost": "70$",
        "model": "armor_plate",
        "threshold": 1,
    },
    "Fire Extinguishers": {
        "name": "Fire Extinguishers",
        "desc": """Gradually restores locomotive
durability up to 400 points
in case of a big damage""",
        "cost": "190$",
        "model": "fire_extinguishers",
        "threshold": 2,
    },
    "Grenade Launcher": {
        "name": "Grenade Launcher",
        "desc": """Active gun, which can do a
lot of damage on a small area.
Press 1 key to aim and shoot.""",
        "cost": "180$",
        "model": "grenade_launcher",
        "threshold": 1,
    },
    "Sleeper": {
        "name": "Sleeper",
        "desc": """Add one more character cell
into the locomotive rest zone""",
        "cost": "140$",
        "model": "sleeper1",
        "threshold": 1,
    },
    "Window Frames": {
        "name": "Window Frames",
        "desc": """With this window frames
characters in the rest zone are
protected from the Stench""",
        "cost": "150$",
        "model": "isolation",
        "threshold": 2,
    },
    "Cluster Howitzer": {
        "name": "Cluster Howitzer",
        "desc": """Shots a cluster rocket, which
splits to four grenades, doing
damage on several circles.
Press 3 to aim and shoot.""",
        "cost": "200$",
        "model": "cluster_bomb_launcher",
        "threshold": 2,
    },
    "Machine Gun": {
        "name": "Machine Gun",
        "desc": """Fires aiming burst. Better be
used for a single target.
Press 2 to aim and shoot.""",
        "cost": "160$",
        "model": "machine_gun",
        "threshold": 2,
    },
    "Protectors": {
        "name": "Protectors",
        "desc": """Armor for wheels and pushing
mechanism. Increases max
Durability to 150%.""",
        "cost": "160$",
        "model": "armor",
        "threshold": 1,
    },
}

FORKS = (
    "Approaching a fork:\npress T to turn right\nignore to proceed",
    "Approaching a fork:\npress T to turn left\nignore to proceed",
)

JOURNAL = ("Journal", "Notes:", "Diary:")

STATUSES = (
    "Cat eyes: +5% accuracy",
    "Dark: -10% accuracy",
    "Dark: -20% accuracy",
    "Tired: -{}% accuracy",
    "Strength factor: x{}",
    "Hemophobia: +25% energy spend",
    "Sick: -20 max energy",
    "Motion sickness: doesn't restore",
)

OUTINGS_GUI = (
    "People to send ({cur_as}/{max_as}):",
    "Total outing score:\n",
    "Don't send",
    "Send",
    "Outing score:",
    "Character classes fit:",
    "Characters condition:",
    "Characters cohesion:",
    "Day part:",
    "Crew:",
    "Recruit",  # 10
    "Don't recruit",
    "You can recruit {name} for {cost}$",
    "Get {trait} trait\n ({desc})",
    "Select one character as a target for the effect:",
)

NOTIFIERS = (
    "Place of interest! Stopping",
    '"{}" outing available in 2 miles',
    "2 miles",
    "1 miles",
    "Stop to start outing",
)
