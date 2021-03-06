"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Train - the main game object, API.

Includes the systems of the Train loading, preparations,
animation, sounds, lights, physics, upgrades.
"""
import copy
import random

from direct.actor.Actor import Actor
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.bullet import BulletBoxShape, BulletCharacterControllerNode
from panda3d.core import PerspectiveLens, PointLight, Spotlight, Vec3

from controls import TrainController
from gui.train import TrainGUI
from train_part import RestPart, TrainPart
from utils import address, take_random
from world.objects import ArmorPlate

UPGRADES = {
    "Ram": {
        "name": "Ram",
        "desc": """With this ram your locomotive
will be breaking road barriers
without getting damage""",
        "cost": "300$",
        "model": "ram1",
    },
    "Floodlights": {
        "name": "Floodlights",
        "desc": """All the negative darkness
factors are no more actual with
these floodlights on""",
        "cost": "400$",
        "model": "floodlights1",
    },
    "Armor Plate": {
        "name": "Armor Plate",
        "desc": """An active shield which can
cover one of the Train parts.
Use 5, 6, 7 keys to move it.""",
        "cost": "70$",
        "model": "armor_plate",
    },
}


class Train:
    """The Train object - the main game object.

    Includes train model, lights, sounds, parts to set
    characters, controller, upgrades and physics.

    Args:
        description (dict):
            Optional. The Train condition description.
            Used for loading a saved Train condition.
    """

    def __init__(self, description=None):
        self.root_node = render.attachNewNode("train_root")  # noqa: F821
        # node to hold camera and Sun
        self.node = self.root_node.attachNewNode("train")

        self.model = Actor(address("locomotive"))
        self.model.reparentTo(self.root_node)

        (
            self._clunk_snd,
            self._clunk2_snd,
            self._filter_open_snd,
            self._barrier_hit_snd,
            self._lighter_snd,
            self._creak_snds,
        ) = self._set_sounds()

        self.ctrl = TrainController(self.model)
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

        self._gui = TrainGUI()

        self._damnability = None

        if description:  # loading params from the last save
            self.damnability = description["damnability"]
            self._miles = description["miles"] - 1
            self.node.setHpr(description["node_angle"])
        else:  # new game params
            self.damnability = 1000
            self._miles = -1

        self.l_brake = False
        self.r_brake = False
        self._is_on_rusty = False
        self._creak_snd_cooldown = False
        self._phys_node = None
        self._train_phys_shape = None
        self._upgrades = []
        self._pre_upgrade = None
        self._floodlights_mat = None
        self._upgrade_highlight = 1
        self._highlight_step = 0.03

        (
            self._smoke,
            self._l_brake_sparks,
            self._r_brake_sparks,
            self._bomb_explosions,
        ) = self._prepare_particles()

        self.smoke_filtered = False
        self._smoke_filter = Actor(address("smoke_filter"))
        self._smoke_filter.hide()
        self._smoke_filter.reparentTo(self.model)
        self._smoke_filter.pose("open", 1)

    @property
    def damnability(self):
        """The Train damnability points.

        Returns:
            int: Current Train damnability.
        """
        return self._damnability

    @damnability.setter
    def damnability(self, value):
        """Set new Train damnability value.

        Updates the damnability GUI.

        Args:
            value (int): New value.
        """
        self._damnability = max(0, min(1000, value))
        self._gui.update_indicators(damnability=self.damnability)

    @property
    def description(self):
        """The Train state description for game saving.

        Returns:
            dict: Saveable Train state description.
        """
        return {
            "damnability": self.damnability,
            "speed": self.ctrl.current_speed,
            "miles": self._miles,
            "node_angle": self.node.getHpr(),
            "upgrades": self.upgrades,
        }

    @property
    def possible_upgrades(self):
        """
        Return the index of the upgrades, which
        can be currently installed on the Train.

        Returns:
            dict: Possible upgrades index.
        """
        ups = copy.deepcopy(UPGRADES)
        for upgrade in self.upgrades:
            ups.pop(upgrade)

        return ups

    @property
    def upgrades(self):
        """The currently installed upgrades.

        Returns:
            list: Ids of the installed upgrades.
        """
        return self._upgrades

    def _clear_brake(self, side, brake):
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

    def _prepare_particles(self):
        """
        Prepare the Train particle effects: smoke,
        sparks and explosions.

        Returns:
            (direct.particles.ParticleEffect.ParticleEffect...):
                Particle effects for the Train.
        """
        smoke = ParticleEffect()
        smoke.loadConfig("effects/smoke1.ptf")
        smoke.setPos(0, 0.32, 0.29)
        smoke.start(self.model, render)  # noqa: F821

        l_brake_sparks = ParticleEffect()
        l_brake_sparks.loadConfig("effects/brake_sparks2.ptf")
        l_brake_sparks.setPos(-0.058, 0.38, 0.025)

        r_brake_sparks = ParticleEffect()
        r_brake_sparks.loadConfig("effects/brake_sparks1.ptf")
        r_brake_sparks.setPos(0.058, 0.38, 0.025)

        # bomb explosion effects
        bomb_explosions = [
            base.effects_mgr.bomb_explosion(self),  # noqa: F821
            base.effects_mgr.bomb_explosion(self),  # noqa: F821
            base.effects_mgr.bomb_explosion(self),  # noqa: F821
        ]
        return smoke, l_brake_sparks, r_brake_sparks, bomb_explosions

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

    def load_upgrades(self, upgrades):
        """Load the Train upgrades saved earlier.

        Args:
            upgrades (list): Names of the upgrades to load.
        """
        for up in upgrades:
            self.install_upgrade(UPGRADES[up])

    def set_physics(self, phys_mgr):
        """Set the Train physics.

        Args:
            phys_mgr (panda3d.bullet.BulletWorld):
                Physical world.
        """
        self._train_phys_shape = BulletCharacterControllerNode(
            BulletBoxShape(Vec3(0.095, 0.55, 0.1)), 10, "train_shape"
        )
        self._phys_node = self.model.attachNewNode(self._train_phys_shape)
        self._phys_node.setZ(0.1)

        phys_mgr.attachCharacter(self._train_phys_shape)

        taskMgr.doMethodLater(  # noqa: F821
            0.1,
            self._check_contacts,
            "check_train_contacts",
            extraArgs=[phys_mgr, self._phys_node.node()],
            appendTask=True,
        )

    def place_recruit(self, char):
        """Place the new recruit somewhere on the Train.

        Args:
            char (personage.character.Character):
                New recruit object.
        """
        for part in self.parts.values():
            if part.free_cells > 0:
                char.move_to(part)
                return

    def brake(self, side, brake):
        """Start braking on the given side.

        Args:
            side (str): Side label: 'l' or 'r'.
            brake (panda3d.core.NodePath):
                Brake shoe model.
        """
        self._clunk_snd.play()

        sparks = self._l_brake_sparks if side == "l" else self._r_brake_sparks
        sparks.start(self.model, self.model)
        sparks.softStart()

        taskMgr.doMethodLater(  # noqa: F821
            30, self._clear_brake, side + "_clear_brake", extraArgs=[side, brake],
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
        """Move the Train into a city hangar."""
        self.root_node.setZ(50)
        self._smoke.disable()

    def move_along_block(self, block):
        """Move the Train along the given world block.

        Args:
            block (world.block.Block):
                The world block to move along.
        """
        self._miles += 1
        self._gui.update_miles(self._miles)

        if block.is_rusty:
            if not self._is_on_rusty:
                self._is_on_rusty = True
                taskMgr.doMethodLater(  # noqa: F821
                    1, self._get_rusty_damage, "do_rusty_damage"
                )
        elif self._is_on_rusty:
            self._is_on_rusty = False
            taskMgr.remove("do_rusty_damage")  # noqa: F821

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

                taskMgr.doMethodLater(  # noqa: F821
                    7, self._stop_creak_cooldown, "stop_creak_coodown"
                )
        return task.again

    def _stop_creak_cooldown(self, task):
        """Stop metal creak sound cooldown."""
        self._creak_snd_cooldown = False
        return task.done

    def _set_lights(self):
        """Configure the Train lights.

        Sets the main Train lighter and lights above
        the doors.

        Returns:
            list: NodePath's of the Train lights.
        """
        lens = PerspectiveLens()
        lens.setNearFar(0, 50)
        lens.setFov(60, 60)

        floodlight = Spotlight("train_main_lighter")
        floodlight.setColor((0.5, 0.5, 0.5, 1))
        floodlight.setLens(lens)
        floodlight.setExponent(0.4)
        floodlight_np = self.model.attachNewNode(floodlight)
        floodlight_np.setPos(0, 0.34, 50)
        render.setLight(floodlight_np)  # noqa: F821

        train_lights = [floodlight_np]

        for name, coors in (
            ("train_right_door_light", (0.073, -0.17, 50)),
            ("train_left_door_light", (-0.073, -0.17, 50)),
            ("train_back_door_light", (0, -0.63, 50)),
        ):
            lamp = PointLight(name)
            lamp.setColor((0.89, 0.81, 0.55, 1))
            lamp.setAttenuation(3)
            lamp_np = self.model.attachNewNode(lamp)
            lamp_np.setPos(*coors)
            render.setLight(lamp_np)  # noqa: F821

            train_lights.append(lamp_np)

        return train_lights

    def _set_sounds(self):
        """Configure the Train sounds.

        Returns:
            (panda3d.core.AudioSound...):
                The Train sounds.
        """
        clunk_snd = base.sound_mgr.loadSfx("sounds/metal_clunk1.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(clunk_snd, self.model)  # noqa: F821

        clunk_snd2 = base.sound_mgr.loadSfx("sounds/metal_clunk2.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(clunk_snd2, self.model)  # noqa: F821

        filter_open_snd = base.sound_mgr.loadSfx("sounds/filter_open.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(filter_open_snd, self.model)  # noqa: F821

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
            clunk_snd,
            clunk_snd2,
            filter_open_snd,
            hit_snd,
            lighter_snd,
            (creak_snd1, creak_snd2, creak_snd3),
        )

    def update_physics(self, y_coor):
        """Update the Train physical shape.

        Args:
            y_coor (float):
                Y coordinate for the main
                Train physical shape
        """
        self._phys_node.setPos(0, y_coor, 0.1)

    def _check_contacts(self, phys_mgr, phys_node, task):
        """Check the Train physical contacts.

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
                if "Ram" not in self._upgrades:
                    self.get_damage(100)

                task.delayTime = 0.3
                return task.again

        task.delayTime = 0.1
        return task.again

    def _set_lamps_material(self, mat):
        """Set the Train lamps emission parameter.

        Used when toggling the lights.

        Args:
            mat (tuple): New lamps material.
        """
        self.model.findMaterial("lamp_glass").setEmission(mat)

        if self._floodlights_mat is not None:
            self._floodlights_mat.setEmission(mat)

    def toggle_lights(self):
        """Toggle the Train lights."""
        self._lighter_snd.play()

        if self.lights_on:
            for light in self._lights:
                light.setZ(50)

            self._set_lamps_material((0, 0, 0, 1))
        else:
            self._lights[0].setZ(0.3)
            for light in self._lights[1:]:
                light.setZ(0.245)

            self._set_lamps_material((0.85, 0.85, 0.85, 1))

        self.lights_on = not self.lights_on

    def get_damage(self, damage):
        """Get damage from an enemy.

        If damage become critical, stop Train.

        Args:
            damage (int): Damage points to get.
        """
        self.damnability -= damage

        if self.ctrl.critical_damage:
            return

        if self.damnability == 0:
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
                self._gui.update_indicators(**{key: getattr(self, key)})

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

        taskMgr.doMethodLater(  # noqa: F821
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

    def use_smoke_filter(self):
        """Use smoke filter to hide from enemies.

        Uses single smoke filter resource.
        """
        if not base.smoke_filters or self.smoke_filtered:  # noqa: F821
            return

        self.smoke_filtered = True
        base.smoke_filters -= 1  # noqa: F821

        taskMgr.doMethodLater(  # noqa: F821
            1, self._smoke.softStop, "filter_smoke", extraArgs=[], appendTask=False
        )
        taskMgr.doMethodLater(  # noqa: F821
            1.6, self._clunk2_snd.play, "close_filter", extraArgs=[], appendTask=False
        )
        taskMgr.doMethodLater(  # noqa: F821
            300, self._stop_filtering_smoke, "stop_filter_smoke",
        )
        self._smoke_filter.setPlayRate(-1, "open")
        self._smoke_filter.show()
        self._smoke_filter.play("open")

    def _stop_filtering_smoke(self, task):
        """Stop filtering the Train smoke and hide filter."""
        self._smoke.softStart()
        self._smoke_filter.setPlayRate(1, "open")
        self._smoke_filter.play("open")

        self._filter_open_snd.play()

        taskMgr.doMethodLater(  # noqa: F821
            2.5,
            self._smoke_filter.hide,
            "hide_smoke_filter",
            extraArgs=[],
            appendTask=False,
        )
        self.smoke_filtered = False
        return task.done

    def install_upgrade(self, upgrade):
        """Install the given upgrade on to the Train.

        Args:
            upgrade (dict): The upgrade description.
        """
        self._upgrades.append(upgrade["name"])

        if upgrade["name"] == "Armor Plate":
            ArmorPlate(self.model)
            return

        up_model = loader.loadModel(address(upgrade["model"]))  # noqa: F821
        up_model.reparentTo(self.model)

        if upgrade["name"] == "Ram":
            taskMgr.remove("update_physics")  # noqa: F821
            taskMgr.remove("check_train_contacts")  # noqa: F821

            base.world.phys_mgr.removeCharacter(self._train_phys_shape)  # noqa: F821
            self._phys_node.removeNode()

            self._train_phys_shape = (
                self._train_phys_shape
            ) = BulletCharacterControllerNode(
                BulletBoxShape(Vec3(0.095, 0.58, 0.1)), 10, "train_shape"
            )

            self._phys_node = self.model.attachNewNode(self._train_phys_shape)
            self._phys_node.setPos(0, 0.03, 0.1)

            base.world.phys_mgr.attachCharacter(self._train_phys_shape)  # noqa: F821

            taskMgr.add(  # noqa: F821
                base.world.update_physics,  # noqa: F821
                "update_physics",
                extraArgs=[0.03],
                appendTask=True,
            )
            taskMgr.doMethodLater(  # noqa: F821
                0.1,
                self._check_contacts,
                "check_train_contacts",
                extraArgs=[base.world.phys_mgr, self._phys_node.node()],  # noqa: F821
                appendTask=True,
            )
            return

        if upgrade["name"] == "Floodlights":
            self._floodlights_mat = up_model.findMaterial("lamp_glass")

            self._lights[0].node().setColor((1, 1, 1, 1))

            for light in self._lights[1:]:
                light.node().setAttenuation(1.7)

    def cover_part(self, part):
        """Cover the given Train part with the armor plate.

        Args:
            part (TrainPart): The Train part to cover.
        """
        self.parts[part].is_covered = True

    def uncover_part(self, side):
        """Uncover the given side of the Train with the armor plate.

        Args:
            side (str): The Train side to incover.
        """
        for part in self.parts.values():
            if side in part.name:
                part.is_covered = False
                break

    def preview_upgrade(self, model):
        """Preview the given upgrade model on the Train.

        Used when buying upgrades in a city.

        Args:
            model (panda3d.core.NodePath): The upgrade model.
        """
        self.clear_upgrade_preview()

        self._pre_upgrade = loader.loadModel(address(model))  # noqa: F821
        self._pre_upgrade.reparentTo(self.model)

        taskMgr.doMethodLater(  # noqa: F821
            0.05, self._highlight_upgrade, "highlight_upgrade"
        )

    def clear_upgrade_preview(self):
        """Stop previewing the currently previewed upgrade."""
        if self._pre_upgrade is not None:
            taskMgr.remove("highlight_upgrade")  # noqa: F821
            self._pre_upgrade.removeNode()
            self._pre_upgrade = None

    def _highlight_upgrade(self, task):
        """Highlight the currently preview upgrade.

        Includes color pulsating of the upgrade model.
        """
        if self._upgrade_highlight >= 1.3:
            self._highlight_step = -0.02

        if self._upgrade_highlight <= 1:
            self._highlight_step = 0.02

        self._upgrade_highlight += self._highlight_step

        self._pre_upgrade.setColorScale(
            self._upgrade_highlight, self._upgrade_highlight, self._upgrade_highlight, 1
        )
        return task.again
