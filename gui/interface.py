"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Game graphical interface API.
"""
from direct.gui.DirectGui import DirectButton, DirectFrame, DirectLabel, DirectWaitBar
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TransparencyAttrib

RUST_COL = (0.71, 0.25, 0.05, 1)
SILVER_COL = (0.51, 0.54, 0.59, 1)
ICON_PATH = "gui/tex/"


class CharacterInterface:
    """Widget with character info."""

    def __init__(self):
        self._char = None  # chosen character
        self._rest_buttons = {}
        self._rest_list_active = False

        char_int_fr = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.3, 0.3, -0.1, 0.1),
            pos=(0.3, 0, -1.9),
            frameTexture=ICON_PATH + "metal1.png",
        )
        char_int_fr.setTransparency(TransparencyAttrib.MAlpha)

        DirectLabel(
            parent=char_int_fr,
            text="Name:",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.23, 0, 0.04),
        )
        self._char_name = DirectLabel(
            parent=char_int_fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=SILVER_COL,
            pos=(-0.11, 0, 0.038),
        )
        DirectLabel(
            parent=char_int_fr,
            text="Type:",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(0.03, 0, 0.04),
        )
        self._char_class = DirectLabel(
            parent=char_int_fr,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=SILVER_COL,
            pos=(0.15, 0, 0.038),
        )
        DirectLabel(
            parent=char_int_fr,
            text="Health",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.23, 0, -0.015),
        )
        self._char_health = DirectWaitBar(
            parent=char_int_fr,
            frameSize=(-0.17, 0.17, -0.002, 0.002),
            value=0,
            barColor=(0.85, 0.2, 0.28, 1),
            pos=(0.06, 0, -0.008),
        )
        DirectLabel(
            parent=char_int_fr,
            text="Energy",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.03, 0.03),
            text_fg=RUST_COL,
            pos=(-0.226, 0, -0.06),
        )
        self._char_energy = DirectWaitBar(
            parent=char_int_fr,
            frameSize=(-0.17, 0.17, -0.002, 0.002),
            value=0,
            barColor=(0.46, 0.61, 0.53, 1),
            pos=(0.06, 0, -0.053),
        )
        self._tip = OnscreenText(
            parent=base.render2d,  # noqa: F821
            text="",
            scale=(0.021, 0.027),
            fg=SILVER_COL,
            bg=(0, 0, 0, 0.4),
        )
        self._tip.hide()

        self.clear_char_info()

    def show_char_info(self, character):
        """Show the given character parameters.

        Args:
            character (personage.character.Character):
                Chosen character object.
        """
        self._char_name["text"] = character.name
        self._char_class["text"] = character.class_.capitalize()

        self._char_health["range"] = character.class_data["health"]
        self._char_health["value"] = character.health
        self._char_energy["value"] = character.energy

        self._char_name.show()
        self._char_class.show()
        self._char_health.show()
        self._char_energy.show()

        self._char = character
        base.taskMgr.doMethodLater(  # noqa: F821
            0.5, self._update_char_info, "track_char_info"
        )

    def clear_char_info(self):
        """Clear the character interface."""
        self._char_name.hide()
        self._char_class.hide()
        self._char_health.hide()
        self._char_energy.hide()

        base.taskMgr.remove("track_char_info")  # noqa: F821
        self._char = None

        for but in self._rest_buttons.values():
            but.destroy()

        self._rest_list_active = False

    def show_tooltip(self, text):
        """Show tooltip with the given text.

        Args:
            unit (str): Text to show in the tooltip.
        """
        self._tip.setText(text)
        self._tip.setX(base.mouseWatcherNode.getMouseX())  # noqa: F821
        self._tip.setY(base.mouseWatcherNode.getMouseY())  # noqa: F821
        self._tip.show()

    def hide_unit_tip(self):
        """Hide unit tooltip."""
        self._tip.hide()

    def show_resting_chars(self, part):
        """Show a list of the characters resting in this part.

        Args:
            part (Train.RestPart): Rest part of Train.
        """
        if self._rest_list_active:
            return

        self._tip.hide()
        self._rest_list_active = True

        x = base.mouseWatcherNode.getMouseX()  # noqa: F821
        z = base.mouseWatcherNode.getMouseY()  # noqa: F821

        self._rest_buttons["title"] = DirectButton(
            pos=(x, 0, z),
            text="Resting:",
            text_fg=RUST_COL,
            frameColor=(0, 0, 0, 0.6),
            scale=(0.04, 0, 0.03),
        )
        shift = -0.039
        for char in part.chars:
            self._rest_buttons[char.id] = DirectButton(
                pos=(x, 0, z + shift),
                text=char.name,
                text_fg=SILVER_COL,
                frameColor=(0, 0, 0, 0.6),
                command=base.common_ctrl.choose_resting_char,  # noqa: F821
                extraArgs=[char.id],
                scale=(0.04, 0, 0.03),
            )
            shift -= 0.033

    def destroy_char_button(self, char_id):
        """Hide the button related to the given character id.

        Args:
            char_id (str): Character id.
        """
        if char_id in self._rest_buttons.keys():
            self._rest_buttons[char_id].destroy()
            self._rest_buttons.pop(char_id)

    def _update_char_info(self, task):
        """Track character parameters on the interface."""
        if self._char.is_dead:
            self.clear_char_info()
            return task.done

        self._char_health["value"] = self._char.health
        self._char_energy["value"] = self._char.energy
        return task.again


class TrainInterface:
    """Train parameters interface."""

    def __init__(self):
        frame = DirectFrame(
            parent=base.a2dBottomRight,  # noqa: F821
            frameSize=(-0.03, 0.03, -0.3, 0.3),
            pos=(-0.03, 0, 0.3),
            frameTexture=ICON_PATH + "metal1.png",
        )
        frame.setTransparency(TransparencyAttrib.MAlpha)
        DirectFrame(
            parent=frame,  # noqa: F821
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            pos=(0, 0, 0.265),
            frameTexture=ICON_PATH + "icon_train.png",
        )
        self._damnability = DirectWaitBar(
            parent=frame,
            frameSize=(-0.25, 0.25, -0.002, 0.002),
            range=1000,
            value=1000,
            barColor=(0.42, 0.42, 0.8, 1),
            pos=(0, 0, -0.023),
        )
        self._damnability.setR(-90)

        frame_miles = DirectFrame(
            frameSize=(-0.1, 0.1, -0.03, 0.03),
            pos=(0.0, 0, -0.97),
            frameTexture=ICON_PATH + "metal1.png",
        )
        self._miles_meter = DirectLabel(
            parent=frame_miles,
            text="0000000",
            frameSize=(0.1, 0.1, 0.15, 0.15),
            text_scale=(0.035, 0.04),
            text_fg=RUST_COL,
            pos=(0, 0, -0.01),
        )

    def update_miles(self, new_miles):
        """Update miles meter widget.

        Args:
            new_miles (int): New milesmeter value.
        """
        self._miles_meter["text"] = str(new_miles).rjust(7, "0")

    def update_indicators(self, **params):
        """Update Train interface with the given parameters.

        Args:
            params (dict): New parameters values.
        """
        if "damnability" in params.keys():
            self._damnability["value"] = params["damnability"]


class ResourcesInterface:
    """Interface to show the current amount of player resources."""

    def __init__(self):
        self._coh_desc_wids = []
        self._coh_desc_shown = False

        frame = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.075, 0.075, -0.025, 0.025),
            pos=(0.075, 0, -0.025),
            frameTexture=ICON_PATH + "metal1.png",
        )
        frame.setTransparency(TransparencyAttrib.MAlpha)
        DirectFrame(
            parent=frame,  # noqa: F821
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            pos=(-0.05, 0, 0),
            frameTexture=ICON_PATH + "icon_dollar.png",
        )
        self._dollars = DirectLabel(
            parent=frame,
            text="300",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=(0.035, 0.035),
            text_fg=RUST_COL,
            pos=(0.01, 0, -0.008),
        )
        self._coh_frame = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.55, 0.55, -0.05, 0.05),
            pos=(2.95, 0, -0.05),
            frameTexture=ICON_PATH + "metal1.png",
        )
        self._coh_frame.setTransparency(TransparencyAttrib.MAlpha)
        self._cohesion = DirectWaitBar(
            parent=self._coh_frame,
            frameSize=(-0.45, 0.45, -0.002, 0.002),
            value=0,
            barColor=SILVER_COL,
            pos=(0, 0, 0.02),
        )
        recall_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            frameTexture=ICON_PATH + "ny_recall_icon.png",
            pos=(-0.27, 0, -0.02),
            relief="flat",
            command=base.team.cohesion_recall,  # noqa: F821
        )
        recall_ico.setTransparency(TransparencyAttrib.MAlpha)

        cover_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.035, 0.035, -0.035, 0.035),
            frameTexture=ICON_PATH + "ny_cover_icon.png",
            pos=(-0.09, 0, -0.01),
            relief="flat",
            command=base.team.cohesion_cover_fire,  # noqa: F821
        )
        cover_ico.setTransparency(TransparencyAttrib.MAlpha)

        heal_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.023, 0.023, -0.023, 0.023),
            frameTexture=ICON_PATH + "ny_heal_icon.png",
            pos=(0.09, 0, -0.015),
            relief="flat",
            command=base.team.cohesion_heal_wounded,  # noqa: F821
        )
        heal_ico.setTransparency(TransparencyAttrib.MAlpha)

        rage_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.035, 0.035, -0.035, 0.035),
            frameTexture=ICON_PATH + "ny_rage_icon.png",
            pos=(0.27, 0, -0.015),
            relief="flat",
            command=base.team.cohesion_rage,  # noqa: F821
        )
        rage_ico.setTransparency(TransparencyAttrib.MAlpha)

        heart_ico = DirectButton(
            parent=self._coh_frame,
            frameSize=(-0.035, 0.035, -0.035, 0.035),
            frameTexture=ICON_PATH + "ny_heart_icon.png",
            pos=(0.445, 0, -0.015),
            relief="flat",
            command=base.team.cohesion_hold_together,  # noqa: F821
        )
        heart_ico.setTransparency(TransparencyAttrib.MAlpha)

        self._coh_icons = (
            {"wid": recall_ico, "file": "recall_icon.png", "value": 20},
            {"wid": cover_ico, "file": "cover_icon.png", "value": 40},
            {"wid": heal_ico, "file": "heal_icon.png", "value": 60},
            {"wid": rage_ico, "file": "rage_icon.png", "value": 80},
            {"wid": heart_ico, "file": "heart_icon.png", "value": 100},
        )
        DirectButton(
            parent=self._coh_frame,
            text="?",
            frameSize=(-0.02, 0.02, -0.02, 0.02),
            frameColor=(0, 0, 0, 0),
            text_bg=(0, 0, 0, 0),
            text_fg=SILVER_COL,
            text_scale=0.03,
            pos=(-0.5, 0, -0.028),
            relief="flat",
            command=self._show_cohesion_abilities,
        ).setTransparency(TransparencyAttrib.MAlpha)

    def _show_cohesion_abilities(self):
        """Show/hide cohesion abilities description."""
        if self._coh_desc_shown:
            self._coh_frame["frameSize"] = (-0.55, 0.55, -0.05, 0.05)

            for wid in self._coh_desc_wids:
                wid.destroy()

            self._coh_desc_wids.clear()
            self._coh_desc_shown = False
            return

        self._coh_desc_shown = True
        self._coh_frame["frameSize"] = (-0.55, 0.55, -0.6, 0.05)
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.035, 0.035, -0.035, 0.035),
                frameTexture=ICON_PATH + "recall_icon.png",
                pos=(-0.45, 0, -0.11),
                relief="flat",
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Recall the past",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.03, 0.03),
                text_fg=SILVER_COL,
                pos=(-0.29, 0, -0.097),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Every character gets +15 energy. Cooldown: 15 min.",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.029, 0.029),
                text_fg=SILVER_COL,
                pos=(-0.055, 0, -0.135),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.045, 0.045, -0.045, 0.045),
                frameTexture=ICON_PATH + "cover_icon.png",
                pos=(-0.45, 0, -0.2),
                relief="flat",
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Cover fire",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.03, 0.03),
                text_fg=SILVER_COL,
                pos=(-0.325, 0, -0.197),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Every character gets +20 accuracy. Cooldown: 10 min.",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.029, 0.029),
                text_fg=SILVER_COL,
                pos=(-0.038, 0, -0.235),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.035, 0.035, -0.035, 0.035),
                frameTexture=ICON_PATH + "heal_icon.png",
                pos=(-0.45, 0, -0.31),
                relief="flat",
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Not leaving ours",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.03, 0.03),
                text_fg=SILVER_COL,
                pos=(-0.283, 0, -0.297),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text=(
                    "Characters with health < 30 "
                    "getting +20 health. Cooldown: 15 min."
                ),
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.029, 0.029),
                text_fg=SILVER_COL,
                pos=(0.03, 0, -0.335),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.045, 0.045, -0.045, 0.045),
                frameTexture=ICON_PATH + "rage_icon.png",
                pos=(-0.45, 0, -0.41),
                relief="flat",
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Common rage",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.03, 0.03),
                text_fg=SILVER_COL,
                pos=(-0.298, 0, -0.397),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Every character gets +30% to damage. Cooldown: 15 min.",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.029, 0.029),
                text_fg=SILVER_COL,
                pos=(-0.023, 0, -0.435),
            )
        )
        self._coh_desc_wids.append(
            DirectButton(
                parent=self._coh_frame,
                frameSize=(-0.043, 0.043, -0.043, 0.043),
                frameTexture=ICON_PATH + "heart_icon.png",
                pos=(-0.45, 0, -0.51),
                relief="flat",
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="Hold together",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.03, 0.03),
                text_fg=SILVER_COL,
                pos=(-0.298, 0, -0.497),
            )
        )
        self._coh_desc_wids.append(
            DirectLabel(
                parent=self._coh_frame,
                text="No characters will die in next 1.5 min. Cooldown: 20 min.",
                frameSize=(0.1, 0.1, 0.1, 0.1),
                text_scale=(0.029, 0.029),
                text_fg=SILVER_COL,
                pos=(-0.029, 0, -0.535),
            )
        )

    def update_money(self, new_value):
        """Update money indicator with the given value.

        Args:
            new_value (int): New amount of money.
        """
        self._dollars["text"] = str(new_value)

    def update_cohesion(self, new_value):
        """Update cohesion indicator with the given value.

        Args:
            new_value (int): New amount of the cohesion points.
        """
        self._cohesion["value"] = new_value

        if base.team.cohesion_cooldown:  # noqa: F821
            return

        for icon in self._coh_icons:
            if new_value >= icon["value"]:
                icon["wid"]["frameTexture"] = ICON_PATH + icon["file"]
            else:
                icon["wid"]["frameTexture"] = ICON_PATH + "ny_" + icon["file"]

    def disable_cohesion(self):
        """Disable all the cohesion abilities."""
        for icon in self._coh_icons:
            icon["wid"]["frameTexture"] = ICON_PATH + "ny_" + icon["file"]
