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
        "It's a beta release. The game is not finally balanced and some"
        " features are in development yet. Enjoy your play!\n"
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
    "FPS meter:",
    "Multi threading:",
    """(boosts FPS, but on some systems
can cause flaky failures on
new game start or loading)""",
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

New Year spirit:
7 - toggle the mode
8 - flapper shot

St. Valentine's Day:
9 - toggle the mode
"""

RESOURCES = (
    "Resources:",
    "Medicine",
    "Cure disease and wounds of a character",
    "Smoke filter",
    "Reduce skinhead attack chance (5 min)",
    "Stimulator",
    "Disable negative traits and deafening (5 min)",
    " mi",
    "Place of interest",
    "Visit at least 8 of 10 to win the game",
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
    """Don't forget to read notes
in the Captain's Journal.
They can tell you a lot.""",
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
    """Increasing crew cohesion unlocks
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
character class and
their energy level""",
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
    "Every character gets +30% strength. Cooldown: 10 min.",
    "Hold together",
    "No characters will die in next 1 min. Cooldown: 10 min.",
)

DISTINGUISHED = (
    "List of distinguished",
    (
        "Here you can praise your people or scold them "
        "to change their traits.\nPointing to a person is "
        "usually harmful for collective relations,\nso every "
        "praise/scold will reduce common crew cohesion a bit.\n\n"
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
                "zone, where you can arrange your crewmates.\n"
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
                "restore unit's energy and health is to make them rest."
            ),
            (
                "Click LMB on a character to choose them; control\n"
                "arrows will appear - click RMB on one to move\n"
                "the character to the related locomotive part,\n"
                "or click RMB on the rest zone to make them rest.\n"
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
                "are several places of interest in Silewer - visit at\n"
                "least 8 of them for useful information. Use the\n"
                "railways scheme (press M) to plan your route.\n"
                "You can also see outing abilities and the Stench\n"
                "coverage on the railways scheme."
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
        "title": "Skinheads rumor about dare newcomers!",
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
        "cost": "170$",
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
        "cost": "180$",
        "model": "cluster_bomb_launcher",
        "threshold": 2,
    },
    "Machine Gun": {
        "name": "Machine Gun",
        "desc": """Fires aiming burst. Better be
used for a single target.
Press 2 to aim and shoot.""",
        "cost": "150$",
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
    "Cohesion increased: +{value} points",
)

NOTIFIERS = (
    "Place of interest! Stopping",
    '"{}" outing available in 2 miles',
    "2 miles",
    "1 miles",
    "Stop to start outing",
)

OUTINGS = [
    {  # 0
        "name": "Car Column",
        "desc": """You're catching your eyes on four big black jeeps, standing in a row.
They are covered with dirt, but even from that big distance you
can say they are in a good shape. No human around makes it
tempting to send some folks to recon the place - is your first
thought. But when the Train engine finally falls silent, you're
hearing voices, flying from the car column side. Definitely,
there are people somewhere there, still, it's not possible to
see them from your spot. So, the initiative becomes little bit
risky. It's worth it to send three of your fighters together
to check the cars.""",
        "results": (
            """{name1}, {name2} and {name3} are jumping off the Train, and
taking a direction to the jeep column. Holding closer together, they
are silently moving from one tree to another, smoothly approaching
to the cars. In some moment you understand that voices, which were
flying to you from the column, vanished. Something is wrong! You're
finding your people by your gaze, and in this moment a machine gun
shots tearing the air. Your whole crew starts to shoot back, slowly
crawling back to the Train, as the enemy seems to be full of ammo.
You're trying to help others with your fire, and the rival shots are
starting to fly to the Train. Taking cover, you're waiting for {name1},
{name2} and {name3} to return and giving the order to start the engine.
Adjutant getting -80 Durability""",
            """{name1}, {name2} and {name3} are taking the direction to the jeeps
by your command. They are moving across the meadow silently for
some time, but suddenly a sturdy with a machine gun appears near one of
the jeeps and starts to shoot at your people, pinning them to the ground.
You're seeing {name3} showing something to others by {hisher3} hand.
{name1} and {name2} turn around and move back to the Train, while {name3}
covering them with aggressive fire. The sturdy, experiencing a bullets
storm, hides behind the car. {name1} and {name2} closing to the Train and
taking a turn around to cover {name3} retreat. Hearing a short pause,
sturdy appears back behind the car and shoots to {name3}, but {heshe3}
returns back to the Train with just a couple of small wounds.
{name3} getting -25 health
{name1} and {name2} getting -15 health""",
            """{name1}, {name2} and {name3} jumping off the Train and moving
to the jeeps column. You're seeing them silently approaching the
cars. Hopes, there is no one inside... Not even throwing a look
inside the cars, your people are simultaneously turning around
and running back to the Train with the full speed. You're taking
your gun, preparing for the fight. But no one follows your
messengers, so you only have to wait them. {name2} climbing the
Train back first. "There are at least fifteen people, lower,
near the river." - {heshe2} explains, breathing heavily. You nod
your head and giving the command to warm up the engine.""",
            """You're sending {name1}, {name2} and {name3} for a short
