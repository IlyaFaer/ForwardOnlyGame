"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Enemy units API.
"""
import random

from direct.directutil import Mopath
from direct.interval.IntervalGlobal import (
    Func,
    LerpHprInterval,
    LerpPosInterval,
    LerpScaleInterval,
    Parallel,
    Sequence,
    SoundInterval,
    Wait,
)
from direct.interval.MopathInterval import MopathInterval
from panda3d.bullet import BulletBoxShape, BulletRigidBodyNode
from panda3d.core import CollisionBox, CollisionSphere, Point3, Vec3

from const import MOUSE_MASK, SHOT_RANGE_MASK
from utils import address, chance, take_random
from .base_enemy_unit import EnemyUnit
from .shooter import Shooter


class EnemyMotorcyclist(EnemyUnit):
    """Enemy unit on motorcycle base class.

    Includes a motocycle explosion effect and a
    collision node appropriate for any motorcyclist.

    Args:
        id_ (int): Enemy unit id.
        class_ (str): Enemy class name.
        class_data (dict): Enemy class description.
        model (actor.Actor): Enemy character model.
        y_positions (list): Free positions along Y.
        enemy_handler (CollisionHandlerEvent): Enemy collisions handler.
    """

    def __init__(self, id_, class_, class_data, model, y_positions, enemy_handler):
        EnemyUnit.__init__(
            self, id_, class_, class_data, model, y_positions, enemy_handler
        )

        self._col_node = self._init_col_node(
            SHOT_RANGE_MASK, MOUSE_MASK, CollisionSphere(0, 0, 0.05, 0.05)
        )
        base.common_ctrl.traverser.addCollider(  # noqa: F821
            self._col_node, enemy_handler
        )
        self._explosion = base.effects_mgr.explosion(self)  # noqa: F821

    def _explode(self):
        """Play explosion sequence of effects and sounds.

        Also includes explosion physics.
        """
        self._explosion.play()

        self._rb_node = BulletRigidBodyNode(self.id + "_physics")
        self._rb_node.setMass(80)
        self._rb_node.addShape(BulletBoxShape(Vec3(0.005, 0.04, 0.028)))
        self._rb_node.deactivation_enabled = False

        phys_node = self.node.attachNewNode(self._rb_node)  # noqa: F821

        self.model.reparentTo(phys_node)
        self.model.setPos(0, -0.01, -0.025)
        base.world.phys_mgr.attachRigidBody(self._rb_node)  # noqa: F821

        # boom impulse
        angle = self.model.getH(render)  # noqa: F821
        x = 0
        y = 0
        if angle == 0:
            y = random.randint(6500, 8500)
        elif angle == 90:
            x = -random.randint(6500, 8500)
        elif angle == -90:
            x = random.randint(6500, 8500)

        self._rb_node.applyForce(Vec3(x, y, random.randint(1500, 2500)), Point3(0))
        self._rb_node.applyTorque(
            Vec3(
                random.randint(-35, 35),
                random.randint(-35, 35),
                random.randint(-35, 35),
            )
        )


class MotoShooter(EnemyMotorcyclist, Shooter):
    """A shooter-motorcyclist unit.

    Includes character and his transport.

    Args:
        model (actor.Actor): Enemy character model.
        id_ (int): Enemy unit id.
        y_positions (list): Free positions along Y.
        enemy_handler (CollisionHandlerEvent): Enemy collisions handler.
        class_data (dict): Enemy class description.
    """

    def __init__(self, model, id_, y_positions, enemy_handler, class_data):
        EnemyMotorcyclist.__init__(
            self, id_, "Moto Shooter", class_data, model, y_positions, enemy_handler
        )
        Shooter.__init__(self)

        self.damage_range = (2, 4)

        self.model.setPlayRate(0.6, "aim_left")
        self.model.setPlayRate(0.6, "aim_right")

        self.shot_snd = self._set_shoot_snd("smg_shot1")

    @property
    def damage(self):
        """This unit one-time calculated damage.

        Returns:
            float: One-time damage made by this unit.
        """
        return random.uniform(*self.damage_range)

    def _aim(self, back):
        """Aim to the Train when got close enough.

        Args:
            back (bool): Unaim.
        """
        if self._y_pos < 0:
            self.model.play("aim_right")
            pos, h = (0.04, 0.022, 0.057), 35
        else:
            self.model.play("aim_left")
            pos, h = (-0.04, 0.019, 0.058), -35

        if not back:
            self._shoot_anim = self._set_shoot_anim(pos, h, 2)

    def _choose_target(self, task):
        """Choose a character/Train as a target.

        Character will be chosen from the list of
        characters set to the TrainPart, in which
        range this enemy is now.
        """
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
        """Die actions for this shooter.

        Returns:
            bool: True, if this shooter dies for the first time.
        """
        if not Shooter._die(self):
            return False

        EnemyUnit._die(self)

    def _missed_shot(self):
        """Calculate if enemy missed the current shot.

        Returns:
            bool: True if enemy missed, False otherwise.
        """
        if self.current_part.is_covered:
            return chance(50)

        return False

    def capture_train(self):
        """The Train got critical damage - stop near it."""
        EnemyMotorcyclist.capture_train(self)

        self._stop_tasks("_shoot", "_choose_target")

    def clear(self, task=None):
        """Clear all the graphical data of this unit."""
        EnemyUnit.clear(self, task)
        base.sound_mgr.detach_sound(self.shot_snd)  # noqa: F821

        if task is not None:
            return task.done

    def enter_the_part(self, part):
        """Start fighting in the given part.

        Args:
            part (train.part.TrainPart): Train part this enemy entered.
        """
        self.current_part = part
        self._aim(False)

        taskMgr.doMethodLater(  # noqa: F821
            1.5, self._choose_target, self.id + "_choose_target"
        )

    def leave_the_part(self, _):
        """Stop fighting in the current part."""
        self._stop_tasks("_shoot", "_choose_target")

        self.model.setPlayRate(-0.6, "aim_left")
        self.model.setPlayRate(-0.6, "aim_right")

        self._aim(True)

        self.current_part = None
        self._target = None


class BrakeThrower(EnemyMotorcyclist):
    """Brake shoes thrower unit.

    Brakers are trying to slow down the Train, to make
    it easier for other enemy units to deal damage.

    Args:
        model (actor.Actor): Enemy character model.
        id_ (int): Enemy unit id.
        y_positions (list): Free positions along Y.
        enemy_handler (CollisionHandlerEvent): Enemy collisions handler.
        class_data (dict): This unit class description.
    """

    def __init__(self, model, id_, y_positions, enemy_handler, class_data):
        EnemyMotorcyclist.__init__(
            self, id_, "Braker", class_data, model, y_positions, enemy_handler
        )
        self.is_jumping = False
        self._train_captured = False

        brake1 = base.loader.loadModel(address("brake1"))  # noqa: F821
        brake1.reparentTo(self.model)
        brake1.setPos(-0.008, -0.019, 0.02)
        brake1.setP(45)

        brake2 = base.loader.loadModel(address("brake1"))  # noqa: F821
        brake2.reparentTo(self.model)
        brake2.setPos(0.008, -0.019, 0.02)
        brake2.setP(45)

        self._brakes = [brake1, brake2]
        self._jump_int = None

        self._l_mopath = Mopath.Mopath(
            objectToLoad=loader.loadModel(address("l_low_jump"))  # noqa: F821
        )
        self._l_mopath.fFaceForward = True

        self._r_mopath = Mopath.Mopath(
            objectToLoad=loader.loadModel(address("r_low_jump"))  # noqa: F821
        )
        self._r_mopath.fFaceForward = True

        self._jump_snd = base.sound_mgr.loadSfx("sounds/moto_jump.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(self._jump_snd, self.model)  # noqa: F821

        self._fall_snd = base.sound_mgr.loadSfx("sounds/moto_fall.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(self._fall_snd, self.model)  # noqa: F821

    def _drop_brake(self, brake):
        """Drop braking shoes to slow down Train.

        Args:
            brake (panda3d.core.NodePath):
                Brake model to drop.
        """
        brake.wrtReparentTo(base.train.model)  # noqa: F821

        if not base.train.r_brake:  # noqa: F821
            pos = 0.058
            base.train.r_brake = True  # noqa: F821
            side = "r"
        else:
            base.train.l_brake = True  # noqa: F821
            pos = -0.058
            side = "l"

        Sequence(
            Parallel(
                LerpPosInterval(brake, 0.5, (pos, 0.7, 0.025)),
                LerpHprInterval(brake, 0.5, (0, 0, 0)),
            ),
            LerpPosInterval(brake, 0.35, (pos, 0.38, 0.025)),
            Func(base.train.brake, side, brake),  # noqa: F821
        ).start()

    def _jump_and_brake(self, task):
        """Jump over the railway and drop a brake shoe."""
        if not self._brakes or self.current_part is None:
            return task.done

        for char in base.world.enemy.active_units.values():  # noqa: F821
            # if someone is jumping now, don't jump
            if (
                type(char) == BrakeThrower and char.id != self.id and char.is_jumping
            ) or (
                base.train.l_brake and base.train.r_brake  # noqa: F821
            ):
                return task.again

        y_target = round(abs(self._y_pos) - 0.55, 2)
        if self._y_pos < 0:
            y_target = -y_target

        if y_target not in self._y_positions:
            return task.again

        self._y_positions.remove(y_target)

        self.is_jumping = True
        self._stop_tasks("_float_move")
        self._move_int.pause()

        taskMgr.doMethodLater(  # noqa: F821
            0.15, self._jump_snd.play, self.id + "_jump_sound", extraArgs=[]
        )
        taskMgr.doMethodLater(  # noqa: F821
            1.5, self._fall_snd.play, self.id + "_fall_sound", extraArgs=[]
        )
        taskMgr.doMethodLater(  # noqa: F821
            1,
            self._drop_brake,
            self.id + "_drop_brake",
            extraArgs=[take_random(self._brakes)],
        )
        self._jump_int = Sequence(
            MopathInterval(
                self._r_mopath if self._y_pos < 0 else self._l_mopath,
                self.model,
                duration=2.5,
                name=self.id + "_low_jump",
                blendType="easeOut",
            ),
            Func(self._finish_jump),
        )
        self._jump_int.start()

        self._y_positions.append(self._y_pos)
        self._y_pos = y_target

    def _finish_jump(self):
        """Finish the jump sequence and return into the normal mode."""
        self.is_jumping = False
        self.model.wrtReparentTo(render)  # noqa: F821
        self.node.wrtReparentTo(render)  # noqa: F821

        self.node.setPos(self.model.getPos(render))  # noqa: F821

        self.model.wrtReparentTo(self.node)
        self.node.wrtReparentTo(base.train.model)  # noqa: F821

        if not self._train_captured:
            taskMgr.doMethodLater(  # noqa: F821
                2, self._float_move, self.id + "_float_move"
            )

    def capture_train(self):
        """The Train got critical damage - stop near it."""
        self._train_captured = True
        self._stop_tasks("_jump_and_brake")

        EnemyMotorcyclist.capture_train(self)

    def enter_the_part(self, part):
        """Start fighting in the given part.

        Args:
            part (train.part.TrainPart): Train part this enemy entered.
        """
        if not part.name.endswith("_front") or self._train_captured:
            return

        self.current_part = part
        taskMgr.doMethodLater(  # noqa: F821
            15, self._jump_and_brake, self.id + "_jump_and_brake"
        )

    def stop(self):
        """Smoothly stop this unit following the Train."""
        self._stop_tasks("_jump_and_brake")
        EnemyUnit.stop(self)

    def leave_the_part(self, part):
        """Stop fighting in the current part."""
        if part.name.endswith("_front"):
            self.current_part = None

    def clear(self, task=None):
        """Clear all the graphical and sound data of this unit."""
        EnemyUnit.clear(self, task)
        base.sound_mgr.detach_sound(self._jump_snd)  # noqa: F821
        base.sound_mgr.detach_sound(self._fall_snd)  # noqa: F821

        if task is not None:
            return task.done

    def _die(self):
        """Make this enemy die.

        Stop all the braking tasks and jumping interval.
        """
        self._stop_tasks("_jump_and_brake", "_fall_sound", "_drop_brake")

        if self._jump_int is not None:
            self._jump_int.pause()

        EnemyUnit._die(self)


class StunBombThrower(EnemyMotorcyclist):
    """Stun-bomb thrower enemy unit.

    This unit type is dealing damage to the Train with bombs.
    Also this unit can deal damage to characters and deafen
    them. The efficiency of the unit depends on the Train
    speed, so this unit type is synergetic with brakers.

    Args:
        model (actor.Actor): Enemy character model.
        id_ (int): Enemy unit id.
        y_positions (list): Free positions along Y.
        enemy_handler (CollisionHandlerEvent): Enemy collisions handler.
        class_data (dict): This unit class description.
    """

    def __init__(self, model, id_, y_positions, enemy_handler, class_data):
        EnemyMotorcyclist.__init__(
            self, id_, "Bomb Thrower", class_data, model, y_positions, enemy_handler
        )
        self._throw_anim = "throw_" + ("right" if self._y_pos < 0 else "left")

        # prepare a hand bomb model
        self._bomb = loader.loadModel(address("hand_bomb1"))  # noqa: F821
        self._bomb.hide()
        self._bomb.reparentTo(self.model)

        if self._y_pos < 0:
            self._bomb_pos = (0.034, 0.021, 0.068)
        else:
            self._bomb_pos = (-0.037, 0.028, 0.073)

        self._bomb.setPos(*self._bomb_pos)

    def capture_train(self):
        """The Train got critical damage - stop near it."""
        self._stop_tasks("_throw")
        EnemyMotorcyclist.capture_train(self)

    def stop(self):
        """Smoothly stop this unit following the Train."""
        self._stop_tasks("_throw")
        EnemyUnit.stop(self)

    def leave_the_part(self, part):
        """Stop fighting in the current part."""
        self.current_part = None

    def enter_the_part(self, part):
        """Start fighting in the given part.

        Args:
            part (train.part.TrainPart): Train part this enemy entered.
        """
        self.current_part = part
        taskMgr.doMethodLater(5, self._throw, self.id + "_throw")  # noqa: F821

    def _throw(self, task):
        """Throw a bomb towards the Train."""
        self.model.play(self._throw_anim)

        if base.train.ctrl.current_speed > 0.84:  # noqa: F821
            coef = 0
        elif base.train.ctrl.current_speed > 0.67:  # noqa: F821
            coef = 0.15
        else:
            coef = 0.35

        x_coor = 0.09 if self._y_pos > 0 else -0.09
        y_coor = random.uniform(-0.5 + coef, 0 + coef)

        taskMgr.doMethodLater(  # noqa: F821
            2.1, self._move_bomb_to, self.id + "_move_bomb", extraArgs=[x_coor, y_coor]
        )
        taskMgr.doMethodLater(  # noqa: F821
            2.6,
            base.train.explode_bomb,  # noqa: F821
            self.id + "_train_explode_bomb",
            extraArgs=[x_coor, y_coor],
        )
        task.delayTime = 10
        return task.again

    def _move_bomb_to(self, x_coor, y_coor):
        """Move this thrower's bomb to the chosen pos.

        Args:
            x_coor (float): X axis coordinate of explosion.
            y_coor (float): Y axis coordinate of explosion.
        """
        self._bomb.wrtReparentTo(base.train.model)  # noqa: F821
        self._bomb.show()
        LerpPosInterval(self._bomb, 0.4, (x_coor, y_coor, self._bomb.getZ())).start()
        taskMgr.doMethodLater(  # noqa: F821
            0.6, self._return_bomb, self.id + "_return_bomb"
        )

    def _return_bomb(self, task):
        """Return the bomb model back to this unit."""
        self._bomb.hide()
        self._bomb.reparentTo(self.model)
        self._bomb.setPos(self._bomb_pos)
        return task.done

    def _die(self):
        """Make this enemy unit die."""
        if EnemyUnit._die(self):
            self._stop_tasks("_throw", "_train_explode_bomb")

    def clear(self, task=None):
        """Clear all the graphical data of this unit."""
        EnemyUnit.clear(self, task)
        self._bomb.removeNode()

        if task is not None:
            return task.done


class DodgeShooter(EnemyUnit):
    """Dodge with a machine gun unit.

    Represents an enemy unit, which attacks with
    long pauses, but also deals a lot of damage.
    """

    def __init__(self, model, id_, y_positions, enemy_handler, class_data):
        EnemyUnit.__init__(
            self, id_, "Gun Dodge", class_data, model, y_positions, enemy_handler,
        )

        self._col_node = self._init_col_node(
            SHOT_RANGE_MASK,
            MOUSE_MASK,
            CollisionBox(Point3(-0.04, -0.12, -0.02), Point3(0.04, 0.11, 0.06)),
        )
        base.common_ctrl.traverser.addCollider(  # noqa: F821
            self._col_node, enemy_handler
        )
        self._shoot_seq = self._set_shoot_anim()
        self._explosion = base.effects_mgr.explosion_big(self)  # noqa: F821
        self._smoke = base.effects_mgr.burn_smoke(self)  # noqa: F821

    def _set_shoot_anim(self):
        """Prepare machine gun shooting animation for this unit.

        Returns:
            direct.interval.MetaInterval.Sequence:
                Shooting animation and sounds sequence.
        """
        shot_snd = base.sound_mgr.loadSfx(  # noqa: F821
            "sounds/combat/machine_gun_shot1.ogg"
        )
        base.sound_mgr.attachSoundToObject(shot_snd, self.model)  # noqa: F821

        fire = loader.loadModel(address("gun_fire2"))  # noqa: F821
        fire.reparentTo(self.model)
        fire.setScale(1, 0.0001, 1)
        if self._y_pos > 0:
            fire.setPos(-0.055, -0.008, 0.076)
            fire.setH(180)
        else:
            fire.setPos(0.065, -0.008, 0.076)

        shoot_par = Parallel(
            Sequence(
                LerpScaleInterval(fire, 0.07, (1, 1, 1)),
                LerpScaleInterval(fire, 0.07, (1, 0.0001, 1)),
                Wait(0.12),
            ),
            SoundInterval(shot_snd, duration=0.25),
        )
        return Sequence(*(shoot_par,) * 20)

    def capture_train(self):
        """The Train got critical damage - stop near it."""
        EnemyUnit.capture_train(self)

        self._stop_tasks("_shoot_at_train", "_do_damage_to_train", "_stop_doing_damage")

    def enter_the_part(self, part):
        """Start fighting in the given part.

        Args:
            part (train.part.TrainPart): Train part this enemy entered.
        """
        self.current_part = part

        self.model.play("turn_right" if self._y_pos < 0 else "turn_left")

        taskMgr.doMethodLater(  # noqa: F821
            2, self._shoot_at_train, self.id + "_shoot_at_train"
        )

    def leave_the_part(self, _):
        """Stop fighting in the current part."""
        self._stop_tasks("_shoot_at_train", "_do_damage_to_train", "_stop_doing_damage")
        self.current_part = None

    def _shoot_at_train(self, task):
        """Start shooting volley, including logic, animations, sounds."""
        self._shoot_seq.start()
        taskMgr.doMethodLater(  # noqa: F821
            0.5, self._do_damage_to_train, self.id + "_do_damage_to_train"
        )
        taskMgr.doMethodLater(  # noqa: F821
            6,
            taskMgr.remove,  # noqa: F821
            self.id + "_stop_doing_damage",
            extraArgs=[self.id + "_do_damage_to_train"],
        )
        task.delayTime = random.randint(15, 18)
        return task.again

    def _do_damage_to_train(self, task):
        """Deal machine gun damage to the Train."""
        if self.current_part.is_covered:
            if chance(40):
                base.train.get_damage(3)  # noqa: F821
        else:
            base.train.get_damage(3)  # noqa: F821

        return task.again

    def _explode(self):
        """Play explosion sequence of effects and sounds.

        Also includes explosion physics.
        """
        self._explosion.play()
        self._smoke.play()

        self._rb_node = BulletRigidBodyNode(self.id + "_physics")
        self._rb_node.setMass(100)
        self._rb_node.addShape(BulletBoxShape(Vec3(0.06, 0.1, 0.028)))
        self._rb_node.deactivation_enabled = False

        phys_node = self.node.attachNewNode(self._rb_node)  # noqa: F821

        self.model.reparentTo(phys_node)
        self.model.setPos(0, 0, -0.03)
        base.world.phys_mgr.attachRigidBody(self._rb_node)  # noqa: F821

        # boom impulse
        angle = round(self.model.getH(render))  # noqa: F821
        x = 0
        y = 0
        if angle == 0:
            y = random.randint(6500, 8500)
        elif angle == 90:
            x = -random.randint(6500, 8500)
        elif angle == -90:
            x = random.randint(6500, 8500)

        self._rb_node.applyForce(
            Vec3(x, y, random.randint(1500, 2500)), Point3(0, -0.1, 0)
        )
        self._rb_node.applyTorque(
            Vec3(
                random.randint(-30, 30),
                random.randint(-30, 30),
                random.randint(-30, 30),
            )
        )

    def _die(self):
        """Die actions for this shooter.

        Returns:
            bool: True, if this shooter dies for the first time.
        """
        if EnemyUnit._die(self):
            self._shoot_seq.finish()
            self._stop_tasks(
                "_shoot_at_train", "_stop_doing_damage", "_do_damage_to_train"
            )
