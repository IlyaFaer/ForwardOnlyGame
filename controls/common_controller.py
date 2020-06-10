"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Common game controls.
"""
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import (
    CollisionHandlerEvent,
    CollisionNode,
    CollisionRay,
    CollisionTraverser,
    TextNode,
)

from utils import address

KEYS_INFO = u"""
Game controls:

Mouse Left Button - choose a character
Mouse Right Button - move chosen character
A - deselect character

W - hold to speed up
S - hold to slow down

\u2190\u2191\u2193\u2192 - move camera
Alt + \u2190\u2191\u2193\u2192 - rotate camera
"+", "-" - zoom camera
C - toggle centered view

F - toggle Train lights
"""


class CommonController:
    """Common controller.

    Includes controls to show game control keys info.

    Args:
        parts (dict):
            Train parts to set characters on.
    """

    def __init__(self, parts):
        self._is_keys_shown = False
        self._keys_info = None
        self._font = None
        self._traverser = None

        self._pointed_obj = ""
        self._chosen_char = None
        self._char_pointer = None
        self.chars = {}

        self._parts = parts

    def set_controls(self, game):
        """Configure common game controls.

        Configure major keys, collisions system
        and controls to manipulate characters.

        Args:
            game (ForwardOnly): Game object.
        """
        self._font = loader.loadFont("arial.ttf")  # noqa: F821
        game.accept("f1", self._show_keys)
        game.accept("a", self._deselect)

        # configure collisions to control characters
        self._char_pointer = loader.loadModel(  # noqa: F821
            address("character_pointer")
        )

        # set mouse ray
        mouse_col_node = CollisionNode("mouse_ray")
        mouse_np = game.cam.attachNewNode(mouse_col_node)
        self._mouse_ray = CollisionRay()
        mouse_col_node.addSolid(self._mouse_ray)

        handler = CollisionHandlerEvent()
        handler.addInPattern("%fn-into")
        handler.addOutPattern("%fn-out")

        self._traverser = CollisionTraverser("main_traverser")
        self._traverser.addCollider(mouse_np, handler)

        # set events and tasks to organize pointing
        # and clicking on characters and parts
        game.accept("mouse1", self._choose_char)
        game.accept("mouse3", self._move_char)
        game.accept("mouse_ray-into", self._point_obj)
        game.accept("mouse_ray-out", self._unpoint_obj)

        game.taskMgr.doMethodLater(0.09, self._collide_mouse, "collide_mouse")
        game.taskMgr.doMethodLater(
            0.1,
            self._traverse,
            extraArgs=[game.render],
            appendTask=True,
            name="main_traverse",
        )

    def _deselect(self):
        """Remove all manipulating interface."""
        self._char_pointer.detachNode()
        for part in self._parts.values():
            part.hide_arrow()

    def _choose_char(self):
        """Event: mouse button pushed on a character.

        Sets a cursor on the clicked character, and
        remembers its object. Also shows manipulation
        interface.
        """
        if self._pointed_obj.startswith("character_"):
            self._chosen_char = self.chars[self._pointed_obj]
            self._char_pointer.reparentTo(self._chosen_char.model)

            for part in self._parts.values():
                part.show_arrow()

    def _move_char(self):
        """Move chosen character to the pointed part."""
        if self._chosen_char:
            if self._pointed_obj.startswith("part_arrow_"):
                self._chosen_char.move_to(self._parts[self._pointed_obj])

    def _point_obj(self, event):
        """Event: mouse pointer hits a collision."""
        self._pointed_obj = event.getIntoNodePath().getName()

    def _unpoint_obj(self, event):
        """Event: mouse pointer moved out of an object."""
        self._pointed_obj = ""

    def _collide_mouse(self, task):
        """Organize active mouse collision object movement.

        Args:
            task (panda3d.core.PythonTask): Point by mouse task
        """
        mpos = base.mouseWatcherNode.getMouse()  # noqa: F821
        self._mouse_ray.setFromLens(base.camNode, mpos.x, mpos.y)  # noqa: F821
        return task.again

    def _traverse(self, render, task):
        """Main traverser task."""
        self._traverser.traverse(render)
        return task.again

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
