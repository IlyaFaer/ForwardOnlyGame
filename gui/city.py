"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Cities GUI.
"""
import random

from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel
from panda3d.core import TransparencyAttrib

from .widgets import ICON_PATH, RUST_COL, SILVER_COL, CharacterChooser, UpgradeChooser


class CityInterface:
    """City GUI.

    Includes healing and regaining energy for the player
    units. Every service requires some money to be spent.
    """

    def __init__(self):
        self._repl_wids = []
        self._recruits = []

        self._amb_snd = loader.loadSfx("sounds/hangar_ambient.ogg")  # noqa: F821
        self._amb_snd.setVolume(0)
        self._amb_snd.setLoop(True)

        self._coins_s_snd = loader.loadSfx("sounds/coins_short.ogg")  # noqa: F821
        self._coins_l_snd = loader.loadSfx("sounds/coins_long.ogg")  # noqa: F821
        self._write_snd = loader.loadSfx("sounds/write.ogg")  # noqa: F821
        self._toot_snd = loader.loadSfx("sounds/toot1.ogg")  # noqa: F821

        self._city_fr = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.35, 0.35, -0.4, 0.7),
            pos=(0.85, 0, -0.82),
            frameTexture=ICON_PATH + "metal1.png",
        )
        self._city_fr.setTransparency(TransparencyAttrib.MAlpha)
        self._city_fr.hide()

        DirectLabel(
            parent=self._city_fr,
            text="Services",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.045, 0.045),
            text_fg=RUST_COL,
            pos=(0, 0, 0.62),
        )
        self._party_but = DirectButton(
            parent=self._city_fr,
            text_scale=0.035,
            text_fg=SILVER_COL,
            text="Party",
            relief=None,
            command=self._show_party,
            extraArgs=[0.56],
            pos=(-0.2, 0, 0.56),
            clickSound=base.main_menu.click_snd,  # noqa: F821
        )
        base.main_menu.bind_button(self._party_but)  # noqa: F821

        self._train_but = DirectButton(
            parent=self._city_fr,
            text_scale=0.035,
            text_fg=RUST_COL,
            text="Train",
            relief=None,
            command=self._show_train,
            extraArgs=[0.56],
            pos=(0, 0, 0.56),
            clickSound=base.main_menu.click_snd,  # noqa: F821
        )
        base.main_menu.bind_button(self._train_but)  # noqa: F821

        base.main_menu.bind_button(  # noqa: F821
            DirectButton(
                parent=self._city_fr,
                pos=(-0.205, 0, -0.33),
                text_fg=RUST_COL,
                text="Back on road",
                relief=None,
                text_scale=0.035,
                command=self._exit_city,
            )
        )

    def _show_train(self, shift):
        """Show the Train management GUI tab.

        Args:
            shift (float): Z-coordinate.
        """
        self._clear_repl_wids()

        self._party_but["text_fg"] = RUST_COL
        self._train_but["text_fg"] = SILVER_COL

        shift -= 0.07
        self._repl_wids.append(
            DirectLabel(
                parent=self._city_fr,
                text="Locomotive",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.035, 0.035),
                text_fg=RUST_COL,
                pos=(-0.22, 0, shift),
            )
        )
        shift -= 0.08
        self._repl_wids.append(
            DirectLabel(
                parent=self._city_fr,
                frameColor=(0, 0, 0, 0.3),
                text_fg=SILVER_COL,
                text="Repair",
                text_scale=(0.03, 0.03),
                pos=(-0.2, 0, shift),
            )
        )
        self._repl_wids.append(
            DirectButton(
                parent=self._city_fr,
                pos=(-0.05, 0, shift),
                text_fg=SILVER_COL,
                text="+50\n25$",
                scale=(0.075, 0, 0.075),
                relief=None,
                text_scale=(0.45, 0.45),
                command=self._repair,
                extraArgs=[50],
            )
        )
        self._repl_wids.append(
            DirectButton(
                parent=self._city_fr,
                pos=(0.07, 0, shift),
                text_fg=SILVER_COL,
                text="+200\n100$",
                scale=(0.075, 0, 0.075),
                relief=None,
                text_scale=(0.45, 0.45),
                command=self._repair,
                extraArgs=[200],
            )
        )

        shift -= 0.09
        self._repl_wids.append(
            DirectLabel(
                parent=self._city_fr,
                text="Upgrades",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.035, 0.035),
                text_fg=RUST_COL,
                pos=(-0.24, 0, shift),
            )
        )
        up_desc = DirectLabel(
            parent=self._city_fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.03,
            text_fg=SILVER_COL,
            pos=(-0.1, 0, shift - 0.14),
        )
        self._repl_wids.append(up_desc)

        up_cost = DirectLabel(
            parent=self._city_fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.035,
            text_fg=SILVER_COL,
            pos=(0.25, 0, shift - 0.18),
        )
        self._repl_wids.append(up_cost)

        but = DirectButton(
            parent=self._city_fr,
            pos=(0.2, 0, shift - 0.3),
            text_fg=RUST_COL,
            text="Purchase",
            relief=None,
            text_scale=0.035,
            clickSound=base.main_menu.click_snd,  # noqa: F821
            command=self._purchase_upgrade,
        )
        self._repl_wids.append(but)
        base.main_menu.bind_button(but)  # noqa: F821

        shift -= 0.05
        self._up_chooser = UpgradeChooser(up_desc, up_cost)
        self._up_chooser.prepare(
            self._city_fr, (0, 0, shift), base.train.possible_upgrades  # noqa: F821
        )
        self._repl_wids.append(self._up_chooser)

    def _purchase_upgrade(self):
        """Buy the chosen upgrade and install it on to the Train."""
        upgrade = self._up_chooser.chosen_item
        if upgrade is None or base.dollars < int(upgrade["cost"][:-1]):  # noqa: F821
            return

        base.dollars -= int(upgrade["cost"][:-1])  # noqa: F821

        base.train.install_upgrade(upgrade)  # noqa: F821
        self._up_chooser.pop_upgrade(upgrade["name"])

    def _show_party(self, shift):
        """Show units management tab.

        Args:
            shift (float): Z-coordinate.
        """
        self._clear_repl_wids()

        self._party_but["text_fg"] = SILVER_COL
        self._train_but["text_fg"] = RUST_COL

        shift -= 0.07
        # team gui
        self._repl_wids.append(
            DirectLabel(
                parent=self._city_fr,
                text="Team",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.035, 0.035),
                text_fg=RUST_COL,
                pos=(-0.27, 0, shift),
            )
        )

        self._char_chooser = CharacterChooser()
        self._char_chooser.prepare(
            self._city_fr, (0, 0, 0.45), base.team.chars  # noqa: F821
        )
        self._repl_wids.append(self._char_chooser)

        shift -= 0.14
        self._repl_wids.append(
            DirectLabel(
                parent=self._city_fr,
                frameColor=(0, 0, 0, 0.3),
                text_fg=SILVER_COL,
                text="Health",
                text_scale=(0.03, 0.03),
                pos=(-0.2, 0, shift),
            )
        )
        self._repl_wids.append(
            DirectButton(
                parent=self._city_fr,
                pos=(-0.05, 0, shift + 0.02),
                text_fg=SILVER_COL,
                text="+10\n10$",
                scale=(0.075, 0, 0.075),
                relief=None,
                text_scale=(0.45, 0.45),
                command=self._heal,
                extraArgs=[10],
            )
        )
        self._repl_wids.append(
            DirectButton(
                parent=self._city_fr,
                pos=(0.07, 0, shift + 0.02),
                text_fg=SILVER_COL,
                text="+50\n50$",
                scale=(0.075, 0, 0.075),
                relief=None,
                text_scale=(0.45, 0.45),
                command=self._heal,
                extraArgs=[50],
            )
        )
        shift -= 0.1
        self._repl_wids.append(
            DirectLabel(
                parent=self._city_fr,
                frameColor=(0, 0, 0, 0.3),
                text_fg=SILVER_COL,
                text="Energy",
                text_scale=(0.03, 0.03),
                pos=(-0.2, 0, shift),
            )
        )
        self._repl_wids.append(
            DirectButton(
                parent=self._city_fr,
                pos=(-0.05, 0, shift + 0.02),
                text_fg=SILVER_COL,
                text="+10\n5$",
                scale=(0.075, 0, 0.075),
                relief=None,
                text_scale=(0.45, 0.45),
                command=self._rest,
                extraArgs=[10],
            )
        )
        self._repl_wids.append(
            DirectButton(
                parent=self._city_fr,
                pos=(0.07, 0, shift + 0.02),
                text_fg=SILVER_COL,
                text="+50\n25$",
                scale=(0.075, 0, 0.075),
                relief=None,
                text_scale=(0.45, 0.45),
                command=self._rest,
                extraArgs=[50],
            )
        )
        shift -= 0.08
        self._repl_wids.append(
            DirectButton(
                parent=self._city_fr,
                pos=(0.2, 0, shift),
                text_fg=SILVER_COL,
                text="Leave unit",
                scale=(0.075, 0, 0.075),
                relief=None,
                text_scale=(0.45, 0.45),
                command=self._send_away,
            )
        )
        shift -= 0.08
        # recruits gui
        self._repl_wids.append(
            DirectLabel(
                parent=self._city_fr,
                text="Recruits",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.035, 0.035),
                text_fg=RUST_COL,
                pos=(-0.25, 0, shift),
            )
        )

        self._recruit_chooser = CharacterChooser()
        self._recruit_chooser.prepare(
            self._city_fr, (0, 0, 0.05), self._recruits  # noqa: F821
        )
        self._repl_wids.append(self._recruit_chooser)

        shift -= 0.13
        self._repl_wids.append(
            DirectButton(
                parent=self._city_fr,
                pos=(0.2, 0, shift),
                text_fg=SILVER_COL,
                text="Hire unit\n200$",
                scale=(0.075, 0, 0.075),
                relief=None,
                text_scale=(0.45, 0.45),
                command=self._hire,
            )
        )

    def _clear_repl_wids(self):
        """Clear widgets in the current tab."""
        for wid in self._repl_wids:
            wid.destroy()

        self._repl_wids = []

    def _exit_city(self):
        """Exit the current city.

        Hide city GUI, remove the hangar scene,
        return the Train back on railway.
        """
        self._toot_snd.play()
        taskMgr.remove("increase_city_snd")  # noqa: F821
        base.train.clear_upgrade_preview()  # noqa: F821

        taskMgr.doMethodLater(0.3, self._dec_amb_snd, "decrease_city_snd")  # noqa: F821
        taskMgr.doMethodLater(  # noqa: F821
            0.1, base.effects_mgr.fade_out_screen, "fade_out_screen"  # noqa: F821
        )
        taskMgr.doMethodLater(3.1, self._clear, "clear_city_gui")  # noqa: F821

    def _clear(self, task):
        """Remove hangar scene and hide city GUI."""
        self._city_fr.hide()
        base.char_gui.clear_char_info()  # noqa: F821
        base.world.unload_hangar_scene()  # noqa: F821
        return task.done

    def _send_away(self):
        """Send the chosen unit away."""
        if len(base.team.chars) == 1:  # noqa: F821
            return

        self._write_snd.play()
        char = self._char_chooser.chosen_item
        char.leave()
        taskMgr.doMethodLater(  # noqa: F821
            0.1, self._char_chooser.leave_unit, char.id + "_leave", extraArgs=[char.id]
        )

    def _hire(self):
        """Hire the chosen unit."""
        if base.dollars - 200 < 0:  # noqa: F821
            return

        char = self._recruit_chooser.chosen_item
        if char is None:
            return

        if not base.train.has_cell():  # noqa: F821
            return

        self._write_snd.play()
        base.dollars -= 200  # noqa: F821

        base.team.chars[char.id] = char  # noqa: F821
        self._recruit_chooser.leave_unit(char.id)

        char.prepare()
        base.train.place_recruit(char)  # noqa: F821
        if not char.current_part.name.startswith("part_rest_"):
            char.rest()

    def _repair(self, value):
        """Repair the Train.

        Spends money.

        Args:
            value (int):
                Points of the Train damnability to repair.
        """
        spent = 25 if value == 50 else 100
        if base.dollars - spent < 0:  # noqa: F821
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
        if base.dollars - value < 0:  # noqa: F821
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
        if base.dollars - spent < 0:  # noqa: F821
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

    def show(self):
        """Show city GUI."""
        self._amb_snd.play()
        taskMgr.doMethodLater(0.3, self._inc_amb_snd, "increase_city_snd")  # noqa: F821
        self._recruits = base.team.gen_recruits()  # noqa: F821
        self._city_fr.show()
        self._show_train(0.56)
