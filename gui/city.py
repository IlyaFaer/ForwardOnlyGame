"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Cities GUI.
"""
import random

from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel
from panda3d.core import TransparencyAttrib

from .character import CharacterChooser
from .train import ICON_PATH, RUST_COL, SILVER_COL


class CityInterface:
    """City GUI interface.

    Includes healing and regaining energy for the player
    units. Every service requires some money to be spent.
    """

    def __init__(self):
        self._amb_snd = loader.loadSfx("sounds/hangar_ambient.ogg")  # noqa: F821
        self._amb_snd.setVolume(0)
        self._amb_snd.setLoop(True)

        self._coins_s_snd = loader.loadSfx("sounds/coins_short.ogg")  # noqa: F821
        self._coins_l_snd = loader.loadSfx("sounds/coins_long.ogg")  # noqa: F821
        self._write_snd = loader.loadSfx("sounds/write.ogg")  # noqa: F821
        self._toot_snd = loader.loadSfx("sounds/toot1.ogg")  # noqa: F821

        self._city_fr = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.35, 0.35, -0.7, 0.7),
            pos=(0.75, 0, -1),
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
        # team gui
        DirectLabel(
            parent=self._city_fr,
            text="Team",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.035, 0.035),
            text_fg=RUST_COL,
            pos=(-0.27, 0, 0.57),
        )

        self._char_chooser = CharacterChooser()

        DirectLabel(
            parent=self._city_fr,
            frameColor=(0, 0, 0, 0.3),
            text_fg=SILVER_COL,
            text="Health",
            text_scale=(0.03, 0.03),
            pos=(-0.2, 0, 0.43),
        )
        DirectButton(
            parent=self._city_fr,
            pos=(-0.05, 0, 0.45),
            text_fg=SILVER_COL,
            text="+10\n10$",
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=(0.45, 0.45),
            command=self._heal,
            extraArgs=[10],
        )
        DirectButton(
            parent=self._city_fr,
            pos=(0.07, 0, 0.45),
            text_fg=SILVER_COL,
            text="+50\n50$",
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=(0.45, 0.45),
            command=self._heal,
            extraArgs=[50],
        )
        DirectLabel(
            parent=self._city_fr,
            frameColor=(0, 0, 0, 0.3),
            text_fg=SILVER_COL,
            text="Energy",
            text_scale=(0.03, 0.03),
            pos=(-0.2, 0, 0.33),
        )
        DirectButton(
            parent=self._city_fr,
            pos=(-0.05, 0, 0.35),
            text_fg=SILVER_COL,
            text="+10\n5$",
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=(0.45, 0.45),
            command=self._rest,
            extraArgs=[10],
        )
        DirectButton(
            parent=self._city_fr,
            pos=(0.07, 0, 0.35),
            text_fg=SILVER_COL,
            text="+50\n25$",
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=(0.45, 0.45),
            command=self._rest,
            extraArgs=[50],
        )
        DirectButton(
            parent=self._city_fr,
            pos=(0.2, 0, 0.25),
            text_fg=SILVER_COL,
            text="Leave unit",
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=(0.45, 0.45),
            command=self._send_away,
        )
        # recruits gui
        DirectLabel(
            parent=self._city_fr,
            text="Recruits",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.035, 0.035),
            text_fg=RUST_COL,
            pos=(-0.25, 0, 0.17),
        )

        self._recruit_chooser = CharacterChooser()

        DirectButton(
            parent=self._city_fr,
            pos=(0.2, 0, 0.04),
            text_fg=SILVER_COL,
            text="Hire unit\n200$",
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=(0.45, 0.45),
            command=self._hire,
        )
        # Train GUI
        DirectLabel(
            parent=self._city_fr,
            text="Train",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.035, 0.035),
            text_fg=RUST_COL,
            pos=(-0.25, 0, -0.07),
        )
        DirectLabel(
            parent=self._city_fr,
            frameColor=(0, 0, 0, 0.3),
            text_fg=SILVER_COL,
            text="Repair",
            text_scale=(0.03, 0.03),
            pos=(-0.2, 0, -0.15),
        )
        DirectButton(
            parent=self._city_fr,
            pos=(-0.05, 0, -0.15),
            text_fg=SILVER_COL,
            text="+50\n25$",
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=(0.45, 0.45),
            command=self._repair,
            extraArgs=[50],
        )
        DirectButton(
            parent=self._city_fr,
            pos=(0.07, 0, -0.15),
            text_fg=SILVER_COL,
            text="+200\n100$",
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=(0.45, 0.45),
            command=self._repair,
            extraArgs=[200],
        )
        DirectButton(
            parent=self._city_fr,
            pos=(-0.2, 0, -0.63),
            text_fg=RUST_COL,
            text="Back on road",
            scale=(0.075, 0, 0.075),
            relief=None,
            text_scale=(0.5, 0.5),
            command=self._exit_city,
        )

    def _exit_city(self):
        """Exit the current city.

        Hide city GUI, remove the hangar scene,
        return Train back to railway.
        """
        self._toot_snd.play()
        base.taskMgr.remove("increase_city_snd")  # noqa: F821
        base.taskMgr.doMethodLater(  # noqa: F821
            0.3, self._dec_amb_snd, "decrease_city_snd"
        )
        base.taskMgr.doMethodLater(  # noqa: F821
            0.1, base.effects_mgr.fade_out_screen, "fade_out_screen"  # noqa: F821
        )
        base.taskMgr.doMethodLater(3.1, self._clear, "clear_city_gui")  # noqa: F821

    def _clear(self, task):
        """Remove hangar scene and hide city GUI."""
        self._city_fr.hide()
        base.world.unload_hangar_scene()  # noqa: F821
        return task.done

    def _send_away(self):
        """Send the chosen unit away."""
        if len(base.team.chars) == 1:  # noqa: F821
            return

        self._write_snd.play()
        char = self._char_chooser.chosen_char
        char.leave()
        base.taskMgr.doMethodLater(  # noqa: F821
            0.1, self._char_chooser.leave_unit, char.id + "_leave", extraArgs=[char.id]
        )

    def _hire(self):
        """Hire the chosen unit."""
        if base.dollars - 200 < 0:  # noqa: F821
            return

        char = self._recruit_chooser.chosen_char
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

        self._char_chooser.chosen_char.health += value
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

        self._char_chooser.chosen_char.energy += value
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
        base.taskMgr.doMethodLater(  # noqa: F821
            0.3, self._inc_amb_snd, "increase_city_snd"
        )
        self._char_chooser.prepare(
            self._city_fr, (0, 0, 0.52), base.team.chars  # noqa: F821
        )
        self._recruit_chooser.prepare(
            self._city_fr, (0, 0, 0.12), base.team.gen_recruits()  # noqa: F821
        )
        self._city_fr.show()
