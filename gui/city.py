"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Cities GUI.
"""
import random

from direct.gui.DirectGui import DGG, DirectButton, DirectFrame, DirectLabel
from panda3d.core import TextNode, TransparencyAttrib

from personage.character_data import TRAITS
from utils import clear_wids
from .widgets import (
    GUI_PIC,
    RUST_COL,
    SILVER_COL,
    CharacterChooser,
    ItemChooser,
    UpgradeChooser,
)


class ResourceChooser(ItemChooser):
    """Widget to choose a resource to buy/sell it.

    Args:
        buy_but (panda3d.gui.DirectGui.DirectButton):
            Button "Buy" a resource.
        sell_but (panda3d.gui.DirectGui.DirectButton):
            Button "Sell" a resource.
    """

    def __init__(self, buy_but, sell_but):
        ItemChooser.__init__(self, is_shadowed=False)
        self._costs = {
            "medicine_boxes": 30,
            "smoke_filters": 35,
            "stimulators": 25,
        }
        self._buy_but = buy_but
        self._sell_but = sell_but

    @property
    def chosen_resource_cost(self):
        """The chosen resource cost.

        Returns:
            int: The chosen resource cost.
        """
        return self._costs[self._chosen_item]

    def _show_info(self):
        """Show the chosen resource info and its cost."""
        if len(self._items) == 0:
            self._name["text"] = ""
            self._chosen_item = None
            return

        if self._ind == len(self._items):
            self._ind = 0
        elif self._ind == -1:
            self._ind = len(self._items) - 1

        key = list(self._items.keys())[self._ind]
        self._chosen_item = self._items[key]

        self._name["text"] = key
        self._buy_but["text"] = "{label}\n{cost}$".format(
            label=base.labels.CITY[15],  # noqa: F821
            cost=str(self._costs[self._chosen_item]),
        )
        self._sell_but["text"] = "{label}\n{cost}$".format(
            label=base.labels.CITY[14],  # noqa: F821
            cost=str(self._costs[self._chosen_item]),
        )


class RecruitChooser(CharacterChooser):
    """Recruits chooser widget.

    Mostly it's working like a simple CharacterChooser,
    but it also calculates a cost of the chosen recruit
    and inserts it into the "Hire unit" button.

    Args:
        hire_but (panda3d.gui.DirectGui.DirectButton):
            "Hire unit" button object.
    """

    def __init__(self, hire_but):
        CharacterChooser.__init__(self, is_shadowed=False)
        self._costs = {}
        self._hire_but = hire_but

    @property
    def chosen_recruit_cost(self):
        """The chosen unit cost.

        Returns:
            int: The chosen unit cost in dollars.
        """
        return self._costs[self._chosen_item.id]

    def _show_info(self):
        """Show the chosen recruit info and his/her cost."""
        CharacterChooser._show_info(self)
        self._hire_but["text"] = "{label}\n{cost}$".format(
            label=base.labels.CITY[13],  # noqa: F821
            cost=str(self._costs[self._chosen_item.id]),
        )

    def prepare(self, parent, pos, items, init_ind=None):
        """Prepare the chooser widget.

        Calculates costs of all the given recruits.

        Args:
            parent (panda3d.core.NodePath): Parent widget.
            pos (tuple): New widget position.
            items (dict): Items to iterate through.
            init_ind (int): Index of the initial value.
        """
        for id_, rec in items.items():
            cost = 150
            for trait in rec.traits:
                for trait_pair in TRAITS:
                    if trait == trait_pair[0]:
                        cost += 20
                        break
                    if trait == trait_pair[1]:
                        cost -= 20
                        break

            self._costs[id_] = cost

        CharacterChooser.prepare(self, parent, pos, items, init_ind=None)


class CityGUI:
    """City GUI.

    Includes several services: healing and regaining energy of the
    player characters, recruiting new characters, repairing the Train,
    buying the Train upgrades.
    """

    def __init__(self):
        self._repl_wids = []
        self._recruits = []
        self._visit_num = 1

        self._amb_snd = loader.loadSfx("sounds/hangar_ambient.ogg")  # noqa: F821
        self._amb_snd.setVolume(0)
        self._amb_snd.setLoop(True)

        self._coins_s_snd = loader.loadSfx("sounds/GUI/coins_short.ogg")  # noqa: F821
        self._coins_l_snd = loader.loadSfx("sounds/GUI/coins_long.ogg")  # noqa: F821
        self._toot_snd = loader.loadSfx("sounds/train/toot1.ogg")  # noqa: F821
        self._add_upgrade_snd = loader.loadSfx(  # noqa: F821
            "sounds/GUI/install_upgrade.ogg"
        )
        self.write_snd = loader.loadSfx("sounds/GUI/write.ogg")  # noqa: F821

        self._reward_fr = None
        self._fr = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.35, 0.35, -0.4, 0.7),
            pos=(0.85, 0, -0.82),
            frameTexture=GUI_PIC + "metal1.png",
            state=DGG.NORMAL,
        )
        self._fr.setTransparency(TransparencyAttrib.MAlpha)
        self._fr.hide()

        DirectLabel(  # Services
            parent=self._fr,
            text=base.labels.CITY[0],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.045,
            text_fg=RUST_COL,
            pos=(0, 0, 0.62),
        )
        self._party_but = DirectButton(  # Party
            parent=self._fr,
            text_scale=0.035,
            text_fg=SILVER_COL,
            text=base.labels.CITY[1],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            relief=None,
            command=self._show_party,
            extraArgs=[0.56],
            pos=(-0.1, 0, 0.56),
            clickSound=base.main_menu.click_snd,  # noqa: F821
        )
        base.main_menu.bind_button(self._party_but)  # noqa: F821

        self._train_but = DirectButton(  # Train
            parent=self._fr,
            text_scale=0.035,
            text_fg=RUST_COL,
            text=base.labels.CITY[2],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            relief=None,
            command=self._show_train,
            extraArgs=[0.56],
            pos=(0.1, 0, 0.56),
            clickSound=base.main_menu.click_snd,  # noqa: F821
        )
        base.main_menu.bind_button(self._train_but)  # noqa: F821

        base.main_menu.bind_button(  # noqa: F821
            DirectButton(  # Exit city
                parent=self._fr,
                pos=(-0.205, 0, -0.35),
                text_fg=RUST_COL,
                text=base.labels.CITY[3],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                relief=None,
                text_scale=0.035,
                command=self._exit_city,
            )
        )
        base.main_menu.bind_button(  # noqa: F821
            DirectButton(  # Turn around and exit
                parent=self._fr,
                pos=(0.1, 0, -0.35),
                text_fg=RUST_COL,
                text=base.labels.CITY[4],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                relief=None,
                text_scale=0.035,
                command=self._exit_city,
                extraArgs=[True],
            )
        )

    def _show_train(self, z_coor):
        """Show the Train management GUI tab.

        Args:
            z_coor (float): Z-coordinate for widgets.
        """
        clear_wids(self._repl_wids)

        self._party_but["text_fg"] = RUST_COL
        self._train_but["text_fg"] = SILVER_COL

        z_coor -= 0.07
        self._repl_wids.append(
            DirectLabel(  # Locomotive
                parent=self._fr,
                text=base.labels.CITY[5],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.035,
                text_align=TextNode.ALeft,
                text_fg=RUST_COL,
                pos=(-0.3, 0, z_coor),
            )
        )
        z_coor -= 0.08
        self._repl_wids.append(
            DirectLabel(  # Repair
                parent=self._fr,
                frameColor=(0, 0, 0, 0.3),
                text_fg=SILVER_COL,
                text=base.labels.CITY[6],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                text_align=TextNode.ALeft,
                text_scale=0.03,
                pos=(-0.25, 0, z_coor),
            )
        )
        self._repl_wids.append(
            DirectButton(
                parent=self._fr,
                pos=(-0.05, 0, z_coor + 0.015),
                text_fg=SILVER_COL,
                text="+50\n15$",
                scale=(0.075, 0, 0.075),
                relief=None,
                text_scale=0.45,
                command=self._repair,
                extraArgs=[50],
            )
        )
        self._repl_wids.append(
            DirectButton(
                parent=self._fr,
                pos=(0.07, 0, z_coor + 0.015),
                text_fg=SILVER_COL,
                text="+200\n60$",
                scale=(0.075, 0, 0.075),
                relief=None,
                text_scale=0.45,
                command=self._repair,
                extraArgs=[200],
            )
        )

        z_coor -= 0.09
        self._repl_wids.append(
            DirectLabel(  # Upgrade
                parent=self._fr,
                text=base.labels.CITY[7],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                text_align=TextNode.ALeft,
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.035,
                text_fg=RUST_COL,
                pos=(-0.3, 0, z_coor),
            )
        )
        up_desc = DirectLabel(
            parent=self._fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.03,
            text_fg=SILVER_COL,
            pos=(-0.1, 0, z_coor - 0.14),
        )
        self._repl_wids.append(up_desc)

        up_cost = DirectLabel(
            parent=self._fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.035,
            text_fg=SILVER_COL,
            pos=(0.23, 0, z_coor - 0.17),
        )
        self._repl_wids.append(up_cost)

        but = DirectButton(  # Purchase
            parent=self._fr,
            pos=(0.2, 0, z_coor - 0.3),
            text_fg=RUST_COL,
            text=base.labels.CITY[8],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            relief=None,
            text_scale=0.035,
            command=self._purchase_upgrade,
        )
        self._repl_wids.append(but)
        base.main_menu.bind_button(but)  # noqa: F821

        z_coor -= 0.05
        self._up_chooser = UpgradeChooser(up_desc, up_cost)
        self._up_chooser.prepare(
            self._fr,
            (0, 0, z_coor),
            base.train.possible_upgrades(self._visit_num),  # noqa: F821
        )
        self._repl_wids.append(self._up_chooser)

    def _purchase_upgrade(self):
        """Buy the chosen upgrade and install it on to the Train."""
        upgrade = self._up_chooser.chosen_item
        if (
            upgrade is None
            or not base.res_gui.check_enough_money(  # noqa: F821:  # noqa: F821
                int(upgrade["cost"][:-1])
            )
        ):
            return

        base.main_menu.click_snd.play()  # noqa: F821
        self._add_upgrade_snd.play()
        base.dollars -= int(upgrade["cost"][:-1])  # noqa: F821

        base.train.install_upgrade(upgrade)  # noqa: F821
        self._up_chooser.pop_upgrade(upgrade["name"])

    def _show_party(self, shift):
        """Show units management tab.

        Args:
            shift (float): Z-coordinate.
        """
        clear_wids(self._repl_wids)

        self._party_but["text_fg"] = SILVER_COL
        self._train_but["text_fg"] = RUST_COL

        shift -= 0.07
        # the crew GUI
        self._repl_wids.append(
            DirectLabel(  # Crew
                parent=self._fr,
                text=base.labels.CITY[9],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                text_align=TextNode.ALeft,
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.035,
                text_fg=RUST_COL,
                pos=(-0.3, 0, shift),
            )
        )

        self._char_chooser = CharacterChooser()
        self._char_chooser.prepare(
            self._fr, (0, 0, 0.45), base.team.chars  # noqa: F821
        )
        self._repl_wids.append(self._char_chooser)

        shift -= 0.14
        self._repl_wids.append(
            DirectLabel(  # Health
                parent=self._fr,
                frameColor=(0, 0, 0, 0.3),
                text_fg=SILVER_COL,
                text=base.labels.CHARACTERS[2],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                text_scale=0.03,
                pos=(-0.2, 0, shift),
            )
        )
        self._repl_wids.append(
            DirectButton(
                parent=self._fr,
                pos=(-0.05, 0, shift + 0.02),
                text_fg=SILVER_COL,
                text="+10\n10$",
                scale=(0.075, 0, 0.075),
                relief=None,
                text_scale=0.45,
                command=self._heal,
                extraArgs=[10],
            )
        )
        self._repl_wids.append(
            DirectButton(
                parent=self._fr,
                pos=(0.07, 0, shift + 0.02),
                text_fg=SILVER_COL,
                text="+50\n50$",
                scale=(0.075, 0, 0.075),
                relief=None,
                text_scale=0.45,
                command=self._heal,
                extraArgs=[50],
            )
        )
        shift -= 0.1
        self._repl_wids.append(
            DirectLabel(  # Energy
                parent=self._fr,
                frameColor=(0, 0, 0, 0.3),
                text_fg=SILVER_COL,
                text=base.labels.CHARACTERS[3],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                text_scale=0.03,
                pos=(-0.2, 0, shift),
            )
        )
        self._repl_wids.append(
            DirectButton(
                parent=self._fr,
                pos=(-0.05, 0, shift + 0.02),
                text_fg=SILVER_COL,
                text="+10\n5$",
                scale=(0.075, 0, 0.075),
                relief=None,
                text_scale=0.45,
                command=self._rest,
                extraArgs=[10],
            )
        )
        self._repl_wids.append(
            DirectButton(
                parent=self._fr,
                pos=(0.07, 0, shift + 0.02),
                text_fg=SILVER_COL,
                text="+50\n25$",
                scale=(0.075, 0, 0.075),
                relief=None,
                text_scale=0.45,
                command=self._rest,
                extraArgs=[50],
            )
        )
        shift -= 0.08
        self._repl_wids.append(
            DirectButton(  # Leave unit
                parent=self._fr,
                pos=(0.2, 0, shift),
                text_fg=SILVER_COL,
                text=base.labels.CITY[12],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                scale=(0.075, 0, 0.075),
                relief=None,
                text_scale=0.45,
                command=self._send_away,
            )
        )
        shift -= 0.08
        # recruits gui
        self._repl_wids.append(
            DirectLabel(  # Recruits
                parent=self._fr,
                text=base.labels.CITY[10],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                text_align=TextNode.ALeft,
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.035,
                text_fg=RUST_COL,
                pos=(-0.3, 0, shift),
            )
        )

        shift -= 0.13
        hire_but = DirectButton(  # Hire unit
            parent=self._fr,
            pos=(0.2, 0, shift),
            text_fg=SILVER_COL,
            text=base.labels.CITY[13],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=0.45,
            command=self._hire,
        )
        self._repl_wids.append(hire_but)

        self._recruit_chooser = RecruitChooser(hire_but)
        self._recruit_chooser.prepare(self._fr, (0, 0, 0.05), self._recruits)
        self._repl_wids.append(self._recruit_chooser)

        shift -= 0.08
        # resources
        self._repl_wids.append(
            DirectLabel(  # Resources
                parent=self._fr,
                text=base.labels.CITY[11],  # noqa: F821
                text_font=base.main_font,  # noqa: F821
                text_align=TextNode.ALeft,
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=0.035,
                text_fg=RUST_COL,
                pos=(-0.3, 0, shift),
            )
        )
        shift -= 0.12
        buy_res_but = DirectButton(  # Buy
            parent=self._fr,
            pos=(0.08, 0, shift),
            text_fg=SILVER_COL,
            text=base.labels.CITY[15],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=0.45,
            command=self._buy_supply,
        )
        self._repl_wids.append(buy_res_but)

        sell_res_but = DirectButton(  # Sell
            parent=self._fr,
            pos=(-0.08, 0, shift),
            text_fg=SILVER_COL,
            text=base.labels.CITY[14],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=0.45,
            command=self._sell_supply,
        )
        self._repl_wids.append(sell_res_but)

        self._res_chooser = ResourceChooser(buy_res_but, sell_res_but)
        self._res_chooser.prepare(
            self._fr,
            (0, 0, -0.165),
            {
                "Medicine box": "medicine_boxes",
                "Stimulator": "stimulators",
                "Smoke filter": "smoke_filters",
            },
        )
        self._repl_wids.append(self._res_chooser)

    def _buy_supply(self):
        """Buy the chosen resource."""
        if not base.res_gui.check_enough_money(  # noqa: F821
            self._res_chooser.chosen_resource_cost
        ):
            return

        random.choice((self._coins_s_snd, self._coins_l_snd)).play()

        base.dollars -= self._res_chooser.chosen_resource_cost  # noqa: F821
        base.plus_resource(self._res_chooser.chosen_item, 1)  # noqa: F821

    def _sell_supply(self):
        """Sell the chosen resource."""
        if not base.resource(self._res_chooser.chosen_item):  # noqa: F821
            return

        random.choice((self._coins_s_snd, self._coins_l_snd)).play()

        base.dollars += self._res_chooser.chosen_resource_cost  # noqa: F821
        base.plus_resource(self._res_chooser.chosen_item, -1)  # noqa: F821

    def _exit_city(self, turn_around=False):
        """Exit the current city.

        Hide city GUI, remove the hangar scene,
        return the Train back on railway.

        Args:
            turn_around (bool): True, if the Train should be turned around.
        """
        self._toot_snd.play()
        self._visit_num += 1
        taskMgr.remove("increase_city_snd")  # noqa: F821
        base.train.clear_upgrade_preview()  # noqa: F821

        taskMgr.doMethodLater(0.3, self._dec_amb_snd, "decrease_city_snd")  # noqa: F821
        taskMgr.doMethodLater(  # noqa: F821
            0.1, base.effects_mgr.fade_out_screen, "fade_out_screen"  # noqa: F821
        )
        taskMgr.doMethodLater(  # noqa: F821
            3.1, self._clear, "clear_city_gui", extraArgs=[turn_around]
        )
        taskMgr.doMethodLater(  # noqa: F821
            2, base.train.resume_smoke, "resume_train_smoke"  # noqa: F821
        )

    def _clear(self, turn_around):
        """Remove hangar scene and hide city GUI.

        Args:
            turn_around (bool): True, if the Train should be turned around.
        """
        self._fr.hide()
        base.char_gui.clear_char_info()  # noqa: F821
        base.world.unload_hangar_scene(turn_around)  # noqa: F821

    def _send_away(self):
        """Send the chosen unit away."""
        if len(base.team.chars) == 1:  # noqa: F821
            return

        self.write_snd.play()
        char = self._char_chooser.chosen_item
        char.leave()
        taskMgr.doMethodLater(  # noqa: F821
            0.1, self._char_chooser.leave_unit, char.id + "_leave", extraArgs=[char.id]
        )

    def _hire(self):
        """Hire the chosen unit."""
        cost = self._recruit_chooser.chosen_recruit_cost
        if not base.res_gui.check_enough_money(cost):  # noqa: F821
            return

        char = self._recruit_chooser.chosen_item
        if char is None:
            return

        if not base.res_gui.check_has_cell():  # noqa: F821
            return

        self.write_snd.play()
        base.dollars -= cost  # noqa: F821

        base.team.chars[char.id] = char  # noqa: F821
        self._recruit_chooser.leave_unit(char.id)

        char.prepare()
        base.train.place_recruit(char)  # noqa: F821
        base.res_gui.update_chars()  # noqa: F821
        if not char.current_part.name == "part_rest":
            char.rest()

    def _repair(self, value):
        """Repair the Train.

        Spends money.

        Args:
            value (int):
                Points of the Train durability to repair.
        """
        spent = 15 if value == 50 else 60
        if not base.res_gui.check_enough_money(spent):  # noqa: F821
            return

        random.choice((self._coins_s_snd, self._coins_l_snd)).play()

        base.train.get_damage(-value)  # noqa: F821
        base.dollars -= spent  # noqa: F821

    def _heal(self, value):
        """Heal the chosen character.

        Spends money.

        Args:
            value (int): Points to heal.
        """
        if not base.res_gui.check_enough_money(value):  # noqa: F821
            return

        random.choice((self._coins_s_snd, self._coins_l_snd)).play()

        self._char_chooser.chosen_item.health += value
        base.dollars -= value  # noqa: F821

    def _rest(self, value):
        """Regain energy of the chosen character.

        Spends money.

        Args:
            value (int): Points to regain.
        """
        spent = 5 if value == 10 else 25
        if not base.res_gui.check_enough_money(spent):  # noqa: F821
            return

        random.choice((self._coins_s_snd, self._coins_l_snd)).play()

        self._char_chooser.chosen_item.energy += value
        base.dollars -= spent  # noqa: F821

    def _inc_amb_snd(self, task):
        """Increase hangar ambient sound."""
        cur_vol = round(self._amb_snd.getVolume(), 2)
        if cur_vol == 1:
            return task.done

        self._amb_snd.setVolume(cur_vol + 0.05)
        return task.again

    def _dec_amb_snd(self, task):
        """Decrease hangar ambient sound."""
        cur_vol = round(self._amb_snd.getVolume(), 2)
        if cur_vol == 0:
            self._amb_snd.stop()
            return task.done

        self._amb_snd.setVolume(cur_vol - 0.05)
        return task.again

    def _show_headhunting_reward(self):
        """Show a reward interface.

        When getting into a city, player gains money as a reward
        for destroying enemies. Money amount depends on what
        enemies were destroyed.
        """
        heads_cost = {
            "MotoShooter": 5,
            "BrakeThrower": 5,
            "StunBombThrower": 10,
            "DodgeShooter": 25,
        }
        if not base.heads:  # noqa: F821
            return

        self._reward_fr = DirectFrame(
            frameSize=(-0.3, 0.3, -0.45, 0.45),
            frameTexture="gui/tex/paper1.png",
            state=DGG.NORMAL,
            pos=(0.9, 0, -0.15),
        )
        self._reward_fr.setDepthTest(False)
        self._reward_fr.setTransparency(TransparencyAttrib.MAlpha)

        heads_list = ""
        costs_list = ""
        total = 0
        for head, num in base.heads.items():  # noqa: F821
            heads_list += head + " x" + str(num) + "\n"
            costs_list += str(num * heads_cost[head]) + "$\n"
            total += num * heads_cost[head]

        DirectLabel(
            parent=self._reward_fr,
            frameColor=(0, 0, 0, 0),
            frameSize=(-0.3, 0.3, -0.1, 0.1),
            text="""The city government awards
