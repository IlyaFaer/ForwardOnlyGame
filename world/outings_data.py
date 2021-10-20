"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Outings scenarios and effects.
"""

ENEMY_CAMP = [
    {
        "index": 0,
        "class_weights": {"soldier": 13.3, "raider": 4, "anarchist": 6},
        "assignees": 3,
        "day_part_weights": {"night": 10, "morning": 0, "noon": 3, "evening": 8},
        "results": (
            {"score": (0, 20), "effects": {"train": {"durability": -80}}},
            {
                "score": (20, 40),
                "effects": {
                    "char_1": {"health": -15},
                    "char_2": {"health": -15},
                    "char_3": {"health": -25},
                },
            },
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"money": 90}},
            {
                "score": (80, 101),
                "effects": {"money": 100, "stimulators": 1, "char_1": {"health": -15}},
            },
        ),
    },
    {
        "index": 1,
        "class_weights": {"soldier": 40, "raider": 20, "anarchist": 9},
        "assignees": 1,
        "day_part_weights": {"night": 0, "morning": 10, "noon": 6, "evening": 4},
        "results": (
            {"score": (0, 20), "effects": {"char_1": {"health": -25}}},
            {"score": (20, 40), "effects": {"char_1": {"health": -10}}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"money": 70}},
            {"score": (80, 101), "effects": {"money": 100}},
        ),
    },
    {
        "index": 2,
        "class_weights": {"soldier": 20, "raider": 6, "anarchist": 12},
        "assignees": 2,
        "day_part_weights": {"night": 0, "morning": 3, "noon": 10, "evening": 7},
        "results": (
            {
                "score": (0, 20),
                "effects": {"char_1": {"health": -35}, "char_2": {"energy": -20}},
            },
            {"score": (20, 40), "effects": {"train": {"durability": -40}}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"money": 80}},
            {"score": (80, 101), "effects": {"money": 100}},
        ),
    },
    {
        "index": 3,
        "class_weights": {"soldier": 20, "raider": 7, "anarchist": 12},
        "assignees": 2,
        "day_part_weights": {"night": 4, "morning": 5, "noon": 10, "evening": 2},
        "results": (
            {
                "score": (0, 20),
                "effects": {"char_1": {"health": -40}, "char_2": {"health": -10}},
            },
            {
                "score": (20, 40),
                "effects": {"char_1": {"health": -10}, "char_2": {"health": -10}},
            },
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"money": 80}},
            {"score": (80, 101), "effects": {"money": 90, "durability": 100}},
        ),
    },
    {
        "index": 4,
        "class_weights": {"soldier": 13.3, "raider": 4, "anarchist": 9},
        "assignees": 3,
        "day_part_weights": {"night": 10, "morning": 0, "noon": 4, "evening": 7},
        "results": (
            {"score": (0, 20), "effects": {}},
            {"score": (20, 40), "effects": {"select_char": {"health": 15}}},
            {"score": (40, 60), "effects": {"money": 40}},
            {"score": (60, 80), "effects": {"money": 60, "smoke_filters": 1}},
            {"score": (80, 101), "effects": {"money": 200}},
        ),
    },
    {
        "index": 5,
        "class_weights": {"soldier": 13.3, "raider": 10, "anarchist": 5},
        "assignees": 3,
        "day_part_weights": {"night": 0, "morning": 2, "noon": 6, "evening": 10},
        "results": (
            {"score": (0, 20), "effects": {"train": {"durability": -60}}},
            {"score": (20, 40), "effects": {"assignees": {"health": -20}}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"money": 80}},
            {"score": (80, 101), "effects": {"money": 130}},
        ),
    },
    {
        "index": 6,
        "class_weights": {"soldier": 20, "raider": 12, "anarchist": 5},
        "assignees": 2,
        "day_part_weights": {"night": 0, "morning": 5, "noon": 10, "evening": 7},
        "results": (
            {"score": (0, 20), "effects": {"money": -90}},
            {"score": (20, 40), "effects": {"char_1": {"health": -20}}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"all": {"health": 10}}},
            {"score": (80, 101), "effects": {"money": 170}},
        ),
    },
    {
        "index": 7,
        "class_weights": {"soldier": 40, "raider": 20, "anarchist": 9},
        "assignees": 1,
        "day_part_weights": {"night": 10, "morning": 7, "noon": 0, "evening": 3},
        "results": (
            {"score": (0, 20), "effects": {"all": {"health": -30}}},
            {"score": (20, 40), "effects": {"char_1": {"energy": -30}}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"all": {"health": 20}}},
            {"score": (80, 101), "effects": {"money": 130}},
        ),
    },
    {
        "index": 8,
        "class_weights": {"soldier": 40, "raider": 20, "anarchist": 9},
        "assignees": 1,
        "day_part_weights": {"night": 10, "morning": 0, "noon": 4, "evening": 7},
        "results": (
            {"score": (0, 20), "effects": {"char_1": {"add_trait": (5, 1)}}},
            {"score": (20, 40), "effects": {"char_1": {"health": -25}}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"recruit": 70}},
            {"score": (80, 101), "effects": {"train": {"durability": 70}}},
        ),
    },
    {
        "index": 9,
        "class_weights": {"soldier": 13.3, "raider": 8, "anarchist": 5},
        "assignees": 3,
        "day_part_weights": {"night": 10, "morning": 7, "noon": 0, "evening": 3},
        "results": (
            {"score": (0, 20), "effects": {"train": {"durability": -60}}},
            {"score": (20, 40), "effects": {"money": -50}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"medicine_boxes": 1}},
            {"score": (80, 101), "effects": {"money": 120}},
        ),
    },
]

LOOTING = [
    {
        "index": 10,
        "class_weights": {"soldier": 20, "raider": 40, "anarchist": 9},
        "assignees": 1,
        "day_part_weights": {"night": 0, "morning": 3, "noon": 10, "evening": 5},
        "results": (
            {
                "score": (0, 20),
                "effects": {"char_1": {"energy": -50, "health": -15}},
            },
            {"score": (20, 40), "effects": {"char_1": {"energy": -15}}},
            {"score": (40, 60), "effects": {"select_char": {"health": 10}}},
            {"score": (60, 80), "effects": {"train": {"durability": 100}}},
            {"score": (80, 101), "effects": {"smoke_filters": 1}},
        ),
    },
    {
        "index": 11,
        "class_weights": {"soldier": 6, "raider": 20, "anarchist": 13},
        "assignees": 2,
        "day_part_weights": {"night": 0, "morning": 7, "noon": 10, "evening": 3},
        "results": (
            {
                "score": (0, 20),
                "effects": {
                    "char_1": {"energy": -50, "health": -30},
                    "char_2": {"energy": -20},
                },
            },
            {
                "score": (20, 40),
                "effects": {"char_1": {"energy": -30}, "char_2": {"energy": -30}},
            },
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"select_char": {"energy": 40}}},
            {"score": (80, 101), "effects": {"medicine_boxes": 1}},
        ),
    },
    {
        "index": 12,
        "class_weights": {"soldier": 9, "raider": 13.3, "anarchist": 3},
        "assignees": 3,
        "day_part_weights": {"night": 8, "morning": 2, "noon": 5, "evening": 10},
        "results": (
            {"score": (0, 20), "effects": {"all": {"energy": -40}},},
            {
                "score": (20, 40),
                "effects": {
                    "char_2": {"energy": -40, "health": -20},
                    "char_1": {"energy": -25},
                    "char_3": {"energy": -25},
                },
            },
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"money": 50}},
            {"score": (80, 101), "effects": {"train": {"durability": 100}}},
        ),
    },
    {
        "index": 13,
        "class_weights": {"soldier": 9, "raider": 13.3, "anarchist": 4},
        "assignees": 3,
        "day_part_weights": {"night": 10, "morning": 2, "noon": 5, "evening": 8},
        "results": (
            {
                "score": (0, 20),
                "effects": {
                    "char_1": {"health": -30},
                    "char_2": {"energy": -30},
                    "char_3": {"health": -30},
                },
            },
            {
                "score": (20, 40),
                "effects": {
                    "char_1": {"energy": -15, "health": -10},
                    "char_2": {"energy": -10},
                    "char_3": {"energy": -10},
                },
            },
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"assignees": {"health": 20}}},
            {"score": (80, 101), "effects": {"money": 40}},
        ),
    },
    {
        "index": 14,
        "class_weights": {"soldier": 7, "raider": 20, "anarchist": 14},
        "assignees": 2,
        "day_part_weights": {"night": 2, "morning": 4, "noon": 10, "evening": 8},
        "results": (
            {"score": (0, 20), "effects": {}},
            {"score": (20, 40), "effects": {"train": {"durability": 50}}},
            {"score": (40, 60), "effects": {"stimulators": 1}},
            {"score": (60, 80), "effects": {"medicine_boxes": 1}},
            {"score": (80, 101), "effects": {"all": {"energy": 35}}},
        ),
    },
    {
        "index": 15,
        "class_weights": {"soldier": 4, "raider": 13.3, "anarchist": 10},
        "assignees": 3,
        "day_part_weights": {"night": 5, "morning": 7, "noon": 10, "evening": 2},
        "results": (
            {"score": (0, 20), "effects": {"assignees": {"health": -20}}},
            {"score": (20, 40), "effects": {"assignees": {"energy": -25}}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"money": 50}},
            {"score": (80, 101), "effects": {"train": {"durability": 100}}},
        ),
    },
    {
        "index": 16,
        "class_weights": {"soldier": 6, "raider": 20, "anarchist": 13},
        "assignees": 2,
        "day_part_weights": {"night": 10, "morning": 0, "noon": 3, "evening": 5},
        "results": (
            {"score": (0, 20), "effects": {"char_1": {"health": -35}}},
            {"score": (20, 40), "effects": {"assignees": {"energy": -15}}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"money": 50}},
            {
                "score": (80, 101),
                "effects": {"medicine_boxes": 1, "smoke_filters": 1},
            },
        ),
    },
    {
        "index": 17,
        "class_weights": {"soldier": 20, "raider": 40, "anarchist": 9},
        "assignees": 1,
        "day_part_weights": {"night": 7, "morning": 0, "noon": 3, "evening": 10},
        "results": (
            {"score": (0, 20), "effects": {"char_1": {"energy": -35}}},
            {"score": (20, 40), "effects": {"train": {"durability": -60}}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"select_char": {"health": 30}}},
            {"score": (80, 101), "effects": {"stimulators": 2}},
        ),
    },
    {
        "index": 18,
        "class_weights": {"soldier": 9, "raider": 40, "anarchist": 19},
        "assignees": 1,
        "day_part_weights": {"night": 0, "morning": 7, "noon": 10, "evening": 4},
        "results": (
            {"score": (0, 20), "effects": {"char_1": {"health": -25}}},
            {"score": (20, 40), "effects": {"money": -30}},
            {"score": (40, 60), "effects": {}},
            {
                "score": (60, 80),
                "effects": {"select_char": {"health": 25, "energy": 20}},
            },
            {"score": (80, 101), "effects": {"durability": 100}},
        ),
    },
    {
        "index": 19,
        "class_weights": {"soldier": 12, "raider": 20, "anarchist": 7},
        "assignees": 2,
        "day_part_weights": {"night": 0, "morning": 5, "noon": 10, "evening": 3},
        "results": (
            {"score": (0, 20), "effects": {"char_2": {"health": -25}}},
            {"score": (20, 40), "effects": {"assignees": {"energy": -20}}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"money": 70}},
            {
                "score": (80, 101),
                "effects": {"stimulators": 1, "medicine_boxes": 1},
            },
        ),
    },
]

MEET = [
    {
        "index": 20,
        "class_weights": {"soldier": 5, "anarchist": 20, "raider": 13},
        "assignees": 2,
        "day_part_weights": {"night": 0, "morning": 10, "noon": 7, "evening": 4},
        "results": (
            {
                "score": (0, 20),
                "effects": {
                    "char_1": {"health": -10},
                    "char_2": {"add_trait": (5, 1)},
                },
            },
            {"score": (20, 40), "effects": {"assignees": {"energy": -15}}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"recruit": 80}},
            {
                "score": (80, 101),
                "effects": {"select_char": {"add_trait": (3, 0)}},
            },
        ),
    },
    {
        "index": 21,
        "class_weights": {"soldier": 10, "anarchist": 40, "raider": 22},
        "assignees": 1,
        "day_part_weights": {"night": 0, "morning": 4, "noon": 8, "evening": 10},
        "results": (
            {"score": (0, 20), "effects": {"char_1": {"add_trait": (3, 1)}}},
            {"score": (20, 40), "effects": {"char_1": {"health": -10}}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"cohesion_gain": 6}},
            {
                "score": (80, 101),
                "effects": {"select_char": {"add_trait": (2, 0)}},
            },
        ),
    },
    {
        "index": 22,
        "class_weights": {"soldier": 8, "anarchist": 13.3, "raider": 4},
        "assignees": 3,
        "day_part_weights": {"night": 8, "morning": 10, "noon": 4, "evening": 0},
        "results": (
            {
                "score": (0, 20),
                "effects": {
                    "char_2": {"add_trait": (1, 1)},
                    "char_3": {"add_trait": (1, 1)},
                },
            },
            {"score": (20, 40), "effects": {"assignees": {"health": -10}}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"money": 100}},
            {
                "score": (80, 101),
                "effects": {"select_char": {"add_trait": (0, 0)}, "money": 100},
            },
        ),
    },
    {
        "index": 23,
        "class_weights": {"soldier": 10, "anarchist": 40, "raider": 21},
        "assignees": 1,
        "day_part_weights": {"night": 0, "morning": 3, "noon": 7, "evening": 10},
        "results": (
            {"score": (0, 20), "effects": {"char_1": {"add_trait": (2, 1)}}},
            {"score": (20, 40), "effects": {"money": -40}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"cohesion_gain": 6}},
            {
                "score": (80, 101),
                "effects": {"select_char": {"add_trait": (5, 0)}},
            },
        ),
    },
    {
        "index": 24,
        "class_weights": {"soldier": 5, "anarchist": 20, "raider": 12.5},
        "assignees": 2,
        "day_part_weights": {"night": 0, "morning": 10, "noon": 7, "evening": 3},
        "results": (
            {
                "score": (0, 20),
                "effects": {"char_1": {"health": -20}, "char_2": {"health": -20}},
            },
            {"score": (20, 40), "effects": {}},
            {"score": (40, 60), "effects": {"select_char": {"health": 30}}},
            {
                "score": (60, 80),
                "effects": {"money": 90, "select_char": {"add_trait": (4, 0)}},
            },
            {"score": (80, 101), "effects": {"recruit": 60}},
        ),
    },
    {
        "index": 25,
        "class_weights": {"soldier": 3, "anarchist": 13.3, "raider": 7},
        "assignees": 3,
        "day_part_weights": {"night": 0, "morning": 3, "noon": 10, "evening": 6},
        "results": (
            {"score": (0, 20), "effects": {"char_2": {"add_trait": (1, 1)}}},
            {"score": (20, 40), "effects": {"money": -40}},
            {"score": (40, 60), "effects": {"medicine_boxes": -1}},
            {"score": (60, 80), "effects": {"money": 70}},
            {
                "score": (80, 101),
                "effects": {"select_char": {"add_trait": (6, 0)}},
            },
        ),
    },
    {
        "index": 26,
        "class_weights": {"soldier": 11, "anarchist": 20, "raider": 5},
        "assignees": 2,
        "day_part_weights": {"night": 3, "morning": 10, "noon": 7, "evening": 0},
        "results": (
            {"score": (0, 20), "effects": {"char_2": {"add_trait": (5, 1)}}},
            {"score": (20, 40), "effects": {"train": {"durability": -50}}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"recruit": 60}},
            {"score": (80, 101), "effects": {"stimulators": 1}},
        ),
    },
    {
        "index": 27,
        "class_weights": {"soldier": 7, "anarchist": 13.3, "raider": 3},
        "assignees": 3,
        "day_part_weights": {"night": 0, "morning": 3, "noon": 10, "evening": 7},
        "results": (
            {
                "score": (0, 20),
                "effects": {"assignees": {"health": -15, "energy": -25}},
            },
            {
                "score": (20, 40),
                "effects": {"char_3": {"health": -7, "add_trait": (6, 1)}},
            },
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"money": 50}},
            {
                "score": (80, 101),
                "effects": {"all": {"energy": 30}, "medicine_boxes": 1},
            },
        ),
    },
    {
        "index": 28,
        "class_weights": {"soldier": 20, "anarchist": 40, "raider": 9},
        "assignees": 1,
        "day_part_weights": {"night": 3, "morning": 0, "noon": 10, "evening": 7},
        "results": (
            {"score": (0, 20), "effects": {"char_1": {"add_trait": (1, 1)}}},
            {"score": (20, 40), "effects": {"char_1": {"health": -20}}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"money": 50}},
            {"score": (80, 101), "effects": {"char_1": {"add_trait": (7, 0)}}},
        ),
    },
    {
        "index": 29,
        "class_weights": {"soldier": 9, "anarchist": 40, "raider": 19},
        "assignees": 1,
        "day_part_weights": {"night": 0, "morning": 3, "noon": 10, "evening": 7},
        "results": (
            {"score": (0, 20), "effects": {"char_1": {"add_trait": (0, 1)}}},
            {"score": (20, 40), "effects": {"money": -50}},
            {"score": (40, 60), "effects": {}},
            {"score": (60, 80), "effects": {"money": -5, "medicine_boxes": 2}},
            {"score": (80, 101), "effects": {"recruit": 60}},
        ),
    },
]
