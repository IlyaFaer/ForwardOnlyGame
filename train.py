"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Train - the main game object, API.

Includes the systems of Train movement, manipulating,
animation, and splitting Train to several parts.
"""
import random
from direct.actor.Actor import Actor
from panda3d.core import (
    CollisionBox,
    CollisionNode,
    CollisionPolygon,
    PerspectiveLens,
    Point3,
    PointLight,
    Spotlight,
)

from const import MOUSE_MASK, NO_MASK, SHOT_RANGE_MASK
from controls import TrainController
from utils import address


class Train:
    """Train object. The main game object.

    Args:
        game (ForwardOnly): Game object.
    """

    def __init__(self, game):
        self.root_node = render.attachNewNode("train_root")  # noqa: F821
        # node to hold camera and Sun
        self.node = self.root_node.attachNewNode("train")

        self.model = Actor(address("locomotive"))
        self.model.reparentTo(self.root_node)

        self._ctrl = TrainController(self.model)
        self._ctrl.set_controls(game, self, self._set_sounds(game.sound_mgr))

        self.parts = {
            "part_locomotive_left": TrainPart(
                self.model,
                "part_locomotive_left",
                positions=[
                    {"pos": (-0.063, -0.02, 0.147), "angle": 90},
                    {"pos": (-0.063, 0.15, 0.147), "angle": 90},
                ],
                arrow_pos={"pos": (-0.2, 0.09, 0.147), "angle": 90},
            ),
            "part_locomotive_right": TrainPart(
                self.model,
                "part_locomotive_right",
                positions=[
                    {"pos": (0.063, -0.02, 0.147), "angle": -90},
                    {"pos": (0.063, 0.15, 0.147), "angle": -90},
                ],
                arrow_pos={"pos": (0.2, 0.09, 0.147), "angle": -90},
            ),
            "part_locomotive_front": TrainPart(
                self.model,
                "part_locomotive_front",
                positions=[{"pos": (0, 0.41, 0.147), "angle": 0}],
                arrow_pos={"pos": (0, 0.55, 0.147), "angle": 0},
            ),
        }

        self._lights = self._set_lights()
        self.lights_on = False

    def move_along_block(self, block):
        """Move Train along the given world block.

        Args:
            block (world.block.Block): world block to move along.
        """
        self._ctrl.move_along_block(block, self.node)

    def switch_to_current_block(self):
        """Switch to the current world block.

        Train root node must be moved to the end of the
        prev block motion path = start of the current one.
        """
        self.model.wrtReparentTo(render)  # noqa: F821
        self.node.wrtReparentTo(render)  # noqa: F821

        # round coordinates to avoid position/rotation errors
        mod_pos = (
            round(self.model.getX()),
            round(self.model.getY()),
            round(self.model.getZ()),
        )
        self.model.setPos(mod_pos)
        self.model.setHpr(
            (
                round(self.model.getH()),
                round(self.model.getP()),
                round(self.model.getR()),
            )
        )
        self.node.setPos(mod_pos)

        self.root_node.setPos(mod_pos)
        self.root_node.setHpr(self.model, 0)

        self.model.wrtReparentTo(self.root_node)
        self.node.wrtReparentTo(self.root_node)

    def _set_lights(self):
        """Configure Train lights.

        Sets the main Train lighter and lights above the
        doors.

        Returns:
            list: NodePath's of the Train lights.
        """
        lens = PerspectiveLens()
        lens.setNearFar(0, 100)
        lens.setFov(60, 60)

        lighter = Spotlight("train_lighter")
        lighter.setColor((1, 1, 1, 1))
        lighter.setLens(lens)
        lighter.setExponent(0.4)
        lighter_np = self.model.attachNewNode(lighter)
        lighter_np.setPos(0, 0.34, 0.3)

        train_lights = [lighter_np]

        for name, coors in (
            ("train_right_door_light", (0.071, -0.176, 0.245)),
            ("train_left_door_light", (-0.071, -0.176, 0.245)),
            ("train_back_door_light", (0, -0.5, 0.245)),
        ):
            lamp = PointLight(name)
            lamp.setColor((0.99, 0.91, 0.5, 1))
            lamp.setAttenuation((3))
            lamp_np = self.model.attachNewNode(lamp)
            lamp_np.setPos(*coors)

            train_lights.append(lamp_np)

        return train_lights

    def _set_sounds(self, sound_mgr):
        """Configure Train sounds.

        Args:
            sound_mgr (direct.showbase.Audio3DManager.Audio3DManager): Sound manager.

        Returns:
            panda3d.core.AudioSound: Train movement sound.
        """
        train_move_sound = sound_mgr.loadSfx("sounds/train_moves1.ogg")
        sound_mgr.attachSoundToObject(train_move_sound, self.model)

        train_move_sound.setLoop(True)
        train_move_sound.play()
        return train_move_sound

    def toggle_lights(self):
        """Toggle Train lights."""
        method = render.clearLight if self.lights_on else render.setLight  # noqa: F821
        for light in self._lights:
            method(light)

        self.lights_on = not self.lights_on


class TrainPart:
    """Train part where characters can be set.

    Args:
        parent (panda3d.core.NodePath):
                Model, to which arrow sprite of this part
                should be parented. To this model will be
                reparented characters as well.
        name (str): Part name.
        positions (list):
            Dicts describing possible positions and
            rotations on this TrainPart.
        arrow_pos (dict): Arrow sprite position and rotation.
    """

    def __init__(self, parent, name, positions, arrow_pos):
        self.parent = parent
        self.enemies_in_range = []
        self._free = positions

        # organize a manipulating arrow
        self._arrow = loader.loadModel(address("train_part_arrow"))  # noqa: F821
        self._arrow.setPos(*arrow_pos["pos"])
        self._arrow.setH(arrow_pos["angle"])

        # set manipulating arrow collisions
        col_node = CollisionNode(name)
        col_node.setFromCollideMask(NO_MASK)
        col_node.setIntoCollideMask(MOUSE_MASK)
        col_node.addSolid(
            CollisionPolygon(
                Point3(-0.06, -0.06, 0),
                Point3(-0.06, 0.06, 0),
                Point3(0.06, 0.06, 0),
                Point3(0.06, -0.06, 0),
            )
        )
        self._arrow.attachNewNode(col_node)

        # shooting zone for this TrainPart
        col_node = CollisionNode("shoot_zone_" + name)
        col_node.setFromCollideMask(NO_MASK)
        col_node.setIntoCollideMask(SHOT_RANGE_MASK)
        col_node.addSolid(CollisionBox(Point3(-0.4, -0.06, 0), Point3(0.4, 0.8, 0.08)))
        col_np = self.parent.attachNewNode(col_node)
        col_np.setPos(arrow_pos["pos"][0], arrow_pos["pos"][1], 0)
        col_np.setH(arrow_pos["angle"])

        # set event of enemy coming
        base.accept("into-shoot_zone_" + name, self.enemy_came)  # noqa: F821
        # set event of enemy leaving
        base.accept("out-shoot_zone_" + name, self.enemy_leave)  # noqa: F821

    def enemy_came(self, event):
        """Enemy unit entered this TrainPart shooting range."""
        self.enemies_in_range.append(event.getFromNodePath().getName())

    def enemy_leave(self, event):
        """Enemy unit leaved this TrainPart shooting range."""
        self.enemies_in_range.remove(event.getFromNodePath().getName())

    def give_cell(self):
        """Choose a non taken cell.

        Returns:
            dict: Position and rotation to set character.
        """
        if not self._free:
            return

        position = random.choice(self._free)
        self._free.remove(position)
        return position

    def release_cell(self, position):
        """Release cell taken earlier.

        Args:
            position (dict):
                Position and rotation of the taken cell.
        """
        self._free.append(position)

    def show_arrow(self):
        """Show manipulating arrow of this TrainPart."""
        self._arrow.reparentTo(self.parent)

    def hide_arrow(self):
        """Hide manipulating arrow of this TrainPart."""
        self._arrow.detachNode()
