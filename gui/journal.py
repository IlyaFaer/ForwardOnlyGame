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

JOURNAL_PAGES = (
    ("diary", "The page text"),
    ("note", "The note text"),
    ("diary", "The page text"),
    ("note", "The note text"),
)


class Journal:
    """Captain's journal GUI object."""

    def __init__(self):
        self._is_shown = False
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
            canvasSize=(-0.31, 0.3, -1.5, 1.5),
            state=DGG.NORMAL,
            pos=(0, 0, -0.1),
            verticalScroll_frameSize=(-0.002, 0.002, -0.5, 0.5),
            verticalScroll_frameColor=(0.51, 0.46, 0.42, 1),
            verticalScroll_thumb_frameColor=(0.31, 0.26, 0.22, 1),
            verticalScroll_incButton_relief=None,
            verticalScroll_decButton_relief=None,
            horizontalScroll_relief=None,
            horizontalScroll_thumb_relief=None,
            horizontalScroll_incButton_relief=None,
            horizontalScroll_decButton_relief=None,
        )
        DirectLabel(
            parent=self._main_fr,
            text="Journal",
            text_font=base.main_font,  # noqa: F821
            text_scale=0.045,
            text_bg=(0, 0, 0, 0),
            frameSize=(0.1, 0.1, 0.1, 0.1),
            pos=(-0.34, 0, 0.52),
            text_align=TextNode.ALeft,
        )
        DirectLabel(
            parent=self._main_fr,
            text="Notes:",
            text_font=base.main_font,  # noqa: F821
            text_scale=0.03,
            text_bg=(0, 0, 0, 0),
            frameSize=(0.1, 0.1, 0.1, 0.1),
            pos=(-0.34, 0, 0.47),
            text_align=TextNode.ALeft,
        )
        DirectLabel(
            parent=self._main_fr,
            text="Diary:",
            text_font=base.main_font,  # noqa: F821
            text_scale=0.03,
            text_bg=(0, 0, 0, 0),
            frameSize=(0.1, 0.1, 0.1, 0.1),
            pos=(-0.34, 0, 0.44),
            text_align=TextNode.ALeft,
        )
        self._page_text = DirectLabel(
            parent=self._fr.getCanvas(),
            text="",
            text_scale=0.03,
            text_font=base.main_font,  # noqa: F821
            text_align=TextNode.ALeft,
            frameSize=(0.02, 0.02, 0.02, 0.02),
            pos=(-0.27, 0, 1.45),
        )
        self._pages = {"diary": [], "note": []}

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

    def add_page(self, num):
        """Add a page into the journal.

        Args:
            num (int): The page number.
        """
        type_, page_text = JOURNAL_PAGES[num]
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
                clickSound=base.main_menu.click_snd,  # noqa: F821
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
        else:
            self._main_fr.show()

        self._is_shown = not self._is_shown
