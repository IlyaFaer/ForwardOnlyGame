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
    CollisionNode,
    CollisionPolygon,
    PerspectiveLens,
    Point3,
    PointLight,
    Spotlight,
)

from controls import TrainController
from utils import address


class Train:
    """Train object. The main game object.

    Args:
        game (ForwardOnly): Game object.
    """

    def __init__(self, game):
        # root Train node
        self.root_node = game.render.attachNewNode("train_root")
        # node to hold camera and Sun
        self.node = self.root_node.attachNewNode("train")

        self.model = Actor(address("locomotive"))
        self.model.reparentTo(self.root_node)

        self._ctrl = TrainController(self.model)
        self._ctrl.set_controls(game, self)

        self.parts = {
            "part_arrow_locomotive_left": TrainPart(
                game.loader,
                self.model,
                "part_arrow_locomotive_left",
                positions=[
                    {"pos": (-0.06, -0.02, 0.147), "angle": -90},
                    {"pos": (-0.06, 0.15, 0.147), "angle": -90},
                ],
                arrow_pos={"pos": (-0.2, 0.09, 0.147), "angle": 90},
            ),
            "part_arrow_locomotive_right": TrainPart(
                game.loader,
                self.model,
                "part_arrow_locomotive_right",
                positions=[
                    {"pos": (0.06, -0.02, 0.147), "angle": 90},
                    {"pos": (0.06, 0.15, 0.147), "angle": 90},
                ],
                arrow_pos={"pos": (0.2, 0.09, 0.147), "angle": -90},
            ),
            "part_arrow_locomotive_front": TrainPart(
                game.loader,
                self.model,
                "part_arrow_locomotive_front",
                positions=[{"pos": (0, 0.42, 0.147), "angle": 180}],
                arrow_pos={"pos": (0, 0.55, 0.147), "angle": 0},
            ),
        }

        self._lights_on = False
        self._lights = self._set_lights()

    def move_along_block(self, block):
        """Move Train along the given world block.

        Args:
            block (world.block.Block): world block to move along.
        """
        self._ctrl.move_along_block(block, self.node)

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
            lamp.setAttenuation((3, 3, 3))
            lamp_np = self.model.attachNewNode(lamp)
            lamp_np.setPos(*coors)

            train_lights.append(lamp_np)

        return train_lights

    def toggle_lights(self, render):
        """Toggle all the Train lights.

        Args:
            render (panda3d.core.NodePath): Game render.
        """
        if not self._lights_on:
            for light in self._lights:
                render.setLight(light)
        else:
            for light in self._lights:
                render.clearLight(light)

        self._lights_on = not self._lights_on


class TrainPart:
    """Train part where characters can be set.

    Args:
        loader (direct.showbase.Loader.Loader): Panda3D models loader.
        parent (panda3d.core.NodePath):
                Model, to which arrow sprite of this part
                should be parented. To this model will be
                reparented characters as well.
        id_ (str): Part id.
        positions (list):
            Dicts describing possible positions and
            rotations on this TrainPart.
        arrow_pos (dict): Arrow sprite position and rotation.
    """

    def __init__(self, loader, parent, id_, positions, arrow_pos):
        self.id = id_
        self.parent = parent
        self._free = positions
        self._taken = []

        # organize a manipulating arrow
        self._arrow = loader.loadModel(address("train_part_arrow"))
        self._arrow.setPos(*arrow_pos["pos"])
        self._arrow.setH(arrow_pos["angle"])

        col_solid = CollisionPolygon(
            Point3(-0.06, -0.06, 0),
            Point3(-0.06, 0.06, 0),
            Point3(0.06, 0.06, 0),
            Point3(0.06, -0.06, 0),
        )
        col_solid.flip()
        col_node = self._arrow.attachNewNode(CollisionNode(self.id))
        col_node.node().addSolid(col_solid)

    def give_cell(self):
        """Choose non taken cell.

        Returns:
            dict: Position and rotation to set character.
        """
        if not self._free:
            return

        position = random.choice(self._free)
        self._free.remove(position)
        self._taken.append(position)
        return position

    def release_cell(self, position):
        """Release cell taken earlier.

        Args:
            position (dict):
                Position and rotation of the taken cell.
        """
        self._taken.remove(position)
        self._free.append(position)

    def show_arrow(self):
        """Show manipulating arrow if this TrainPart."""
        self._arrow.reparentTo(self.parent)

    def hide_arrow(self):
        """Hide manipulating arrow if this TrainPart."""
        self._arrow.detachNode()
