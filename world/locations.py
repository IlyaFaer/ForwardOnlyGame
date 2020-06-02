"""Locations configurations.

Describes what models should be used on each
location and their arrangement formulas.
"""

LOCATIONS = {
    "Plains": {
        "with_quantity": (
            {
                "models": (
                    "sp_grass1",
                    "sp_grass2",
                    "sp_grass3",
                    "sp_grass4",
                    "sp_grass5",
                    "sp_grass6",
                    "sp_grass7",
                ),
                "quantity": (10, 40),
                "square": "wide",
            },
            {
                "models": ("tree1", "tree2", "tree3",),
                "quantity": (10, 20),
                "square": "wide",
            },
            {"models": ("stone1",), "quantity": (2, 8), "square": "wide"},
        ),
        "with_chance": (
            {"models": ("grave1", "grave2"), "chance": 7, "square": "wide"},
            {"models": ("fireplace1", "tent"), "chance": 8, "square": "wide"},
        ),
    }
}
