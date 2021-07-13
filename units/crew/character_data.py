"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Character and enemies classes definitions.
"""

CLASSES = {
    "male_soldier": {
        "health": 100,
        "energy_gain": 50,
        "energy_spend": 30,
        "healing": 27,
        "shots_num": 2,
        "shot_snd": "rifle_shot1",
    },
    "female_soldier": {
        "health": 80,
        "energy_gain": 40,
        "energy_spend": 30,
        "healing": 27,
        "shots_num": 2,
        "shot_snd": "rifle_shot1",
    },
    "male_raider": {
        "health": 100,
        "energy_gain": 35,
        "energy_spend": 23,
        "healing": 17,
        "shots_num": 1,
        "shot_snd": "shotgun_shot1",
    },
    "female_raider": {
        "health": 80,
        "energy_gain": 30,
        "energy_spend": 23,
        "healing": 17,
        "shots_num": 1,
        "shot_snd": "shotgun_shot1",
    },
    "male_anarchist": {
        "health": 100,
        "energy_gain": 50,
        "energy_spend": 30,
        "healing": 27,
        "shots_num": 3,
        "shot_snd": "pistol_shot1",
    },
    "female_anarchist": {
        "health": 80,
        "energy_gain": 40,
        "energy_spend": 30,
        "healing": 27,
        "shots_num": 2,
        "shot_snd": "pistol_shot1",
    },
}

NAMES = {
    "male": (
        "Aaron",
        "Adam",
        "Aidan",
        "Alex",
        "Alexis",
        "Antony",
        "Arnold",
        "Ben",
        "Bruce",
        "Chris",
        "Clint",
        "Cody",
        "Cory",
        "Craig",
        "Donnie",
        "Ed",
        "Elijah",
        "Eric",
        "Frank",
        "James",
        "Jerome",
        "Jordan",
        "Josh",
        "Justin",
        "Lewis",
        "Mathew",
        "Max",
        "Mike",
        "Nathan",
        "Neill",
        "Paul",
        "Peter",
        "Philip",
        "Roy",
        "Shawn",
        "Sid",
        "Steven",
        "Tim",
        "Thomas",
        "Tyler",
    ),
    "female": (
        "Adriana",
        "Angelina",
        "Barbara",
        "Casey",
        "Charlotte",
        "Christine",
        "Claudia",
        "Clara",
        "Cobie",
        "Dolores",
        "Elizabeth",
        "Emily",
        "Emma",
        "Eva",
        "Gillian",
        "Helena",
        "Isabela",
        "Jennifer",
        "Jessica",
        "Julia",
        "Karen",
        "Kate",
        "Laura",
        "Maeve",
        "Megan",
        "Melissa",
        "Mia",
        "Miranda",
        "Naomi",
        "Olivia",
        "Rachael",
        "Radha",
        "Samara",
        "Sara",
        "Scarlett",
        "Sofia",
        "Stephanie",
        "Teresa",
        "Vanessa",
        "Victoria",
    ),
}

TRAITS = [
    ("Fast hands", "Snail"),
    ("Cat eyes", "Fear of dark"),
    ("Masochism", "Hemophobia"),
    ("Immunity", "Weak immunity"),
    ("Liberal", "Loner"),
    ("Bloodthirsty", "Nervousness"),
    ("Deep breath", "Motion sickness"),
    ("Mechanic", "Pharmacophobia"),
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
    "Loner": "x1.3 damage while alone on the Train part",
    "Bloodthirsty": "+7 health for a killed enemy unit",
    "Nervousness": "+25% energy spend while in fight",
    "Deep breath": "Avoid the Stench poison for the first 1 min",
    "Motion sickness": "Doesn't restore on high movement speed",
    "Mechanic": "Repairs the Train, while not resting",
    "Pharmacophobia": "Self-healing 40% slower",
}