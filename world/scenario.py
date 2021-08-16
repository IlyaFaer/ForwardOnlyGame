"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The main game scenario.
"""
import random

from direct.gui.DirectGui import (
    DGG,
    DirectButton,
    DirectFrame,
    DirectLabel,
)
from panda3d.core import TransparencyAttrib

from gui.widgets import GUI_PIC, RUST_COL
from .scenario_data import SCENARIO


class Scenario:
    """The game scenario orchestrator.

    Tracks on which part of the scenario the player is, controls
    the next scenario steps and performs choice consequences effects.

    One scenario chapter includes a situation in which the player
    has to make a decision. Decision will have consequences, positive
    or negative, but in any case the player will become one step
    closer to figuring out the way to survive the Stench. After
    every chapter the player will also get a note written in a
    diary fashion. The note will give the player more info about
    the Stench, Captain, the Adjutant and how the cataclysm
    started to destroy the World.

    Args:
        current_chapter (int): The chapter number to start with.
    """

    def __init__(self, current_chapter=None):
        if current_chapter is not None:
            self.current_chapter = current_chapter
        else:
            self.current_chapter = -1

        self._list = DirectFrame(
            frameSize=(-0.73, 0.73, -0.9, 0.9),
            frameTexture=GUI_PIC + "paper1.png",
            state=DGG.NORMAL,
        )
        self._list.setDepthTest(False)
        self._list.setTransparency(TransparencyAttrib.MAlpha)
        self._list.hide()

        self._name = DirectLabel(
            parent=self._list,
            text="",
            frameSize=(0.4, 0.4, 0.4, 0.4),
            text_scale=0.05,
            pos=(-0.4, 0, 0.7),
        )
        self._type = DirectLabel(
            parent=self._list,
            text="Scenario",
            frameSize=(0.4, 0.4, 0.4, 0.4),
            text_scale=0.035,
            pos=(-0.13, 0, 0.699),
        )
        self._desc = DirectLabel(
            parent=self._list,
            text="",
            frameSize=(0.6, 0.6, 0.6, 0.6),
            text_scale=0.04,
            pos=(0, 0, 0.55),
        )

        self._buts = []
        z_coor = -0.5
        for _ in range(3):
            self._buts.append(
                DirectButton(
                    parent=self._list,
                    text="Text",
                    text_fg=RUST_COL,
                    text_shadow=(0, 0, 0, 1),
                    frameColor=(0, 0, 0, 0),
                    frameSize=(-9, 9, -0.3, 0.7),
                    scale=(0.05, 0, 0.05),
                    clickSound=base.main_menu.click_snd,  # noqa: F821
                    pos=(0, 0, z_coor),
                )
            )
            z_coor -= 0.1

        self._done_but = DirectButton(
            parent=self._list,
            text="Done",
            text_fg=RUST_COL,
            text_shadow=(0, 0, 0, 1),
            frameColor=(0, 0, 0, 0),
            frameSize=(-9, 9, -0.3, 0.7),
            scale=(0.05, 0, 0.05),
            clickSound=base.main_menu.click_snd,  # noqa: F821
            pos=(0, 0, -0.8),
            command=self.hide_chapter,
        )

    def _choose_variant(self, var):
        """Process the player's choice and do consequences.

        Args:
            var (str): Variant id.
        """
        consequences = SCENARIO[self.current_chapter]["variants"][var]
        for but in self._buts:
            but.hide()

        self._desc["text"] = consequences["desc"]
        for effect in consequences["effects"]:
            getattr(self, effect[0])(*effect[1])

        base.journal.add_page(self.current_chapter)  # noqa: F821
        self._done_but.show()

    def do_build_camp_effect(self):
        """Do effects for building a camp for orphans choice."""
        base.helped_children = True  # noqa: F821

    def do_get_money(self, money):
        """Get or lose the given amount of money.

        Args:
            money (int): Money amount to get/lose.
        """
        base.dollars += money  # noqa: F821

    def do_plus_resource(self, name, value):
        """Change the given resource amount.

        Args:
            name (str): Resource name.
            value (int): Amount delta.
        """
        base.plus_resource(name, value)  # noqa: F821

    def do_enemy_inc_effect(self):
        """Make enemy stronger effect."""
        base.world.enemy.score += 3  # noqa: F821

    def do_character_effect(self, char, effect):
        """Do choice consequences effect to the given character.

        Args:
            char (units.crew.character.Character):
                The character to do effect to.
            effect (dict): The effect description.
        """
        for key, value in effect.items():
            setattr(char, key, getattr(char, key) + value)

    def do_characters_effect(self, effect, to_one=False):
        """Do choice consequences effects to the crew.

        Args:
            effect (dict): Effect description.
            to_one (bool): Effect targets only one random character.
        """
        if to_one:
            self.do_character_effect(
                random.choice(list(base.team.chars.values())), effect  # noqa: F821
            )
            return

        for char in base.team.chars.values():  # noqa: F821
            self.do_character_effect(char, effect)

    def do_locomotive_damage(self, damage):
        """Do some damage to the Adjutant.

        Args:
            damage (int): Amount of damage to do.
        """
        base.train.get_damage(damage)  # noqa: F821

    def do_no_effect(self):
        """No choice consequences method."""
        pass

    def hide_chapter(self):
        """Hide the scenario GUI."""
        self._list.hide()

    def do_stench_moves_effect(self, steps):
        """Move the Stench frontier several miles deeper into the Silewer.

        Args:
            steps (int): Number of miles to cover with the Stench.
        """
        for _ in range(steps):
            base.world.make_stench_step()  # noqa: F821

    def start_chapter(self, task):
        """Start a new scenario chapter."""
        self.current_chapter += 1

        base.train.ctrl.set_controls(base.train)  # noqa: F821
        base.camera_ctrl.enable_ctrl_keys()  # noqa: F821

        base.world.outings_mgr.hide_outing()  # noqa: F821
        base.traits_gui.hide()  # noqa: F821

        if self.current_chapter <= 3:
            self.show_chapter_situation()  # noqa: F821

            base.world.drop_place_of_interest()  # noqa: F821

        return task.done

    def show_chapter_situation(self):
        """Show the situation description and the possible variants."""
        self._done_but.hide()
        self._name["text"] = "Chapter " + str(self.current_chapter + 1)
        self._desc["text"] = SCENARIO[self.current_chapter]["intro"]

        for index, var in enumerate(SCENARIO[self.current_chapter]["variants"]):
            self._buts[index]["text"] = var
            self._buts[index]["extraArgs"] = [var]
            self._buts[index]["command"] = self._choose_variant
            self._buts[index].show()

        self._list.show()