you with money for
your help in clearing
the region of skinheads.

Heads you've taken:
"""
            + "\n" * 15
            + "Total reward:\n"
            + str(total)
            + "$",
            text_scale=0.03,
            pos=(0, 0, 0.35),
        )
        DirectLabel(
            parent=self._reward_fr,
            frameColor=(0, 0, 0, 0),
            frameSize=(-0.3, 0.3, -0.1, 0.1),
            text=heads_list,
            text_scale=0.03,
            text_align=TextNode.ALeft,
            pos=(-0.21, 0, 0.08),
        )
        DirectLabel(
            parent=self._reward_fr,
            frameColor=(0, 0, 0, 0),
            frameSize=(-0.3, 0.3, -0.1, 0.1),
            text=costs_list,
            text_scale=0.03,
            text_align=TextNode.ALeft,
            pos=(0.16, 0, 0.08),
        )
        DirectButton(
            parent=self._reward_fr,
            pos=(0, 0, -0.38),
            text="Acquire",
            text_fg=RUST_COL,
            text_shadow=(0, 0, 0, 1),
            frameColor=(0, 0, 0, 0),
            command=self._acquire_reward,
            extraArgs=[total],
            scale=(0.04, 0, 0.04),
        )

    def _acquire_reward(self, dollars):
        """Claim a reward, given by a city for destroying enemies.

        Args:
            dollars (int): Gained dollars amount.
        """
        self._coins_l_snd.play()
        base.dollars += dollars  # noqa: F821

        self._reward_fr.destroy()
        self._reward_fr = None
        base.clear_heads()  # noqa: F821

    def show(self):
        """Show city GUI."""
        self._amb_snd.play()
        taskMgr.doMethodLater(0.3, self._inc_amb_snd, "increase_city_snd")  # noqa: F821
        self._recruits = base.team.gen_recruits()  # noqa: F821
        self._fr.show()
        self._show_train(0.56)

        self._show_headhunting_reward()