recon of the place. Your crewmates are moving to the jeep column,
while you track them from the Train; seeing how {name2} opens a
car and starts to rummage in the glove compartment. Suddenly,
you hear cries, but not of your messengers. Still, they are
reacting fast, and turning back to the Train. Looks like
someone detected them! Confirming this, several naked people
appearing near the jeeps. But to the moment they grabbed their
guns and started to shoot, {name1}, {name2} and {name3} are
jumping onto the Train. "No empty hands!" - {name2} proclaims
and shows dollars on {hisher2} palm.
You're getting 90$""",
            """{name1}, {name2} and {name3} are taking the direction to the jeeps
column. {name2} and {name3} are opening two of the cars at once,
while {name1} stands on the watch. You're seeing {name2} grabbing a
canister from the car inners. With this find {heshe2} without stops moves
back to the Train. {name3} in the next few seconds rummages the jeep,
but in some moment {name1} jumps on {hisher1} place and starts to
shoot to somewhere behind the column. {name3} grabs the first thing
{heshe3} see and turns to the Train. {name1} takes few more seconds
to shoot at those on the other side, but they fight back tough, so
{heshe1} has to retreat. Returning fast, your people show the catch.
You're getting 100$ and 1 stimulator
{name1} getting -15 health""",
        ),
    },
    {  # 1
        "name": "Big Tent",
        "desc": """It takes not less than ten seconds for you to understand is
something there, or it's just a big bush. Yes, something is definitely
there - a square dark green tent, very similar to a soldier's one.
It doesn't look like there are people in there, but the tent is
still standing, so most likely someone cares about it. The maximum
number of sleepers in such a tent equals to six, and they should
have to hear the Adjutant approaching. No signs of movement
means no human, right? It's little bit dangerous, but makes sense
to send someone to check if anything useful lies in this tent.""",
        "results": (
            """You're ordering {name1} to move closer to the tent and take a
look at it. {name1} jumps off the Train and runs fast to the spot.
You're tracking {himher1} from the cabin, staying sharp. Approaching
the tent closer {name1} slows down little by little, but in some
moment {heshe1} suddenly grabs {hisher1} leg and falls on the ground. You
jump out of the cabin and bring binoculars to your eyes. No one
appeared anywhere, so you're catching a breath and taking a more
careful look at {name1}. It seems like {heshe1} failed into a trap.
You're moving binoculars away and, jumping down to the ground,
take direction to {name1} to help {himher1} to get out.
{name1} getting -25 health""",
            """{name1} takes {hisher1} gear and heads to the tent by your command.
You're staying on the Train on the watch, holding your gun with
one hand. {name1} cautiously moves through the green meadow to the
tent, and once the tent starts to swing. You're throwing up your gun
and taking the spot on the sight. An old man jumps out of it and,
turning a big shotgun onto {name1}, thunders the air with a shot.
As the distance between {name1} and the shooter is too long for a
shotgun, it most likely was a warning shot. In the next moment the old
man sees you and the Train, and he freezes. "{name1}, get back!" -
you're shouting, and {heshe1} starts to move to the Train back forward.
The old man continue to hold his gun up, but he don't shoot any more.
"He got me a little" - {name1} climbs up on the Train and shows
{hisher1} bloody shoulder. {name1} getting -10 health""",
            """You're sending {name1} to take a closer look at the tent. {name1}
takes {hisher1} gun and fastly moves to the place. The meadow smells
with flowers and cool, sleepy birds are chirping around, and there
is no any single sign of a human. No garbage, no crumpled grass, no
defensive traps. Getting closer to the tent, {name1} sees that it's full
of shot holes. No doubts, someone crept up to it and shoot away all who
was inside. Not very nobly. {name1} accurately moves to the tent entrance
and takes a look into it. Several skeletons in soldiers uniform, and no
guns, supplies or anything useful at all. Someone already looted the
place clean. In disappointed mood {name1} returns back to the Train.""",
            """By your command, {name1} gears up and takes a direction to
the square tent. First half of {hisher1} way {heshe1} runs fast,
but then {name1} slows down hard, carefully looking under {hisher1}
feet. You're staying sharp as it looks like there are traps there,
and where traps - there people, who set them. Still, {name1}
approaching the tent without any sign of a trouble. Taking an
accurate look inside, {heshe1} disappears in the tent inners.
You're feeling little bit nervous, but several minutes passes,
and {name1} walks out on the meadow. Carefully choosing the steps,
{heshe1} returns back to the Train and shakes a bunch of dollars
in {hisher1} left hand, showing it to you.
You're getting 70$""",
            """You're sending {name1} for a small recon. Taking {hisher1} gun,
{heshe1} moves fast to the tent, while you're tracking {hisher1} movement
through the binoculars. At a few seconds {heshe1} closes to the spot from the
side, and suddenly tissue entrance of the tent flyes up with loud gun
shots. {name1} lighting fast ups {hisher1} gun and makes several shots. Silence
falls on the meadow... {name1} carefully taking a look inside the tent and
enters it. In the next second {heshe1} jumps out of it and runs back to the
Train. "Skinhead scum!" - {heshe1} says, entering the Train cabin. - "Seems
like he tried to shot me before he actually saw me. Missed." - {heshe1} adds,
pointedly putting several banknotes onto the table.
You're getting 100$""",
        ),
    },
    {  # 2
        "name": "Bus",
        "desc": """The big red two-storied bus standing at the middle of the meadow
catches your attention from a very long distance. Bringing the
binoculars to your eyes, you're seeing that it's little bit old
and shabby, but sand bags and logs placed around the car in
defensive positions tells it's still inhabited. You also see
that second floor doesn't have any glass in windows - probably
a sniper point, but, except this fact, the bus seems to be safe.
It makes sense to send a couple of people to check if there
is something valuable in there.""",
        "results": (
            """You're sending {name1} and {name2} to take a look at the bus.
Moving to the car, they are looking around carefully. The meadow is
visible for three hundreds meters around, and nothing promises troubles,
so after a couple of minutes of walk they relax. In that moment a shot
thunders in the air. Sniper! You're seeing his long gun barrel protruding
from the empty window on a second floor. Another shot thunders, and
{name1} falls to the ground with a loud shout. Taking your gun you're aiming
the bus and starting to shoot at it as fast as you can. Sniper disappears
in the dark car inners, so {name2} takes down {hisher2} gun, lifting
{name1} and pulling {himher1} to the Train under your cover fire.
{name1} getting -35 health
{name2} getting -20 energy""",
            """By your order {name1} and {name2} taking their gears and walking
to the bus. Looking at the car through binoculars you catch some kind
of a movement there. You whistles to notice your people about probable
troubles, and they taking lower poses. In the next second bus starts to
sway, and gun flames are blinking in the car's windows. {name1} and {name2}
shooting back at the same moment, but gang in the vehicle seems to be
more numerous, so they both retreating to the Train. Enemy gun fire
is terribly inaccurate, still, bullets are flying and flying to you,
throwing sparkles all around and ringing with the Train metal. You're
commanding to start moving, and {name1} with {name2} are jumping on the
Train on the run. Rival bullets following you for two more minutes,
and then suddenly falls silent. Adjutant getting -40 durability""",
            """{name1} and {name2} taking their guns and moving in the direction
of the bus. Nearlands of the vehicle seems silent, so your people are
moving to the spot fast, but in some moment both are suddenly stopping.
You're passing your gaze around to understand what has gone wrong.
Jeep! Big black jeep roaring in a distance of kilometer seems to be
heading to the old bus! Feeling the bad luck, you're shouting to your
people: "{name1}, {name2}, get back!". Gazing at each other for a second
they are turning around and retreating to the Train. Jeep in the same
time approaches the bus, several armed people are jumping outside.
Their mood seems to be aggressive, still, they doesn't start firing.
It's better to move along before they changed their mind.""",
            """Driven by your command, {name1} and {name2} are taking the
direction to the old vehicle. As the meadow looks too open, they are
running fast to cross it as soon as possible. Disappearing within the
car, your people start to rummage through it, swinging the old metal
carcass. While it all happening, you see a big jeep on a horizon.
Whistling loudly to your people, you're preparing for a fight. It takes
two more minutes for {name1} and {name2} to jump outside the bus. The
gang in the jeep, approaching fast, start to shoot, and you're opening
fire back. {name1} and {name2}, using your cover shooting, are
returning back to the Train with several banknotes, and you're
deciding to move along before the bus beholders came too close.
You're getting 80$""",
            """While you were deciding who to send for a search, several
skinhead scums are jumped out of the bus. Your whole crew, seeing
them, starts to shoot, and after six-eight seconds all of the rivals are
falling down on the ground. Taking a quick look at the vehicle through
binoculars you're commanding {name1} and {name2} to go to it. They
both energetically jumping off the Train and moving to the bus. You're
staying on the watch for case if more skinheads will come. Your
people entering inside the car, and returning back into a field of
view in less than thirty seconds. Getting back to the Train, they
showing you a bunch of crumpled dollars.
You're getting 100$""",
        ),
    },
    {  # 3
        "name": "Gas Station",
        "desc": """For at least twenty minutes you've been watching a highway to
the left of the railway. No cars, no light posts - road was
completely empty. But, finally, you're seeing a white square
advertisement sign of a small gas station. There is no vehicle
nearby, nor people, otherwise the building looks well
maintained. Hm-m. Fuel - is always good, but suspicious
silence of the nearlands makes you little bit wary. Place
should be checked for resources, and if to send someone, you
should send two, so that messengers could deal with possible
troubles together.""",
        "results": (
            """{name1} and {name2} are closing to the gas station, seeing a lot
of bullet shells scattered all around. They throw gazes at each other
and proceeding further much more slower. Entering into the looted
building, full of broken metal, plastic and wood stuff, they decide
to turn around and move back to the Train, but in that moment gun
shot thunders in the air, and the gas automates exploding with
horrorable noize. {name2} gets back to the reality first, and sees
that {name1} has a lot of cut wounds. Taking a quick look around,
{heshe2} detects no threats - seems, the one tried to explode them,
and retreated right after the shot. Lifting {name1} on the shoulders,
{heshe2} moves back to the Train.
{name1} getting -40 health
{name2} getting -10 health""",
            """{name1} and {name2} starting to move to the gas station by your
command. It takes a couple of minutes for them to come to the
building, which looks like people were here seconds ago. Entering
inside, {name1} and {name2} trying to find something really useful,
but only see bubble gum, chips and crackers. Suddenly, {name1} catches
{hisher1} attention on a strong smoke smell. Throwing a look through
the window, {heshe1} pushes {name2} and jerkely runs to the entrance.
{name2} follows {himher1}, and outside they see that someone surrounded
them with a ring of fire. "Faster!" - {name2} commands and runs
through the wall of flame, trying to cross it before it grown too strong.
Breaking through the fire, they see no one, no ambush or something.
Strange. With a couple of scorches they return to the Train.
{name1} and {name2} getting -10 health""",
            """You're choosing {name1} and {name2} as messengers for this walk.
They grab their stuff and take the direction to the gas station. Getting
closer to the building, they hear music. More than that, entering the
station they see several people: cashier, security guard guy and waiter.
Not to scare anyone they move their guns down, and doing a try
to talk with the gas station inhabitants, but all of them are speaking
at some weird language, which {name1} and {name2} doesn't know. As
dwellers doesn't seem to be dangerous, just several people, who still
lives here despite the End of Days, {name1} and {name2} deciding
to leave them as they were and move along.""",
            """{name1} and {name2} moving to the gas station by your order.
Getting closer to the building, they hear music and see three people
within. In the next moment from the other side of the station four
skinheads with guns appear, with clear intent to attack the gas
point. {name1} and {name2}, not yet detected by robbers, upper their
guns and shooting off all of these cruds. The station dwellers moving
outside the building to see what's happening, and understand that your
people saved them from skinheads. They applaud {name1} and {name2},
speaking of weird language unfamiliar to your messengers. {name1} and
{name2} nod their heads, turning back to the Train, but one of the
dwellers stops them and gives them several dollar banknotes.
You're getting 80$""",
            """{name1} and {name2} fastly moving to the gas station. Getting
closer, they slow down, but after several seconds they see that the
building is abandoned. The glass door is open, music is still playing,
but dust lies everywhere and silence fills the air. {name1} and {name2}
together walking around the station, enter it and, seeing no threats,
splitting to check two places simultaneously: the cash and the storeroom.
Cash machine, fortunately, is open, and {name2} finds a toolbox really
fast. Energetically taking their lucky catches, {name1} and {name2} in
a good mood returning back to the Train.
You're getting 90$ and +100 Adjutant durability""",
        ),
    },
    {  # 4
        "name": "Trailers",
        "desc": """From a very long distance you're catching your eyes on several grey
rectangles. Buses? That can promise troubles as well as a good place
for looting. While the Adjutant getting closer to the vehicle, it
becomes clear that it's not just a bunch of cars, it's a small
auto camp. Five big trailers with clotheslines stretched between
them, soccer balls and bonfires looking quiet, but definitely
inhabited. You're not able to find any human by your eyes, and
this fact makes the situation even harder: there can be dozens
of fighters there. It makes sense to prepare well before
entering this trailer camp.""",
        "results": (
            """You're making a decision to send {name1}, {name2} and
{name3} to investigate the trailer camp. They're taking their gear and
move towards the grey cars. Nothing promises troubles for several
minutes, but at some moment car engines tearing the air apart. You
all uppering your guns to fight back the enemy. Trailers are starting
to skid, throwing grey dirt all around, and your messengers making
few steps back to the Train side not to get lost in these clouds. Red
and white trailer lights are floating in hazy distance, but you're
hearing no shots. They are just leaving. Taking few more seconds to
think, you're commanding your people to return back to the crew.""",
            """You're deciding to send {name1}, {name2} and {name3} for a recon
of the place. While they are gearing up, you're looking at the trailers
camp trying to understand, if there is an ambush there. Once you hear
the vehicle engines starting, and in the next second trailers are
getting under way. Your people standing up just beside you, managing
to find out what is going on. "Looks like they are leaving." - {name2}
says. "Well, at least they didn't start to shoot." - {name1} adds. Yes,
that's definitely a good thing... Trailers are distancing fast, and the
dust settles to the ground, unveiling some stuff left by those people.
"Let's take a look at it!" - {name2} pronounces and jumps off the Train.
You're finding a cure that can heal 15 health of one character""",
            """{name1}, {name2} and {name3} jumping off the Train to do a recon
of the trailer camp. In the same moment grey cars start their engines
and making a spurt to leave the place. Your people are holding
several seconds pause to see what will happen next... All the trailers
except one are moving away fast. {name3} throws a gaze to {name1} and
{name2} and points to the car with {hisher3} head. Closing to the vehicle,
they open it, and {name1} with {name3} are entering inside. It takes
time for them to search through the car. Not much of lucky finds,
mostly there is just an old useless stuff, like someone very old
and most likely little bit mad was living in the truck, but at least
{name3} finds 40$ in there. With this find your messengers return back.
You're getting 40$""",
            """By your command, {name1}, {name2} and {name3} taking their gear
and jumping to the ground. Right in this second all the trailers, except
one, spurt away. In the remaining car your people hear some fuss.
While they are getting closer to the vehicle, the window of it opens,
and a gun barrel leans out, starting to shoot all around without aiming.
Making a circle movement around the trailer, your people open it and do
several shots inside. The rival gun silences. {name1} and {name2} enter
the car for several seconds and walk out together, holding a big tool
box. Lifting it onto the Train, {name2} puts {hisher2} hand in {hisher2} pocket and
gets out a bunch of dollar papers. "Plus to the filter" - {heshe2} smiles.
You're getting 1 smoke filter and 60$""",
            """{name1}, {name2} and {name3} energetically jump off the Train
and take the direction to the trailers camp. After few seconds of
silence they hear some movement near the cars. Uppering their guns,
they see several skinheads with pistols, swingingly moving to them.
Not giving a chance, your people shoot out them and start to move
from one trailer to another. In every one of them they see injectors,
white powder, stinky vomit and one-three stoned to nearly death
skinheads. "A drug party, ha?" - {name2} says. - "Let's take what
is useful for us and leave them where they are." {name1} and {name3}
agreeing on that, and they three start to collect things.
You're getting 200$""",
        ),
    },
    {  # 5
        "name": "Construction",
        "desc": """Standing on a cool air, you're observing the horizon line. For
the few last hours you saw twelve wooden houses, burned to
the ground. Seems like someone is clearing these lands,
probably skinheads. It's worth staying sharp... Once you're
seeing a two-floored construction. Concrete, with metal
rods, but definitely unfinished - there are no doors,
window glasses, roof, only bare walls. "Let's make a short
stop there!" - you're commanding. That's not very logical,
but something makes you think there is somewhat useful in
this building. Still, considering the burned houses
nearby, it's better stay vigilant.""",
        "results": (
            """You're deciding to send {name1}, {name2} and {name3}
to recon the construction site. Your people are preparing for a walk,
but in the moment they are going to jump off the Train, you're hearing
some fuss at the building. Suddenly, a big guy with a machine gun appears
on the second floor, and flame of his gun starts to rush between two
concrete walls. Bullets loudly knocking on the Train sheathing, promising
a lot of damage. In some moment the guns silences, and you're uppering
your head. A lot of shot holes are gapping on the Train. Are these armor-
piercing bullets!? Is it worth getting this guy? It's probably better to
leave before this gun made even more damage to the locomotive.
Adjutant durability -60""",
            """You're giving {name1}, {name2} and {name3} an order to check
the construction site. Taking their guns, your fighters are jumping off
the Train and getting to the place. The building seems to be completely
empty and uninhabited. There are no even signs of temporary camp. In
disappointed mood, {name2} catches {hisher2} eyes on the basement entrance.
"Oh, you think we should?" - {name1} asks, understanding where {name2}
gazes. Why not, your people are going down to the dark wet basement.
Flashlights are floating on an empty walls and floor. Nothing. "Do you
feel it?" - {name3} asks. - "Smells like canella". {name2} harshly
stops. "Canella?! We better go!". Starting to understand, your
messengers running out of the basement on to fresh air. "We should
lavage ourselves, it can be very poisonous." - {name3} finalizes.
{name1}, {name2} and {name3} getting -20 health""",
            """You're sending {name1}, {name2} and {name3} to check the place.
While they are on their way, you're staying on a watch to prevent any
surprises. The Stench have taken near 5% of the Earth, but people already
became non compos. Or maybe they always were, the Stench only released
their atrocity, revealed it? While they were afraid of laws, they were
quiet, proving their true selves only inside. And now, when no one
knows what to do and what will happen next, when no one controls the
situation, when no one will come to help, they decided to do what
their nature whispers... You're seeing your people walking out of
the construction. Looking disappointed, {name2} from that far shows
that there was nothing useful there, nor interesting. Well, it's
time to start the engine.""",
            """Your crew mates - {name1}, {name2} and {name3} are taking a direction
 to the construction site. Nothing promises troubles for some time,
but when they getting down to the basement, the cry tears air.
Fast uppering their guns, your messengers see a thin guy, holding
his hands above his head. "Don't touch me!" - he shouts. As he
doesn't have a weapon, {name1} takes {hisher1} gun aside. "He is
skinhead." - {heshe1} pronounces surely. "Yes, yes!" - the guy answers. -
"But they left me. Now I'm alone. Take my money and don't touch me!"
- he gets his left hand into the pocket and throws several banknotes
outside of it. "Don't touch me!". Raising the money, {name2} takes away
{hisher2} gun as well and points others to the exit.
You're getting 80$""",
            """{name1}, {name2} and {name3} jump off the Train and
run to the construction site. Getting closer, they smell smoke, so,
holding teamwise, they starting to move fast from one room to another,
covering each other and taking every turn on a sight. Skinheads,
confused and, probably, stoned, are appearing from time to time,
but your messengers are shooting them one by one without any delays.
Cleared the whole two-floored building in four minutes, they
make a short pause, and then start to rummage through rival
stuff. It doesn't look like a lot of useful things, but these
guys definitely had some money.
You're getting 130$""",
        ),
    },
    {  # 6
        "name": "Cloth Piece",
        "desc": """The horizon line is lost behind trees for hours. The lands
seems to be very wild, still, you've given an order to everyone
to keep eyes open... And at some minute you're hearing your
crewmates calling you outside the cabin. Exiting the locomotive
deckhouse, you're taking a binocular and gazing into the pointed
direction. First you don't see anything except trees. But after
few seconds a big piece of dark green cloth reveals, strained
between two tree trunks. "It definitely looks like a shelter..."
- you're pronouncing, thinking how many people should be
sent there. Probably, two fighters will be enough.""",
        "results": (
            """After overthinking the situation you're deciding to send
{name1} and {name2} for a scouting. They both take their gear and
jump off the Train. You see them moving to behind of the cloth piece...
Ten minutes passed, and finally you see your people running back to
the Train. While they are getting closer, you're starting to suspect
something wrong - too nervous is their behavior. "There was an ambush."
- {name2} says, climbing to the Train. - "They've taken {name1} as a
hostage and demanded ransom." {name1} climbs to the Train next:
"Sorry!". {name2} continues: "I've gave them 90$ to free {himher1}.
Let's go before they wanted more."
You losing 90$""",
            """You're sending {name1} and {name2} to see what is this
piece of cloth is for. Your people run to the place fast, but in last
thirty meters they slow down and start to move much more careful. The
strained cloth seems to be a disguise - they find metal dishes, backpacks
and some other stuff behind it. The camp is long forsaken, still, as
they are already there, your messengers rummaging the things. In
some moment a loud rustle sounds in air, and big web with stones
falls down to {name1}'s head. {name2}, who was standing few meters
aside, raises the gun and circles on {hisher2} place... But no one
showing up... {name1} in that time gets out of the web and, covering
a blooding wound on {hisher1} head, touches {name2} to show that
{heshe1}'s ready to return back to the Train. And they return fast.
{name1} getting -20 health""",
            """After a couple of minutes of thinking you're deciding to
send {name1} and {name2} to check the place. They fastly running to the
strained cloth and hiding behind it; silence and still falls on the near
lands. While waiting them, the Stench comes on your mind. Are there
people who can survive in it? Is there a kind of natural immunity to
this phenomenon? You never heard about such a thing. Though, news in
our days are not very often at all. Only death statistics and territory
cover reports... Finally, you see your people returning back. There
is nothing in their hands, so you doesn't wonder, when {name1} comes
closer and says: "Negative!". Well, time to continue the path.""",
            """You're sending {name1} and {name2} for a short
recon of the place. In fast pace they run to the cloth piece,
and when the distance to it becomes less than twenty meters,
several skinheads jumping out of the strained cloth. Not
giving any chances, {name1} and {name2} with accurate shots
dropping rivals one by one. Ensuring there are no more
threats, they start to search through the wooden boxes,
piled up behind the cloth. Most of them are already empty,
but {name1} and {name2} find a bunch of personal first aid
kits. Giving high five to each other, they take the catch
and, satisfied, returning back to the crew.
Your crewmates getting +10 health""",
            """After little overthinking you decide to send {name1}
and {name2} to take a look at the place. Fastly moving to the
spot, they hide behind the strained cloth, and few seconds later
show up again with a big ammo box. Seeing this, you jump off
the Train and move towards them to cover, as their hands are
busy. When you got closer, {name1} explains: "No one at home!
We decided to take it, as there is a couple of gnawed bodies
there. Doesn't look like a good campers." Uppering the heavy
box on to the Train, you're giving an order to start engine.
With this catch you'll save some money on the next stop.
You're getting 170$""",
        ),
    },
    {  # 7
        "name": "Kid's camp",
        "desc": """From a big distance you've noticed several dark green
buildings. Got closer, you see that they are old, but still in a
good shape. A bunch of colorful attractions makes you think that
this is a summer camp for kids. There are no kids, however, but
the place is definitely inhabited, most likely by skinheads -
you see bodies lying here and there, smoke rising from a couple
of buildings and a lot of fresh litter. It looks like the
current owners of the camp didn't notice your arrival, so it
makes sense to send just one scout for a quet place recon.""",
        "results": (
            """You're sending {name1} for a scouting. Without delays {heshe1} takes
the direction to the camp and silently approaches it. The place seems
quiet for some time, but suddenly several doors are opening, and shots
are tearing the air. Falling to the ground, {name1} start to shoot
all around, and you're trying to help {himher1} from the Train. It takes
about three minutes for your messenger to get back to you, but the
skinheads doesn't want to leave you be - they run to the locomotive
with loud shouts. Lucky for you, they didn't think about getting into
open place until it became too late. Your coordinated fire drops them
one by one. Making a quick roll call, you understand that you all,
however, got some wounds during this skirmish.
All of your crewmates are getting -30 health""",
            """You're choosing {name1} as a scout. Jumping to the ground, {heshe1}
puts on a hood against the cold wind and walks to the spot. It takes
a couple of minutes for your messenger to understand that the camp is
empty, at least right now. Walking around, {heshe1} tries to find
something useful, but nothing except empty paper boxes and clothes
shows up. In some moment a strong wind gust swepts in the air, and
{name1} hear a metal creak. Uppering {hisher1} head, {heshe1} see that big
metal water storage, standing in the middle of the camp, leans
over, and in the next second fails to the ground. Dirty water rises
between the buildings, and {name1} spurts back to the locomotive. Wet
and cold, {heshe1} jumps to the Train and runs into the deck, closer
to the engine to get warm faster.
{name1} getting -30 energy""",
            """You're deciding to send {name1} alone to take a look at the camp.
Grabbing {hisher1} gun, {heshe1} runs to the spot and starts to quetly
walk through the green buildings. It seems like the camp is forsaken
several hours ago - empty backpacks, clothes, some photos - the usual
stuff for a kid's camp, but nothing really useful while you're on a
road. Having examined three buildings, {name1} walks to the street
and feels a cold wind blowing. Not wanting to stay longer in such a
weather, {heshe1} takes a direction back to the locomotive: there is
nothing valuable in this place anyway.""",
            """By your command, {name1} jumps down to the ground. Getting
closer to the camp, {heshe1} sees several skinhead sentries. That,
however, doesn't scare your messenger and {heshe1} sneaks into the
building with a red cross. It appears to be not just a medical
structure, but also a weapon storage. Throwing a gaze at the
containments, {name1} notices a big first aid kit and moves to it.
Several syringes, paper boxes of tablets, white bandages - {name1}
takes the whole kit and moves out of the building. Carefully walking
out of the camp aside of the watch, {heshe1} runs to the locomotive
and proudly enters the deck house with {hisher1} rich catch.
All of your crewmates getting +20 health""",
            """{name1} becomes your messenger. Grabbing {hisher1} stuff,
{heshe1} silently jumps down to the ground and moves into the camp.
Only a couple of skinhead sentries lazily walk around the
buildings, talking loudly. Without an effort {name1} sneaks
into the camp and penetrates the wooden building, which looks
pretty much like a storage. Inside {heshe1} sees so many different
things that it becomes hard to tell, what is actually stored
in here. Jewelry, money, paintings, sculptures - it looks like
skinheads are robbing everyone around and store the catch here. It's
a pirate treasure! Hearing some kind of a fuss on the street,
{name1} grabs several small things, lying closely, and silently
exits the building to take a direction to the locomotive.
You're getting 130$""",
        ),
    },
    {  # 8
        "name": "Auto Repair",
        "desc": """An old highway, stretched out to the left of the railway, has taken
your attention, and your supervision at some moment pays
off: you see an auto repair shop. It's small, just three
car places without utility rooms, but it's still something.
Roller shutters are all closed, window glasses are intact
- everything says the place is over watched by someone.
It makes sense to send a scout to take a closer look
at the building. It's an auto repair shop after all,
meaning there should be tools, which can be used for
the locomotive maintenance.""",
        "results": (
            """You're sending {name1} to the auto repair shop for a closer look.
While your messenger approaches the building, you notice some kind
of a movement inside it - shadows slide near windows, but nothing
promises troubles so far. You do a loud whistle and show {name1}
that it's better to stay sharp. Nodding {hisher1} head, {heshe1} slows
a little and moves further with more caution. Suddenly all three
roller shutters explode, and orange fire mushrooms break out of
the building. Shock wave knocks {name1} down to the ground, and
makes locomotive windows shaking. Getting up, {name1} runs back
to you, while you're observing the auto shop burning remnants.
Seems like something gone terribly wrong inside it...
{name1} getting Nervousness""",
            """{name1} takes {hisher1} gun and moves to the auto repair shop by your
command. On the middle of {hisher1} way the right roller shutter
moves up with a loud bolt, and a couple of men start to shoot at
your messenger. You upper your gun and cover {name1}. Just several
seconds of shooting, and both of the rivals fall to the ground. With
caution {name1} continue the way, but suddenly an explosion tears
the shop, throwing its plastic and metal walls to all sides at
once. {name1} falls to the ground because of the shock wave, but
gets up in the next seconds. Looks like no serious wounds happened.
While {heshe1} returns back to the locomotive, you're thinking if
there were more people and they decided to explode
themselves, or it is just an occasional catastrophe?
{name1} getting -25 health""",
            """{name1} takes a direction to the auto repair shop. You're tracking
{himher1} from the locomotive. Silently your messenger gets closer and
opens a roller shutter. Nothing happens, no shooting, no people
appearing, looks like the building is abandoned recently. {name1}
carefully enters inside and disappears from your gaze for at least
ten minutes. You're becoming nervous little by little, but finally
{heshe1} exits the shop. You see nothing in {hisher1} hands, and,
climbing to the locomotive, your messengers confirms your
thoughts - there was nothing. Someone already looted the
building, taking every-single-thing useful.""",
            """{name1} takes {hisher1} gun and, following your command, walks
towards the auto repair shop. It's clear that someone is in there:
through the window you see shadows moving. {name1} see them as
well, so {heshe1} makes a circle around the shop and climbs to
its roof. Ceiling windows make it possible for {himher1} to drop
the ambushing skinheads even before they understood who's firing.
Climbing down and entering the shop, {name1} walks out with someone
else. When close enough to the locomotive, {heshe1} explains:
"There was a hostage there. Thought maybe we can give a ride."
Looking at your scout's companion, you evaluate a possible recruit.
One person can be recruited""",
            """{name1}, following your command, takes {hisher1} gear and walks
to the auto repair shop. Getting closer to the building, {heshe1} opens
a roller shutter and enters inside. For some time silence flies in the
air, but suddenly you hear shots. Three, four-five, six... A couple of
seconds passes, and you see {name1} in the entrance arch, showing you
that everything is okay. Disappearing in the shop inners, {heshe1} returns
back after a half of minute with a big metal box. Tools, ha?! You're
commanding others to help {himher1} with the catch, while you're
listing the parts of the locomotive, which should be given an
engineering attention in the first place.
Adjutant durability +70""",
        ),
    },
    {  # 9
        "name": "Stone Circle",
        "desc": """Three meters fencing, standing right in the center of the meadow,
attracted your attention from a very big distance. Looking through
binoculars, you see semicircle light grey parts of hollow cylinders,
put one to another, organizing a circle of stone walls, covering
about sixty square meters. The camp is tough! A big wooden tower
standing in the center of the stronghold seems to be not inhabited,
but ones who built it definitely were planning to stay here for a
long time. Unlikely they left the camp. So, it requires to be very
careful on reckoning the place: it can turn into a good catch as
well as into a hard fight.""",
        "results": (
            """You instruct {name1}, {name2} and {name3} to approach the camp
and take a careful look at it. Your messengers energetically jump
down to the ground and walk to the place. Suddenly, you see some
kind of an unrest move on the top of the tower. In the next moment
a loud shot thunders in the air, and a bunch of sparks flyes out
of the Adjutant hull. Inclining your head for a second, you gaze to
where the bullet hit, and see a big smoking hole. An anti-tank
rifle?! Can't be! You shout to your scouts to get back to the train,
and giving a command to start engine. No more shots rattle - looks
like the camp beholders are satisfied with your retreat. Still, the
big hole in the hull has to be repaired now. Not good!
Adjutant getting -60 Durability""",
            """{name1}, {name2} and {name3} take their gear and go to the camp.
Nothing promises troubles, your messengers enter the concrete circle.
Several minutes passes, and you see them exiting back. There is nothing
in their hands... Still, while they're getting closer, you understand
that something bad happened inside the camp. The first who started to
speak, {name2}, explains: "There was a trap. About forty well-armed
fighters, professionals. They took our money, but let us keep our guns."
{name1} interrupts the speech: "Let's move before they decided to attack
the train itself!". Weighing the information, you decide not to disturb
the camp dwellers anymore. Forty professionals - it's too much.
You're losing 50$""",
            """You're sending {name1}, {name2} and {name3} to take a closer
look at the camp. Nothing promises troubles, the place stays quite,
your people enter the concrete circle, and about ten minutes you
don't see or hear any fuss. Calmly exiting the camp, scouts move back
to the Adjutant. Getting closer, {name3} reports to you: "The camp
seems to be not inhabited yet. There are some tools, construction
materials, but nothing really valuable." Nodding your head, you wait
when your messengers get on the locomotive, and command to start
the engine. Maybe it's not as bad that you didn't meet the camp
owners. They seem to be serious people not to be crossed.""",
            """You decide that {name1}, {name2} and {name3} will be a good
recon party. Without delays they take direction to the camp.
Nothing promises troubles, you don't see any movement in the
camp and its tower, so your people entering the concrete
circle calmly. About fifteen minutes passed, and you see
them again, carrying something in their hands. "There was a
drug cache there. Really a lot of chemicals are carefully
buried within these walls, but {name1} have a sharp eye.
So, we've taken some of them, those medically useful
chemicals of course." - {name3} explains. Well, better
us than addicts.
You're getting 1 medicine""",
            """You choose {name1}, {name2} and {name3} to be a recon party this
time. Your people organizedly move to the camp, and, getting to the
entrance, start to shoot. You take your gun to be prepared to cover
them, but your scouts just sit near the entrance and shoot, shoot,
shoot. Several minutes passed, and the fight finally silences. Your
messengers enter the camp, and the waiting starts... About fifteen
minutes later you see your people exiting the concrete circle. "There
were a lot of armed guys, but they were mostly stoned bad. We've
cleared the place and gathered some money." - {name1} reports and
puts a bunch of dollars on your desk. - "Nothing more useful for
us there." - {heshe1} finalizes. Well, that's still a victory!
You're getting 120$""",
        ),
    },
    {  # 10
        "name": "Abandoned Car",
        "desc": """At the first look you didn't pay attention to a
dark green spot in the middle of the meadow. But in the
next second it becomes clear that it is not a part of the
landscape, it's a car! It looks abandoned and old, standing
there for a long time. Still, glass seems to be unbroken,
and doors are closed, so it may make sense to check if
something remain within.""",
        "results": (
            """As the car stands in 50 meters far from
railway, you're sending {name1} alone to search it for supplies.
{name1} approaches to the car thinking: where to look first?
Glove compartment! Of course, {heshe1}'s opening the door, taking
a sit and starts to feel the contain of the glove compartment.
"It's too hot in this car." - {name1} thinking, but in the next
moment {heshe1} feels something crawls on {hisher1} legs.
Turning {hisher1} look down {heshe1} sees hundreds of big red
ants creeping on {hisher1} knees and chest. Trying to drop them off,
{heshe1} only makes them crawl on hands. With screems {heshe1}
jumps out of the car and starts to roll on the grass trying
to deal with agressive insects.
{name1} getting -50 energy and -15 health""",
            """As the car stands not very far from
railway, you're sending {name1} alone to search it for supplies.
{name1} energetically moves to the car and starts a find. The
car looks old, and feels hot inside, but seems like no one looted it
yet. Still, vehicle insides doesn't contain anything interesting. {name1}
gets out and makes a circle around the car. Trunk - here is the place
to search! Opening the trunk {heshe1} sees a shovel and a big sack.
Fermer staff? Taking out {hisher1} knife, {heshe1} flogs the sack. The
first thing that falls from it is a human skull with two small holes
on the occiput. Looks like someone just tried to cover his tracks...
{name1} getting -15 energy.""",
            """As the car stands close to a railway, you've
sent {name1} alone to look for supplies in the vehicle. {name1}
moves to the car, opens it and gets inside. It's hot and dusty within
the car, every movement raises the dense fug, but {hisher1} search
doesn't end with nothing. It appeared that a first aid kit is still there,
and, opening it, {name1} sees that it contains several not overdue meds!
That can regain 10 health of a single character.""",
            """The car stands close enough to a railway to fear
nothing, so you're sending {name1} alone for a looting. {name1}
runs to the car, and disappears inside. From the train you're
not able to see what's {heshe1} doing there, and it takes a
half of hour to wait for the results. {name1} jumps out of the
car and moves to you with a small box in {hisher1} hands.
"That guy wasn't very thrifty, I've found only these tools."
- {heshe1} says. Well, it's still better than nothing: we can
repair the train a little.
Adjutant durability +100""",
            """The car stand too close to the railway to fear
anything, so you're sending {name1} alone for a search. {name1}
closes to the car fast and starts to sort through it, throwing
away useless stuff, like toys, tent, rubber boat... You're
looking at all of these from the train starting to think this
stop is pointless. But then {name1} moves to the trunk, opens
it and screams victoriously. In the next second you see a big
grey tool box in {hisher1} hands, and uppering your hand with
a like-finger.
You're getting a Smoke Filter""",
        ),
    },
    {  # 11
        "name": "Meadow Tent",
        "desc": """The big dark green spot on the meadow attracted your
attention in the same moment. What do we have here? Seems to
be an abandoned tent. There are no signs of a bonfire,
smoke, or any human, so the camp is probably long forsaken.
Still something useful can remain there, who knows. It's
worth checking. The place seems to be open, quite and calm,
but it's little bit distant. If something will go wrong
it'll be a long way back for your crewmates. So a couple
of people should be sent for a surprise case.""",
        "results": (
            """You're sending {name1} and {name2} as a loot party.
Closing to the place they see several backpacks lying around
the tent. "I'll check the tent" - {name1} says and moves towards
it. {name2} takes {hisher2} hands on backpacks. One by one {heshe2}
opens them and sees ropes, climber equipment, fishing stuff, but there
is definitely no anything we can use. Suddenly {heshe2} hears {name1}
shouting from the tent. {name2} takes {hisher2} gun and jumps to the
crewmate. "Snake! A God damn snake!" - {heshe1} shouts and shows a bloody
hand. With a short gaze {name2} sees that there is no supplies in the
tent, so {heshe2} takes {name1} and pulls {himher1} back to Train.
{name1} getting -50 energy and -30 health
{name2} getting -20 energy""",
            """{name1} and {name2} are moving to the tent by your
command. The vibrations of the train still tremble at their feet, but the
still ground feels good. Air smells with withered grass, and cool
soft wind complements the place. But in the next moment {name1} feels
something else. Rotten meat. {name2} glances at {himher1} as {heshe2}
smells the same. Closing to the tent, they are starting to understand
what is the source of that stink. {name2} moves forward. "Let me do
this!" - {heshe2} pulls the zipper, and directs a lantern into the tent. Bodies!
Two rotten bodies, with bones sticking out, maggots, and nothing more.
Both characters are getting -30 energy""",
            """You've decided to send {name1} and {name2} to check the place.
They are taking their guns and moving to the tent, while you're
looking for possible threats. The meadow seems to be still and
quiet though. Your people are closing to the tent and starting
to walk around it and prowl. It appears there are several
backpacks at the forsaken camp place, but {name1} and {name2}
doesn't take anything with them. Nothing interesting? You're
waiting for several more minutes, but nothing changes. Finally,
{name1} and {name2} are opening the tent, taking a quick look
inside, and turning back to the Train. Obviously, there
was nothing useful in there. At all.""",
            """{name1} and {name2} are taking their things and moving to the
camp place. The meadow looks still, smells with withered grass,
warm wind makes the way pleasant. Closing to the tent, {name1} and
{name2} are starting to search for supplies through the things left
in the camp. Ropes, empty cans, some climber stuff, even an album with
old photos. Finding nothing, {name1} decides to take a look at the tent
- {heshe1} pulls the zipper and stick {hisher1} head into the stifling inners.
The tent looks empty at the first gaze, but suddenly {name1} caughts
{hisher1} eyes on a bottle of an energy drink. "Well, it's something!"
 - {heshe1} pronounces and takes the bottle.
Single character can get +40 energy""",
            """You're sending {name1} and {name2} to search the camp for
anything useful. Your people are getting to the forsaken tent
in two minutes and starting a find. You're seeing them
rummaging in bags left there, but nothing gives a sign of
lucky find. Done with backpacks {name2} opens the tent zipper
and moves inside. It takes a few minutes for {himher2} to deal
with the inner stuff, but to everyone's joy {heshe2} shows up
with a white aid kit. Smiling both {name1} and {name2} are
returning to Train with this burden.
You're getting 1 Medicine""",
        ),
    },
    {  # 12
        "name": "Old Hut",
        "desc": """Called by one of your crewmates, you're walking out of
the cabin and in the same moment seeing an old hut not far from
the railway. Putting binoculars to your eyes, you're looking at
it with good feeling. The house seems to be very old, built
with dark ancient logs. No smoke rises from the chimney. Taking
a few second to assess the prospects, you're thinking about
sending three people to search the place for anything that can
help you on the road. And, who knows, maybe someone is still
living in that ancient hut...""",
        "results": (
            """You're commanding {name1}, {name2} and {name3}
to gear up. People are taking their stuff and moving to the hut.
Approaching to it they see that the house is long abandoned, but they
moving into it for a lookup anyway. They splitting up: one person for
one room. Finding nothing, but dust, within half of hour, almost without
hope they open a floor basement entrance, and hooray! They see
several tens of cans! With such a catch, you decided to throw a feast!
But after several hours it comes clear that food expired.
All of your crewmates are getting -40 energy""",
            """{name1}, {name2} and {name3} are gearing up for
a walk. It takes few minutes for them to reach the hut. They see an
opened door, broken windows and wild weeds right before the entrance -
looks like this place is long forsaken. "Well, we're already here,
let's take a look!" - {name2} proposes. People are entering the house,
and in the next moment {name2}, who went upfront, falls on the ground
under a dog attack. {name1} and {name3} are raising their guns, but
they can't shoot, as it's a big risk to shot {name2} instead of the
big brute. Removing weapons they are getting to {himher2} to fight
the animal with their hands and handy items.
{name2} getting -20 health and -40 energy
{name1} and {name3} getting -25 energy""",
            """You're sending {name1}, {name2} and {name3} for a search.
People are easy running to the hut and disappearing in it. You're
looking for them from Train. Time passing, but nothing happens, so
you're starting to get nervous. Suddenly, you hear cries and two shots.
That doesn't sound good! Two minutes passes, and finally you're seeing
your people. They are moving fast to the Train, keeping their backside
on sights, though no one follows them. Coming closer {name1} explains to
you what happened back there: "Big dog, looks like it lives there.
And we found nothing". Your people are getting on the Train in
disappointed mood, and you're commanding to move.""",
            """{name1}, {name2} and {name3} are gearing up and taking direction
to the hut. Approaching to it, they see that wood building is long
abandoned: weeds are crossing the door, windows are broken, and
stillness fills the air. {name2} and {name3} are moving into the house,
while {name1} is standing outside on a watch. It takes a lot of time
for {name3} to check all the broken furniture in the first room, but
{heshe3} finds nothing. {name2} appears to become more lucky: {heshe2}
managed to find 50$ within a lady's old bag. With such a results
{name2} and {name3} are leaving the silent and dusty house, and
joining {name1} to get back to Train and others.""",
            """You're asking {name1}, {name2} and {name3} to go for a
search. They're taking their things and fastly moving to the
hut. Splitting up - one person to one room - they are
rummaging through old broken furniture, clothes that is
covering the floor with a thick layer of dust, metal dishes
and other stuff. Nothing useful comes to your messengers for
some time. "Oh, I got something!" - {name2} shouts loudly.
{name1} and {name3} moving to the room {heshe2} was checking,
and seeing a big tool kit. {name1} and {name2} are taking it
together and moving back to Train, while {name3} is
watching around for possible threats.
Adjutant durability +100""",
        ),
    },
    {  # 13
        "name": "Monastery",
        "desc": """You've caught your eyes on some kind of a big dark spike
from a very long distance. It was difficult to understand what it
actually is, but when the Train went around a hill, and the building
appeared before you in its best, you're seeing an old monastery. Its
black wood looks rotten, and the big hole on roof makes it clear that
this building was left years ago. Still the monastery in such a
wilderness place should have had a big supplies storage. Monks
probably didn't take everything when they were leaving.""",
        "results": (
            """You're sending {name1}, {name2} and {name3} to
the monastery. {name1} and {name3} are entering the old building,
while {name2} stays outside to cover crew mates retreat in case of
problems. For some time {heshe2} doesn't hear anything, so {heshe2}
relaxes a little. But in the next minute eerie noise comes from
the monastery. Taking a look inside {name2} sees that part of the
roof collapsed! Jumping inside {heshe2} start to call for {name1}
and {name3}: fortunately both are alive, though it takes some
time to dig them out of the wreck.
{name1} and {name3} getting -30 health
{name2} getting -30 energy""",
            """{name1}, {name2} and {name3} are moving to the
monastery. Entering it they see dust, web and a lot of wood wreck.
Looks like this building is looted long ago. Still {name1}, {name2}
and {name3} are splitting to search through the place faster.
Everything goes okay, until {name2} and {name3} hear an awful noise
and {name1} cry. They run to the sounds source, and find {name1}
felt through the old wood floor. Putting the guns down they are
getting to the hole to lift {himher1} from it. Its luck that {heshe1}
didn't get any injury, only a couple of big scratches.
{name1} getting -10 health and -15 energy
{name2} and {name3} getting -10 energy""",
            """You're letting {name1}, {name2} and {name3} to go for a find.
They are closing to the monastery fast, but in some moment hear
strange sounds and shouts. Moving closer to the building, they decide
to take a look through the window. {name2} sets a knee to give a lift
to {name3}, while {name1} stands near on a watch for troubles, as in
this noise they hear human voices, and they are many. Lifting up, {name3}
takes a look inside the monastery, and sees at least forty people
in there. Dirty, unkempt and completely crazy, they are ripping to shreds
several animals and eating them raw, all covered in blood. Seems like kind
of cultists are celebrating the End of the World. {name3} moves down and
silently explains what {heshe3} saw. Deciding not to disturb this mad
gathering, your people returning back to the Train.""",
            """On your command {name1}, {name2} and {name3} are moving
to the monastery. First they are approaching the building
quietly, but soon they see it's forsaken long time ago.
Entering inside, they find a lot of wood wreck. Air
smells mold and dust, silence soar in the old monastery.
Walking along the building, they discover a huge wall
icon, which seems untouched by time. Colors are
saturated, lack of any cracks or dirt - it looks
surprisingly well for this place. {name1}, {name2} and
{name3} spending a couple of minutes staring at it, and
its beauty in the midst of devastation inspires them.
{name1}, {name2} and {name3} getting +20 health""",
            """By your command {name1}, {name2} and {name3} going to the
monastery. Entering the old building they see a lot of wood and metal
wreck. Nothing valuable though, so they are splitting for a more
careful search. {name3} chooses the basement and goes down into it.
Walls looking wet, spider web is everywhere, but {heshe3} sees a big chest
in the first second. The rusty lock doesn't want to broke, so {name3}
calls others. {name1} and {name2} are coming into the basement and with
strength of the three they manage to open the chest. With pleasure they
see gold dishes in it! Most likely not very pricy today, still something.
You're getting +40$""",
        ),
    },
    {  # 14
        "name": "Wrecked Truck",
        "desc": """You're looking at the horizon line trying to find a sign of
a civilization. A couple of hours passed, and there were no single
building, litter or any other sign of human. What are these wild
plains? But once a distant grey spot attracts your eyes. You're
taking a look at it through your binocular. Truck! Even from that
big distance you can say it is damaged bad: at least one wheel is
ripped off and the metal cargo hold is dented. Still, you can
afford a short stop and fast recon of the transport crash site.
It's not accurate to say from that distance, but looks like there
are a lot of things scattered around it.""",
        "results": (
            """{name1} and {name2} are going to the distant truck in
hope to find something valuable there. It takes at least a half of hour
for them to get to the transport. Looking through a binocular you see
them walking around the car, squatting, touching some stuff lying
all around the truck... Time passes and passes, but you don't detect
any signs of a lucky find. Spending few more minutes there {name1}
and {name2} are returning back to the Train. "Someone outstripped
us." - {name2} explains. - "And didn't left a tiny bit of the cargo." """,
            """You're commanding {name1} and {name2} to go to the
truck and do a search through its last resting place. They are running to
the spot wearily and starting to rummage in the broken plastic boxes
lying near the car. Most part of them are already emptied by someone
else, but {name1} and {name2} not losing hope. And after rummaging not
less than twenty containers they finally see one untouched. Opening it
they are staring at a bunch of metal details. And tools! "With this stuff
we can repair our Train a little!" - {name2} whopping. They are taking
the box together and returning back to you with it.
Adjutant durability +50""",
            """You're sending {name1} with {name2} to take a look
at the crash site. {name2} takes a big backpack in hope there will be
something to bring back. Both they are moving to the damaged truck
and starting to search through the plastic boxes scattered around the
place. At the first minute they understand that someone already emptied
every container at the place, probably, the same one who attacked the
truck - they see a lot of sleeves, shot holes and some blood spots.
Taking a look inside the car cabin, {name2} finds that it wasn't looted
somewhy, and there is a small black plastic box with several syringes
inside. Gazing at the label carefully, {name2} understands that it's
some kind of a not very legal doping. Well, it's still something!
You're getting 1 stimulator""",
            """{name1} and {name2} are taking their guns and going to the damaged
truck. Fastly closing to it, they see a lot of sleeves and shot
holes - it's not just a crash, someone attacked the transport!
No bodies around, but your people notice several big and dark
blood spots. They are exchanging their glances and starting
to open plastic containers left right on the road one by
one. Mostly they are empty, but in one of them {name1} finds
a couple of aid kits. The first one seems damaged bad, but
the second looks okay, so {name1} grabs it. As {name2}
didn't find anything, but broken containers, your people
returning back to the Train with this only find.
You're getting +1 medicine""",
            """By your command {name1} and {name2} are gearing up and
taking a walk to the truck. Coming closer to it, they see that a big fight
was here. Looks like a gang attacked the transport to rob it or something
like that. {name1} and {name2} starting to rummage through the boxes
scattered all around. The fight site appears to be looted several times
by different people, hopes to find something useful are fading with every
second, but suddenly {name2} sees an untouched container with energy
drinks. "Hey, {name1}, come here!" - {heshe2} shouts. They are taking
the box together to bring it back to the Train.
Every character getting +35 energy""",
        ),
    },
    {  # 15
        "name": "Grey Smoke",
        "desc": """From a very long distance you are seeing a big, wide
straight column of thick grey smoke, rising from the forest
in a couple of kilometers from the railway. That seems
questionably. It can be either a big bonfire in a large
human camp, or a forest conflagration. In both cases the
situation can turn very dangerous for your messengers, so
it makes sense to send several tough fighters to see
what's going on there.""",
        "results": (
            """You're sending {name1}, {name2} and {name3} for a recon,
admonishing them to be careful and cautious. Your people taking
a direction to the wide smoke column. It takes fifteen minutes for
them to come to the place, where they see a lot of fire sources. That's
definitely a forest conflagration! Not thinking too long, your people
turning around and moving back to the Train. The dense smoke doesn't
give an opportunity to navigate the way, so your messengers are
moving astray along the forest, consumed by flames, trying to find
the right direction for not less than half of hour. Finally, they
see the Train main lighter you're turned on to help them to get out.
Covered with soot and small scorches, inhaled smoke they are
getting back on the machine.
{name1}, {name2} and {name3} getting -20 health""",
            """Your recon party is moving to the pillar of grey smoke.
You're tracking their progress from the Train through binoculars. Your
people are running to the forest spot fast and disappear between dark
green trees. Thick grey smoke rises and rises, getting more wide with
every minute. No, it's not a bonfire, it's definitely a conflagration.
Time passes, and you're becoming nervous, as three of your crew
mates are not showing up. Maybe it's worth to walk to the place by
yourself... Finally, you see them! Slow and tired, they return back
to the Train, inhaled a lot of smoke and probably intoxicated.
{name1}, {name2} and {name3} getting -25 energy.""",
            """{name1}, {name2} and {name3} are taking a direction to the smoke
column, by your command. Running fast, they come to the place in
twelve minutes and see a small wood hut, engulfed in flames. As there
are no screams or any movement, they could say there is no people
inside, at least, alive. The hut itself looks really ancient, it's most
likely was long forsaken. {name1}, rubbing {hisher1} forehead, warmed up by
the fire, makes a step back: "Let's go until it's grown into the forest
conflagration, and locked us inside a ring of flames!". Without any
arguments {name2} and {name3} turning around and taking a direction
back to the Train.""",
            """By your order, {name1}, {name2} and {name3} run to the grey
smoke column. Getting closer, they see a lot of red spots between
the trees - it's a forest conflagration, a big one! Throwing a
gaze to others, {name2} suddenly proposes: "Let's hunt! Animals
will run chaotically away from flames and smoke, and food is
something we always need." Thinking a couple of seconds, {name1}
and {name3} agree on that, and they three are going to the
forest... After twenty minutes of hunting they getting a deer.
Not very big, but it's even better - not a problem to get it to
the Train. "With this meat we can save some proviant money!" -
{name2} declares. - "Good job!"
You're getting +50$""",
            """Leaded by your order, {name1}, {name2} and {name3} moving
in the smoke column direction. Quickly getting to the place, they
see a big military truck, exploded with rocket launcher a couple
of hours ago. Blood, glass, metal and body parts of several
soldiers are scattered all around. Getting closer to the truck
cargo hold, your people see big boxes traces on the ground -
somebody already looted the place. Still, {name3} jumps onto
the truck to take a closer look at the inner part of the cargo
hold. To everyone's joy, {heshe3} moves outside the car with a
big plastic box of tools. Seems like assaulters have only
taken weapons.
Adjutant durability +100""",
        ),
    },
    {  # 16
        "name": "Silo",
        "desc": """When the Train started to move along sown fields, you've
concentrated your gaze. Where fields, there are people and
resources. And, yes, in some moment you see a big brown silo.
While the Train is getting closer, you discerning a couple of
small buildings near the metal reservoir as well. From that
distance they look quiet and deserted, but they are definitely
in a very good shape, so they are, probably, populated. It's
worth to send a couple of your people to check if there is
something useful for a road in there.""",
        "results": (
            """{name1} and {name2} becomes your messengers this time.
They cross the silent wheat field without any sign of trouble, but,
getting closer to the buildings, both rising their weapons. {name1}
points to the small hut first, and they take the direction to it.
Suddenly, they hear some kind of a stomp, and in the next moment
giant bull pushes {name1} with his brown head, knocking {himher1}
down to the ground. {name2} lighting rapid turns around and shots
near the bull's legs, but the animal doesn't pay any attention and
prepares to kick {name1} again. Turning {hisher2} gun into its head,
{name2} kills the brute. In the next second {heshe2} sees two more
bulls moving out of the barn, and that is enough for {himher2} to help
{name1} get up and spurt back to the Train.
{name1} getting -35 health""",
            """{name1} and {name2}, chosen by you as a recon party,
are heading to the brown metal cylinder of the silo. Field and the
buildings looking quiet, only wooden creak sometime sounds in air.
Still, getting closer to the place, your people start to suspect something
wrong, as there are bullet holes on the walls, window glass, and smell of
death flyes in the air. Silently moving through the buildings, {name1}
and {name2} doesn't see anything useful, anything at all, like somebody
cleared the house without remainder. Deciding to take a look at the silo
itself, your people are getting to it and opening the metal door. All of
a sudden, black swarm of flies breaks out of the silo, and your
crewmates see tens of dead bodies in there. "Let's go, before the author
came back!" - {name1} says, and they both fastly turning back.
{name1} and {name2} getting -15 energy""",
            """{name1} and {name2}, by your order, taking their gear
and moving to the silo. Nothing promises any troubles, but when
your people got closer to the buildings, four men with guns
showing up. They all look like hereditary rednecks, but
their M16 and Beretta's shine like it's a special forces
property. "What do you want? You doesn't look like skinheads."
- an old man steps forward. {name1} and {name2} exchange
glances, but before they started to talk, the man continues:
"We don't wanna hurt anyone, but you better go away". {name1}
makes a step back: "No problem, we'll go". Not touching locals,
your people making a slow turn around and heading back to you.""",
            """You're commanding {name1} and {name2} to go for a recon.
Your crewmates are closing to the place, but four hulk rednecks with
guns appearing towards them. {name1} and {name2} stopping, showing they
are not attacking. An old man steps forward: "Aren't you folks, who
came from abroad, and now killing skinheads all around?" {name1} and
{name2} exchange gazes. "Sounds like us" - {name2} answers. "Benny,
give'em paper!" - old man shouts. Tall guy approaches your people and
holds out a 50$ banknote. "Those bastards killed a lot of good folks
here." - the old man pronounces loudly. - "Thanks for clearing the
filth. Keep up the good work!" - he uppers his hand, and all the
rednecks turn back to their place. In good mood your people return.
You're getting +50$""",
            """You're sending {name1} and {name2} to take a closer look
at the place. Your messengers closing to the silo; silence meets them,
so they entering inside the buildings. The lack of furniture or
sign of people - seems like the place is forsaken, and hosts took
everything. Walking outside the last of three buildings, {name1}
points to the metal cylinder of silo with {hisher1} head.
{name2} agrees, and they both get closer to it. Opening the
steel door, they see that there is no even a gram of grain.
But pointing a flashlight inside the structure, they catch
their eyes on two metal boxes. {name2} jumps inside and opens
the first one: medicines! "Whoh!" - {heshe2} shouts and opens
the second one: a smoke filter! Now, that's a find!
You're getting 1 smoke filter and 1 medicine""",
        ),
    },
    {  # 17
        "name": "Wooden Barn",
        "desc": """Gazing at the horizon line, you've been overlooking corn
fields for the last two hours. But suddenly you see a big
dark wooden barn, standing on the edge of the green field,
a little covered with snow. Large entrance gates are opened,
but lack of chains and locks makes you think it was never
actually closed. So, it can be a good place for looting as
well as just an empty building. Who should be sent to
clarify the situation?""",
        "results": (
            """{name1}, chosen as your messenger, takes {hisher1} gear
and runs to the barn fast. You're staying sharp, looking at the
nearlands very careful, but nothing promises any troubles. Entering
the barn in the meantime, {name1} sees several old naked bodies,
hanged from the ceiling. Big numbers of bruises and dry blood
saying that these people were tortured. Moving {hisher1} eyes out
of the terrible sight, {name1} walks to the table, covered with
different stuff. Passports. Opening them one by one, {name1} sees
that all of them are foreign. Looks like this place belonged to
skinheads, and here they were killing those, who came from abroad.
Throwing the last gaze at the hanged, {name1} exits the barn.
{name1} getting -35 energy""",
            """You're sending {name1} to recon the old building.
Jumping off the locomotive, {heshe1} takes a direction to the barn,
but in the next moment you see a fire flash in the gates opening.
A big rocket with a loud hiss flies in the direction of the train
and explodes just in a couple of meters aside of its wheels. {name1}
makes several shots, and in the next second a man in a brown coat
falls from behind the gates. You're nodding to {name1}, permitting
{himher1} to take a look at the barn. Jumping off the locomotive,
you're observing the wheels: damage doesn't seem very serious, still,
it's damage. {name1} in the meantime exits back, showing that
there was nothing interesting inside the wooden barn.
Adjutant getting -60 durability""",
            """As the barn doesn't seem to be very inhabited
and it stands very close to the railway, you're deciding to send
{name1} just alone. Not poking around too long, {heshe1} runs to
the building, enters it and observes emptiness. It's clear that
owner took everything useful and flew away. The only strange
detail is several horse skeletons. They were left here, on leashes,
and now seem to be dead for a very long time. Not the most humane
decision! Still, we don't know what actually happened here, maybe
it's not what it looks like. Anyway {name1} returns back empty.""",
            """{name1}, chosen as your messenger, takes {hisher1}
gear and moves to the old barn. Quetly entering the building,
{heshe1} sees horse skeletons on leashes with bugs crawling
on them; the place seems to be not looted, so it can be said
the owner leaved in a hurry. Walking around, {name1} catches
{hisher1} eyes on an aid kit. It looks to be intended for
animals, but inside {name1} finds several syringes that
can be also useful for humans. Nothing more attracts your
messenger attention, so {heshe1} takes medicines and
returns back to the Train.
Single character can get +30 health""",
            """{name1}, driven by your command, jumps to the ground and
moves to the wooden barn. Nothing promises troubles, so {heshe1} enters
inside and starts to rummage through the old stuff. The place doesn't
seem looted, but all the things are really ancient - horse leashes, rusty
tools, dark blue cloth pieces... The owner probably was a jockey - {name1}
see several saddles and a blue jockey suit. Almost without hope your
envoy opens a first aid kit and finds a horse doping there. Hm-m, it
can be diluted and used for people as well. {name1} decides to take
the syringe and go back to the train, as there is nothing more in here.
You're getting 2 stimulators""",
        ),
    },
    {  # 18
        "name": "Refugees Camp",
        "desc": """From at least 500 meters you've caught your eyes
on some kind of a rubbish pile. Dark cloth pieces, black heaps
of bonfires and several colored plastic boxes... Getting
closer to the place, you understand, that it was a temporary
camp, most likely of foreigners, who came to Silewer in
search of a shelter. Well, that makes sense to take a look
at the place, maybe something useful left there. One
messenger should be enough.""",
        "results": (
            """You decide to send {name1} into the camp for a recon of
the place. As the nearlands are very open, only several trees
obstruct the gaze, you don't expect any troubles. {name1} gets
closer to the camp remnants, inclines and starts to rummage through
the things scattered around. Nothing attracts {hisher1} attention
for a very long time: empty cans, plastic bottles, cling film, and
nothing interesting. But in some moment {heshe1} sees a big cauldron,
covered with metal cap. Unlikely it's worth checking, but {name1}
opens it, and recoils in the same second - a vile cloud of rotten
food flyes from under it. Coughing wildly, {name1} turns back to
you. It appears, the things left in the cauldron was so ancient
that became even little bit poisonous.
{name1} getting -25 health.""",
            """You're choosing {name1} as a messengers for this recon.
Without delays, {heshe1} takes {hisher1} gun and jumps down to the ground.
The pale grass, covered with water because of the cold air and the
locomotive warmth faced with each other, appears to be very slippery.
{name1}, touching it with {hisher1} legs, loses balance, and falls to
the ground. You see several papers flying out of {hisher1} pocket, and
by wind blowing raise up really fast. {name1} gets up, and you try to
find the loss with your eyes, but looks like the papers flew away.
Recounting {hisher1} money, {name1} pronounces sadly: "Thirty dollars!
It's about thirty dollars just got lost in wind."
You're losing 30$""",
            """You're sending {name1} for a fast overview of the camp
remnants. Taking the gun, {heshe1} jumps off the locomotive and runs
to the place. It looks like someone attacked the refugees, as there
are several dark red blood spots on the grass, and bullet liners are
shining here and there. There are no bodies, but if there was something
useful in this place, it's already taken. Making a couple of circles
around and carefully looking at what's left, just for sure, {name1}
takes direction back to the locomotive. Nothing.""",
            """After a short overthinking you decide to send {name1} to
take a closer look at the camp remnants. Carefully watching around,
{heshe1} walks to the place. It appears there was a skirmish in
here: {heshe1} sees bullet liners and even a round of a scorched grass.
A grenade explosion, ha? There are also several bodies, skinheads and
others. The camp was left in a hurry, so {name1} starts to rummage
through the stuff scattered around. After several minutes of a search
{heshe1} finally see a personal pocket aid kit. Opening it, {name1}
finds a tiny syringe of a painkiller, water clearing tablets and
even more. That's actually a good catch!
Single character can get +25 health and +20 energy""",
            """You make a decision to send {name1} for the place recon.
Without long preparations {heshe1} moves to the camp. Getting closer,
{heshe1} finds a lot of bullet liners, blood spots, but no bodies. It seems
like there was a skirmish, but refugees successfully left. {name1} starts
to observe things remaining at the place. Just a couple of seconds
makes it clear that the camp dwellers left all the heavy equipment and
tools. Inspired, {name1} takes the most valuable things and returns
to the locomotive to ask others to join. In three runs you and your
people take almost everything useful from the camp.
Adjutant durability +100""",
        ),
    },
    {  # 19
        "name": "Motor Boat",
        "desc": """In some moment you catch your eyes on a big white spot in the
middle of the meadow. Your first thought is that it's a snow heap,
but it's not enough snow failing from the skies to gather this
big pile. Getting closer to the place, you understand this is a
motor boat, lying on a hindcarriage forsaken near the dark grey
stone of an old road. Looks like someone decided to get rid of an
excess cargo right in the middle of the way. Chances are low to
find something useful there, but it still worth sending a couple
of people to take a closer look at the boat.""",
        "results": (
            """You're sending {name1} and {name2} for a better recon of
the loss. They move to the white boat fast. It appears it stands
on a very-very old hindcarriage, rusty and shabby. Without any word
{name2} climbs on it to be able to see the boat inners, and in the
next moment the hindcarriage bends over with a loud creak. The
boat slides right to {name2} and pushes {hisher2} leg to the back wall
of the carriage. Trying to hold a cry, {name2} drops {hisher2} gun
and by two hands pushes the boat back. Understanding, that it can
turn into a serious trauma, {name1} also throws {hisher1} gun and
makes an attempt to help the crew mate. In several seconds of efforts
they push the boat back enough to release {name2}'s leg. Looking
at the bloody spot on trousers, they hurry up back to you.
{name2} getting -25 health""",
            """You decide to choose {name1} and {name2} for this outing.
Not delaying the fulfillment, they run to the boat and examine
it carefully. It seems like the loss owners didn't left anything,
except the boat itself, still {name1} notices a small metal box,
pinned down by the wherry to the hildcarriage bottom. "Let's get
it up a little, I'll kick the box with my leg." - {heshe1} proposes. With
no arguments {name2} gets on the carriage, and they make efforts
hard to get the boat up. Successfully releasing the box, they drop
the trans and, heavy breathing, open the conitainer. Nothing! "For
God's sake!" - {name2} whoops. - "The damn thing was overweighting,
and there is nothing! To Hell the stuff!". They both turn back.
{name1} and {name2} getting -20 energy""",
            """You've decided to send {name1} and {name2} for a revision.
Not pocking around, they run to the boat fast and start to
examine it. The trans seems to be long forsaken, covered
with dirt and in some parts even with rust. However, your
messengers see three small metal containers with padlocks.
Using the gun's butts, they open them one by one... and
they all are empty! "That looks like a joke." - {name2}
pronounces annoyed. - "A very stupid one." {name1} takes
several seconds to think, but in the end agrees on that
they were played. "Let's return to the Adjutant then."
- {heshe1} adds.""",
            """{name1} and {name2}, chosen for the task, running to the
boat fast. The white trans seems to be ancient, dirty and
even rusty in some parts. Its owners most likely have taken
all the things except the boat itself. Still, after a
careful examination, {name2} sees an old skin wallet, lying
in few meters from the hildcarriage. Getting to it, {heshe2}
opens the thing and see several old soaked dollar papers.
Well, if to dry them carefully, the recon can even turn
successful. With such a catch you messengers go back.
You're getting 70$""",
            """By your command, {name1} and {name2} take a direction to
the white boat. While getting closer to it, they see that it's really
ancient. Doesn't look like its owners left something behind, but your
scouts still getting on to the hindcarriage and take a look inside
the transport inners. And, luck, it appears that a kind of an aid
kit is still there. "A suite for a survival on water." - it says.
Opening the kit, your people check shelf life of the inners, and
yeah! Some things are still intact and okay to use. Closing the box,
{name1} and {name2} clap a high-five and run back to the locomotive.
You're getting 1 stimulator and 1 medicine""",
        ),
    },
    {  # 20
        "name": "Tents",
        "desc": """Gazing around, you're catching your eyes on a thick column of
smoke rising right from the ground. A look through binoculars
unveils that there is a tent camp at the bottom of the smoke
pillar, and you're giving your people an order to prepare for
a fight. At the next few seconds you understand that there
are mostly women and children in the camp. Looks strange -
during our days it's not very sensibly to travel without
several protectors. Still, they may had not be planning so,
and it's worth checking these people out. Maybe they need
assistance or something. Two messengers should be enough.""",
        "results": (
            """You're ordering {name1} and {name2} to gently approach the
tent camp not to scare inhabitants, and see what's going on in
there. Your fighters walking to the place, and you see them talking
with dwellers. Suddenly, several men rise from the tents, and in the
next moment jump to {name1} and {name2}! You can't say from that
distance, but seems like those people don't have guns, only knives.
Doing several shots, {name1} and {name2} running back to the Train.
No one follows them - probably, all the attackers were killed. Jumping
on the Train, {name1} shows a big cut on {hisher1} shoulder. "Those
bastards want to join skinheads! Tried to kill us to impress them."
You nod to the machinist, ordering to start engine.
{name1} getting -10 health
{name2} getting Nervousness""",
            """{name1} and {name2} following your order to gently approach
the camp and see if everything is okay there. They move fast
for some time, but at some point they both stop. Straining your eyes,
you're trying to understand what's happening. Suddenly, several thugs
with knives and metal pipes rising from the tents, and run to your
people. Doing a bunch of shots, {name1} and {name2} turning back to
the Train. You hear a loud shout: "Killing will make you skinhead!" It's
clear! Uppering your gun, you're starting to cover your messengers with
fire. They successfully getting to the Train, and you all dropping rivals
with coordinated shooting. "Thanks!" - {name2} breaths. {name1} nods to
you. "Okay, let's move!" - you command, and the Train engine starts.
{name1} and {name2} getting -15 energy""",
            """You're sending {name1} and {name2} for a short recon. They
take their gear and move to the place. You're tracking them from
the Train, seeing how they carefully approach the camp; a couple of
women go to meet them. Their conversation lasts for several minutes,
and then {name1} and {name2} turning back to you. {name1} climb to
the locomotive first: "They are travelling to the nearest city. Not
fighters. We proposed them assistance, but they don't want to cooperate
with us at any sense." {name2} appears to the left of {name1} and
shrugs {hisher2} shoulders, showing {heshe2} don't understand what
made those people to think that way. "Okay, let's continue!" - you're
commanding... Understandable, trust is not often that days.""",
            """You're giving an order to {name1} and {name2} to move
to the tent camp and see if everything is alright there. Your
people getting to the place in minute, and you see them
starting to speak with the inhabitants. The campers looks
calm and positive, so you're relaxing a bit... After several
minutes of talk, your people turn back to the Train, but you
also see one more person with them. They getting closer to
you, and {name1} explains: "Looks like we've found a
recruit. Do we have a free place?" Taking a quick gaze at
the newbie, you're starting to think if the crew needs one
more head.
One person can be recruited""",
            """{name1} and {name2} taking a direction to the tent camp
by your command. You're seeing them approaching the place and
speaking with inhabitants. After a couple of minutes of conversation
{name2} runs back to you, but {name1} continue to stand with two women.
{name2} jumps on the Train and explains: "No fighters, just several
females with children. They afraid of us, refusing to join, but me and
{name1} think we could give them a sack of coal. They are low on
resources." You silently nod, and {name2} takes a present for those
people. You're waiting for about 10 minutes, and both {name1} and
{name2} return back to you. "Good people" - {name2} finalizes.
"But very distrustful." "No wonder." - you're answering.
Single character can get Immunity""",
        ),
    },
    {  # 21
        "name": "Lying Man",
        "desc": """Thinking about the Stench nature, you're absently looking around
the Train, when suddenly you find yourself gazing at a human
body. It almost blended with withered grass and is covered
with snow - seems, the man is dead. There is nothing around:
no buildings, signs of human, even trails... Probably, he
died by himself... It makes sense to take a look at him,
who knows what can be found. Deciding to make a walk, you're
thinking who should you take as a companion. Nothing
promises troubles, so anyone should fit.""",
        "results": (
            """You're deciding to take {name1} as a companion for this small
walk. You both jump off the Train and take a direction to the body.
At some point you're noticing some kind of a movement. Is this
guy still alive? Or it's just a wind plays with the cape? {name1}
moves forward, and takes a seat near the body. Carefully, {heshe1}
turn over the man, and from under his corpse a mustard color
cloud rises suddenly. Not having time to react, {name1} inhales
it and jumps aside the body. "Oh, shit!" - {heshe1} inclines and
spits. "Faster, go for the doc!" - you're pushing {himher1} to
the Train and stopping your breath as well.
{name1} getting Weak Immunity""",
            """You take your gun and turn your head to the locomotive deckhouse:
"{name1}, you're with me!". Like {heshe1} waited for these words,
{name1} walks out on air, and you both jump out of the Train. It
takes just a half of minute to approach the body, wrapped in a grey
cape. "Wait!" - {name1} uppers {hisher1} hand and points to some kind
of a small hills around the corpse. Interesting! {name1} lifts a stone
from the ground and throws it to the lying man. In the next moment
everything turns black, and you hear a terrible din. After several
seconds of emptiness, you're returning back to the reality. {name1}
gets up from the ground and shakes off. "That looks like a homemade
mine." - {heshe1} pronounces loudly. Fortunately, no one injured.
{name1} getting -10 health""",
            """You're asking {name1} to follow you on this walk. Without
counter-arguments, {heshe1} takes {hisher1} gun and moves to the
right of you. The silent pause holds for some time. You know what is
the cause. "You're okay?" For a couple of seconds you think {name1}
won't answer, but {heshe1} does: "Yeah... yeah. My brother in the
better world now. I'm okay." At that point you're approaching the
lying body, taking a knee down near it and turn it over. The old
frozen corpse creaks. He's dead. A lack of wounds sais he indeed
died naturally, without someone's "help". No one looted the body,
but it anyway doesn't look like a rich source, so you're deciding
not to disturb the dead man. "Let's get back!" - you pronounce,
and you both taking a direction to the Train.""",
            """You're commanding {name1} to gear up. In a couple of minutes
{heshe1} jumps off the Train and follows you in the lying body
direction. Fast approaching the spot, {name1} moves in front of
you and takes a knee sit near the man. "Dead, definitely." - {heshe1}
pronounces. - "It looks like he was travelling somewhere distant.
No supplies, no money, he doesn't even have warm clothes. Died here
alone." You're making a step towards {name1}: "These times no
one should be alone." {name1} stands up: "Good we have our own crew"
- {heshe1} smiles to you. - "Thanks, you've brought us together."
Silently nodding, you point to the Train with your head.
Crew cohesion +6""",
            """You're taking {name1} as a companion for this walk and
jumping off the Train. It takes a half of minute to get to the body.
Silently approaching to the man, {name1} inclines, then turns him over.
Surprisingly, you both see an old open-eyed face, covered with blood
and dirt. The man is alive! Making a step back, {name1} gazes at you.
The old man in the mean time starts to speak: "If it's in you, cut it
out! You better cut it out!" He uppers his hands and starts to shake
them - the sleeves goes down, unveiling his arms, covered with fresh
cuts. "When they'll got you, cut them out!" - he repeats. {name1} makes
a step towards you and silently pronounces: "We better leave him."
Taking a moment to overthink, you're deciding that it's a good idea,
this man is mad and most likely diseased. No way to help him.
Single character can get Masochism""",
        ),
    },
    {  # 22
        "name": "Assassin",
        "desc": """In the moment the Train stopped, you're finding your eyes on a dark
silhouette of an armed man. He doesn't seem to be aggressive, so
you're giving him some time to come closer. "Hey, guys!" - he says,
smiling. - "Nice to meet you, I may need some help." "We're listening" -
you answer. "Locals paid me to convince to deal with skinheads,
who camped in the nearby mine. There are a lot of those imbitsils,
so I'm gonna ask you to join me. I'll give you half of my lucre."
You're taking an attentive look at the man. He seems to be a pro,
well-armed, trained and cold blooded. Hitman probably. Doesn't look
like he's going to lure you into a trap - he could kill you much
easier, if he'd want. Than why not to give him a hand!?""",
        "results": (
            """Several hours passed since you've sent {name1}, {name2} and
{name3} to help the assassin, and you finally see your people walking
back to the Train. All three, they are covered with dirt and soot,
their clothes torn. Helping each other, they climb up to the locomotive,
and {name2} reporting: "We've entered the mine and started to shoot
skinheads one by one. But something went wrong, and we've been
littered with stones. It took us an eternity to dig out." "An
eternity!" - {name3} repeats, inclining {hisher3} head. {name2}
adds: "The hitman is dead we suppose." Ordering your people
to get clean and rest, you're commanding the machinist to take off.
{name2} and {name3} getting Fear of dark""",
            """{name1}, {name2} and {name3} following the hitman and go dark
for several hours. The lack of any signs of your people makes you
little bit nervous, but in some moment you see them returning back
to the Train. They all look tired and dirty, but no one seem to be
seriously injured. "No good news." - {name1} explains to you,
climbing up to the locomotive. - "There was tens of skinheads,
and we barely made it out there alive. Our new friend wasn't so
lucky." - {heshe1} sighs. - "We have a couple of scratches,
nothing serous." Well, at least everyone is in one piece; the
locomotive engine starts to warm up.
{name1}, {name2} and {name3} getting -10 health""",
            """You're sending {name1}, {name2} and {name3} with the smiling
assassin. After all, skinheads are the disease to be cured, no matter
if it is an end the world. A couple of hours passes, when you finally
see your people. They look neutral, and there are no the hitman
with them. Getting closer to the Train, {name3} explains what's
happened: "Those bastards were waiting for us. Our friend didn't
make it, and we barely made it out there ourselves." They all climb
up to the Train. "We better hurry up" - {name2} adds. - "Who knows,
they could have decide to follows us." Well, on that you all agree.""",
            """You're sending {name1}, {name2} and {name3} with the hitman
as a support. They fastly disappear behind the hill, and two
hours passed, before they get on sight again. Throwing a gaze
through binoculars, you see that everyone is okay. The hitman
is not with your people. "We've finished them all." - {name1}
says, getting closer to the Train. - "The man gave us some
money and vanished, like he never been there." Climbing up to
the Train, your messengers moving each to their places. Well,
the job is done, bad people were stopped, and some money
earned. Sounds like a lucky outing!
You're getting 100$""",
            """{name1}, {name2} and {name3} following the hitman as a
support. A couple of hours passes before you see your people again.
From 200 meters you can see that their campaign was successful -
they smile and actively discuss something. Getting closer to you,
{name1} start to describe you the details of the operation, others
joining him. "This guy was like a shadow!" "{name2} shooted three
bastards in a second!" "We've been moving like a single one person."
The hotly told history sounds to you like a battle to remember!
Everyone done something, the vespiary burned to the ground, and
every messenger is very impressed by the hitman skills.
You're getting 100$
Single character can get Fast hands""",
        ),
    },
    {  # 23
        "name": "New Outpost",
        "desc": """From a big distance you're catching your eyes on a small building,
near which a lot of people silhouettes are looming. Getting closer,
you see a lot of construction equipment, and the building itself
looks like a small outpost, still in construction progress.
Concrete walls, a couple of bases for towers, big metal gates...
Workers, hearing the Train engine, directing their gazes at you,
without any sign of aggression. Definitely, they are not
skinheads, but their uniform and equipment seems to be in a
very good shape - aren't they came here by government request?
It's worth sending a messenger to have a word with them at least.
Maybe they have some valuable info about the situation in the
country, or just nearby lands!?""",
        "results": (
            """You're listing the crew within mind, and decide to send {name1}.
Without delays, {heshe1} grabs {hisher1} gun and walks to the construction
sight. You take your binoculars and point it to your fighter. Nothing
wrong seems to be happening, {name1} simply speaks with two workers,
but suddenly you hear a loud crash. Gazing the place to which workers
run, you see a man pinned down by a big metal object: dark red blood
spreads all around him, his shouts tear the air. Moving the binoculars
away, you see {name1} running back to the Train. "They build new
outpost to hold skinheads spreading." - {heshe1} says, climbing up to
the locomotive. You see that {hisher1} eyes are open wide, and the skin
became pale. "You're okay?" Turning head to you, {name1} keeps silent
for a second... "Yes. I guess. Just..."  - {heshe1} looks at the outpost.
{name1} getting Hemophobia""",
            """{name1} seems to be a good candidate for the task, so you're
giving {himher1} an order to speak with those people. Jumping off to
the ground, {heshe1} goes to the construction sight and speaks with
workers for some time... Does one more weaponized camp protect
from the Stench? Probably, not, still, they are building it... You
see {name1} giving something to the workers, and next turns back.
Jumping back to the Train, {heshe1} explains: "These people are trying
to build their own stronghold, for those, whom nearby cities doesn't
want to invite. I've gave them some money, 'cause it looks like a good
idea for me." - {name1} throws a gaze to the construction sight. Well,
who knows, who knows, this idea can also be completely useless.
You're losing 40$""",
            """{name1} seems to be an appropriate person to speak with
workers, so you're sending {himher1} to the construction sight. It takes
ten minutes for {himher1} to get there and to speak with a couple of
workers with dirty faces and orange uniform. Nothing wrong happening,
so you're sitting down to your chair, waiting for {name1} to return.
Entering the deckhouse, {heshe1} gets closer to you: "Well, they are
building a new outpost to hold skinheads in this region. The nearby
city supports this project, so I suppose they are in better condition
than we are." Nodding your head, you're giving an order to start engine.
At least that means the next city is a good place for a stop.""",
            """Running through the crew list, you're deciding to send {name1}
for negotiations. Energetically {heshe1} takes {hisher1} gun and directs
to the construction sight, but in the next minute a couple of
workers are moving out of the outpost, towards {name1}. Getting
closer to each other, {name1} and workers exchange handshakes, and
all three going to the locomotive. You see that builders' faces
become more interested with every step. "Wow, what a beautiful
machine you have!" - one of them pronounces. - "That's actually
a stronghold on wheels! That's incredible!" - the same man
proclaims. - "You're very lucky to get your hands on it!"...
After several minutes of talk the workers turn back to their
outpost, but the jealous words still make you proud.
Crew cohesion +6""",
            """You're deciding to send {name1} to negotiate with workers.
Jumping to the ground, {heshe1} moves to the spot, and sees that one
of the builders went out of the outpost towards {himher1}. After a
minute of talking {name1} figures out that these people are building
a new outpost to hold skinheads in this region. The worker asks {name1}
to follow him, and they both go to the opposite side of the camp. There
your messenger sees a lot of dead bodies laid out in rows - about
forty men. "These are skinheads bastards we already stopped here."
- the worker brags. "Looks significant!" - {name1} answers and means
it. It's really significant to clear so much filth. "Right, I have to
return to my people" - {heshe1} takes leave of the constructor and,
throwing the last gaze at bodies, takes a direction to the Train.
Single character can get Bloodthirsty""",
        ),
    },
    {  # 24
        "name": "Cargo Column",
        "desc": """For the last ten minutes you've been observing a road, which
turned to the railway and has been following it in a straight
parallel. A lot of pits and cracks showing that the road isn't
very well maintained, most likely it's really old. Still, in the
next minute you see a big column, staying on the grey concrete:
bus, several big trucks, filled with different stuff, such as
furniture, metal and garden inventar, and a couple of smaller
cars. Several heavy machine guns and at least ten weaponized
men are complementing the picture. The beholders doesn't look
like thugs, so it's probably makes sense to speak with them.
Maybe they have something to trade or exchange.""",
        "results": (
            """You decide that {name1} and {name2} will be a party - those
people are armed after all. You fighters climb down from the Train
and direct to the cars. Getting closer, they start to speak with
column defenders, and in some moment they both move up their guns
and start to shoot. Car column spurts away in the same second, which
is strange, as they had more people than you. Still, your messengers
returning back to you, both with light wounds. Climbing to the
locomotive, {name1} explains: "Marauders, taking the stuff out of
the regions covered with the Stench. Stealers in the other words."
- {heshe1} takes a look at {hisher1} wound on the left shoulder. - "I'll go
find the doctor." Gazing at smoke clouds, you think how organized
and weaponized the marauders are. Seems a big business.
{name1} and {name2} getting -20 health""",
            """You choose {name1} and {name2} to negotiate with the column men.
They both carefully getting closer to the cars and start to speak with
a big guy in a cap. You're analyzing the column itself: well-armed
people, cargo cars, good organization - all the signs of professionals,
still, they doesn't show any aggressive intentions. Several more
minutes passes, and your people turning back to the locomotive. The
car column starts the engines. {name1} and {name2} getting closer to
you: "So, they are government people, transporting cargoes and people
between several cities. Trying to do whatever they can to help folks
in the country." Okay then, it's not a bad piece of news. Good to see
that rulers are still in a strive, together with people.""",
            """{name1} and {name2} taking a direction to the cars column by your
order. While they're approaching the big man meeting them, you're
analyzing the cortege: a lot of cargo, a lot of guns, and...
refugees!? You didn't see them at the first minute, they probably
were hiding, but now started to peek out. Dirty, ragged, different
aged... You patiently wait for your people to figure out the
details. They take something from the big man and turn back
to the locomotive. "This is a help from a local city - they
transporting people away from the Stench." - {name2} tells,
entering the deck house. - "They kindly gave us some medicine."
- {heshe2} puts a small white box on the table. Well, that's
actually very kind of them!
Single character can get +30 health""",
            """You decide to send {name1} and {name2} for a speak. They take
guns and go to the cars, while two men move towards them
from their side. After few seconds of talk {name1} and {name2}
take guns away and follow the men. You see they're helping
to pull up a big object, probably fallen out of the truck.
Is it why they stopped? Looking at smiling fighters, telling
goodbye to your people, you see that yes. While their cars
start to move, {name1} and {name2} come closer to you, telling:
"Positive guys! Transporting people away from the Stench.
Asked for help and gave us this" - {name2} shows dollars.
You're getting +90$
One character can get Liberal""",
            """You're sending {name1} and {name2} to negotiate with the column
guys. They carefully approaching the men, and starting to talk.
Several minutes passed, and then you see a silhouette jumping out of
the bus and following your people. What does it mean? "Hey, captain!"
- {name1} says loudly. - "These are refugees transportation party, came
from the nearby city to help people to get out of the Stench. No any
problem with them, but there is a recruit, who wants to join us. What
will you say?" You're viewing the candidate from high to down. Well,
that is something to carefully think about.
One person can be recruited""",
        ),
    },
    {  # 25
        "name": "Ill Deer",
        "desc": """For a long time you've been observing only light snowflakes, calmly
moving in the air, bringing thoughtfulness. But in some moment a
strange low distant sound attracts your attention. First you think
of an old airplane engine, still, after several seconds you understand
it's an animal. In the same moment you see something dark on
the rails ahead, something blocking your path. Fastly taking the
binoculars to your eyes, you point it to the dark thing... And it
appears to be a deer! Huge, old and weak, most likely very ill,
lying right on the rails, crying to around. The animal better
be moved somewhere else! It'll be not very easy to deal with the
problem by your own, anyway three people should remain at the
Train to keep it safe. Who should you choose?""",
        "results": (
            """{name1}, {name2} and {name3} stay at the Train. {name1}
and {name3} jumping off the locomotive, start to look around, while
{name2} enters the deckhouse. The lights are off! {name2} uppers {hisher2}
gun and silently moves to the lower level. The strong smell of diesel
flows around, the lights are also off here. {name2} takes a couple
more stepts in the switchers direction, when something jumps out
of the shadows and pushes {himher2} strong. Barely standing at {hisher2}
feet, {heshe2} sees a shadow of a human, slipping out of the door.
Hearing something, {name3} turns around and see a thin pale guy
running out of the door, jumping down to the ground. He has nothing
in his hands, so {name3} decides not to shoot. "He didn't get time
to grab anything." - {name2} says, appearing at the door. - "Let go."
{name2} getting Fear Of Dark""",
            """{name1}, {name2} and {name3} stays near the Train by your
order. They promptly take positions around the locomotive, waiting for
your return. It didn't take long from you to move the ill deer away
from the rails, so you're returning fast. Jumping on the Train, you
enter the deckhouse and take a sit at your table... Something's
wrong. All of your stuff lie as it always does, but... something
changed. Opening the bottom drawer, you clearly see that some of
your money disappeared! You fastly exit the deckhouse and start to
gaze around. No one. Nothing. All of your fighter seem to be quiet
and calm. Someone entered the locomotive, took some of your money
and vanished! Converting the money, you see that not actually
much of money was stolen, 40$ probably. Anyway, it's no good!
You're losing 40$""",
            """You're leaving {name1}, {name2} and {name3} to keep the
locomotive safe, and take a direction to the deer. Just several seconds
passed, and your sentinels hear some kind of a fuss in the deckhouse.
Opening the door inside, they see a girl about 18 years old, who
rummage through the things left on the table. She doesn't look thin,
or dirty, or anything like this. Good clothes, well face, clean hairs.
"Go away!" - {name3} uppers {hisher3} gun. Seeing that it's better not
to try tricking, the girl silently moves her hands up and takes a
direction to the exit. {name3} follows her outside to ensure she won't
do anything stupid, while {name1} and {name2} gazing at each other.
What was that? {name2} opens the aid kit: "I have an idea." Empty
syringe of painkillers lies inside with a blood drop on it. Addict!
You're losing -1 medicine""",
            """You're ordering {name1}, {name2} and {name3} to stay, while
you deal with the deer. In some moment all three sentinels hear
fuss in the deckhouse. Not poking around, they jump to the
train and open the door. An armed thug is waiting them, aiming
his pistol to the entrance, but not shooting. Your fighters
doesn't accept this act, so they do several shots at the man.
With a wondering face he falls down on the floor. {name1}
silently moves closer to him and raises a bunch of dollars.
"Stealer!" - {heshe1} finalizes. Slapping the man's pockets,
{heshe1} raises even more money. "Well, who came with a sword
to us..." - {name2} says, getting closer to get rid of the body.
You're getting 70$""",
            """You're taking your guns, but suddenly a kind of a grenade flies
into the open window. Grey tear gas starts to spread around fast with
a loud hiss. Pushing {name1} to the exit, you're grabing {name2}'s
shoulder with another hand and pull {himher2} with you. Exiting on
the air, you all upper your guns, trying to look through the tears.
For several seconds you don't see anything specific, but then you
catch your eyes on a couple of distant people. Without delays you
aim your gun and start to shoot at them, making them run away really
fast. Silence falls on the meadow, and you all take several minutes
to deal with tears. When your gaze clears completely, you take one
more careful look around, but no one seems to be in nearlands. Good!
The ambush was not successful. Time to ventilate the deckhouse.
Single character can get Deep Breath""",
        ),
    },
    {  # 26
        "name": "Injured",
        "desc": """You've noticed a big grey truck long ago. It has been riding in
parallel with you for about twenty miles, and now it started to
approach - the highway probably turned to the railways. The truck
seems to be in a good shape, and when it got closer you see that
it has several massive machine guns. Still, the people on the car
doesn't show any aggressive intentions, and the car stops on railway
to road crossroads in two hundred meters in front of you. Looks like
a dialog invitation, ha!? That makes sense to send a couple of people
to speak with those guys to get info about nearlands.""",
        "results": (
            """You're sending {name1} and {name2} for a talk with the truck
party. Approaching quetly, your fighters smell something heavy.
A guy from the truck jumps to the ground: "Yo, folks!" - he smiles.
- "Have wounds?" - he examines both your messengers. - "We're taking
injured folks from all around, trying to get them to safety." He leads
{name1} and {name2} to behind of the truck and shows its inners.
There are at least fourty people covered with blood and dirty medical
bandages. So, that heavy cold metallic smell is their blood. {name2}
feels small needles started to run on {hisher2} back. "Skinheads
become more aggressive." - the man from the truck pronounces sadly.
- "We do our best..." Convincing him they are okay, your people
return back to you, trying to deal with the impact of the seen.
{name2} getting Nervousness""",
            """{name1} and {name2} taking a direction to the truck by
your order. Getting little bit closer, they see a dark inscription
on the car: "Injured". So, these guys are helping wounded people
around the place? Sounds good! {name1} and {name2} speed up their
steps, but in some moment people on the truck see something wrong
and start to shoot! Not giving them any chances, you all start
to fight back, and, feeling that gun power is on your side, the
truck spurts away really fast. What's happened? No one seems to
be wounded, and that's good, but, taking a look at the locomotive,
you see several big holes, made by the truck's machine guns.
Adjutant durability -50""",
            """{name1} and {name2} start to move to the truck by your
command. While they are getting closer, a man from the truck jumps
down to the ground and meets them. "Hi, folks!" - he says loudly. -
"We're trying to get these injured people to the nearest city". Oh,
here is what the truck for! Your messengers follow the man, and he
shows them that there are at least thirty people in the car, all
covered in blood and white medical bandages. "Do you have seriously
wounded guys?" - he asks politely. "No, no, nothing we can't handle,
thanks." - {name1} answers fastly. - "That's nice to see someone
cares" - {heshe1} adds. "We all should do what we can!" - the man
pronounces loudly. - "Okay then, we better hurry!" - he smiles once
again to your messengers and moves back to the truck.""",
            """{name1} and {name2} start to move to the truck. A man
jumps down from it to meet them. "Hey, folks!" - he greets them
loudly. - "If you have badly wounded guys, we can take them to
the nearest city." {name1} and {name2} think for a couple of
seconds. "Well, we're okay, I guess." - {name1} answers to the
man. "That's great news!" - he almost shouts. - "Maybe you need
one more gun? We have a potential recruit for you." - he whistles
to the truck, and someone in baggy clothes jumps down to the ground
and takes a direction to your people. "The wounds are healed, and
the element is eager to go to war! We're little bit tired already!"
"Well, that's something for our captain to decide" - {name1} answers.
One person can be recruited""",
            """Your messengers, {name1} and {name2}, take direction to
the truck. A man jumps from the car down to the ground and starts
to move towards them. "Hey, folks!" - he says loudly. - "We're
helping wounded people all around the place. Don't any of you
need help?" {name1} and {name2} exchange glances, wondering the
man's kindness. "We're okay, thanks!" - {name1} answers. "Alright!"
- the man says something to his people, and one of them throws
a grey box to him. - "Take this at least!" - he holds out a box
to {name2}. Throwing one more glance to {name1}, {heshe2} takes
the gift, still wondering why the guy is so helpful. "Okay, let's
go!" - the man smiles to your messengers and climbs to the car.
You're getting 1 stimulator""",
        ),
    },
    {  # 27
        "name": "Old Church",
        "desc": """The tall wooden spear that attracted your attention and made you
stop here appears to be a part of an old church. Its dark wooden
walls are ancient, white paint on the windows became grey, but you
see several people in black cassocks near it. They all are also old
- you can notice their long hoary beards. The people doesn't look
dangerous or even able to fight back in case of troubles, so you're
thinking about sending several of your crewmates to speak with
locals. As an old dwellers they probably can tell you something
useful about the region you travelled into.""",
        "results": (
            """You decide to send {name1}, {name2} and {name3} to negotiate
with monks. Seeing your people jumping off the Train, dwellers move
inside the church, keeping the door open however. Exchanging gazes,
your messengers approach carefully and hear a worship. Getting
closer to the door, {name3} takes a look inside, and in that
moment a hiss sounds in the air. In the next second scouts see
orange clouds in front of eyes, feel something heavy in their
heads, and cold sweat covers their skin. The Stench! Trying to
hold breath, without clear seeing of the way, they run back to the
Train... They find themselves on the half of a road between the
locomotive and the church, where the Stench didn't reach. "Let's
go, let's go, go!" - they shout, from a run jumping on the Train.
{name1}, {name2} and {name3} get -15 health and -25 energy""",
            """You're choosing {name1}, {name2} and {name3} as a negotiation
party. Your people carefully get closer to the monks, and one of
the dwellers makes a step forward: "These sinners came from the
Hinnom Valley, they brought us the Stench of Hell itself!". In
the next moment a bunch of big rocks fly to your messengers.
Making several shots into the sky, {name1} commands others to get
back to the Train. Monks, seeing guns, run in different directions.
Retreating to you, your scouts climb to the Train fastly. It appears
{name3} got a rock right into {hisher3} head. The wound doesn't
seem to be very serious, but it's still very unpleasant.
{name3} getting -7 health and Motion Sickness""",
            """{name1}, {name2} and {name3}, chosen as a talk group, jump
off the Train and go to the monks. The priests gather together,
looking at your people with a great attention. {name1} moves forward
and starts to speak with the Lord's people. The dwellers talk with
meek phrases, looking confused and embarrassed. It seems like they
don't have a lot of guests here... A couple of minutes of talking
ends with an invitation for a meal in the church. Exchanging gazes,
your people politely reject the proposition. Something not right with
these monks. They speak shy and meek, but their eyes are energetically
moving on your scouts, making small stops on the guns, knives
and sometimes on the Train standing in distance. It's better
not to trust these guys. Thus, your people return empty.""",
            """You choose {name1}, {name2} and {name3} as a negotiation
group. Your people take their guns and move to the monks. After
several minutes of talking one of the church inhabitants, a
young one, takes your messengers aside and speaks with them
tet-a-tet. It appears he want to buy a gun! "The elder part of
the commune thinks that God will keep us save, but, you know,
Lord will help those who will help themselves." - he explains,
stretching out a dollar banknote. Not thinking too long, {name2}
gives him {hisher2} excess pistol and takes money. Friendly
smiling, the priest hides the gun under cassock and says goodbye.
You're getting 50$""",
            """You decide to send {name1}, {name2} and {name3} to talk
with the church beholders. Your people walk to the monks, and
the dwellers meet them with an open arms. It appears they heard
about your company fighting skinheads here and there, helping
people in the country. Two of the monks move into the church
and return back several minutes later with a basket of gifts!
Giving your people blesses and promising to pray for you, they
spend your messengers to the very Train. After all the goodbyes
said you open the basket and see cheese, wine, bread, flowers,
and, plus to this, a bunch of medicines and bandages! Exchanging
smiles, you and your crewmates start to prepare a feast.
All of your crewmates getting +30 energy
You're getting +1 medicine""",
        ),
    },
    {  # 28
        "name": "Old Carriage",
        "desc": """ "On the east departure of Salzburg, on highway 158, big skirmish
happened today about 10:25 a.m.! Refugees, who got stuck in traffic,
started to threaten the people around to make them clear the road,
which caused a real fight..." Turning off the radio, you walk
outside the deck house. Fight for survival expands... A big dark
metal thing lying on the meadow between trees interrupts your heavy
thoughts. It seems to be an old railway carriage, moved out of the
way and abandoned. It wouldn't attract your attention, but you
also see a thin column of grey smoke, uppering from its inners.
Someone made a camp there?! It worth checking, maybe those
people need help or something.""",
        "results": (
            """You call {name1} closer and show {himher1} the carriage. Squinting
eyes, {heshe1} nodds {hisher1} head and gears up for an outing. It
takes just several minutes for {himher1} to get to the carriage, and
you see how your messenger enters inside. In the next moment a din
thunders in the air. You're moving binoculars to your eyes, but
can't get what happened. Taking one more crew mate, you run to
the carriage and, getting closer, see the problem. Heavy metal
door of the carriage slammed, prisoning {name1} inside. With common
efforts for about five minutes you finally release your trapped
messenger. Covered with spider web and dust, {heshe1} coughs, but
you don't see serious wounds. And the carriage itself appears
to be empty, you see only snow intensively melting to steam.
{name1} getting Fear Of Dark""",
            """You decide {name1} will be an appropriate messengers this time.
Taking the gun, {heshe1} runs to the carriage, while you're observing
{hisher1} progress from the locomotive. {name1} slows down and approaches
the carriage quietly. You see {himher1} opening the sliding doors
and making a step inside. In that moment one of the doors breaks
down and falls right on your messenger. Pushing the metal thing away,
{name1} presses {hisher1} right hand to {hisher1} body. For several
seconds {heshe1} disappears inside the carriage, but then exits and
takes a direction to you. It seems like nothing interesting was there,
while {name1} got a minor right arm injury. Well, it could be worse.
{name1} getting -20 health""",
            """You call {name1} and explain {himher1} your thoughts. Nodding {hisher1}
head, {heshe1} runs to the carriage. You observe your messenger progress
from the Adjutant, seeing how {heshe1} carefully opens the carriage
doors and enters inside. Several minutes passes, and {name1} exits,
walking back to you. Getting closer, {heshe1} tells you the following:
"A refugees family made a camp there. Not sure how long they live in
that metal thing, but they are not going to leave. And they don't
want anything with us. They're not aggressive though, just not very
trustful. Can't blame them." Agreeing on that, you're giving a command
to warm up the Adjutant's engine. Let's continue the road.""",
            """You ask {name1} to get closer and explain {himher1} your thoughts.
Without arguments {heshe1} takes {hisher1} gear and walks to the
lying carriage. Carefully opening it, your messenger enters inside.
Time passes, three minutes, five, ten. At some moment you're going
to send more people to the carriage, to check if everythings is okay
with {name1}, but finally {heshe1} exits from the carriage. Getting
closer to the Adjutant, {heshe1} explains: "There are kids there!
Not very young, but still kids. Asked me for some ammo and gave
me money. I've tried to reject, but they said they have a lot of
money. Not sure if it is true, still, I wasn't able to convince
them. Thus, we have some income." - {heshe1} puts a dollar paper
on the metal table. You give a command to warm up the engine.
You're getting 50$""",
            """You're sending {name1} to take a closer look at the lying carriage.
Your crewmate gears up and runs to the place, and then disappears
inside. After several seconds {heshe1} shows up and uppers {hisher1}
hand, making it clear that everything is alright. You take a seat and
start waiting. Not less than a half of hour passes, before {name1}
exits the carriage and runs back to you. "There are several refugees,
hiding in that carriage." - {heshe1} explains. - "Asked me to help them
with a water purifier. I'm not an expert, but dealt with the thing.
Still, they didn't have anything to repay except the kind words, so..."
You're accepting this - well, there's nothing wrong in helping
others. After all, your party is not in a critical state. You're
giving an order to start the Adjutant's engine.
{name1} getting Mechanic""",
        ),
    },
    {  # 29
        "name": "Romani Truck",
        "desc": """Getting closer to a dark green spot, you've noticed earlier, you see
that it's some kind of a romani truck. Old and battered by a
long travelling, it stands right in the middle of the meadow,
opened to the right side like a showcase. A lot of colorful
knick knacks, metal dishes, clothes - all of it hanging on
the walls and lying, pinned down by a rough rope. A human body
in a grey suit stands near the truck, smoking and looking
carefully to your locomotive. From that distance you can't
tell if there is anything you can use on a road, so it makes
sense to send someone to see what the trader has to sell.""",
        "results": (
            """You're ordering {name1} to speak with the man and see what
he can offer. Your messenger jumps on the ground and without sudden
moves gets closer to the trader. You see them speaking for a couple of
minutes, and then the man takes a grenade launcher. {name1} moves
several steps aside of him and waits for the demonstration. The truck
owner aims into a tree standing in about thirty meters, and in the
next moment the gun in his hands explodes. {name1} staggers back...
Seeing that there is no more threat, {heshe1} approaches the place
where the truck owner was. Doesn't seem much left of him... While
{name1} moves back to the train, you notice that {hisher1} movements
are little bit inaccurate - the explosion probably deafened {name1}.
{name1} getting Snail""",
            """You're sending {name1} for shopping. Without sudden moves {heshe1}
approaches the trader truck and starts negotiations. Several minutes
passed, and you see that your messenger buys something, looking like
a grenade launcher. With this burden and a box of ammo {name1} returns
back to the locomotive. "The man was already going to continue his way."
- {heshe1} says. As an approval you see that the truck starts its engine and
moves away. "Let's try one shot!" - {name1} proposes. Opening the ammo
box, {heshe1} puts a grenade into the gun and, aiming to a tree in a
thirty meters, does a shot... Zilch. Gazing at you, {name1} changes the
grenade, shots and... Zilch. "Whatta?!" - {name1} pronounces annoyed.
Trying other shells, you understand that the gun doesn't work.
Tricked! And the trader already got too far to get the bastard.
You're losing 50$""",
            """{name1} becomes your messenger this time. With no delays {heshe1}
approaches the trader, and you see them negotiating. Minute, two,
five, ten - you notice that {name1} makes a step back toward the
train, and then one more, and more, but the truck owner doesn't give
up and continue mumble without a half-second pause. You wait
for about fifteen more minutes, and finally {name1} speeds up. While
approaching the locomotive, {heshe1} shakes {hisher1} head, showing that
it was horrorable. You all smile seeing this. "Man, this octopus!" -
{heshe1} pronounces, while climbing on the train. - "He really got me!
Let's spurt away before he decided to follow me to the Adjutant!" """,
            """{name1} takes a direction to the trader truck. You see {himher1}
approaching the showcase and speaking with the car owner. It takes
just a couple of minutes for your messenger to make a deal with the
trader, and {heshe1} moves back to the locomotive. From the first
second you understand that there are two aid kits in {hisher1} hands.
"Can you believe this?" - {name1} asks loudly, while climbing on the
train. - "Two medicine boxes for just five bucks! Apologies, four and
ninety nine. I wasn't able to walk along!". "Did you check the shelf
life?" - you asking carefully. "Sure, who do you think I am?" - {name1}
answers fast. Satisfied by the bought you command to start engine.
You're getting 2 meidicines for 5$""",
            """{name1}, chosen as a negotiator this time, walks to the
trader truck. You see {himher1} speaking with the car owner for about
ten minutes, and during this conversation they doesn't throw a gaze
to the merchandise. Interesting! A couple more minutes passed, and
{name1} takes a direction back to the Adjutant. Patiently waiting for
{hisher1} report, you hear following: "The trader is desperate, wants
to join us. Says, has experience running trains, not steam though,
but claims to be useful in maintain anyway." Finding this
interesting, you wave your hand, asking the trader to come closer.
One person can be recruited""",
        ),
    },
]

