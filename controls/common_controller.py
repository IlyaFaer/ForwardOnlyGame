"""Common game controls."""
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode

KEYS_INFO = u"""
Game controls:

"W" - hold to speed up
"S" - hold to slow down
\u2190\u2191\u2193\u2192 - move camera
Alt + \u2190\u2191\u2193\u2192 - rotate camera
"""


class CommonController:
    """Common controller.

    Includes controls to show game control keys info.
    """

    def __init__(self):
        self._is_keys_shown = False
        self._keys_info = None
        self._font = None

    def set_controls(self, game):
        """Configure common game controls.

        Args:
            game (ForwardOnly): Game object.
        """
        self._font = game.loader.loadFont("arial.ttf")
        game.accept("f1", self._show_keys)

    def _show_keys(self):
        """Show/hide control keys info."""
        if not self._is_keys_shown:
            self._keys_info = OnscreenText(
                text=KEYS_INFO,
                align=TextNode.ACenter,
                font=self._font,
                pos=(0, 0.7),
                fg=(0.7, 0.7, 0.7, 1),
            )
        else:
            self._keys_info.destroy()

        self._is_keys_shown = not self._is_keys_shown
