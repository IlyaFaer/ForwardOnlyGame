"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Train - the main game object, API.

Includes the systems of Train loading, preparations,
animation, sounds, lights. Train is splitted into
several parts.
"""
from direct.actor.Actor import Actor
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.bullet import BulletBoxShape, BulletCharacterControllerNode
from panda3d.core import (
    CollisionBox,
    CollisionNode,
    CollisionPolygon,
    PerspectiveLens,
    Point3,
    PointLight,
    Spotlight,
    Vec3,
)

from const import MOUSE_MASK, NO_MASK, SHOT_RANGE_MASK
from controls import TrainController
from gui.train import TrainInterface
from utils import address, take_random


class Train:
    """Train object. The main game object.

    Includes train model, lights, sounds, parts to set
    characters and controller.

    Args:
        description (dict): Train condition description.
    """

    def __init__(self, description=None):
        self.root_node = render.attachNewNode("train_root")  # noqa: F821
        # node to hold camera and Sun
        self.node = self.root_node.attachNewNode("train")

        self.model = Actor(address("locomotive"))
        self.model.reparentTo(self.root_node)

        self._smoke = ParticleEffect()
        self._smoke.loadConfig("effects/smoke1.ptf")
        self._smoke.setPos(0, 0.32, 0.28)
        self._smoke.start(self.model, render)  # noqa: F821

        move_snd, stop_snd, brake_snd, self._clunk_snd, self._lighter_snd = (
            self._set_sounds()
        )

        self.ctrl = TrainController(self.model, move_snd, stop_snd, brake_snd)
        self.ctrl.set_controls(self)

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
            "part_rest_locomotive": RestPart(self.model, "part_rest_locomotive"),
        }

        self._lights = self._set_lights()
        self.lights_on = False

        self._interface = TrainInterface()

        if description:  # loading params from the last save
            self.damnability = description["damnability"]
            self._miles = description["miles"] - 1
            self.node.setHpr(description["node_angle"])
        else:  # init params
            self.damnability = 1000
            self._miles = -1

        self.l_brake = False
        self.r_brake = False

        self._l_brake_sparks = ParticleEffect()
        self._l_brake_sparks.loadConfig("effects/brake_sparks2.ptf")
        self._l_brake_sparks.setPos(-0.058, 0.38, 0.025)

        self._r_brake_sparks = ParticleEffect()
        self._r_brake_sparks.loadConfig("effects/brake_sparks1.ptf")
        self._r_brake_sparks.setPos(0.058, 0.38, 0.025)

    @property
    def condition(self):
        """Train condition for game saving.

        Returns:
            dict: Train condition values.
        """
        cond = {
            "damnability": self.damnability,
            "speed": self.ctrl.current_speed,
            "miles": self._miles,
            "node_angle": self.node.getHpr(),
        }
        return cond

    def set_physics(self, phys_mgr):
        """Set Train physics.

        Args:
            phys_mgr (panda3d.bullet.BulletWorld):
                Physical world.

        Returns:
            panda3d.core.NodePath: Train physical node.
        """
        shape = BulletCharacterControllerNode(
            BulletBoxShape(Vec3(0.095, 0.48, 0.1)), 10, "train_shape"
        )
        node = self.model.attachNewNode(shape)
        node.setZ(0.1)

        phys_mgr.attachCharacter(shape)
        return node

    def has_cell(self):
        """Check if there is a free cell for a new unit.

        Returns:
            bool: True, if there is a free cell.
        """
        cells_num = 0
        for part in self.parts.values():
            cells_num += part.free_cells

        return cells_num >= 2

    def place_recruit(self, char):
        """Place the new recruit somewhere on Train.

        Args:
            char (personage.character.Character):
                New recruit object.
        """
        for part in self.parts.values():
            if part.free_cells > 0:
                char.move_to(part)
                return

    def brake(self, side, brake):
        """Start braking.

        Args:
            side (str): Side label: 'l' or 'r'.
            brake (panda3d.core.NodePath):
                Brake model to drop.
        """
        self._clunk_snd.play()
        sparks = self._l_brake_sparks if side == "l" else self._r_brake_sparks
        sparks.start(self.model, self.model)
        sparks.softStart()

        base.taskMgr.doMethodLater(  # noqa: F821
            30,
            self._clear_brake,
            side + "_clear_brake",
            extraArgs=[side, brake],
            appendTask=True,
        )
        if self.l_brake and self.r_brake:
            self.ctrl.max_speed = 0.5
            self.ctrl.brake_down_to(0.5)
            return

        self.ctrl.max_speed = 0.75
        self.ctrl.brake_down_to(0.75)

    def slow_down_to(self, target):
        """Slow down Train to the given speed.

        Args:
            target (float): Target speed.
        """
        self.ctrl.slow_down_to(target)

    def move_to_hangar(self):
        """Move Train into city hangar."""
        self.root_node.setZ(50)
        self._smoke.disable()

    def _clear_brake(self, side, brake, task):
        """Stop braking.

        Args:
            side (str): Side label: 'l' or 'r'.
            brake (panda3d.core.NodePath):
                Brake model to drop.
        """
        if side == "l":
            self._l_brake_sparks.softStop()
            self.l_brake = False
        else:
            self._r_brake_sparks.softStop()
            self.r_brake = False

        self.ctrl.max_speed += 0.25
        brake.removeNode()
        return task.done

    def move_along_block(self, block):
        """Move Train along the given world block.

        Args:
            block (world.block.Block): world block to move along.
        """
        self._miles += 1
        self._interface.update_miles(self._miles)

        self.ctrl.move_along_block(block, self.node)

    def switch_to_current_block(self):
        """Switch to the current world block.

        Train root node must be moved to the end of the
        prev block motion path = start of the current one.
        """
        self.model.wrtReparentTo(render)  # noqa: F821
        self.node.wrtReparentTo(render)  # noqa: F821

        # round coordinates to fix position/rotation errors
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

        Sets the main Train lighter and lights above
        the doors.

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
                Train movement, stopping, braking, lighter
                toggle sounds.
        """
        move_snd = base.sound_mgr.loadSfx("sounds/train_moves1.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(move_snd, self.model)  # noqa: F821
        move_snd.setLoop(True)
        move_snd.play()

        stop_snd = base.sound_mgr.loadSfx("sounds/train_stop1.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(stop_snd, self.model)  # noqa: F821

        brake_snd = base.sound_mgr.loadSfx("sounds/train_brake.ogg")  # noqa: F821
        brake_snd.setLoop(True)
        base.sound_mgr.attachSoundToObject(brake_snd, self.model)  # noqa: F821

        clunk_snd = base.sound_mgr.loadSfx("sounds/metal_clunk1.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(clunk_snd, self.model)  # noqa: F821

        lighter_snd = base.loader.loadSfx("sounds/switcher1.ogg")  # noqa: F821
        lighter_snd.setVolume(0.8)
        return move_snd, stop_snd, brake_snd, clunk_snd, lighter_snd

    def toggle_lights(self):
        """Toggle Train lights."""
        self._lighter_snd.play()

        method = render.clearLight if self.lights_on else render.setLight  # noqa: F821
        for light in self._lights:
            method(light)

        self.lights_on = not self.lights_on

    def speed_to_min(self):
        """Accelerate Train to minimum combat speed."""
        self.ctrl.speed_to_min()

    def get_damage(self, damage):
        """Get damage from an enemy.

        If damage become critical, stop Train.

        Args:
            damage (int): Damage points to get.
        """
        self.damnability -= damage
        self._interface.update_indicators(damnability=self.damnability)

        if not self.ctrl.critical_damage:
            if self.damnability <= 0:
                self.ctrl.critical_damage = True
                self.ctrl.stop()

                base.world.enemy.capture_train()  # noqa: F821
                base.team.surrender()  # noqa: F821

    def do_effects(self, effects):
        """Do outing effects to Train.

        Args:
            effects (dict): Effects and their values.
        """
        for key, value in effects.items():
            if hasattr(self, key):
                setattr(self, key, getattr(self, key) + value)
                self._interface.update_indicators(**{key: getattr(self, key)})

    def stop_sparks(self):
        """Stop sparks effects."""
        self._l_brake_sparks.softStop()
        self._r_brake_sparks.softStop()


class TrainPart:
    """Train part where characters can be set.

    Contains characters set to this part and enemies
    within its shooting range.

    Args:
        parent (panda3d.core.NodePath):
                Model, to which arrow sprite of this part
                must be parented. Characters will be
                parented to this model as well.
        name (str): Part name.
        positions (list):
            Dicts describing possible positions and
            rotations on this TrainPart.
        arrow_pos (dict): Arrow position and rotation.
    """

    def __init__(self, parent, name, positions, arrow_pos):
        self.parent = parent
        self.chars = []
        self.name = name
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

        base.accept("into-shoot_zone_" + name, self.enemy_came)  # noqa: F821
        base.accept("out-shoot_zone_" + name, self.enemy_leave)  # noqa: F821

    @property
    def free_cells(self):
        """The number of free cells on this part.

        Returns:
            int: The number of free cells
        """
        return len(self._cells)

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
            enemy.leave_the_part(self)

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

        self.chars.append(character)
        return take_random(self._cells)

    def release_cell(self, position, character):
        """Release a cell taken earlier.

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


class RestPart:
    """Part of Train on which characters can rest.

    Rest helps to regain energy.

    Args:
        parent (panda3d.core.NodePath):
                Model, to which characters will be
                reparented while on this part.
        name (str): Part name.
    """

    def __init__(self, parent, name):
        self.parent = parent
        self.chars = []
        self.enemies = []
        self.name = name

        # rest zone collisions
        col_node = CollisionNode(name)
        col_node.setFromCollideMask(NO_MASK)
        col_node.setIntoCollideMask(MOUSE_MASK)
        col_node.addSolid(
            CollisionBox(Point3(-0.09, -0.36, 0.15), Point3(0.09, -0.17, 0.27))
        )
        parent.attachNewNode(col_node)

    @property
    def free_cells(self):
        """The number of free cells on this part.

        Returns:
            int: The number of free cells.
        """
        return 2 - len(self.chars)

    def give_cell(self, character):
        """Check if there is a free cell.

        Args:
            character (personage.character.Character):
                Character to move to this part.

        Returns:
            dict: Blank dict with position to move character to.
        """
        if len(self.chars) >= 2:
            return None

        self.chars.append(character)
        return {"pos": (0, 0, 0), "angle": 0}

    def release_cell(self, position, character):
        """Release one cell on this part.

        Args:
            position (dict):
                Position and rotation of the taken cell.
            character (personage.character.Character):
                Character to remove from this part.
        """
        self.chars.remove(character)

    def show_arrow(self):
        """Rest parts doesn't have manipulating arrows."""
        pass

    def hide_arrow(self):
        """Rest parts doesn't have manipulating arrows."""
        pass
