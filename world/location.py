"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Locations configurations. Describes which models should be
used on each location and their arrangement formulas.
"""

PLAINS_TREES = ("tree1", "tree2", "tree3", "red_tree", "yellow_tree")
PLAINS_GRASS = (
    "sp_grass1",
    "sp_grass2",
    "sp_grass3",
    "sp_grass4",
    "sp_grass5",
    "sp_grass6",
    "sp_grass7",
)

LOCATION_CONF = {
    "ambient_sounds": ("meadow_noon", "meadow_night"),
    "with_quantity": (
        {"models": PLAINS_TREES, "quantity": (13, 23), "square": "wide"},
        {"models": ("small_tree1",), "quantity": (1, 3), "square": "wide"},
        {"models": ("stump1",), "quantity": (1, 4), "square": "wide"},
        {"models": PLAINS_GRASS, "quantity": (20, 35), "square": "wide"},
        {"models": ("stone1",), "quantity": (2, 8), "square": "wide"},
    ),
    "with_chance": (
        {"models": ("grave1", "grave2"), "chance": 6, "square": "wide"},
        {
            "models": ("fireplace1", "tent", "hay_stack1"),
            "chance": 7,
            "square": "wide",
        },
        {"models": ("tire1",), "chance": 2, "square": "wide"},
        {"models": ("cart1",), "chance": 4, "square": "wide"},
        {"models": ("chapel1", "spring1"), "chance": 1, "square": "wide"},
    ),
    # enemy territory configurations
    "et_with_quantity": (
        {"models": PLAINS_TREES, "quantity": (5, 10), "square": "narrow"},
        {"models": ("small_tree1",), "quantity": (1, 3), "square": "narrow"},
        {"models": PLAINS_GRASS, "quantity": (15, 40), "square": "wide"},
        {"models": ("stone1",), "quantity": (2, 8), "square": "wide"},
    ),
    "et_with_chance": (
        {"models": ("stump1",), "chance": 7, "square": "narrow"},
        {"models": ("cart1",), "chance": 4, "square": "narrow"},
    ),
}
