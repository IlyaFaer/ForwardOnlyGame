"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Common game controls: keyboard and mouse clicks.
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


class CommonController:
    """Common controller.

    Includes controls to show game control keys info,
    mouse clicking and common collisions.

    Args:
        parts (dict): Locomotive parts to set characters on.
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
        self.handler = None

        self._move_char_snd = loader.loadSfx("sounds/move_char.ogg")  # noqa: F821
        self._char_pointer = loader.loadModel(  # noqa: F821
            address("character_pointer")
        )
        self._char_pointer.setLightOff()

    @property
    def chosen_char(self):
        """The chosen character object.

        Returns:
            units.crew.character.Chatacter:
                The currently chosen character object.
        """
        return self._chosen_char

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

    def _choose_obj(self):
        """Event: left mouse button clicked.

        Organizes clicking on active objects:
        characters, rest zone, enemies.
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

            self._chosen_char.play_yes()
            return

        if self._pointed_obj == "part_rest":
            self.deselect()
            base.change_mouse_pointer("normal")  # noqa: F821
            base.char_gui.show_resting_chars(  # noqa: F821
                base.train.parts[self._pointed_obj]  # noqa: F821
            )

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
            if (
                self.chosen_char is not None
                and self.chosen_char.id != self._pointed_obj
            ):
                base.change_mouse_pointer("exchange")  # noqa: F82
            return

        if self._pointed_obj.startswith("enemy_"):
            base.char_gui.show_tooltip(  # noqa: F821
                base.world.enemy.active_units[self._pointed_obj].tooltip  # noqa: F821
            )
            if self.chosen_char is not None:
                base.change_mouse_pointer("attack")  # noqa: F821
            return

        if self._pointed_obj == "part_rest":
            base.char_gui.show_tooltip(base.labels.TIPS[1])  # noqa: F821
            if self.chosen_char is not None:
                base.change_mouse_pointer("rest")  # noqa: F821

    def _show_char_relations(self):
        """Show the chosen character relations GUI."""
        if not self.chosen_char:
            return

        self._is_relations_shown = not self._is_relations_shown

        if self._is_relations_shown:
            base.team.show_relations(self.chosen_char)  # noqa: F821
        else:
            base.team.hide_relations()  # noqa: F821

    def _show_keys(self):
        """Show/hide control keys info."""
        if self._is_keys_shown:
            self._keys_info.destroy()
        else:
            self._keys_info = OnscreenText(
                text=base.labels.KEYS_INFO,  # noqa: F821
                align=TextNode.ACenter,
                font=base.main_font,  # noqa: F821
                scale=0.055,
                pos=(0, 0.8),
                fg=(0.7, 0.7, 0.7, 1),
            )

        self._is_keys_shown = not self._is_keys_shown

    def _traverse(self, task):
        """Main traverser task."""
        self.traverser.traverse(render)  # noqa: F821
        return task.again

    def _unpoint_obj(self, event):
        """Event: mouse pointer moved out of an object."""
        self._pointed_obj = ""
        base.char_gui.hide_tip()  # noqa: F821
        base.change_mouse_pointer("normal")  # noqa: F821

    def choose_char(self, char_id):
        """Choose a character with the given id.

        Args:
            char_id (str): Id of the Character to choose.
        """
        self._pointed_obj = char_id
        self._choose_obj()
        self._pointed_obj = None

    def deselect(self, clear_resting=True):
        """Hide manipulating GUI and deselect character.

        Args:
            clear_resting (bool):
                Optional. A flag indicating if the list of the
                resting characters should also be closed.
        """
        self._char_pointer.detachNode()
        self._chosen_char = None

        for part in self._parts.values():
            part.hide_arrow()

        base.char_gui.clear_char_info(clear_resting)  # noqa: F821

        if self._is_relations_shown:
            base.team.hide_relations()  # noqa: F821
            self._is_relations_shown = False

    def set_controls(self):
        """Configure common game controls.

        Configure major keys, collisions system
        and controls to manipulate characters.
        """
        base.accept("f1", self._show_keys)  # noqa: F821
        base.accept("escape", base.main_menu.show)  # noqa: F821
        base.accept("r", self._show_char_relations)  # noqa: F821
        base.accept("m", base.world.rails_scheme.show)  # noqa: F821
        base.accept("j", base.journal.show)  # noqa: F821
        base.accept("0", base.main_menu.show_scp)  # noqa: F821

        # configure mouse collisions
        col_node = CollisionNode("mouse_ray")
        col_node.setIntoCollideMask(NO_MASK)
        col_node.setFromCollideMask(MOUSE_MASK)
        self._mouse_ray = CollisionRay()
        col_node.addSolid(self._mouse_ray)

        # set common collisions handler
        self.handler = CollisionHandlerEvent()
        self.handler.addInPattern("%fn-into")
        self.handler.addAgainPattern("%fn-again")
        self.handler.addOutPattern("%fn-out")

        self.traverser = CollisionTraverser("traverser")
        self.traverser.addCollider(
            base.cam.attachNewNode(col_node), self.handler  # noqa: F821
        )
        self.set_mouse_events()

        taskMgr.doMethodLater(0.03, self._collide_mouse, "collide_mouse")  # noqa: F821
        taskMgr.doMethodLater(0.04, self._traverse, name="main_traverse")  # noqa: F821

    def set_mouse_events(self):
        """
        Set events to organize pointing and clicking
        on characters, enemies and the Train parts.
        """
        base.accept("mouse1", self._choose_obj)  # noqa: F821
        base.accept("mouse3", self._char_action)  # noqa: F821
        base.accept("mouse_ray-into", self._point_obj)  # noqa: F821
        base.accept("mouse_ray-again", self._point_obj)  # noqa: F821
        base.accept("mouse_ray-out", self._unpoint_obj)  # noqa: F821
