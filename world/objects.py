"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Active world objects API.
"""
import random

from direct.actor.Actor import Actor
from direct.directutil import Mopath
from direct.interval.IntervalGlobal import (
    Func,
    LerpAnimInterval,
    LerpHprInterval,
    LerpPosInterval,
    LerpScaleInterval,
    Parallel,
    Sequence,
    SoundInterval,
    Wait,
)
from direct.interval.MopathInterval import MopathInterval
from direct.particles.ParticleEffect import ParticleEffect
from direct.showbase.Transitions import Transitions
from panda3d.bullet import BulletBoxShape, BulletRigidBodyNode
from panda3d.core import (
    CollisionNode,
    CollisionSphere,
    PerspectiveLens,
    PointLight,
    Spotlight,
    Vec3,
)

from const import MOUSE_MASK, NO_MASK, SHOT_RANGE_MASK
from units.shooter import Shooter
from utils import address, chance, take_random

BARRIER_THRESHOLD = 8
ROCKET_THRESHOLD = 16


class Barrier:
    """Enemy barrier.

    Deals damage to the locomotive on a hit.

    Args:
        block (world.block.Block): Block to set this barrier on.
    """

    def __init__(self, block):
        id_ = "barrier_" + str(random.randint(1, 10000))
        y_coor = random.randint(8, 16)
        self._rb_nodes = []

        self._prepare_physics(
            id_, block, 0.07, y_coor,
        )
        self._prepare_physics(
            id_, block, -0.07, y_coor,
        )

    def _prepare_physics(self, id_, block, x_coor, y_coor):
        """Prepare physics for the given barrier model.

        Args:
            id_ (str): Barrier id. Used as a prefix in rigid body id.
            block (world.block.Block): Block to set barrier on.
            x_coor (float): X coordinate to set block on.
            y_coor (float): Y coordinate to set block on.
        """
        rb_node = BulletRigidBodyNode(id_ + str(x_coor))
        rb_node.setMass(150)
        rb_node.addShape(BulletBoxShape(Vec3(0.05, 0.005, 0.05)))

        phys_np = block.rails_mod.attachNewNode(rb_node)
        phys_np.setPos(x_coor, y_coor, 0.07)
        phys_np.setH(random.randint(-20, 20))
        loader.loadModel(address("barrier1")).reparentTo(phys_np)  # noqa: F821

        base.world.phys_mgr.attachRigidBody(rb_node)  # noqa: F821
        self._rb_nodes.append(rb_node)

    def clear(self):
        """Clear physical shapes."""
        for rb_node in self._rb_nodes:
            base.world.phys_mgr.removeRigidBody(rb_node)  # noqa: F821

        self._rb_nodes.clear()


class Rocket:
    """An enemy rocket object.

    A rocket is overtaking the locomotive
    from behind and making a hit at it.
    """

    def __init__(self):
        x_coor, side = random.choice(((0.553, "left"), (-0.553, "right"), (0, "top")))

        self._model = Actor(address("rocket1"))
        self._model.reparentTo(base.train.model)  # noqa: F821
        self._model.setPos(x_coor, -7, 0.5)

        self._smoke = ParticleEffect()
        self._smoke.loadConfig("effects/smoke_tail.ptf")
        self._smoke.start(self._model, render)  # noqa: F821

        path = Mopath.Mopath(
            objectToLoad=loader.loadModel(  # noqa: F821
                address("rocket_{}_path".format(side))
            )
        )
        path.fFaceForward = True

        self._hiss_snd = base.sound_mgr.loadSfx("sounds/rocket_fly.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(self._hiss_snd, self._model)  # noqa: F821

        self._hiss_snd2 = base.sound_mgr.loadSfx("sounds/rocket_hiss.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(self._hiss_snd2, self._model)  # noqa: F821

        self._hiss_snd.play()
        seq = Sequence(
            LerpPosInterval(
                self._model, 7, (x_coor, -0.627, 0.561), blendType="easeOut"
            ),
            Wait(0.8),
            Parallel(
                SoundInterval(self._hiss_snd2),
                MopathInterval(
                    path, self._model, duration=0.5, name="rocket_current_path"
                ),
            ),
            Func(self._explode, side),
        )
        seq.start()

    def _explode(self, side):
        """Explode the rocket and deal damage to the locomotive.

        Args:
            side (str):
                Locomotive's side where the rocket is exploded.
        """
        self._model.cleanup()
        self._model.removeNode()
        self._smoke.softStop()

        self._hiss_snd.stop()
        base.sound_mgr.detach_sound(self._hiss_snd)  # noqa: F821
        base.sound_mgr.detach_sound(self._hiss_snd2)  # noqa: F821

        base.train.explode_rocket(side)  # noqa: F821
        taskMgr.doMethodLater(  # noqa: F821
            2, self._smoke.disable, "disable_rocket_smoke", extraArgs=[],
        )


class SCPTrain:
    """SCP rival train object."""

    def __init__(self):
        self._positions = [-0.25, -0.07, 0.06, 0.22]
        self._side = random.choice((0.7, -0.7))
        self._glow_step = 0.05
        self._glow_strength = 0.2
        self._move_int = None
        self._ray_step = 0.9
        self._ray_strength = 70
        self._ray_np = None
        self._ray_alpha = 1
        self._suns = []

        self.wave = 1
        self.model = loader.loadModel(address("SCP"))  # noqa: F821
        self.model.reparentTo(base.train.model)  # noqa: F821
        self.model.setX(self._side)

        self._lamp = PointLight("scp_glow")
        self._lamp.setColor((0.39, 0, 0.59, 1))
        self._lamp.setAttenuation(self._glow_strength)
        lamp_np = self.model.attachNewNode(self._lamp)
        lamp_np.setZ(0.2)
        render.setLight(lamp_np)  # noqa: F821

        taskMgr.doMethodLater(0.06, self._glowing_pulse, "scp_glowing")  # noqa: F821
        taskMgr.doMethodLater(  # noqa: F821
            1, self._gen_instances, "generate_instances"
        )

        self._prepare_light_ray()

        taskMgr.doMethodLater(7, self._float_move, "float_move")  # noqa: F821
        for delay, num in (
            (3, 1),
            (3.7, 2),
            (4.1, 3),
            (4.7, 4),
        ):
            taskMgr.doMethodLater(  # noqa: F821
                delay, self._move_suns, "start_suns", extraArgs=[num]
            )

    @property
    def side(self):
        """Side, where the SCP train is located.

        Returns:
            str: The current side letter.
        """
        return "l" if self._side < 0 else "r"

    def _move_suns(self, num):
        """Make the suns move step.

        Args:
            num (int): Num of the step.
        """
        transition = Transitions(loader)  # noqa: F821
        transition.setFadeColor(1, 1, 1)
        transition.fadeOut(0.06)

        factor = -1 if self._side > 0 else 1

        if num == 1:
            for i in range(4):
                self._suns.append(VioletSun(self))
        elif num == 2:
            y_offset = -0.1
            for sun in self._suns:
                sun.model.setPos(
                    random.uniform(0.4, 0.6) * factor,
                    y_offset + random.uniform(-0.1, 0.1),
                    0.4,
                )
                y_offset += 0.1
        elif num == 3:
            y_offset = -0.15
            for sun in self._suns:
                sun.model.setPos(
                    sun.model.getX() + 0.45 * factor,
                    y_offset + random.uniform(-0.1, 0.1),
                    0.4,
                )
                y_offset += 0.15
        elif num == 4:
            y_offset = -0.35
            for sun in self._suns:
                sun.model.setPos(
                    sun.model.getX() + 0.55 * factor,
                    y_offset + random.uniform(-0.1, 0.1),
                    0.05,
                )
                y_offset += 0.22
                sun.model.wrtReparentTo(base.train.model)  # noqa: F821
                sun.approach_train(factor)

        transition.fadeIn(0.03)

    def _prepare_light_ray(self):
        """Prepare the light ray SCP weapon and its effects."""
        lens = PerspectiveLens()
        lens.setNearFar(0, 30)
        lens.setFov(30, 30)

        self._ray = Spotlight("scp_ray")
        self._ray.setColor((0.39, 0, 0.59, 1))
        self._ray.setLens(lens)
        self._ray.setExponent(70)

        self._ray_np = base.train.model.attachNewNode(self._ray)  # noqa: F821
        self._ray_np.setPos(0, 0, -50)
        self._ray_np.setP(-90)
        render.setLight(self._ray_np)  # noqa: F821

        self._volume_ray = loader.loadModel(address("violet_ray"))  # noqa: F821
        self._volume_ray.reparentTo(base.train.model)  # noqa: F821
        self._volume_ray.setBillboardPointWorld()
        self._volume_ray.setDepthWrite(False)
        self._volume_ray.setZ(0.5)
        self._volume_ray.setAlphaScale(0)
        self._volume_ray.hide()

        self._scorch_parts = ParticleEffect()
        self._scorch_parts.loadConfig("effects/scorch.ptf")
        self._scorch_parts.reparentTo(self._ray_np)
        self._scorch_parts.setY(0.6)

        col_node = CollisionNode("light_ray_cn")
        col_node.setIntoCollideMask(NO_MASK)
        col_node.setFromCollideMask(MOUSE_MASK)
        col_node.addSolid(CollisionSphere(0, 0, 0, 0.17))

        base.common_ctrl.traverser.addCollider(  # noqa: F821
            self._scorch_parts.attachNewNode(col_node),
            base.common_ctrl.handler,  # noqa: F821
        )

        base.accept("light_ray_cn-into", self._scorch)  # noqa: F821
        base.accept("light_ray_cn-out", self._stop_scorch)  # noqa: F821
        taskMgr.doMethodLater(10, self._ray_charge, "scp_ray_charge")  # noqa: F821

    def _scorch(self, event):
        """Scorch the Adjutant crew members with the light ray."""
        name = event.getIntoNodePath().getName()
        if name.startswith("character_"):
            char = base.team.chars[name]  # noqa: F821
            taskMgr.doMethodLater(  # noqa: F821
                0.25, char.get_scorch_damage, char.id + "_scorch_damage"
            )

    def _stop_scorch(self, event):
        """Stop scorching process."""
        name = event.getIntoNodePath().getName()
        if name.startswith("character_"):
            taskMgr.remove(base.team.chars[name].id + "_scorch_damage")  # noqa: F821

    def _ray_charge(self, task):
        """Do a light ray attack.

        Represents a scorching ray of light, coming
        from the skies to the Adjutant.
        """
        task.delayTime = 0.07

        if self._ray_np.getZ() == -50:
            y_pos = random.uniform(-0.17, 0.27)
            self._ray_np.setPos(random.uniform(-0.13, 0.13), y_pos, 0.7)

            self._volume_ray.show()
            self._volume_ray.setY(y_pos)

        if self._ray_strength < 0.03:
            self._ray_step = 1.1

        if self._ray_strength < 20:
            self._scorch_parts.start(self._ray_np, render)  # noqa: F821
            self._scorch_parts.softStart()

        if self._ray_strength > 20 and self._ray_step > 1:
            self._scorch_parts.softStop()

        self._ray_strength *= self._ray_step
        self._ray_alpha *= self._ray_step
        self._volume_ray.setAlphaScale(1 - self._ray_alpha)

        if self._ray_strength > 70:
            self._volume_ray.hide()
            self._ray_np.setZ(-50)
            self._ray_step = 0.9
            self._ray_strength = 70
            taskMgr.doMethodLater(10, self._ray_charge, "scp_ray_inc")  # noqa: F821
            return task.done

        self._ray.setExponent(self._ray_strength)
        return task.again

    def _gen_instances(self, task):
        """Generate enemy instances.

        Enemy instances are copies of the Adjutant crew members.
        """
        num_insts = 0
        delay = 0.5
        for num, char in enumerate(base.team.chars.values()):  # noqa: F821
            taskMgr.doMethodLater(  # noqa: F821
                delay,
                base.world.enemy.prepare_scp_instance,  # noqa: F821
                str(num) + "_scp_instance",
                extraArgs=[self, self._positions, char, num],
            )
            delay += random.uniform(0.5, 1.2)
            num_insts += 1
            if num_insts == 4:
                break

        return task.done

    def _float_move(self, task):
        """Make enemy floatly move along the Train."""
        self._move(random.randint(2, 4), (self._side, random.uniform(-0.2, 0.2), 0))
        task.delayTime = random.randint(4, 5)
        return task.again

    def _move(self, period, new_pos):
        """Run a new movement interval with the given parameters.

        Args:
            period (tuple): Interval duration bounds.
            new_pos (tuple): New enemy position.
        """
        if self._move_int is not None:
            self._move_int.pause()

        self._move_int = LerpPosInterval(
            self.model, period, new_pos, blendType="easeInOut"
        )
        self._move_int.start()

    def _glowing_pulse(self, task):
        """Play SCP train glow pulsating effect."""
        self._glow_strength += self._glow_step
        self._glow_strength = round(self._glow_strength, 2)

        self._lamp.setAttenuation(self._glow_strength)

        if self._glow_strength in (0.2, 1.3):
            self._glow_step *= -1

        return task.again

    def next_wave(self):
        """Start the next wave of SCP train and instances attack."""
        self.wave += 1
        self._positions = [-0.25, -0.07, 0.06, 0.22]
        self._side *= -1

        if self._move_int is not None:
            self._move_int.pause()

        self.model.setX(self._side)

        taskMgr.doMethodLater(  # noqa: F821
            1, self._gen_instances, "generate_instances"
        )

    def move_ray(self, diff, task):
        """Move the light ray along the Adjutant.

        Args:
            diff (float): Direction where to move the light ray.
        """
        if self._ray_np.getZ() != -50:
            y_pos = self._ray_np.getY() + diff
            self._ray_np.setY(y_pos)
            self._volume_ray.setY(y_pos)

        return task.again


class SCPInstance(Shooter):
    """An SCP instance.

    An enemy unit appearing on SCP train. Represents
    a copy of one of the Adjutant crew members.

    Args:
        class_data (dict):
            Description of a class of the unit, whose copy this
            SCP instance must be.
        class_ (str): The original unit class name.
        sex (str): The original unit sex.
        scp_train (world.objects.SCPTrain): The SCP train object.
        index (int): The instance number.
        enemy_handler (panda3d.core.CollisionHandlerEvent):
            Enemy units collisions handler.
    """

    def __init__(
        self, class_data, class_, sex, positions, scp_train, index, enemy_handler
    ):
        self._scp_train = scp_train
        self.id = "scp_instance_" + str(index)
        self.is_dead = False
        self.health = class_data["health"]

        Shooter.__init__(self)

        animations = {
            name: address(class_ + "-" + name) for name in ("die", "stand_and_aim")
        }

        self.model = Actor(address(sex + "_" + class_), animations)
        self.model.reparentTo(scp_train.model)
        self.model.enableBlend()
        self.model.setControlEffect("stand_and_aim", 1)
        self.model.loop("stand_and_aim")

        self._particles = ParticleEffect()
        self._particles.loadConfig(
            "effects/instance_appear_{}.ptf".format(self._scp_train.side)
        )
        self._particles.start(self.model, render)  # noqa: F821
        taskMgr.doMethodLater(  # noqa: F821
            1.7, self._particles.disable, self.id + "_stop_appearing", extraArgs=[]
        )

        self._target = None
        self.node = self.model.attachNewNode("np_" + self.id)
        self.shot_snd = self._set_shoot_snd(class_data["shot_snd"])

        self._col_node = self._init_col_node(
            SHOT_RANGE_MASK, MOUSE_MASK, CollisionSphere(0, 0, 0.05, 0.05)
        )
        base.common_ctrl.traverser.addCollider(  # noqa: F821
            self._col_node, enemy_handler
        )

        if class_ == "soldier":
            z = 0.064 if sex == "male" else 0.062
        elif class_ == "raider":
            z = 0.047
        elif class_ == "anarchist":
            z = 0.06 if sex == "male" else 0.057

        self._shoot_anim = self._set_shoot_anim(
            (0.004, 0.045, z), 97, class_data["shots_num"]
        )

        y_pos = take_random(positions)
        self.model.setPos(
            -0.065 if scp_train.side == "r" else 0.065, y_pos, 0.09,  # noqa: F821
        )
        if scp_train.side == "r":
            self.model.setH(90)
            self.current_part = base.train.parts["part_right"]  # noqa: F821
        else:
            self.model.setH(-90)
            self.current_part = base.train.parts["part_left"]  # noqa: F821

        self.current_part.enemies.append(self)

        taskMgr.doMethodLater(  # noqa: F821
            1.5, self._choose_target, self.id + "_choose_target"
        )

    @property
    def damage(self):
        """Damage amount for one shot."""
        return random.choice((2, 3))

    @property
    def shooting_speed(self):
        """Pause between shots."""
        return 1.7 + random.uniform(0.1, 0.9)

    def _choose_target(self, task):
        """Choose a target to shoot."""
        if self.current_part.is_covered:
            if self._target != base.train:  # noqa: F821
                self._target = base.train  # noqa: F821

                # (re-)start shooting
                self._stop_tasks("_shoot")
                taskMgr.doMethodLater(  # noqa: F821
                    0.5, self._shoot, self.id + "_shoot"
                )
        else:
            targets = self.current_part.chars + [base.train]  # noqa: F821

            if self._target not in targets or chance(5):
                self._target = random.choice(targets)

                # (re-)start shooting
                self._stop_tasks("_shoot")
                taskMgr.doMethodLater(  # noqa: F821
                    0.5, self._shoot, self.id + "_shoot"
                )

        task.delayTime = 0.5
        return task.again

    def _die(self):
        """Instance death sequence.

        Stop all the character's tasks, play death animation
        and plan the character object clearing.
        """
        if not Shooter._die(self):
            return False

        self.is_dead = True
        base.common_ctrl.traverser.removeCollider(self._col_node)  # noqa: F821
        self._col_node.removeNode()

        taskMgr.doMethodLater(  # noqa: F821
            self.clear_delay, self.clear, self.id + "_clear"
        )

        LerpAnimInterval(self.model, 0.1, "stand_and_aim", "die").start()
        self.model.play("die")

        taskMgr.doMethodLater(3, self._hide, self.id + "_hide")  # noqa: F821

    def _hide(self, task):
        """Hide the main model."""
        self.model.hide()
        return task.done

    def _init_col_node(self, from_mask, into_mask, solid):
        """Initialize this instance collision node.

        Args:
            from_mask (panda3d.core.BitMask_uint32_t_32):
                FROM collision mask.
            into_mask (panda3d.core.BitMask_uint32_t_32):
                INTO collision mask.
            solid (panda3d.core.CollisionSolid):
                Collision solid for this unit.
        """
        col_node = CollisionNode(self.id)
        col_node.setFromCollideMask(from_mask)
        col_node.setIntoCollideMask(into_mask)
        col_node.addSolid(solid)
        return self.model.attachNewNode(col_node)

    def _missed_shot(self):
        """Chance of the instance shot missed."""
        return chance(20)

    def _stop_tasks(self, *names):
        """Stop this instance related tasks.

        Args:
            names (tuple): Tasks' names to stop.
        """
        for name in names:
            taskMgr.remove(self.id + name)  # noqa: F821

    def get_damage(self, damage):
        """Getting damage.

        Start dying if needed.

        Args:
            damage (int): Damage points to get.
        """
        self.health -= damage
        if self.health <= 0:
            self._die()

    @property
    def clear_delay(self):
        """
        Delay between this instance death and clearing the
        instance object.

        Returns:
            float: Seconds to wait before clearing.
        """
        return 3.5

    def clear(self, task):
        """Clear this instance.

        Release models and sounds memory, release the part
        cell and delete the instance from the instances list.
        """
        self.model.cleanup()
        self.model.removeNode()
        base.sound_mgr.detach_sound(self.shot_snd)  # noqa: F821
        self.current_part.enemies.remove(self)

        if not self.current_part.enemies:
            self._scp_train.next_wave()

        return task.done


class VioletSun:
    """A single violet sun, coming from the SCP train.

    Args:
        scp_train (world.object.SCPTrain): The SCP train object.
    """

    def __init__(self, scp_train):
        self._scp_train = scp_train
        self._sides = {"l": "left", "r": "right"}

        self.model = loader.loadModel(address("violet_sun"))  # noqa: F821
        self.model.reparentTo(scp_train.model)  # noqa: F821
        self.model.setZ(0.3)

    def _explode(self):
        """Explode the sun, doing damage to the Adjutant."""
        base.train.explode_rocket(self._sides[self._scp_train.side])  # noqa: F821
        Sequence(
            LerpScaleInterval(self.model, 0.05, (0, 0, 0)), Func(self.model.removeNode),
        ).start()

    def approach_train(self, factor):
        """Make the sun approach the Adjutant.

        Args:
            factor (int):
                X-coordinate factor to set the sun on the
                correct side of the Adjutant.
        """
        length = random.randint(18, 25)
        Sequence(
            Parallel(
                LerpHprInterval(
                    self.model,
                    length,
                    (
                        random.randint(0, 360),
                        random.randint(0, 360),
                        random.randint(0, 360),
                    ),
                    blendType="easeInOut",
                ),
                LerpPosInterval(
                    self.model,
                    length,
                    (0.09 * factor, random.uniform(-0.05, 0.15), 0.17),
                ),
            ),
            Func(self._explode),
        ).start()
