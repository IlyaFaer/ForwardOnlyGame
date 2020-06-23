"""Locations configurations.

Describes what models should be used on each
location and their arrangement formulas.
"""

PLAINS_TREES = ("tree1", "tree2", "tree3")
PLAINS_GRASS = (
    "sp_grass1",
    "sp_grass2",
    "sp_grass3",
    "sp_grass4",
    "sp_grass5",
    "sp_grass6",
    "sp_grass7",
)

LOCATIONS = {
    "Plains": {
        "ambient_sounds": ("meadow_noon", "meadow_night"),
        "enemy": "Skinheads",
        "with_quantity": (
            {"models": PLAINS_GRASS, "quantity": (10, 40), "square": "wide"},
            {"models": PLAINS_TREES, "quantity": (10, 20), "square": "wide"},
            {"models": ("small_tree1",), "quantity": (1, 3), "square": "wide"},
            {"models": ("stone1",), "quantity": (2, 8), "square": "wide"},
        ),
        "with_chance": (
            {"models": ("grave1", "grave2"), "chance": 6, "square": "wide"},
            {"models": ("fireplace1", "tent"), "chance": 7, "square": "wide"},
            {"models": ("stump1",), "chance": 7, "square": "wide"},
        ),
        # enemy territory configurations
        "et_with_quantity": (
            {"models": PLAINS_GRASS, "quantity": (10, 40), "square": "wide"},
            {"models": PLAINS_TREES, "quantity": (5, 10), "square": "narrow"},
            {"models": ("small_tree1",), "quantity": (1, 3), "square": "narrow"},
            {"models": ("stone1",), "quantity": (2, 8), "square": "wide"},
        ),
        "et_with_chance": (),
    }
}
