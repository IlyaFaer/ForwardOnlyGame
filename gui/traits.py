"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

List Of Distinguished - a GUI to control characters' traits.
"""
from direct.gui.DirectGui import (
    DGG,
    DirectButton,
    DirectFrame,
    DirectLabel,
)
from panda3d.core import TransparencyAttrib

from utils import take_random
from .widgets import GUI_PIC, RUST_COL, SILVER_COL, CharacterChooser


class TraitsGUI:
    """GUI to praise/scold characters.

    This GUI gives players an opportunity to
    control their characters' traits.
    """

    def __init__(self):
        self._cur_char = None
        self._ind_chosen = None
        self._new_chosen = False
        self._need_update = False
        self.is_shown = False

        self._cur_traits = []
        self._new_traits = []

        self._open_snd = loader.loadSfx("sounds/GUI/paper1.ogg")  # noqa: F821
        self._close_snd = loader.loadSfx("sounds/GUI/paper2.ogg")  # noqa: F821
        self._scold_snd = loader.loadSfx("sounds/GUI/scold.ogg")  # noqa: F821
        self._praise_snd = loader.loadSfx("sounds/GUI/praise.ogg")  # noqa: F821

        self._list = DirectFrame(
            frameSize=(-0.75, 0.75, -0.77, 0.77),
            frameTexture=GUI_PIC + "paper1.png",
            state=DGG.NORMAL,
        )
        self._list.setDepthTest(False)
        self._list.setTransparency(TransparencyAttrib.MAlpha)
        self._list.hide()

        DirectLabel(  # List of distinguished
            parent=self._list,
            text=base.labels.DISTINGUISHED[0],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            frameSize=(0.4, 0.4, 0.4, 0.4),
            text_scale=0.045,
            pos=(-0.35, 0, 0.65),
        )
        DirectLabel(  # the praise/scold mechanisms description
            parent=self._list,
            text=base.labels.DISTINGUISHED[1],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            frameSize=(0.3, 0.3, 0.3, 0.3),
            text_scale=0.035,
            text_bg=(0, 0, 0, 0),
            pos=(0, 0, 0.54),
        )
        self._char_chooser = CharacterChooser(is_shadowed=True)

        DirectLabel(  # Cohesion points:
            parent=self._list,
            text=base.labels.DISTINGUISHED[2],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.035,
            text_bg=(0, 0, 0, 0),
            pos=(0.3, 0, 0.065),
        )
        self._cohesion_pts = DirectLabel(
            parent=self._list,
            text="",
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.035,
            text_bg=(0, 0, 0, 0),
            pos=(0.47, 0, 0.065),
        )
        self._cur_traits_num = DirectLabel(  # Current traits
            parent=self._list,
            text="",
            text_font=base.main_font,  # noqa: F821
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.032,
            text_bg=(0, 0, 0, 0),
            pos=(0.3, 0, -0.08),
        )
        DirectLabel(  # New traits:
            parent=self._list,
            text=base.labels.DISTINGUISHED[3],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            frameSize=(0.1, 0.1, 0.1, 0.1),
            text_scale=0.032,
            text_bg=(0, 0, 0, 0),
            pos=(-0.35, 0, -0.08),
        )
        traits_fr = DirectFrame(
            parent=self._list,
            frameSize=(-0.65, 0.6, -0.18, 0.2),
            pos=(0, 0, -0.32),
            frameColor=(0, 0, 0, 0.3),
        )

        shift = 0.15
        for index in range(3):
            self._cur_traits.append(
                (
                    DirectButton(
                        pos=(0.3, 0, shift),
                        text="",
                        text_fg=SILVER_COL,
                        text_scale=0.032,
                        text_font=base.main_font,  # noqa: F821
                        parent=traits_fr,
                        frameSize=(-0.2, 0.2, -0.05, 0.05),
                        relief=None,
                        command=self._choose_trait,
                        extraArgs=[self._cur_traits, self._new_traits, index],
                    ),
                    DirectButton(
                        pos=(0.3, 0, shift - 0.045),
                        text="",
                        text_fg=SILVER_COL,
                        text_scale=0.027,
                        text_font=base.main_font,  # noqa: F821
                        parent=traits_fr,
                        frameSize=(-0.2, 0.2, -0.05, 0.05),
                        relief=None,
                        command=self._choose_trait,
                        extraArgs=[self._cur_traits, self._new_traits, index],
                    ),
                )
            )
            self._new_traits.append(
                (
                    DirectButton(
                        pos=(-0.35, 0, shift),
                        text="",
                        text_fg=SILVER_COL,
                        text_scale=0.032,
                        text_font=base.main_font,  # noqa: F821
                        parent=traits_fr,
                        frameSize=(-0.2, 0.2, -0.05, 0.05),
                        relief=None,
                        command=self._choose_trait,
                        extraArgs=[self._new_traits, self._cur_traits, index],
                    ),
                    DirectButton(
                        pos=(-0.35, 0, shift - 0.045),
                        text="",
                        text_fg=SILVER_COL,
                        text_scale=0.027,
                        text_font=base.main_font,  # noqa: F821
                        parent=traits_fr,
                        frameSize=(-0.2, 0.2, -0.05, 0.05),
                        relief=None,
                        command=self._choose_trait,
                        extraArgs=[self._new_traits, self._cur_traits, index],
                    ),
                )
            )
            shift -= 0.12

        self._add_but = DirectButton(
            pos=(0, 0, 0),
            text=">",
            text_fg=SILVER_COL,
            parent=traits_fr,
            frameColor=(0, 0, 0, 0),
            relief=None,
            scale=(0.06, 0, 0.07),
            clickSound=base.main_menu.click_snd,  # noqa: F821
        )
        self._praise_but = DirectButton(
            pos=(-0.35, 0, -0.57),
            text=base.labels.DISTINGUISHED[4],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            text_fg=RUST_COL,
            text_shadow=(0, 0, 0, 1),
            frameColor=(0, 0, 0, 0),
            parent=self._list,
            command=self._gen_new_traits,
            scale=(0.04, 0, 0.04),
            clickSound=base.main_menu.click_snd,  # noqa: F821
        )
        self._scold_but = DirectButton(
            pos=(0.3, 0, -0.57),
            text=base.labels.DISTINGUISHED[5],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            text_fg=SILVER_COL,
            text_shadow=(0, 0, 0, 1),
            frameColor=(0, 0, 0, 0),
            parent=self._list,
            scale=(0.04, 0, 0.04),
            clickSound=base.main_menu.click_snd,  # noqa: F821
        )
        DirectButton(
            pos=(-0.02, 0, -0.7),
            text=base.labels.DISTINGUISHED[6],  # noqa: F821
            text_font=base.main_font,  # noqa: F821
            text_fg=RUST_COL,
            text_shadow=(0, 0, 0, 1),
            frameColor=(0, 0, 0, 0),
            parent=self._list,
            scale=(0.04, 0, 0.04),
            clickSound=base.main_menu.click_snd,  # noqa: F821
            command=self.hide,
        )

    def _add_trait(self):
        """Add the chosen new trait to character's traits."""
        if not self._new_chosen or self._ind_chosen is None:
            return

        char = self._char_chooser.chosen_item
        if len(char.traits) == 3:
            return

        self._praise_snd.play()
        char.traits.append(self._new_traits[self._ind_chosen][0]["text"])

        for but_pair in self._new_traits:
            but_pair[0]["text"] = ""
            but_pair[1]["text"] = ""

        self._add_but["text_fg"] = SILVER_COL
        self._add_but["command"] = None

        self._need_update = True
        self._ind_chosen = None
        base.char_gui.move_status_label(-1)  # noqa: F821

    def _choose_trait(self, traits, clear_traits, ch_index):
        """Highlight the trait on which the player clicked.

        Args:
            traits (list): List of traits, one of which was chosen.
            clear_traits (list):
                List of traits, which highlight must be dropped.
            ch_index (int): Index of the chosen trait.
        """
        self._ind_chosen = ch_index
        self._new_chosen = traits == self._new_traits

        if self._new_chosen:
            self._add_but["text_fg"] = RUST_COL
            self._add_but["command"] = self._add_trait

            self._scold_but["text_fg"] = SILVER_COL
            self._scold_but["command"] = None
        else:
            self._scold_but["text_fg"] = RUST_COL
            self._scold_but["command"] = self._scold

            self._add_but["text_fg"] = SILVER_COL
            self._add_but["command"] = None

        for index in range(len(traits)):
            clear_traits[index][0]["text_fg"] = SILVER_COL
            clear_traits[index][1]["text_fg"] = SILVER_COL

            if index == ch_index:
                traits[index][0]["text_fg"] = RUST_COL
                traits[index][1]["text_fg"] = RUST_COL
            else:
                traits[index][0]["text_fg"] = SILVER_COL
                traits[index][1]["text_fg"] = SILVER_COL

    def _gen_new_traits(self):
        """Generate new traits on praise.

        One of these traits player can choose
        to add to the character's traits list.
        """
        if base.team.cohesion < 5:  # noqa: F821
            return

        char = self._char_chooser.chosen_item

        pos_traits = list(base.labels.TRAIT_DESC.keys())  # noqa: F821
        for trait in char.traits + char.disabled_traits:
            pos_traits.remove(trait)

        for index in range(3):
            new_trait = take_random(pos_traits)
            self._new_traits[index][0]["text"] = new_trait
            self._new_traits[index][0]["text_fg"] = SILVER_COL
            self._new_traits[index][1]["text"] = base.labels.TRAIT_DESC[  # noqa: F821
                new_trait
            ]
            self._new_traits[index][1]["text_fg"] = SILVER_COL

        base.team.spend_cohesion(4)  # noqa: F821

    def _scold(self):
        """Erase the chosen character's trait."""
        if self._new_chosen or base.team.cohesion < 4:  # noqa: F821
            return

        self._scold_snd.play()
        trait = self._cur_traits[self._ind_chosen][0]["text"]
        char = self._char_chooser.chosen_item
        if trait in char.traits:
            char.traits.remove(trait)
        if trait in char.disabled_traits:
            char.disabled_traits.remove(trait)

        self._ind_chosen = None
        self._need_update = True
        base.char_gui.move_status_label(1)  # noqa: F821

        self._scold_but["text_fg"] = SILVER_COL
        self._scold_but["command"] = None

        base.team.spend_cohesion(4)  # noqa: F821

    def _update_traits(self, task):
        """Update the list of the character's traits."""
        self._cohesion_pts["text"] = str(int(base.team.cohesion))  # noqa: F821

        if self._char_chooser.chosen_item == self._cur_char and not self._need_update:
            return task.again

        self._need_update = False
        self._cur_char = self._char_chooser.chosen_item

        self._scold_but["text_fg"] = SILVER_COL
        self._scold_but["command"] = None

        traits = self._cur_char.traits + self._cur_char.disabled_traits
        self._cur_traits_num["text"] = "{label} ({num}/3):".format(
            label=base.labels.DISTINGUISHED[7], num=str(len(traits))  # noqa: F821
        )

        if len(traits) == 3:
            self._praise_but["text_fg"] = SILVER_COL
            self._praise_but["command"] = None
        else:
            self._praise_but["text_fg"] = RUST_COL
            self._praise_but["command"] = self._gen_new_traits

        for index in range(3):
            if index + 1 <= len(traits):
                trait = traits[index]
                self._cur_traits[index][0]["text"] = trait
                self._cur_traits[index][0]["text_fg"] = SILVER_COL
                self._cur_traits[index][1][
                    "text"
                ] = base.labels.TRAIT_DESC[  # noqa: F821
                    trait
                ]
                self._cur_traits[index][1]["text_fg"] = SILVER_COL
            else:
                self._cur_traits[index][0]["text"] = ""
                self._cur_traits[index][0]["text_fg"] = SILVER_COL
                self._cur_traits[index][1]["text"] = ""
                self._cur_traits[index][1]["text_fg"] = SILVER_COL

        return task.again

    def hide(self):
        """Hide the GUI."""
        if self.is_shown:
            taskMgr.remove("update_traits_ctrl")  # noqa: F821
            base.char_gui.clear_char_info()  # noqa: F821
            self._list.hide()
            self.is_shown = False
            taskMgr.doMethodLater(  # noqa: F821
                0.07, self._close_snd.play, "play_close_snd", extraArgs=[]
            )

    def show(self):
        """Show the GUI."""
        if (
            self.is_shown
            or base.world.outings_mgr.gui_is_shown  # noqa: F821
            or base.world.rails_scheme.is_shown  # noqa: F821
        ):
            return

        self._open_snd.play()
        self.is_shown = True

        char_id = base.char_gui.char.id  # noqa: F821
        base.common_ctrl.deselect()  # noqa: F821

        self._char_chooser.prepare(
            self._list,
            (-0.25, 0, 0.08),
            base.team.chars,  # noqa: F821
            list(base.team.chars.keys()).index(char_id),  # noqa: F821
        )
        self._list.show()
        taskMgr.doMethodLater(  # noqa: F821
            0.25, self._update_traits, "update_traits_ctrl"
        )
