"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

GUI used for teaching players.
"""
from direct.gui.DirectGui import DGG, DirectButton, DirectFrame, DirectLabel
from panda3d.core import TransparencyAttrib

from .widgets import RUST_COL, SILVER_COL

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
            "Brake thrower will try to overtake you and\n"
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
            "do a lot of damage to your locomotive, but the\n"
            "machine gun overheat fast and requires time to\n"
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
            "Their new thought - telecontrolled rockets can\n"
            "do a lot of damage to your locomotive. Use Armor\n"
            "Plate upgrade to cover a side targeted by a rocket."
        ),
        "preview": "rocket",
        "but_text": "They won't stop us!",
        "title": "Skinheads start to use rockets!",
    },
}

MECHANIC_DESC = {
    "locomotive": {
        "descs": (
            (
                "This is the Adjutant - your locomotive. It helps\n"
                "you to move fast enough to overtake death, so\n"
                "take care of it. If it'll not be able to ride, your\n"
                "hours are numbered. The locomotive durability is\n"
                "reflected in the right bottom corner of the GUI."
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
                "Your main problem is the Stench. Its poisonous\n"
                "clouds are spreading fast and chaotic. If you\n"
                "got into it, you better accelerate to cross the\n"
                "cloud as fast as possible. You also should not\n"
                "stay long on the same place or ride in circles."
            ),
        ),
        "previews": ("the_stench1",),
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
                "of outings, each offers own type of trophies and\n"
                "prefers an exact unit class to be sent for it."
            ),
            (
                "An outing have five finals; the higher is your score,\n"
                "the better is final. Score includes four items:\n"
                "class fit - for the sent units class, condition - for\n"
                "their health and energy, cohesion - for total cohesion\n"
                "of the units, and a small special piece of score."
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
                "seen in his/her Status GUI. Also keep an eye for\n"
                "the disease icon - a sick character can bring a\n"
                "lot of troubles for the crew. Try to isolate\n"
                "diseased and cure them as soon as possible."
            ),
        ),
        "previews": ("character_status1", "character_status2"),
    },
}


class EnemyDesc:
    """Enemy class/object description.

    A teaching note about enemy class/object. Is shown on
    player's screen, when a new enemy class/object is added
    into the list of attacking enemy units.
    """

    def __init__(self, class_):
        self._fr = DirectFrame(
            frameSize=(-0.5, 0.5, -0.5, 0.5),
            frameColor=(0.14, 0.14, 0.14, 0.82),
            state=DGG.NORMAL,
        )
        DirectLabel(
            parent=self._fr,
            text=CLASS_DESCS[class_]["title"],
            text_fg=RUST_COL,
            text_scale=0.038,
            pos=(0, 0, 0.44),
            frameColor=(0, 0, 0, 0),
        )
        DirectFrame(
            parent=self._fr,
            frameTexture="teach_shots/{}.png".format(CLASS_DESCS[class_]["preview"]),
            pos=(0, 0, 0.15),
            frameSize=(-0.39, 0.39, -0.24, 0.24),
        ).setTransparency(TransparencyAttrib.MAlpha)
        DirectLabel(
            parent=self._fr,
            pos=(0, 0, -0.18),
            frameColor=(0, 0, 0, 0),
            text_fg=SILVER_COL,
            text_scale=0.035,
            text=CLASS_DESCS[class_]["desc"],
        )
        base.main_menu.bind_button(  # noqa: F821
            DirectButton(
                parent=self._fr,
                text=CLASS_DESCS[class_]["but_text"],
                text_scale=0.04,
                relief=None,
                pos=(0, 0, -0.45),
                text_fg=RUST_COL,
                command=self._hide,
                clickSound=base.main_menu.click_snd,  # noqa: F821
            )
        )

    def _hide(self):
        """Destroy the teaching note."""
        self._fr.destroy()


class MechanicDesc:
    """Teaching description of a game mechanic.

    Args:
        mechanic (str): The name of the game mechanic to be explained.
    """

    def __init__(self, mechanic):
        self._page = 0

        self._fr = DirectFrame(
            frameSize=(-0.5, 0.5, -0.5, 0.5),
            frameColor=(0.14, 0.14, 0.14, 0.82),
            state=DGG.NORMAL,
        )
        DirectLabel(
            parent=self._fr,
            text="Tutorial: " + mechanic,
            text_fg=RUST_COL,
            text_scale=0.038,
            pos=(0, 0, 0.44),
            frameColor=(0, 0, 0, 0),
        )
        self._preview = DirectFrame(
            parent=self._fr,
            frameTexture="teach_shots/{}.png".format(
                MECHANIC_DESC[mechanic]["previews"][self._page]
            ),
            pos=(0, 0, 0.15),
            frameSize=(-0.39, 0.39, -0.24, 0.24),
        )
        self._preview.setTransparency(TransparencyAttrib.MAlpha)

        self._desc = DirectLabel(
            parent=self._fr,
            pos=(0, 0, -0.18),
            frameColor=(0, 0, 0, 0),
            text_fg=SILVER_COL,
            text_scale=0.035,
            text=MECHANIC_DESC[mechanic]["descs"][self._page],
        )
        is_last_page = self._page + 1 == len(MECHANIC_DESC[mechanic]["descs"])

        self._but = DirectButton(
            parent=self._fr,
            text="Got it!" if is_last_page else "Next",
            text_scale=0.04,
            relief=None,
            pos=(0, 0, -0.45),
            text_fg=RUST_COL,
            command=self._hide if is_last_page else self._next_page,
            extraArgs=[] if is_last_page else [mechanic],
            clickSound=base.main_menu.click_snd,  # noqa: F821
        )
        base.main_menu.bind_button(self._but)  # noqa: F821

        base.train.ctrl.pause_movement()  # noqa: F821

    def _hide(self):
        """Destroy the teaching note."""
        self._fr.destroy()
        base.train.ctrl.start_move()  # noqa: F821

    def _next_page(self, mechanic):
        """Show the next page of the mechanic tutorial.

        Args:
            mechanic (str): The explained mechanic name.
        """
        self._page += 1

        is_last_page = self._page + 1 == len(MECHANIC_DESC[mechanic]["descs"])

        if is_last_page:
            self._but["text"] = "Got it!"
            self._but["command"] = self._hide
            self._but["extraArgs"] = []

        self._preview["frameTexture"] = "teach_shots/{}.png".format(
            MECHANIC_DESC[mechanic]["previews"][self._page]
        )
        self._desc["text"] = MECHANIC_DESC[mechanic]["descs"][self._page]
