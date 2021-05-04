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
