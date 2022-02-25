"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Captain's journal GUI.
"""
from direct.gui.DirectGui import (
    DGG,
    DirectButton,
    DirectFrame,
    DirectLabel,
    DirectScrolledFrame,
)
from panda3d.core import TextNode, TransparencyAttrib
from gui.widgets import RUST_COL, SILVER_COL


class Journal:
    """Captain's journal GUI object.

    Args:
        winned (bool):
            Flag, saying if the player already won the game.
    """

    def __init__(self, winned=False):
        self._is_shown = False
        self._read_coordinates = False
        self._winned = winned

        self._main_fr = DirectFrame(
            parent=base.a2dTopLeft,  # noqa: F821
            frameSize=(-0.37, 0.38, -0.6, 0.6),
            state=DGG.NORMAL,
            pos=(0.37, 0, -1),
            frameTexture="gui/tex/paper1.png",
        )
        self._main_fr.setTransparency(TransparencyAttrib.MAlpha)
        self._main_fr.hide()

        self._fr = DirectScrolledFrame(
            parent=self._main_fr,
            frameSize=(-0.35, 0.3, -0.46, 0.5),
            frameColor=(0, 0, 0, 0),
            canvasSize=(-0.31, 0.3, -3, 1.5),
            state=DGG.NORMAL,
            pos=(0, 0, -0.1),
            verticalScroll_frameSize=(-0.003, 0.003, -0.5, 0.5),
            verticalScroll_frameColor=(0.46, 0.41, 0.37, 1),
            verticalScroll_thumb_frameColor=(0.31, 0.26, 0.22, 1),
            verticalScroll_incButton_relief=None,
            verticalScroll_decButton_relief=None,
            horizontalScroll_relief=None,
            horizontalScroll_thumb_relief=None,
            horizontalScroll_incButton_relief=None,
            horizontalScroll_decButton_relief=None,
        )
        DirectLabel(  # Journal
            parent=self._main_fr,
            text=base.labels.JOURNAL[0],  # noqa: F821
            text_font=base.cursive_font,  # noqa: F821
            text_scale=0.053,
            text_bg=(0, 0, 0, 0),
            text_fg=(0, 0, 0.25, 1),
            frameSize=(0.1, 0.1, 0.1, 0.1),
            pos=(-0.34, 0, 0.52),
            text_align=TextNode.ALeft,
        )
        DirectLabel(
            parent=self._main_fr,
            text=base.labels.JOURNAL[1],  # noqa: F821
            text_font=base.cursive_font,  # noqa: F821
            text_scale=0.038,
            text_fg=(0, 0, 0.25, 1),
            text_bg=(0, 0, 0, 0),
            frameSize=(0.1, 0.1, 0.1, 0.1),
            pos=(-0.34, 0, 0.47),
            text_align=TextNode.ALeft,
        )
        DirectLabel(
            parent=self._main_fr,
            text=base.labels.JOURNAL[2],  # noqa: F821
            text_font=base.cursive_font,  # noqa: F821
            text_scale=0.038,
            text_fg=(0, 0, 0.25, 1),
            text_bg=(0, 0, 0, 0),
            frameSize=(0.1, 0.1, 0.1, 0.1),
            pos=(-0.34, 0, 0.44),
            text_align=TextNode.ALeft,
        )
        self._page_text = DirectLabel(
            parent=self._fr.getCanvas(),
            text="",
            text_scale=0.045,
            text_font=base.cursive_font,  # noqa: F821
            text_align=TextNode.ALeft,
            text_fg=(0, 0, 0.25, 1),
            frameSize=(-0.02, 0.02, -3.5, 0.5),
            frameColor=(0, 0, 0, 0),
            pos=(-0.27, 0, 1.45),
        )
        self._pages = {"diary": [], "note": []}

        self._open_snd = loader.loadSfx("sounds/GUI/journal.ogg")  # noqa: F821
        self._page_snd = loader.loadSfx("sounds/GUI/journal_page.ogg")  # noqa: F821
        self._close_snd = loader.loadSfx("sounds/GUI/journal_close.ogg")  # noqa: F821

    @property
    def winned(self):
        """The flag indicating if the player already won.

        Returns:
            bool: True if the player already won, False otherwise.
        """
        return self._winned

    def _open_page(self, type_, num):
        """Open the given page of the journal.

        Args:
            type_ (str): Page type: diary or note.
            num (int): Number of the page.
        """
        self._page_text["text"] = self._pages[type_][num]["page"]
        for page_type in ("diary", "note"):
            for page in self._pages[page_type]:
                page["but"]["text_fg"] = RUST_COL

        self._pages[type_][num]["but"]["text_fg"] = SILVER_COL
        self._page_snd.play()

        if type_ == "note" and num == 3:
            self._read_coordinates = True

    def add_page(self, num):
        """Add a page into the journal.

        Args:
            num (int): The page number.
        """
        type_, page_text = base.labels.JOURNAL_PAGES[num]  # noqa: F821
        number = len(self._pages[type_]) + 1
        page_rec = {
            "page": page_text,
            "but": DirectButton(
                parent=self._main_fr,
                text="№" + str(number),
                text_font=base.main_font,  # noqa: F821
                text_fg=RUST_COL,
                text_shadow=(0, 0, 0, 1),
                frameColor=(0, 0, 0, 0),
                scale=(0.029, 0, 0.029),
                command=self._open_page,
                extraArgs=[type_, number - 1],
                pos=(-0.32 + number * 0.1, 0, 0.47 if type_ == "note" else 0.44,),
            ),
        }
        self._pages[type_].append(page_rec)

    def show(self):
        """Show/hide the journal GUI."""
        if self._is_shown:
            self._main_fr.hide()
            self._close_snd.play()
            if not self._winned and self._read_coordinates:
                self._winned = True

                page = DirectFrame(
                    frameSize=(-0.73, 0.73, -0.9, 0.9),
                    frameTexture="gui/tex/paper1.png",
                    state=DGG.NORMAL,
                )
                page.setDepthTest(False)
                page.setTransparency(TransparencyAttrib.MAlpha)
                page.show()

                DirectLabel(
                    parent=page,
                    text=base.labels.UNTERRIFF_DISCOVERED_TITLE,  # noqa: F821
                    text_font=base.main_font,  # noqa: F821
                    frameSize=(0.6, 0.6, 0.6, 0.6),
                    text_scale=0.043,
                    pos=(0, 0, 0.65),
                )

                DirectLabel(
                    parent=page,
                    text=base.labels.UNTERRIFF_DISCOVERED,  # noqa: F821
                    text_font=base.main_font,  # noqa: F821
                    frameSize=(0.6, 0.6, 0.6, 0.6),
                    text_scale=0.037,
                    pos=(0, 0, 0.55),
                )

                DirectButton(  # Done
                    parent=page,
                    pos=(0, 0, -0.77),
                    text=base.labels.DISTINGUISHED[6],  # noqa: F821
                    text_font=base.main_font,  # noqa: F821
                    text_fg=RUST_COL,
                    text_shadow=(0, 0, 0, 1),
                    frameColor=(0, 0, 0, 0),
                    command=page.destroy,
                    extraArgs=[],
                    scale=(0.05, 0, 0.05),
                    clickSound=base.main_menu.click_snd,  # noqa: F821
                )

            self._read_coordinates = False
        else:
            self._main_fr.show()
            self._open_snd.play()

        self._is_shown = not self._is_shown
