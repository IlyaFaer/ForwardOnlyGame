"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Train - the main game object, API.

Includes the systems of Train loading, preparations,
animation, sounds, lights.
"""
import random

from direct.actor.Actor import Actor
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.bullet import BulletBoxShape, BulletCharacterControllerNode
from panda3d.core import PerspectiveLens, PointLight, Spotlight, Vec3

from controls import TrainController
from gui.train import TrainInterface
from train_part import RestPart, TrainPart
from utils import address, take_random


class Train:
    """Train object. The main game object.

    Includes train model, lights, sounds, parts to set
    characters and controller.

    Args:
        description (dict):
            The Train condition description. Used for
            loading a saved Train condition.
    """

    def __init__(self, description=None):
        self.root_node = render.attachNewNode("train_root")  # noqa: F821
        # node to hold camera and Sun
        self.node = self.root_node.attachNewNode("train")

        self.model = Actor(address("locomotive"))
        self.model.reparentTo(self.root_node)

        (
            move_snd,
            stop_snd,
            brake_snd,
            self._clunk_snd,
            self._barrier_hit_snd,
            self._lighter_snd,
            self._creak_snds,
        ) = self._set_sounds()

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

        self._damnability = None

        if description:  # loading params from the last save
            self.damnability = description["damnability"]
            self._miles = description["miles"] - 1
            self.node.setHpr(description["node_angle"])
        else:  # init params
            self.damnability = 1000
            self._miles = -1

        self.l_brake = False
        self.r_brake = False

        self._phys_node = None

        self._is_on_rusty = False
        self._creak_snd_cooldown = False

        self._prepare_particles()

    @property
    def damnability(self):
        """Train damnability.

        Returns:
            int: Current Train damnability.
        """
        return self._damnability

    @damnability.setter
    def damnability(self, value):
        """Set new Train damnability value.

        Args:
            value (int): New value.
        """
        self._damnability = max(0, min(1000, value))
        self._interface.update_indicators(damnability=self.damnability)

    @property
    def description(self):
        """The Train state description for game saving.

        Returns:
            dict: Saveable Train state.
        """
        cond = {
            "damnability": self.damnability,
            "speed": self.ctrl.current_speed,
            "miles": self._miles,
            "node_angle": self.node.getHpr(),
        }
        return cond

    def _prepare_particles(self):
        """
        Prepare the Train particle effects: smoke and
        sparks.
        """
        self._smoke = ParticleEffect()
        self._smoke.loadConfig("effects/smoke1.ptf")
        self._smoke.setPos(0, 0.32, 0.28)
        self._smoke.start(self.model, render)  # noqa: F821

        self._l_brake_sparks = ParticleEffect()
        self._l_brake_sparks.loadConfig("effects/brake_sparks2.ptf")
        self._l_brake_sparks.setPos(-0.058, 0.38, 0.025)

        self._r_brake_sparks = ParticleEffect()
        self._r_brake_sparks.loadConfig("effects/brake_sparks1.ptf")
        self._r_brake_sparks.setPos(0.058, 0.38, 0.025)

        # bomb explosion effects
        self._bomb_explosions = [
            base.effects_mgr.bomb_explosion(self),  # noqa: F821
            base.effects_mgr.bomb_explosion(self),  # noqa: F821
            base.effects_mgr.bomb_explosion(self),  # noqa: F821
        ]

    def set_physics(self, phys_mgr):
        """Set the Train physics.

        Args:
            phys_mgr (panda3d.bullet.BulletWorld):
                Physical world.
        """
        shape = BulletCharacterControllerNode(
            BulletBoxShape(Vec3(0.095, 0.55, 0.1)), 10, "train_shape"
        )
        self._phys_node = self.model.attachNewNode(shape)
        self._phys_node.setZ(0.1)

        phys_mgr.attachCharacter(shape)

        base.taskMgr.doMethodLater(  # noqa: F821
            0.1,
            self._check_contacts,
            "check_train_contacts",
            extraArgs=[phys_mgr, self._phys_node.node()],
            appendTask=True,
        )

    def has_cell(self):
        """Check if there is a free cell for a new unit.

        Returns:
            bool: True, if there is a free cell.
        """
        cells_num = 0
        for part in self.parts.values():
            cells_num += part.free_cells

            if cells_num >= 2:
                return True

        return False

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
                Brake shoe model.
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
        """Slow down the Train to the given speed.

        Args:
            target (float): Target speed.
        """
        self.ctrl.slow_down_to(target)

    def move_to_hangar(self):
        """Move the Train into city hangar."""
        self.root_node.setZ(50)
        self._smoke.disable()

    def _clear_brake(self, side, brake, task):
        """Stop braking on the given side.

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
        """Move the Train along the given world block.

        Args:
            block (world.block.Block):
                The world block to move along.
        """
        self._miles += 1
        self._interface.update_miles(self._miles)

        if block.is_rusty:
            if not self._is_on_rusty:
                self._is_on_rusty = True
                base.taskMgr.doMethodLater(  # noqa: F821
                    1, self._get_rusty_damage, "do_rusty_damage"
                )
        elif self._is_on_rusty:
            self._is_on_rusty = False
            base.taskMgr.remove("do_rusty_damage")  # noqa: F821

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

    def _get_rusty_damage(self, task):
        """Do damage because of rusty rails.

        The Train is getting damage on rusty rails, if
        its speed is higher than 0.7. Damage is indicated
        with a metal creak sound.
        """
        if self.ctrl.current_speed > 0.7:
            self.damnability -= 2

            if not self._creak_snd_cooldown:
                random.choice(self._creak_snds).play()
                self._creak_snd_cooldown = True

                base.taskMgr.doMethodLater(  # noqa: F821
                    7, self._stop_creak_cooldown, "stop_creak_coodown"
                )
        return task.again

    def _stop_creak_cooldown(self, task):
        """Stop metal creak sound cooldown."""
        self._creak_snd_cooldown = False
        return task.done

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

        lighter = Spotlight("train_main_lighter")
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
            (panda3d.core.AudioSound...):
                Train movement, stopping, braking, barrier hit,
                lighter toggle and metal creaking sounds.
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

        hit_snd = base.sound_mgr.loadSfx("sounds/concrete_hit1.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(hit_snd, self.model)  # noqa: F821

        lighter_snd = base.loader.loadSfx("sounds/switcher1.ogg")  # noqa: F821
        lighter_snd.setVolume(0.8)

        creak_snd1 = base.loader.loadSfx("sounds/metal_creak1.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(creak_snd1, self.model)  # noqa: F821

        creak_snd2 = base.loader.loadSfx("sounds/metal_creak2.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(creak_snd2, self.model)  # noqa: F821

        creak_snd3 = base.loader.loadSfx("sounds/metal_creak3.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(creak_snd3, self.model)  # noqa: F821

        return (
            move_snd,
            stop_snd,
            brake_snd,
            clunk_snd,
            hit_snd,
            lighter_snd,
            (creak_snd1, creak_snd2, creak_snd3),
        )

    def update_physics(self):
        """Update the Train physical shape."""
        self._phys_node.setPos((0, 0, 0.1))

    def _check_contacts(self, phys_mgr, phys_node, task):
        """Check Train physical contacts.

        Used to play sounds on physical objects hitting
        and getting damage from barriers.

        Args:
            phys_mgr (panda3d.bullet.BulletWorld):
                Physical world.
            phys_node (panda3d.bullet.BulletCharacterControllerNode):
                Train physical node.
        """
        contacts = phys_mgr.contactTest(phys_node).getContacts()
        if not contacts:
            return task.again

        for contact in contacts:
            if contact.getNode1().getName().startswith("barrier_"):
                self._barrier_hit_snd.play()
                self.get_damage(100)

                task.delayTime = 0.3
                return task.again

        task.delayTime = 0.1
        return task.again

    def toggle_lights(self):
        """Toggle Train lights."""
        self._lighter_snd.play()

        method = render.clearLight if self.lights_on else render.setLight  # noqa: F821
        for light in self._lights:
            method(light)

        self.lights_on = not self.lights_on

    def speed_to_min(self):
        """Accelerate the Train to minimum fight speed."""
        self.ctrl.speed_to_min()

    def get_damage(self, damage):
        """Get damage from an enemy.

        If damage become critical, stop Train.

        Args:
            damage (int): Damage points to get.
        """
        self.damnability -= damage

        if not self.ctrl.critical_damage:
            if self.damnability <= 0:
                self.ctrl.critical_damage = True
                self.ctrl.stop()

                base.world.enemy.capture_train()  # noqa: F821
                base.team.surrender()  # noqa: F821

    def do_effects(self, effects):
        """Do outing effects to the Train.

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

    def explode_bomb(self, x_coor, y_coor):
        """Explode a bomb on the Train.

        Args:
            x_coor (float): X coordinate of explosion.
            y_coor (float): Y coordinate of explosion.
        """
        if not self._bomb_explosions:
            return

        explosion = take_random(self._bomb_explosions)
        explosion.setPos(x_coor, y_coor, 0.155)
        explosion.play()

        base.taskMgr.doMethodLater(  # noqa: F821
            2.55,
            self._bomb_explosions.append,
            "return_bomb_explosion_effect",
            extraArgs=[explosion],
        )
        self.damnability -= 4

        if y_coor < -0.1:  # too far from characters
            return

        for char in self.parts[
            "part_locomotive_left" if x_coor < 0 else "part_locomotive_right"
        ].chars:
            if abs(char.model.getY() - y_coor) < 0.11:
                char.get_damage(3)
                char.get_stunned(5)
