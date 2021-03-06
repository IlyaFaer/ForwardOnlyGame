"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Common game controls: keys and mouse clicks.
"""
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import (
    CollisionHandlerEvent,
    CollisionNode,
    CollisionRay,
    CollisionTraverser,
    TextNode,
)

from const import MOUSE_MASK, NO_MASK
from utils import address

KEYS_INFO = u"""
Game controls:

Mouse Left Button - choose a character
Mouse Right Button On Arrow - move character
R - show the character's cohesion with others
Choose a character and click on resource button to use it

W - hold to accelerate
S - hold to slow down
F - toggle Train lights

Camera:
\u2190\u2191\u2193\u2192 or push screen edge with mouse - move
Alt + \u2190\u2191\u2193\u2192 or hold mouse wheel - rotate
"+", "-" or scroll mouse wheel - zoom
C - toggle centered view
"""


class CommonController:
    """Common controller.

    Includes controls to show game control keys info,
    mouse clicking and common collisions.

    Args:
        parts (dict): Train parts to set characters on.
        chars (dict): Characters index.
    """

    def __init__(self, parts, chars):
        self._chars = chars
        self._parts = parts

        self._is_keys_shown = False
        self._is_relations_shown = False
        self._keys_info = None  # on screen text object
        self._pointed_obj = ""
        self._chosen_char = None

        self._move_char_snd = loader.loadSfx("sounds/move_char1.ogg")  # noqa: F821

        self._font = loader.loadFont("arial.ttf")  # noqa: F821
        self._char_pointer = loader.loadModel(  # noqa: F821
            address("character_pointer")
        )
        self._char_pointer.setLightOff()

    @property
    def chosen_char(self):
        """Returns the chosen character.

        Returns:
            personage.character.Chatacter:
                The currently chosen character object.
        """
        return self._chosen_char

    def set_controls(self):
        """Configure common game controls.

        Configure major keys, collisions system
        and controls to manipulate characters.
        """
        base.accept("f1", self._show_keys)  # noqa: F821
        base.accept("escape", base.main_menu.show)  # noqa: F821
        base.accept("r", self._show_char_relations)  # noqa: F821

        # configure mouse collisions
        col_node = CollisionNode("mouse_ray")
        col_node.setIntoCollideMask(NO_MASK)
        col_node.setFromCollideMask(MOUSE_MASK)
        self._mouse_ray = CollisionRay()
        col_node.addSolid(self._mouse_ray)

        # set common collisions handler
        handler = CollisionHandlerEvent()
        handler.addInPattern("%fn-into")
        handler.addAgainPattern("%fn-again")
        handler.addOutPattern("%fn-out")

        self.traverser = CollisionTraverser("traverser")
        self.traverser.addCollider(
            base.cam.attachNewNode(col_node), handler  # noqa: F821
        )
        # set events and tasks to organize pointing
        # and clicking on characters and Train parts
        base.accept("mouse1", self._choose_obj)  # noqa: F821
        base.accept("mouse3", self._char_action)  # noqa: F821
        base.accept("mouse_ray-into", self._point_obj)  # noqa: F821
        base.accept("mouse_ray-again", self._point_obj)  # noqa: F821
        base.accept("mouse_ray-out", self._unpoint_obj)  # noqa: F821

        taskMgr.doMethodLater(0.05, self._collide_mouse, "collide_mouse")  # noqa: F821
        taskMgr.doMethodLater(0.06, self._traverse, name="main_traverse")  # noqa: F821

    def choose_char(self, char_id):
        """Choose a character with the given id.

        Args:
            char_id (str): Id of the Character to choose.
        """
        self._pointed_obj = char_id
        self._choose_obj()
        self._pointed_obj = None

    def deselect(self):
        """Hide manipulating GUI and deselect character."""
        self._char_pointer.detachNode()
        self._chosen_char = None

        for part in self._parts.values():
            part.hide_arrow()

        base.char_gui.clear_char_info()  # noqa: F821

        if self._is_relations_shown:
            base.team.hide_relations()  # noqa: F821
            self._is_relations_shown = False

    def _choose_obj(self):
        """Event: left mouse button clicked.

        Organizes clicking on active objects:
        characters, rest zones.
        """
        if not self._pointed_obj:
            self.deselect()
            return

        if self._pointed_obj.startswith("character_"):
            self._chosen_char = self._chars[self._pointed_obj]
            self._char_pointer.reparentTo(self._chosen_char.model)

            for part in self._parts.values():
                part.show_arrow()

            base.char_gui.show_char_info(self._chosen_char)  # noqa: F821
            if self._is_relations_shown:
                base.team.show_relations(self._chosen_char)  # noqa: F821

            return

        if self._pointed_obj.startswith("part_rest_"):
            base.char_gui.show_resting_chars(  # noqa: F821
                base.train.parts[self._pointed_obj]  # noqa: F821
            )

    def _char_action(self):
        """Event: right mouse button pressed.

        Make the chosen character act on the pointed object.
        """
        if self._pointed_obj and self._chosen_char:
            if self._pointed_obj.startswith("part_"):
                if self._chosen_char.move_to(self._parts[self._pointed_obj]):
                    self._move_char_snd.play()
                return

            if self._pointed_obj.startswith("enemy_"):
                self._chosen_char.attack(
                    base.world.enemy.active_units[self._pointed_obj]  # noqa: F821
                )
                return

            if self._pointed_obj.startswith("character_"):
                self.chosen_char.exchange_pos(self._chars[self._pointed_obj])
                self._move_char_snd.play()

    def _point_obj(self, event):
        """Event: mouse pointer hits a collision solid."""
        pointed_obj = event.getIntoNodePath().getName()
        if pointed_obj == self._pointed_obj and pointed_obj is not None:
            return

        self._pointed_obj = pointed_obj

        # show_tooltip
        if self._pointed_obj.startswith("character_"):
            base.char_gui.show_tooltip(  # noqa: F821
                self._chars[self._pointed_obj].tooltip
            )
            return

        if self._pointed_obj.startswith("enemy_"):
            base.char_gui.show_tooltip(  # noqa: F821
                base.world.enemy.active_units[self._pointed_obj].tooltip  # noqa: F821
            )
            return

        if self._pointed_obj.startswith("part_rest_"):
            base.char_gui.show_tooltip("Rest zone")  # noqa: F821

    def _unpoint_obj(self, event):
        """Event: mouse pointer moved out of an object."""
        self._pointed_obj = ""
        base.char_gui.hide_tip()  # noqa: F821

    def _collide_mouse(self, task):
        """Organize mouse collision ray movement.

        Args:
            task (panda3d.core.PythonTask): Point by mouse task
        """
        if not base.mouseWatcherNode.hasMouse():  # noqa: F821
            return task.again

        mpos = base.mouseWatcherNode.getMouse()  # noqa: F821
        self._mouse_ray.setFromLens(base.camNode, mpos.x, mpos.y)  # noqa: F821
        return task.again

    def _traverse(self, task):
        """Main traverser task."""
        self.traverser.traverse(render)  # noqa: F821
        return task.again

    def _show_keys(self):
        """Show/hide control keys info."""
        if self._is_keys_shown:
            self._keys_info.destroy()
        else:
            self._keys_info = OnscreenText(
                text=KEYS_INFO,
                align=TextNode.ACenter,
                font=self._font,
                pos=(0, 0.7),
                fg=(0.7, 0.7, 0.7, 1),
            )

        self._is_keys_shown = not self._is_keys_shown

    def _show_char_relations(self):
        """Show the chosen character relations GUI."""
        if not self.chosen_char:
            return

        self._is_relations_shown = not self._is_relations_shown

        if self._is_relations_shown:
            base.team.show_relations(self.chosen_char)  # noqa: F821
        else:
            base.team.hide_relations()  # noqa: F821