OUTING_TYPES = {"Looting": "Looting", "Meet": "Meet", "Enemy Camp": "Enemy Camp"}

PRONOUNS = ("he", "his", "him", "she", "her", "her")

SCENARIO = (
    {  # 1
        "intro": """Kenneth - the Adjutant mechanic approaches your table and
sits to the right of you. "Captain, we probably have a
trouble." You're uppering a spoon full of dry porridge
to your mouth: "Yeah?!" "Yeah. Come see me after your
snack is over." He gets up and leaves the deckhouse.

Finished the awfully tasteless portion, you're walking to the
lower level of the Adjutant. Before you pronounce the first
word, Kenneth rises his finger up, asking you to stay silent
and listen. You're concentrating on the noises... "Hear that?"
- the mechanic points to the left side of the room, and you
understand what he's trying to say. Some metal screeching can
be heard from the wall. "That's an axle box, something's
acting up." - Kenneth explains silently. - "We need to check
it, it'll take time." You're trying to remember how far was
the Stench frontier, when you last heard about it. "Our
options?" Looking at you, Kenneth calculates something in his
mind: "We need five hours long stop to deal with it." It's
much. "Other options?" The mechanic seems to be not very
pleasant to say it, but he does: "We can try to do it on move.
But it's dangerous, complex and will require two men - me
here and someone on the other side of the locomotive. The
second guy can get injured I warn you. Anyway not dealing with
it can cause significant pace lose. Your call, Cap." """,
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
be considered while planning the further route...

Four hours passed, and the crew reports you that the axle
box is good to go. Calling everyone back on board, you're
commanding to continue the road in the same moment. Four
hours is not five, but it's still long. Better keep your
pace high now.

The Stench frontier came 20 miles closer to you,
but the Adjutant is in a good shape for now.

You're getting a Captain's diary page. Better read it while
on move not to lose distance from the Stench frontier.
Press J to open/close Captain's journal.""",
                "effects": (("do_stench_moves_effect", [20]),),
                "goodness": 5,
            },
            "Try to deal with the axle box on move": {
                "desc": """You're giving Kenneth command to choose one of your crew mates
and try to deal with the axle box on move. You see that the
mechanic doesn't like your decision, but he still accepts
the order. You're returning back to the deckhouse, and
some time later see Kenneth taking one of the fighters
with him to the lower level of the Adjutant. For several
long hours they slip out of your radars...

Exiting on the fresh air, you incline above the railings
and see a blood spot on one of the wheels, blinking on
every turnover. Without delays you go to find the
mechanic. Kenneth, seeing you concerned, uppers his hands
in the same moment: "It's okay, it's okay! Small wound,
but the axle box is fine now. Nothing serious!" Making a
deep breath, you nod your head, trying to calm down. You
knew the risks from the beginning, but it's still about
your people safety. It's good that the helper didn't get
serious wounds. You better find them later to say thanks.

One of your fighters getting -20 health

You're getting a Captain's diary page. Better read it while
on move not to lose distance from the Stench frontier.
Press J to open/close Captain's journal.""",
                "effects": (("do_characters_effect", [{"health": -20}, True]),),
                "goodness": 1,
            },
            "Ignore the problem": {
                "desc": """It's worth not to stop for such long period. Asking Kenneth
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

The Adjutant loses 50 Durability

You're getting a Captain's diary page. Better read it while
on move not to lose distance from the Stench frontier.
Press J to open/close Captain's journal.""",
                "effects": (("do_locomotive_damage", [50]),),
                "goodness": 3,
            },
        },
    },
    {  # 2
        "intro": """Taking a closer look at the bunch of people walking through
the meadow, you understand that there are mostly children.
Weird! Asking a couple of crewmates to follow you, you
get closer to the crowd, seeing a woman moving towards
your party. In a few words she tells that they are
workers and children from an orphan shelter.
Understanding that the Stench moves fast to the place,
and the governors are too busy saving themselves,
adults, who worked there, gathered all the children
and decided to move to Silewer on foot. Looking at
pale and tired kids, you silently think that it was
really tough idea. But probably it saved their lives...

Complaining about walking for six hours without a stop,
the woman asks you to help them build a field camp. You
understand that it'll take a lot of time, as there are
about sixty children. On the other hand, it doesn't look
right to just leave them here, in the foreign country,
tired and shelterless. Maybe there is some time to help
them a little?""",
        "variants": {
            "Help them to build a camp": {
                "desc": """Feeling some qualm inside, you give your people order to help
the children. Losing time is not okay... Still, twenty minutes
later, seeing your people and children smiling while setting
up big tents, igniting bonfires and boiling pottage in big
cauldrons, you forget these heavy thoughts. This small break
will be useful for the crew as well...

It takes about two hours to finish preparing the camp.
Getting a lot of thanks from the children and their teachers,
you gather again on the Adjutant. Everyone seems to be
enlivened, still, the road calls. Giving an order to start
engine, you approach a couple of your crewmates, who are
viewing some kind of an article on a smartphone. "Hey,
Captain, you need to see this! Some of those children visited
kinda scientist summit some time ago and took an interview
there. The woman speaks about interesting things." Telling
them that you're going to take a closer look at the article
later, you go to the deckhouse to plan the route, considering
the recent delay.

The Stench frontier came 20 miles closer to you

A note added into Captain's journal. You can read it
on move not to stay long at the same place, losing
distance from the Stench frontier.""",
                "effects": (
                    ("do_build_camp_effect", []),
                    ("do_stench_moves_effect", [20]),
                ),
                "goodness": 5,
            },
            "Agree in words, but steal from them": {
                "desc": """Calling the crew to speak aside, you're trying to convince
them to use an ability to replenish resources. "The situation
is getting tougher day after day, it's becoming about us or
them." Your crewmates lower their eyes. Everybody know that
sooner or later it'll come to this, still, no one wants to take
responsibility. "It's hard to admit, but those children are not
going to make it. They are not fighters nor survivors. The first
meet with skinheads, and..." The crew continue to keep silence,
bit you feel them accepting the situation, so you're giving an
order: "Build the camp hastily and take useful stuff in case you
see it!" Your crewmates, avoiding to look at each other, go out
of the deckhouse... About an hour and half passed, and all of
your people gather together on the Adjutant. They still doesn't
want to look at each other, but they put an aid kit and an energy
drink on the table. "Okay, let's move on!" - you command.

Some time later you find a paper on your table, which looks like
an interview log. It appears those children visited a kind of a
scientist summit recently and had a word with one of scientists.
No ideas why someone left the paper for you, but it worth reading.

You're getting 1 medicine and 1 stimulator
Soon people of Silewer will know that you've stolen from kids.
This will be a bad example of what foreigners are like and will
bring more people under the skinhead banners.

A note added into Captain's journal. You can read it
on move not to stay long at the same place, losing
distance from the Stench frontier.""",
                "effects": (
                    ("do_enemy_inc_effect", []),
                    ("do_plus_resource", ["medicine_boxes", 1]),
                    ("do_plus_resource", ["stimulators", 1]),
                ),
                "goodness": 1,
            },
            "Don't help them and continue the road": {
                "desc": """You go back to the deckhouse and negotiate with the crew. It
appears most of them would like to help orphans, but all
understand that it'll take at least several hours. The Stench
will not let you wait, so it makes sense to move faster.
People know nothing about the cataclysm behavior, in theory
it can accelerate or appear somewhere far from the supposed
source in Germany. Overthinking it again, again and again,
you decide to ignore the teachers plea. The crew don't like
the decision very much, but everyone mind the situation. A
hard silence forms in the air. No one wants to go there and
say those orphans that you're going to leave. "So, what?" - you
ask quietly. - "Should we continue the road without the last
word? What's the point in it?" Your crewmates lower their
eyes and nod their heads. Taking this as an answer, you give
a command to go...

Some time later you see a paper on your table. Running through
it with your eyes, you find out it's an interview log. Those
orphans visited kind of a scientist summit some time ago and
took an interview from one of the scientists. Most likely one
of your people got it from the children somehow. No thoughts
why it was left on your table, but it should be read.

A note added into Captain's journal. You can read it
on move not to stay long at the same place, losing
distance from the Stench frontier.""",
                "effects": (("do_no_effect", []),),
                "goodness": 3,
            },
        },
    },
    {  # 3
        "intro": """Looking at an aged house, standing in about 200 meters aside of
the railway, you see some kind of a fuss there. The hut is
really old, the walls are crumbled, the junk dark wooden
roof holds on a promise, but through small windows you can
discern several people moving actively inside. You also
hear some noise, even screams sometimes. It's worth checking
the place...

You take a couple of your crewmates and get closer to the
building. It appears a police jeep is standing from the other
side of the hut. Entering the house, you see a couple of men
in uniform, threatening an old pair and a young girl, most
likely their daughter. Interrupted and surprised, the police
officers look at you, trying to understand who are you.
Seeing your guns, they become very friendly: "Hey, folks!
Nothing interesting here, we're just helping this family with
something." Throwing a gaze at the scared people, you realise
it's a lie. "Maybe we can bet a deal and live on happy?" - one
of the officers does a step to you, lingering a wallet from his
pocket. No doubts, they are caught doing something bad, two
officers threatening people in backcountry - witnesses can turn
it dangerous for them. The law didn't collapse completely yet.""",
        "variants": {
            "Take the bribe and go away": {
                "desc": """Nodding your head to the door, you're commanding your people
to leave the house. It's not your fight, not your people, not
your business. The threatened family keeps silence, but you
can feel with your skin that, seeing your gesture, they've
lost the last hope for a better end. As if emptiness filled
the part of the room, where they're sitting. Taking money
from the officer, you exit the hut without a word... While
walking back to the Adjutant, you're all trying to hear anything
from the house side, but nothing happens. Turning your head
back, you see one of the men standing near the door, looking
at your crew. Seems like they are scared by themselves and
doesn't believe you'll just leave. Still, you're leaving.
Soon this will be happening everywhere - those, who has
power and strength, will be using it to survive, destroying
others if needed. And it will be needed. You can't save
all the others anyway, but you can take care about your crew.

You're getting $100

You've got one more diary page in Captain's
journal. Better read it on move.""",
                "effects": (("do_get_money", [100]),),
                "goodness": 3,
            },
            "Kill the bastards and free the family": {
                "desc": """Lighting fast overthinking the situation, you upper your gun
and shoot both policemen. With the same surprised faces they
loudly fall to the floor. Taking away the gun, you do a step
towards the threatened people, but they all upper their hands
in the same moment. "Please, just leave us!" - the old man says
with a trembling voice. Seeing they became even more frightened
than before you killed the intruders, you realise that it
wasn't a good idea to do it all in front of them... Everyone
in the room seems to be little bit lost. It probably will be
better to just leave. Still, you decide to give an order to
your people to pull both bodies out of the hut and drop them
in some distance. Without arguments, they take both dead
policemen and exit the house. After a few seconds long pause
you throwing the last gaze at the frightened family: "Sorry...
Sorry for the mess." Not getting any sound from them, you're
leaving the hut.

You've got one more diary page in Captain's
journal. Better read it on move.""",
                "effects": (("do_no_effect", []),),
                "goodness": 1,
            },
            "Use your superiority and intimidate them": {
                "desc": """You see clearly that all the points are on your side. These
two men are weekly armed, they are policemen, and they were
caught on very bad dids. Every part of the situation is
against them. Tinkering the gun in your hands, you say
overbearingly: "You two better leave this family and forget
the way to this house!" Smiles disappear from their faces
in the same moment. Throwing gazes to each other, they seem
to be confused greatly. "We all will forget what happened
here, you only need to leave" - you add. - "But if you have
counter arguments... Well..." - you move the gun again.
"Okay!" - one of the policemen uppers his hands. The second
one follows his gesture in the next second. "We'll go. Let's
just... Just forget about what happened here." - the officer
seems to be even ashamed, and this fact makes you think they'll
not return here - maybe they even understood the filth of their
doings... When the men left, and their car engine silenced
somewhere in distance, the young girl stands up: "Thank you!
Thank you!" - she seems to be too touched, and you all hear
her gratitude for several minutes. In return she proposes your
crew a medical examination. Yeah, she's a doctor! Feeling the
very lucky coincidence here, you command your people to use
the opportunity.

All people in the crew getting +20 Health

You've got one more diary page in Captain's
journal. Better read it on move.""",
                "effects": (("do_characters_effect", [{"health": 20}, False]),),
                "goodness": 5,
            },
        },
    },
    {  # 4
        "intro": """From a very far distance you can discern that near the small
motel a long line of cars jamms. You can even see a
string of people standing in front of the entrance. Looks
like a lot of Silewer newcomers want to rent a room here.
Sending your people to try to get inside the building, you
caught your eyes on two banches of refugees arguing hard.
Getting closer to them, you can hear that they are brawling
because of the last place in the building. When they see
you, however, they become silent, gazing at your guns. In
a couple of moments you take a place of judge here, you
see both sides looking at you with hopes to get your help.
Observing them, you get it that one of them is a man with
sick boy, about eight years old, most likely his son. The
lad doesn't look good, his face is pale, dark rounds mark
his eyes and skin is covered with sweat. But on the other
side of the conflict you see a pregnant woman, skinny and
tired. Both the father and the woman expect your judgment
somewhy, probably because others are too busy to think
about people around... Or maybe it's just because of
guns... Anyway the decision is yours - there is only one
place left in the motel and someone will have to sleep
in the car here.""",
        "variants": {
            "The pregnant woman should rest": {
                "desc": """Thinking about the situation, you tend to think that
the woman is the one to take the last place. The man
with the sick boy throws something on the ground and,
grabbing his son, goes away. The woman, who still seem
to be scared, thanks you greatly - you can even see tears
in her eyes. Seeing your people returning back from the
motel, you say her goodbye and join the crew. According
their words, the place is filled to the very top, some
unfamiliar people even rent rooms together. Plus to what
you already understood by yourself, your crew mates
give you a log paper - one of them heard motel dwellers
conversing about the same scientist those orphans were
interviewing. She was here not long ago! That's
something should be read.

You're going to give a command to start an engine, but
suddenly you see the man, who was trying to get the last
place in the motel. The one you forced to go - he walks
from the Adjutant back in the motel direction. What does
it mean? You ask the crew to check if everything is okay
on the locomotive, and it appears the man ignited it!
You deal with fire fast, but still the Adjutant gets
some damage.

The Adjutant loses 70 Durability
You've got one more note in the Captain's journal""",
                "effects": (("do_locomotive_damage", [70]),),
                "goodness": 5,
            },
            "The man with the sick son should rest": {
                "desc": """Overthinking the conflict, you decide that the man with
the sick boy should rest in the motel. The woman seems to
be tired, but not hard ill. Saying something silently, most
likely damnations, she leaves the place. The man holds
out his hand: "Thank you!" - he lowers his eyes back to
son: "Jerry!" The boy slowly gets what his father is asking:
"Thanks!" - he pronounces with a weak voice. Left them,
you join your crew. They tell you that the motel is filled
to the very top, but it's something you already got by
yourself. In addition, they give you a note - they heard
a conversation between two motel dwellers, who saw the same
scientist woman those orphans were interviewing. And they
said that she's one of those who responsible for cataclysms
like the Stench. Interesting! Should be read.

You're doing a short technical review of the Adjutant and
then start the engine to continue the road.

Soon all the Silewer will know that armed foreigners forced
a pregnant woman to leave the motel, where she was going to
rest after long road. This will bring more people into the
skinhead bands.
You've got one more note in the Captain's journal.""",
                "effects": (("do_enemy_inc_effect", []),),
                "goodness": 3,
            },
            "Force them both out and take their place": {
                "desc": """The last room in the motel... Maybe it's better to keep
it for your crew? A couple of hours in not moving place
and shower would be good. Looking straight at both the
man and the pregnant woman, you say in a cold voice: "Me
and my crew will take the room." Your visavis stagger back,
surprised greatly by the turn. Several seconds they look
at each other, and then simultaneously turn around and go
away. You join your crew, stand in line and then rent the
room... The short rest goes okay, one of your crew mates
even give you a paper, on which he noted a conversation
between two motel dwellers, who were speaking about that
scientist woman, interviewed by orphans you met earlier,
blaming her in cataclysms like the Stench. Interesting!

In some moment you understand that a kind of a noise
increases fast in the motel. Taking your guns, you all
get out of the room and get into a fight! It takes about
ten minutes for you to exit the building. Without clear
understanding what happened - are refugees, who didn't
manage to get a room, decided to attack the building? -
you return back to the Adjutant. No one got serious
wounds, still, there are several small injuries. Not
the best stop!

All people in the crew getting -20 health
You've got one more note in the Captain's journal""",
                "effects": (("do_characters_effect", [{"health": -20}]),),
                "goodness": 1,
            },
        },
    },
    {  # 5
        "intro": """Seeing a couple of cars and a crowd, you're giving an order
to stop the Adjutant and see what happened. Approaching, you
understand that a fight just finished here - a big bus is full of
bullet holes, and a black jeep lies on its side, also shot bad.

A man walks to you and tells: "Some bandits were following a
column of black jeeps. Good they didn't decide to stop for us,
still, several gun bursts hit our bus." Looking at dense smoke
rising from it, you get it's not gonna ride. The man notices
your gaze and asks for help in repair. You start weighing,
while your collocutor adds: "We searched the jeep for tools -
poor bastards both caught bullets. Unfortunately, there is
nothing useful, only tons of paper, some high science mumbo
jumbo and gas masks." Listening to the guy more carefully,
you start to suspect you already know who was in those
cars... Helga Wagner! Looks like you're almost following her.
Interesting. It's worth checking the jeep - last pieces of
info about the Wahrsager project sounded intriguingly.

The only thing left to decide is of helping these people.
Throwing one more gaze at the bus, you see a lot of bags
on the car top, german car number - they are refugees.
If bandits they met were skinheads, shooting at the
bus wasn't occasional. The scum can return here when
they'll deal with Helga's group...""",
        "variants": {
            "Help them to repair the bus": {
                "desc": """Overthinking the situation carefully, you decide to
help these people. Your crew brings tools from the
Adjutant and starts to reanimate the car. Taking part in
it, you're studying the refugees. Confused and nervous,
they seem frustrated hard. Usually, refugees coming TO
Europe, but the Stench seems to be turning everyone into
the opposite direction. Europe! The place of comfort,
order and civilization became the most dangerous place
in the World. Where to go now? Who'll welcome us?
Countries, which are not able to help themselves? Most
of their citizens would like to live in Europe, but it's
unlikely they want us to come to them and take their
places. Especially now, when number of places reduces
really fast, and no one know if it'll stop one day...

A couple of hours passed, and the bus engine finally
starts to roar, gathered from, literally, pieces. People
give you sluggish thanks, you see they are still too
shocked after getting under a machine gun fire. Anyway,
they at least can now move forward.

The Stench frontier came 20 miles closer to you.
In the black jeep your people found a piece of Helga's
diary. It's added to your journal, worth reading.""",
                "effects": (("do_stench_moves_effect", [20]),),
                "goodness": 5,
            },
            "Give them tools from the Adjutant": {
                "desc": """Seeing you doubt, the man proposes: "Maybe you can
at least bring us some tools? Money is critically
needed now, but we'll pay you!" Don't do a stop,
help them and get some money - sounds good. You're
commanding the crew to give the people stuff, which'll
help to repair the shot bus, while the man gathers
money from his passengers. Approaching you back, he
gives you $80 totally. "Not much actually, sorry." -
he pronounces quietly. - "Those people are still
shocked by the skirmish, that's not what we expected.
Not in the second day of the road at least!" Nodding
your head, you think that it's weakly said. Usually
people go TO Europe, not out of it. But now the spot
of comfort, civilization and order became the most
dangerous place in the whole World. A lot of directions
changed to opposite. Who'll welcome new refugees from
Europe? People, who wanted to refuge to Europe? Looking
at the bus covered with bullet holes, you think it's
unlikely. What happens in Silewer is just a start,
it'll become more worse, if the Stench will grow.

You're getting $80.
Soon you'll understand that you gave too many things to
those people, so you're not able to fix problems on the
locomotive. The Adjutant getting -70 Durability.

In the black jeep your people found a piece of Helga's
diary. It's added to your journal, worth reading.""",
                "effects": (("do_locomotive_damage", [70]), ("do_get_money", [80])),
                "goodness": 3,
            },
            "Don't help them": {
                "desc": """Overthinking the situation, you decide it's too risky to
do another stop. The bus looks pretty bad - it'll take
hours to reanimate it. You don't have hours.

Saying goodbye to the man, you turn back to the Adjutant,
by the way looking at the bus passengers. Refugees.
Yeah, it's time people come out of Europe instead of
moving into it, who'd knew. The spot of order,
civilization and comfort became the most dangerous place
in the World. An interesting question is: who will
welcome new refugees? Looks like the answer to this
is right in front of your eyes - the bus shotted from
a machine gun. And this can be only a beginning! No one
stopped the Stench yet, no one have any ideas about it
actually. If it'll continue to grow, more people will
left their homes and will go to the neighbour countries
and even further. Some will not stop in face of any
counteraction, because it's no longer about simply
comfort and wealth, it became about survival...

Climbing on the Adjutant, you give an order for your
crew to search the black jeep for anything useful and
continue the road. Survival - so, let's not waste time!

In the black jeep your people found a piece of Helga's
diary. It's added to your journal, worth reading.""",
                "effects": (("do_no_effect", []),),
                "goodness": 1,
            },
        },
    },
    {  # 6
        "intro": """Running a rag across the floor, you're working out your turn
to cleanup the Adjutant. Tidiness is important - so many days
in the same cold and coarse locomotive rises chances of
sickness and pests emergence...

At some moment Daren, the Adjutant machinist, approaches you.
You see he has something to tell you, but he can't find the
proper words. "Come on, Daren, birth it." - you say, trying to
make things faster. "Well... We've a problem. It's big.
Precisely, we don't have food." Stopping to run the rag, you
straighten your back: "How so?!" "Well, everyone is waiting
you." - he answers and disappears in the doorway. Thinking a
couple of seconds what it should mean, you decide to hurry
up - if EVERYONE is waiting, it's serious.

Entering the back room, you see all of your people standing
in a circle. Everyone seems to be concerned, but you don't
find any aggression in the room, fortunately. "Well, Captain,
here we are." - Kenneth starts the talk. - "Our food supplies
are running out faster than we thought. We need to speak
about limits, otherwise, we'll soon start to starve." Rubbing
wet hands, you're trying to concentrate on the new problem.
In current situation everybody should be energetic and
healthy, as there are a lot of maintenance questions and
the need to fight. But if it's impossible, maybe it's worth
choosing who should have a priority in food questions?!""",
        "variants": {
            "Fighters will have food priority": {
                "desc": """Keeping silence for about two minutes, you come to
a decision that fighters, those who protect the Adjutant
from skinheads and who search resources on outings,
should eat enough. If they'll not be able to fight back,
you all will become victims of savages people turning
into. As for the Adjutant mechanic and machinist, well,
their work is less nervous and doesn't require that
big efforts and concentration.

Pronouncing your decision to the crew, you see they are
not very pleased with it. Most likely, they are ready to
starve together, instead of choosing special ones...
Still, these days require tough turns and tactical
thinking. Fortunately, Kenneth and Daren doesn't seem to
be offended that their ration was reduced. They are not
young, both seen a lot in their lives, they understand
and can handle it. Good. Not that good, of course, but
at least you don't need to think about riot in the crew.

Finishing the talk, you return back to your cleaning duty.

Some time later you'll find out that reducing mechanic's
ration was not the best solution, because malnutrition
lowered his competence, and the locomotive suffered.
The Adjutant getting -80 Durability.

You're getting a new diary page. Check the Journal.""",
                "effects": (("do_locomotive_damage", [80]),),
                "goodness": 1,
            },
            "Adjutant maintainers will have priority": {
                "desc": """You're keeping silence for several minutes, weighing
all the points. Fighters are needed, but you have enough
ammunition - it's the main part of the defence. But if
the locomotive engine will stop... In this case you all,
without counter arguments, will die really soon. Keeping
the pace is important, more important right now than
killing those savages.

With this in mind, you're pronouncing your thoughts to
the crew. Kenneth and Daren seems to be not very
pleasant with your solution - they both are not young,
they've seen a lot and can handle some starvation. Your
order little bit offends their pride. Still, order is
yours, and you believe the mechanic and the machinist
should been in the best condition that is possible in
the current situation.

Finishing the talk, you return to your cleaning duty.

Some time later it'll become obvious that fighters
tired much faster with this malnutrition, and their
productivity significantly reduced.

All the fighters getting -40 energy.

You're getting one more diary page. Check the Journal.""",
                "effects": (("do_characters_effect", [{"energy": -40}]),),
                "goodness": 3,
            },
            "Limit food for all": {
                "desc": """Taking a couple of minutes to think about the situation,
you decide it's not the best idea to make a part of the
crew somewhat special. Everyone is important, everyone
here do something for the whole company. If food supplies
are not enough, it'll be better to reduce ration equally
for all, no matter their duties.

Sounding your solution, you see that everyone in the room
is completely okay with it. Good, the team spirit is still
here, and the food crisis will be dealt with by common
and equal limitation.

Calculating the new ration with others, you understand
the limitation will be actually small - spreaded to every
person, it became not very significant for separately
taken member of the crew. With this, you all approve
the decision and return to your duties.

Ration limitation results:
All the characters getting -10 energy and the Adjutant
getting -20 Durability.

You're getting one more diary page. Check the Journal.""",
                "effects": (
                    ("do_characters_effect", [{"energy": -10}]),
                    ("do_locomotive_damage", [20]),
                ),
                "goodness": 5,
            },
        },
    },
    {  # 7
        "intro": """The traffic jam stretched to the left of the railway lasts
for about 15 miles, and it's only the part you've seen,
there are even more cars around the highway turn.
Massive! And at some moment you see the start of this
serpent - a road blockpost.

You order to make a stop, take several people and go
to the place. From the very far distance you can
discern shouts - refugees are arguing with the police
hard. You order others to stay in distance, and
give them your gun not to provoke anyone. Getting
closer to the officers, you see that they completely
closed the way, they're not even checking, just holding
this huge column of refugees. You can't understand
if they have a government order, or it's something
they've decided to do on their own.

The blockpost doesn't seem to be strong, and people,
most likely, understand this. Probably, one more news
report about the Stench came closer will billow these
people to do something agressive.

Should you care about it? Maybe it's worth to speak
with someone and try to regulate the situation. Not
much of hopes, still, it can work...""",
        "variants": {
            "Ask officers to let people ride": {
                "desc": """Seeing that officers are on the alert and can start
to shoot at any moment, you approach them slowly and
quietly. The one standing in front seem to be getting
that you're not a threat, so he nods you. You come
closer, saying: "Hey! Quite a mess here." The officer
takes a look at the people: "Weakly said! But we have
an order not to let them get deeper into the country.
There is already disorder everywhere."

You incline your head and calmly silently say: "Just
try to understand them. The Stench is coming, they're
trying to survive, save their families... No one yet
said it'll stop - chances we all will soon become
refugees." The officer seems to be overthinking your
words. "The Stench is in just several hours from here.
You'll have to leave the blockpost eventually, if you
want to survive." The officer throws a glance at others,
it looks like they understood what we're talking about.
"Okay... We actually got it that we need to leave, it's
just..." You nod your head in agreement gesture.

The officer gives a command to open the gates, and the
refugees feverishly return to their cars to continue
the way.

More refugees in the Silewer will soon make skinheads
much more active.

You're getting a new diary page. Check the Journal.""",
                "effects": (("do_enemy_inc_effect", []),),
                "goodness": 5,
            },
            "Instigate a refugees assault": {
                "desc": """You are silently approaching the refugees, and,
seeing that you're a fighter, they move closer towards
you. You feel they are ready, there are several active
guys, and others are going to support them, they only
need a small push. Thinking that they have a right to
do this, as the Stench is getting closer, and it's not
fair for so many people to just die here, you're
starting to say something, but in the next moment
you see they don't even listen. Your appearance is
enough for them to start the assault, without words.

Everything around you comes to move, the crowd turns
to an avalanche. You're retreating to safe distance,
as riot becomes chaotic and uncontrollable from the
very start. Police officers are smashed in just
several seconds, and the long serpent of cars starts
to feverishly crawl through the demolished gates.

When the situation became little bit more calm,
your people get closer to the blockpost and take
some stuff from it: tools and guns.

Knowing about the assault, skinheads will become
much more aggressive. The Adjutant gets 90 Durability.

You're getting one more diary page. Check the Journal.""",
                "effects": (
                    ("do_locomotive_damage", [90]),
                    ("do_enemy_inc_effect", []),
                ),
                "goodness": 1,
            },
            "Don't do anything": {
                "desc": """Slowly and silently getting closer to the blockpost, you
try not to attract attention - the situation smells
gasoline, it's better to stay quiet.

Several refugees, males, are actively arguing with
the officers, and you see that everyone here
understand that policemen have very weak positions.
People in behind seems to be ready to rush forward
in case of a one wrong move. It's just six officers,
armed, but there are hundreds of refugees against
them. And some of them may be armed as well...

Still, for some time the tension here will hold.
Not willing to be the rock which starts the avalanche,
you're silently turning around and go to your crew
mates. It's better just to leave.

You're getting one more diary page. Check the Journal.""",
                "effects": (("do_no_effect", []),),
                "goodness": 3,
            },
        },
    },
    {  # 8
        "intro": """While you're looking at the map, trying to plan the further
route, Daren approaches you silently. "Captain, we
need to talk." - he observes the room. - "Privately,
I mean." His lowered voice makes you feel it's
somehow related to other crew members, and this is
pretty strange to hear from Daren, who doesn't
gossip about others at all.

You showing that you'll follow him, and he leads
you out on a fresh air. "Captain, we... I think
we've a stealer on our ship." "What?!" - you're
trying to make sure that he's really saying it.
"Our supplies, they're running out fast. And after
we've reduced ration it didn't change, at
all. Someone is stealing food, constantly."

This is an accusation you didn't expect. The crew
seems to be honest and patient, all of them, who
could do this? And, more than this, what to do
with it? Find the stealer first or just talk
with everyone? The situation can harm cohesion
bad in unpredictable way.""",
        "variants": {
            "Ask Daren to investigate deeper": {
                "desc": """Overthinking it again and again, you understand that
speaking about it with the whole crew is a bad
idea. They'll start to suspect each other, think
about it, maybe even blame... No, it should be
solved quietly, perfectly, with only the one who's
doing it. It's not clear for now how to regulate
this behaviour, but let's be solving one problem
at a time.

You're quietly saying Daren to observe the storage,
try to figure out who's the stealer, but not to stop
them yet. He likes your idea to deal with it without
making noise and he promises to find the stealer.

After several days of observing Daren will still
don't know who's stealing the supplies. No one
seems to be doing anything wrong, but food
disappears as it would be stolen by a ghost.

Forced to buy more food in cities, you're losing
money - about $60.

One of your crew mates intercepts a radio
transmission on which Helga Wagner is instructed
about a place safe from the Stench. Check
the Journal for the transmission log.""",
                "effects": (("do_get_money", [-60]),),
                "goodness": 3,
            },
            "Speak with the crew": {
                "desc": """After some overthinking you're coming to the
idea to speak with the whole crew. The problem should
be solved fast, and the stealer should be ashamed in
front of their crew mates. It seems fair.

You're gathering the whole collective and describe
them the situation. People seems to be surprised
and confused, but, looking at them, you don't see
the stealer among them. No one reacts like a
delinquent. And several days later Daren will
tell you that supplies are still disappearing.
The suspicions you brought into the crew,
however, make the collective atmosphere a bit
colder and even wary.

Daren's attempts to hunt down the stealer are also
resultless - no one seems to be taking more than
they should, but supplies are still missing, like
a kind of a ghost stealing them right through
the walls.

Crew cohesion is decreased by 5 points.

One of your crew mates intercepts a radio
transmission on which Helga Wagner is instructed
about a place safe from the Stench. Check
the Journal for the transmission log.""",
                "effects": (("do_spend_cohesion", [5]),),
                "goodness": 1,
            },
            "Speak with everyone separately": {
                "desc": """The idea of making noise of this situation looks pretty
bad to you. It's not easy to stay optimistic during
the days of late, no need to make people suspect
or even blame each other. It's better to speak with
them one by one, and try to find the stealer quietly.

You're spending several hours in talks, trying to
understand your every crew mate mood. It doesn't
look like any of them is desperate enough to steal
from the common storage. You're still cautiously
alluding that there can be problems, but no one
reacts in an unusual way.

Several days later Daren will tell you that food
is still missing, though he didn't notice anyone
taking more that they should. Like a ghost is
stealing supplies.

However, heart-to-heart conversations you've done
with every crew member increases the cohesion.

One of your crew mates intercepts a radio
transmission on which Helga Wagner is instructed
about a place safe from the Stench. Check
the Journal for the transmission log.""",
                "effects": (("do_spend_cohesion", [-5]),),
                "goodness": 5,
            },
        },
    },
    {  # 9
        "intro": """Hearing cries and a lot of noise inside the machinery section,
you hurry up there to figure out what's happening. You
see that your crew mates are trying to pull out a boy
about nine years old out of the dark of the locomotive
mechanisms. The lad's left leg is grinded, he seems to
be losing consciousness, there is blood everywhere.
Seeing you, Daren shouts: "Cap, it's our food thief I
bet! Been hiding in the mechanisms. I've decided to
clean up things today, and he probably got scared,
tried to get deeper, got too close to the moving parts,
and then..."

Kenneth, who's also here, moves closer to you. You can
feel he's shaking. He silently asks: "What should we
do, Captain? We're no medics here, and the kid is hurt
bad. We can try to transfuse blood, probably from two
people, as he lost really a lot. Or we can use
medicaments to stabilize him. We need to act quickly,
he's leaving, and we're not good enough for such an
operation I'm afraid. Every second counts!"

Assessing your crew state and the medicines supply,
you're trying to find the right solution to this
unexpected distress.""",
        "variants": {
            "Save the kid with transfusion": {
                "desc": """You're giving an order to figure out the lad's blood type
and start transfusion as soon as possible. The child
didn't deserve this! If he would just... just tell
you, that he's here. Probably was too afraid you'll
get him off somewhere in the wild lands, alone. Or
even worse... Deft enough to hide under your noses
for such a long period! Most likely one of those
orphans you met earlier...

It appears two of your crew mates has the same blood
type that the kid does, so with common efforts
you're all trying to organize a blood transfusion
system of improvised means.

Several hours passed, and you understand that it's
working! The child's hands stop trembling, his skin
gets a bit of colors. Yes, the kid is stabilized,
though his leg and stress he transferred are going
to keep him in the bed for a long time.

Two of your crew mates losing 30 health.
While you've been saving the child, one of your
sentries recorded a new encrypted message from
Unterriff. Check the Journal to read it.""",
                "effects": (("do_transfusion_effect", []),),
                "goodness": 5,
            },
            "Save the kid with medicines": {
                "desc": """Lighting fast overthinking the situation, you decide
that the child should be saved, still, it's better
not to involve your crew too much. You have your
own route, you promised your people that you'll
lead them through this in one piece. And the
blood transfusion is a risk, which calls your
promise into question.

Your people start to gather all the medicines and
stuff needed to stabilize the child. It appears
you don't really have enough for such an
operation, but you don't lose hope.

After several hours full of stress and hard work
you understand that you saved the boy. It cost
a lot of energy and supplies, but his limbs stop
trembling, skin gets some color and blood
pressure becomes more acceptable. He'll be okay,
though full recovery will take a lot of time.

You're losing 2 medicines. In case of lack of
medicines your fighters lose 40 energy.

While you've been saving the child, one of your
sentries recorded a new encrypted message from
Unterriff. Check the Journal to read it.""",
                "effects": (("do_medicine_save", []), ("do_medicine_save", []),),
                "goodness": 3,
            },
            "Don't save the kid": {
                "desc": """Fastly overthinking the situation, you're coming to the conclusion
that you can't help the child. You have your own way,
you need to save your crew. And blood transfusion or
spending extremely valuable medicines in such a
critical situation? No.

You're ordering not to waste anything to save the
kid. A long tense pause fills the air in the
locomotive. Everybody seems to be so shocked by your
decision that can't even say anything, they are just
looking at you.

Daren becomes the first who voices: "Cap... but...
child. We can't just... No!" You're repeating your
order, and several people exit the machinery in the
same second, overreacting hard. Others still stay
in hopeless attempts to help.

You're returning to your desk, and several hours
later Kenneth, walking near you, shakes his head,
showing that the kid died.

Your ruthless decision becomes a heavy hit to the
crew spirit. People seem to be crushed, and they
blame you in this darkest of the days. Leader's fate.

Crew cohesion is decreased by 30 points.
One of your sentries recorded a new encrypted
message from Unterriff. Check the Journal to read it.""",
                "effects": (("do_spend_cohesion", [30]),),
                "goodness": 1,
            },
        },
    },
    {  # 10
        "intro": """Observing flakes of snow calmly getting down from the skies,
you hear someone's approaching you. Kenneth. "Captain,
we've caught one more transmission from Unterriff."
You're nodding your head, showing that you're
following him. Together you enter the deckhouse,
where the crew is gathered around the radio.
"Starts!" - Daren shouts, making everyone go silent.

"Code 773-L, I repeat, code 773-L. Message for all the
Unterriff-8 program members. The Stench cataclysm
is designated as the highest level menace. All the
members with code 773-L and higher are recommended
to immediately move to the designated rendezvous point.
Reception party will be revoked in 173 hours. If
you're not able to get to them in time, you'll have
to follow the road 804 and proceed to the path
described in the item 26.3.1 of your project
Unterriff agreement by yourself, I repeat, by
yourself. At the Unterriff gates you'll have to
identify yourself by the microchip attached to your
agreement. Persons without a chip or below code
773-L will not be allowed to Unterriff-8 facility."

The message suddenly breaks up. Everyone seem to be
concerned - a whole system is built around Unterriff.
Chips, agreements, hierarchy of codes... But you had
no idea! No one had! Seems there are a lot of...
chosen ones, who are welcome in the underwater
shelter, but not all. Someone selected those, who
must survive, and those who not.""",
        "variants": {
            "Plan the route": {
                "desc": """Kenneth moves to the center of the deckhouse, holding
hand on his forehead. "Road 804, road 804... I
know the place! I've been there a couple of times.
It's a railway path stretched along the Black Sea
coast. There are several small forsaken branches
forked from it in the direction of the sea..."

"I suppose, not forsaken. Just not for everyone."
- you say silently.

Kenneth uppers his eyes to you: "Then, I assume...
let's go! Though, we still need an access chip to
get inside the facility..."

You're nodding your head confidently. You already
have ideas about what to do next. They started
a great gathering - there will be a lot of fuss
in the region. It can help you.

Looking out everyone inside the deckhouse, you're
surely saying: "Seems like they forgot to send us
an invitation card. Well, we'll get it by
ourselves. Let's go see this Unterriff!" """,
                "effects": (("do_no_effect", []),),
                "goodness": 0,
            },
        },
    },
)

