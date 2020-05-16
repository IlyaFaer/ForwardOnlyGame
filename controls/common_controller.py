"""Common game controls."""
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import (
    CollisionHandlerEvent,
    CollisionNode,
    CollisionRay,
    CollisionTraverser,
    TextNode,
)

MOD_DIR = "models/bam/"
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

    Args:
        characters (dict):
            Characters under the player control index.
    """

    def __init__(self, characters):
        self._is_keys_shown = False
        self._keys_info = None
        self._font = None
        self._traverser = None

        self._char_pointer = None
        self._characters = characters

    def set_controls(self, game):
        """Configure common game controls.

        Configure major keys, collisions system
        and controls to manipulate characters.

        Args:
            game (ForwardOnly): Game object.
        """
        self._font = game.loader.loadFont("arial.ttf")
        game.accept("f1", self._show_keys)

        # configure collisions to control characters
        self._char_pointer = game.loader.loadModel(MOD_DIR + "character_pointer.bam")

        # set mouse ray
        mouse_col_node = CollisionNode("mouse_ray")
        mouse_np = game.cam.attachNewNode(mouse_col_node)
        self._mouse_ray = CollisionRay()
        mouse_col_node.addSolid(self._mouse_ray)

        handler = CollisionHandlerEvent()
        handler.addInPattern("%fn-into")

        self._traverser = CollisionTraverser("main_traverser")
        self._traverser.addCollider(mouse_np, handler)

        # set events and tasks to organize
        # pointing and clicking on characters
        game.accept("mouse1", self._choose_character)
        game.accept("mouse_ray-into", self._point_character)

        game.taskMgr.doMethodLater(0.1, self._point_by_mouse, "point_by_mouse")
        game.taskMgr.doMethodLater(
            0.15,
            self._traverse,
            extraArgs=[game.render],
            appendTask=True,
            name="main_traverse",
        )

    def _choose_character(self):
        """Event, when mouse button was pushed on a character.

        Sets a cursor on the clicked character.
        """
        self._char_pointer.reparentTo(
            self._characters[int(self._pointed_character)].model
        )

    def _point_character(self, event):
        """Event, when mouse pointer hits a character."""
        self._pointed_character = event.getIntoNodePath().getName()

    def _point_by_mouse(self, task):
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
