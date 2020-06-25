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

    Includes train model, lights, parts to set characters
    and sounds.
    """

    def __init__(self):
        self.root_node = render.attachNewNode("train_root")  # noqa: F821
        # node to hold camera and Sun
        self.node = self.root_node.attachNewNode("train")

        self.model = Actor(address("locomotive"))
        self.model.reparentTo(self.root_node)

        train_move_snd, self._lighter_snd = self._set_sounds()

        self._ctrl = TrainController(self.model, train_move_snd)
        self._ctrl.set_controls(self)

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

        self.damnability = 1000

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

    def _set_sounds(self):
        """Configure Train sounds.

        Returns:
            (panda3d.core.AudioSound, panda3d.core.AudioSound):
                Train movement, lighter toggle sounds.
        """
        train_move_sound = base.sound_mgr.loadSfx(  # noqa: F821
            "sounds/train_moves1.ogg"
        )
        base.sound_mgr.attachSoundToObject(train_move_sound, self.model)  # noqa: F821

        train_move_sound.setLoop(True)
        train_move_sound.play()

        lighter_snd = base.loader.loadSfx("sounds/switcher1.ogg")  # noqa: F821
        lighter_snd.setVolume(0.8)
        return train_move_sound, lighter_snd

    def toggle_lights(self):
        """Toggle Train lights."""
        self._lighter_snd.play()

        method = render.clearLight if self.lights_on else render.setLight  # noqa: F821
        for light in self._lights:
            method(light)

        self.lights_on = not self.lights_on

    def speed_to_min(self):
        """Accelerate Train to minimum combat speed."""
        self._ctrl.speed_to_min()

    def get_damage(self, damage):
        """Get damage from an enemy.

        If damage become critical, stop Train.

        Args:
            damage (int): Damage points to get.
        """
        self.damnability -= damage
        base.train_interface.update_indicators(  # noqa: F821
            damnability=self.damnability
        )
        if self.damnability <= 0:
            if not self._ctrl.critical_damage:
                self._ctrl.critical_damage = True
                self._ctrl.stop()

                base.world.enemy.capture_train()  # noqa: F821
                base.team.surrender()  # noqa: F821


class TrainPart:
    """Train part where characters can be set.

    Contains characters set to this part and enemies
    within its shooting range.

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
        self.chars = []
        # enemies within shooting range of this part
        self.enemies = []
        self._cells = positions

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
        """Enemy unit entered this part shooting range."""
        enemy = base.world.enemy.active_units.get(  # noqa: F821
            event.getFromNodePath().getName()
        )
        if enemy is not None:
            self.enemies.append(enemy)
            enemy.enter_the_part(self)

    def enemy_leave(self, event):
        """Enemy unit leaved this part shooting range."""
        enemy = base.world.enemy.active_units.get(  # noqa: F821
            event.getFromNodePath().getName()
        )
        if enemy is not None:
            self.enemies.remove(enemy)
            enemy.leave_the_part()

    def give_cell(self, character):
        """Choose a non taken cell.

        Args:
            character (personage.character.Character):
                Unit to set to this part.

        Returns:
            dict: Position and rotation to set character.
        """
        if not self._cells:
            return

        position = random.choice(self._cells)
        self._cells.remove(position)

        self.chars.append(character)
        return position

    def release_cell(self, position, character):
        """Release cell taken earlier.

        Args:
            position (dict):
                Position and rotation of the taken cell.
            character (personage.character.Character):
                Character to remove from this part.
        """
        self._cells.append(position)
        self.chars.remove(character)

    def show_arrow(self):
        """Show manipulating arrow of this TrainPart."""
        self._arrow.reparentTo(self.parent)

    def hide_arrow(self):
        """Hide manipulating arrow of this TrainPart."""
        self._arrow.detachNode()