SCENARIO_LABELS = ("Chapter ", "Scenario", "Seepage")
CITY_NAMES = ("Sneeuwstad", "Naaldstad")

PREAMBULA = """Good morning, Captain!

We've crossed Silewer border at 11:45 pm, the checkpoint was abandoned. Soon we've made
a stop near an improvised refugees camp. Criminals, looking pretty much like skinheads,
were humiliating the camp dwellers in the meantime. We've shown them our guns, and they
let those people be, but also promised to find us later. Still, we've decided not to
wake you up and let you rest till the morning...

The Adjutant, our good locomotive, is in acceptable shape, and crew is ready for duty.
Munich just went dark, which means the Stench frontier is in a couple of hours behind.
We should keep the speed high not to let those poisonous orange clouds overtake us.

That's all, Captain, handing command over to you!"""

JOURNAL_PAGES = (
    (
        "diary",
        """Never wrote diaries earlier, but now I feel
that I need to put all of my thoughts
down on paper and try to look at what
happened recently, see a bigger picture...

About a month ago social networks gave
birth to a new flow of videos: people were
filming streets, talking about some kind
of orange mist. Though there was no mist!
What they were trying to film were only
buildings, cars, sidewalks and crystal
clear air. Like they were hallucinating.

It all looked as a new stupid prank or a
creepy thread we got used to, so no one
took it serious first. Zoomers do have
fun as usual. I thought the same, I must
confess... But in some moment they
started to find bodies, for real. Big
news agencies picked up the story:
people are dying right on a street,
but no one able to say why! Here
someone said out loud: they die because
of the orange mist, spotted there.

As it usually happens, government first
tried to hide the adversities scale. They
started to speak of stupid explanations,
ask citizens to stay at home if possible
and use respirators; censor newspapers,
websites and discredit rumor authors.
They also closed several city blocks, but
only those in dormitory areas. Recreation
and business regions, which bring money,
of course, were working in normal regime,
so there you still could trip over a
corpse not yet removed by the police.
In the meantime, in Germany, Switzerland,
Netherlands more and more people were
getting that something serious is
happening.

Finally, several police officers, seeing
that the disaster is gaining momentum,
gathered all their conscience and decided
to whistleblow. Photos they posted
publicly were showing tens of dead bodies
on streets, like a new Jonestown, and
several documents, where chemical
specialists were summaring up that the
orange mist, called by them as "The
Stench", selectively kills people, no
matter how good is their isolation or
air filtering...

This action caused panic to stroke most
of the Europe countries, and in this
moment I reilized I should do something.""",
    ),
    (
        "note",
        """Interview protocol from 2021-06-23, Zurich,
56th World Scientist Summit.
Interviewer: Emily Schlosser
Interviewee: doctor Helga Wagner,
leading system engineer of Wahrsager
project team.

- E: Helga, could you explain our
subscribers in simple words what the
Wahrsager project actually is?
- H: Before talking about the project
itself we should remember determinism:
the methodology which proclaims that
every event in the world has particular
causes. This idea actually means that
our past directs our future. With this
in mind our group of scientist tried to
find a way to take a look at our past,
see what was actually happening there,
measure previous events and, probably,
we hope, use this information to predict
our future! That's how the Wahrsager
project idea was created.

- E: What you're talking about sounds
pretty much like a time machine!
- H: Ya! But let's mention this machine
doesn't make passages into another time,
it only gives us an ability to take a
look at it, do a detailed snapshot, which
can be analyzed. Like a photo (smiles).
The main point here is accuracy - our
world consists of immeasurably number
of events, which influence each other.
We need Laplace's Demon to get results,
as without high accuracy our data will
be giving pretty unreliable predictions.

- E: Sounds incredible! But it seems you
need the best equipment and experts.
- H: Sure, our team consists of the
highest level professionals, and it's
a great honor for me to work with these
brilliant people! As for equipment, our
government provides us everything we
needed since we've run the very first
presentation.

- E: Could you tell us how it was?
- H: Right now we proceeded further than
that, but the first presentation included
only a chamber with a chemical substance
and equipment, which was able to show
the state of this substance 48 hours
back in the past...

On this question our interview came to
its end, as doctor Wagner was called by
her colleagues to take part in some kind
of an urgent online meeting.""",
    ),
    (
        "diary",
        """When it became obvious that the Stench
adversity is real, and it's not going to
stop in the near future, I decided to close
my company. Those who worked for me -
we were always like a family. I don't have
another, so it was hard to say goodbye to
everyone... Still, we all made a decision
to leave the city as soon as possible.
The first Stench reports were made in
Germany and Switzerland, most likely on
the west, so we had an approximate
direction - considering that the mist is
going to spread in circle.

As we were little bit slowly, we really got
stuck! Airplanes, which've taken some
people, flew away and refused to return.
No single airplane left in the whole
country! As for the cars, well, it was even
worse - every road on the east of the city
was clogged up in miles, MILES!
Everybody was trying to leave the place.

Here one of my friends, a machinist,
called me. He was in search of people,
who are brave or desperate enough to help
him to hijack the locomotive he was
working on during the last several years.
He know me as a daredevil and decided
to call me first. I liked his idea and
made a proposition to my workers. Some
of them have families, so they refused
to take part in this risky operation,
but three of them and Kenneth, my old
friend mechanic, agreed.

Daren, the machinist, who proposed all
of it, told us about the Adjutant -
tough locomotive he was driving, the
fast and powerful machine, which is old,
but very reliable transport. He said he
knows a forsaken closed railway, which
condition is still quite good and which
can lead us out of the city. On that we
all made a decision.""",
    ),
    (
        "note",
        """Following is what I've heard from one of
the motel dwellers, who was in a very
dissatisfied manner telling a story about
a strange woman to his friend.

According to the source of information,
yesterday in the morning he met a woman
with a very strange thing on her neck,
looking pretty much like a high-tech gas
mask. She had several metal boxes and
a bunch of helpers, all seem to be a part
of university or a science group.

The woman have been talking a lot with
someone on the other end of the phone.
He said she was reporting. According to
what our man heard, they were working on
some kind of a machine, which attracted
government attention pretty strong.

It's able to make a window into the past
(Wahrsager project, no doubts). They
wanted to use it to check if people are
lying about things already happened, and
for espionage - getting info about what
happened some time ago, but didn't yet
caused any consequences. As the machine
shows how it was actually been, without
embellishing, hiding or concealing, just an
objectively truth, it all sound really smart.
Let's say, a spy was rooted a couple of
days ago into your organization; with this
machine you can see the past, the period
when he was recruited and instructed.
You'll detect danger before the guy will
actually get hands on something valuable.
You can actually track anyone! With some
delay, yes, but still...

The woman also told about their early
experiments. They created portable version
of the machine and tried to look into
1928 to investigate a murder of a 10
years old girl named Grace. They've got
good results and were able to track the
whole horrors of the crime from the
very start to the last second.

An interesting thing is that on images
scientists noticed color deformation of
some fluids (blood?!). They said that
it has too much of red and green.
Which means they were more ORANGE
than they should. (I think here the guy
gave free rein to his imagination,
and there was nothing about it in
the scientist's conversation).

To the end of the story the man cursed
scientists, saying that it's they who
start adversities like the Stench,
Bhopal Disaster, Fukushima-1 Nuclear
Accident, Minamata Disease and others,
and one day they will kill us all.
On that the interesting part of the
conversation ends.""",
    ),
    (
        "note",
        """Helga Wagner science diary.
A record made on 2021-07-06. Several
dark spots on the paper hints the
author was crying while writing it.

Finally, I have time to put my thoughts
on a paper. Can't remember when I wrote
the last time. Three month ago? More? Not
in a mood to check now...

Those bastards, bastards ruined our work
today! Fat ugly politicians decided
Wahrsager should be used for espionage.
Espionage! I suspected long ago that
their interest is not that big, they
don't want to pay tons of money to
make it really great. They don't need
to see future, they just want a damn
spying machine to catch video of
another fat ugly politician shagging
with his student boyfriend. Blackmail! So
stupid that I want to puke!!! A machine
which can PREDICT FUTURE will be used
for prying at deeds of the last days!

Of course, now I can't leave. They've
thrown hooks, and now we all are slaves
of our own ambitions...

Gut, it's a science diary, not a school
girl crying napkin. Back to business. The
curator forced us to check what is
Wahrsager time limit. We've taken a look
at different ages, even before humans
appeared on Earth. Looks like the last
machine version doesn't have a limit at
all. The strange thing we all noticed -
the more ancient times we're trying to
look at the more color deformation we get.
Everything becomes orange. No one have
ideas what it is, we're working hard
on understanding the phenomenon.

Still, we probably are late on it. About
a month ago those idiots asked us to try
to open a passage into the past. Now I'm
trying to imagine what another stupid
thing they had on their minds, but back
there we were thrilled to try! And we
tried...

Jeffrey Bowers, our assistant from US,
accepted a risk to spend 10 seconds in
8000 BCE and take a fistful of sand from
there. At the very first moment since we
opened the passage, he fallen into some
kind of a seizure, lost consciousness for
several minutes, then returned to the
world of living, started to rave and to
knock his teeth from time to time.
Analysis shown he feeled cold for some
time, which is strange - we were sending
him into the Arabian desert. The
experiments were paused until we'll
understand everything.

Several days later Jeffrey became well
and soon returned to work, but we all
noticed that from time to time he uppers
his eyes to the ceiling, like he sees
something there... Later we all saw it...""",
    ),
    (
        "diary",
        """When we decided on who's going for
the Adjutant, when and how, it appeared
that only six of us are in the company.
Daren said he'll try to find more people,
but no one else responded to him.

In such a collective, seeing that the
situation becoming more and more hot, we
decided not to waste time, took guns,
supplies and one night went to the
railway station, where Daren was working.

When we got there, it appeared that we are
not the only that smart people in the city.
Looking at a bunch of thugs preparing the
Adjutant for a road, I feeled like a good
chance is eluding me. All of us...

We all frozen, trying to understand what to
do next, but in some moment Daren stood
up and loudly asked: "Ronnie?! That you?".
A fat heavily breathing guy walked out
of hangar shadows. "It's a strange
coincidence you're here after rejecting
my proposition." The fat guy finally
identified Daren and smiled: "Ah, that's
you, my honest friend! I decided I don't
need your old ass and took other guys to
release this metal beast. So, thank you
for friendship, but we'll take it from here!"

Thoughts flewed through my head faster
than light. There is no way to bet a
deal with such a bastard, the
locomotive is not big enough to
accommodate two of our groups, and
this chance can be the last one in
the whole city. The time to act has come
much earlier than I expected... Still,
it's time to act.

I've draw my pistol and without any
words stood up from my cover and shot
the fat bastard. As I hoped within my
soul, others understood what needs to
be done without explicit instructions
- everyone started to shoot. In closed
hangar insides sounds of guns were
thunder-like, but after several seconds
it became obvious that our rivals are
not as prepared as us. Forced them out
of the building, we all jumped on the
locomotive and pushed pedal to the
metal before we lose the opportunity.

That was our first skirmish on long road...
As Daren promised, we were able to leave
the city by a forsaken and overgrown with
grass railway. He knew all the neighbour
roads, so our pace was quite fast. We
didn't meet anyone at all, like we were
the last ones leaving the country on a
train. Most likely we were.""",
    ),
    (
        "diary",
        """The Stench, the Stench, the Stench...
What is it? Despite of everything that we
saw, I still don't even have a strong
opinion on it. It's not just a mist, no,
it's a state. You can't see it from
distance, but when you get into a cloud...
It's like standing under a waterfall,
like something is pressuring you with
vibrations. They are not low or high,
just... the middle, but they are very
heavy, rough.

Yes, vibrations pressure on you, it all
starts to shake in front of your eyes.
Skin covers with sticky cold sweat in
the same moment. You're freezing, so,
in addition to air vibrations, you
start to shiver by yourself and knock
your teeth.

It feels like you're a weakly balanced
machine working on high frequencies, too
high, so high that your organism starts
to worn in minutes. You're losing all
of your energy and can disctinctly feel,
like parts of your body stopping in a
completely exhausted condition.

After you spent about a minute in the
Stench, you need at least 10 minutes
just to return to reality and stop
shivering.

And the smell. They called it "The Stench",
but it should better be called "The Hell".
Because it smells like a very strong
burnt plastic mixed with moisture and
mold. You breath it, and it scorches your
lungs, fills it with fat cinter from inside.

With all of this, it's pretty hard to
keep your consciousness within a cloud.
All you want is to leave it as soon as
possible, but you can never see where it
ends. From inside the Stench looks
endless, a veil, which goes into infinity
in all directions. Only when you got
out, you can see that it was... a
comparatively small cloud.

The thing I fear is that one day there
will be nowhere to get out, and that
this day will come real soon. The
Stench is spreading, every hour it
covers more and more of Europe.
Governments and scientists are useless,
it feels like no one really working on
it, everyone is just trying to hype
and earn on the disaster.

In the meantime Silewer is already
full of refugees, and what we'll see
in the next country? How fast hordes
of people will stuck without an
ability to make a step further in
the queue to survival?""",
    ),
    (
        "note",
        """Following is the log of an encrypted
radio transmission we've intercepted.
It contains a conversation between
Helga Wagner (H) and her bosses (B).

- B: Helga Wagner group, Helga Wagner
group, come in.
- H: Hearing you loud and clear.
- B: Glad to hear from you, Helga,
are you alright? We heard you've
been attacked several times on
your way through Silewer.
- H: Yes, we've lost a couple of men
and some science documentation. It
doesn't contain any sensitive
information, so we decided not to
waste time for retrieving the
documents back.
- B: Helga, the situation in Silewer is
getting out of control, and we don't
have jurisdiction to regulate it. We
recommend you not to do unnecessary
stops there.
- H: Oh, I assure you, we don't.
- B: Good. Helga, our people are waiting
you in the location, which coordinates
we've sent you just a minute ago. Come
there, they'll take you to Unterriff,
it's safe here.
- H: Sorry, you said "Unterriff"? I thought
it's a fable!
- B: No, Helga, it's real, the city is
under the Black Sea, so it's going
to be a short way for you. We're
waiting for you.
- H: Oh, but... How? I mean... How???
- B: Just get here soon, it's safe
down here.
- H: How do you know the Stench
can't get there?
- B: Helga, we pretty sure we know
how to protect the city from the
Stench. It was designed for exactly
such occasions, there is everything
that's needed for a comfort life.
Just get here, the Stench adversity
is spreading in an unpredictable
way, it doesn't fit wind or
atmosphere masses movements. We
can't analyze it and we're not
sure how much time you have to
get to Unterriff, so we advise
you to hurry.
- H: Yes, I got you, sorry, I just...
I guess I need some time to
process what you said.
- B: Process it, Helga, and make
your way to Unterriff. Reach us
on this frequency in case you
need anything. The situation
is complicated, but we'll do
our best to help you.
- H: Yes, sir, thanks. We're on our
way. Helga Wagner group out.
""",
    ),
    (
        "note",
        """The following is a log of another radio
transmission we've intercepted from
Unterriff.

- B: Helga Wagner group, Helga Wagner
group, come in.
- H: Helga Wagner group on the line,
hearing you loud and clear.
- B: Helga, where are you now? Are you
getting closer to the rendezvous point?
- H: Yes, we're almost out of Silewer.
- B: Good! We're reaching you, because
there are two more groups of our
people, who're following your path
through the country. They're meeting
heavy resistance from the local bands.
Can you advise a safe route?
- H: Oh, sir! I'm afraid it'll be hard!
We think about 30% of the country is
already covered with the Stench - all
of it on South-West. North, however,
is under skinheads control.
- B: Helga, you keep saying "skinheads".
What does it mean?
- H: It means it's an alt-right band
of criminals, who've been harassing
foreigners in Silewer for years. Because
of the Stench and a wave of refugees
they've got huge support from locals
recently. People say they have a new
leader, who ordered to rob everyone, not
just foreigners, and prepare for a big
war for survival! They have supplies,
ammunition, people, and they're
getting more every day!
- B: What do you advise, Helga?
- H: We've crossed the country by
Checkpoint 46 - Sneeuwstad - Naaldstad
route, but this path is no more safe.
We've heard someone purposefully rides
along the railway, giving hell to
skinheads. They've gathered significant
forces to stop those people and get
their locomotive for themselves, so I
think it's safer to stay away of
railways. Say them to take to the
South, about 80 miles.
- B: Thank you, Helga! We'll tell
them! What else can you say?
- H: The situation is bad. Police
almost disappeared or joined skinheads,
and everyone feels it. Shooting, robbery,
killing is already everywhere. A lot of
people are trying to loot as much
supplies as they can and get under
the ground. Stashes and bunkers.
For others transport became the main
value, as it can get you away from the
Stench - tell your people not to leave
their cars without guard, not even for a
second. And let them ready for fight!
- B: Thanks, Helga, we'll pass on
your words to them! We all appreciate
your help. Looking forward to see
you in Unterriff. If you don't have
anything else, then Unterriff out.
- H: Helga Wagner group out.""",
    ),
    ("note", ""),
)

UNTERRIFF_DISCOVERED_TITLE = "Hope"
UNTERRIFF_DISCOVERED = """
When read the log, you're walking into the deckhouse
and asking everyone to gather. Pacing from wall to
wall, waiting for all to take their places, you're
trying to find the right words.

"Attention, everyone! We've got information, which
gives us hope. A hope that we can get to safety.
There is... an underwater city called Unterriff."
- you can see how your crew mates start to exchange
glances. - "It seems this place is built by government
or other powerful structure, so chances are high
that it's a real deal. We have coordinates, which
lead us close to the Black Sea. I think... and I
hope you agree with me, we must check this clue. No
one can guarantee it'll save us from the Stench...
but, at least, we have a clear direction now."

Everyone's keeping silence for several seconds.
"I guess we've to try!" - Daren shouts finally,
and others start to happily nod their heads and
smile. The crew agree!

Then let's leave this cold inimical country and
search for Unterriff! Turn up the heat!
"""

CREDITS = """
Great job, Captain! You've found your way through
this rough and inimical country of Silewer. It's
not over yet, and there will be more to sacrifice,
but until now you survived the adversity. Let's
summarize the decisions you've made.
\n\n
Chapter 1
"Something's acting up"
- {decision_0}

Chapter 2
"Orphans"
- {decision_1}

Chapter 3
"Bad cops"
- {decision_2}

Chapter 4
"The last place"
- {decision_3}

Chapter 5
"Refugees not welcome"
- {decision_4}

Chapter 6
"Low on food"
- {decision_5}

Chapter 7
"Blockpost"
- {decision_6}

Chapter 8
"Supplies stealer"
- {decision_7}

Chapter 9
"Little one"
- {decision_8}
\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n
These decisions characterize you {leader_desc}
\n\n\n\n\n\n\n\n\n\n\n\n\n
Forward Only
Episode 1
Seepage
\n\n
Developed by
Ilya Faer
\n\n\n\n\n\n\n\n
To be continued...
"""

ROUGH_LEADER = """
as a cold blooded and harsh leader. You see
your purpose and you achieve it no matter
the cost. The real life is cruel and unjust,
you accept it and bring sacrifices when
necessary. To make the machine move, you
have to burn fuel after all.
"""

OPPORTUNIST_LEADER = """
as an opportunist. It's hard to say
whether you're good or cruel, you're
mostly a selective one. You're making
decisions that better fit the situation
itself, than morals. And it brings good
as well as pain to those around you.
"""

EMPATHIC_LEADER = """
as an empathetic leader. You're doing
your best for your people, but you also
make sure not to hurt others without
a good strong reason. Even the End Of
Days doesn't destroy your compassion
and human decency. Hold this!
"""
