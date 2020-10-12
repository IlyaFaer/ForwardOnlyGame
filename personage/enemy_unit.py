"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Enemy unit API.
"""
import random

from direct.directutil import Mopath
from direct.interval.IntervalGlobal import (
    Func,
    LerpHprInterval,
    LerpPosInterval,
    Parallel,
    Sequence,
)
from direct.interval.MopathInterval import MopathInterval
from panda3d.bullet import BulletBoxShape, BulletRigidBodyNode
from panda3d.core import CollisionSphere, Point3, Vec3

from const import MOUSE_MASK, SHOT_RANGE_MASK
from utils import chance, address
from .shooter import Shooter
from .unit import Unit
from utils import take_random


class EnemyUnit(Unit):
    """Base class of enemy units.

    Args:
        id_ (int): Enemy unit id.
        class_ (str): Enemy class name.
        class_data (dict): Enemy class description.
        model (actor.Actor): Enemy character model.
        y_positions (list): Free positions along Y.
        enemy_handler (CollisionHandlerEvent): Enemy collisions handler.
    """

    def __init__(self, id_, class_, class_data, model, y_positions, enemy_handler):
        Unit.__init__(self, "enemy_" + str(id_), class_, class_data)

        self.transport_snd = None
        self._move_int = None
        self._tooltip = "Skinhead - " + self.class_

        self._y_positions = y_positions
        self._y_pos = take_random(self._y_positions)

        self._x_range = (-0.3, 0.4) if self.class_data["part"] == "side" else (0.6, 1.3)

        self.node = render.attachNewNode(self.id + "_node")  # noqa: F821
        self.node.setPos(self._io_dist, -7, 0)

        self.model = model
        self.model.pose("ride", 1)
        self.model.reparentTo(self.node)

        self._col_node = self._init_col_node(
            SHOT_RANGE_MASK, MOUSE_MASK, CollisionSphere(0, 0, 0.05, 0.05)
        )
        base.common_ctrl.traverser.addCollider(  # noqa: F821
            self._col_node, enemy_handler
        )
        self._explosion = base.effects_mgr.explosion(self)  # noqa: F821

        # organize movement and aiming tasks
        time_to_overtake = random.randint(33, 50)

        self._move(time_to_overtake, (self._y_pos, random.uniform(*self._x_range), 0))
        base.taskMgr.doMethodLater(  # noqa: F821
            time_to_overtake + 2, self._float_move, self.id + "_float_move"
        )

    @property
    def _io_dist(self):
        """Enemy Y-distance for approach and back off."""
        if self._y_pos > 0:
            return self._y_pos + 0.45
        return self._y_pos - 0.45

    @property
    def tooltip(self):
        """Tooltip to show on mouse pointing to this enemy.

        Returns:
            str: This unit fraction and class.
        """
        return self._tooltip

    @property
    def shooting_speed(self):
        """Delay between shots of this unit.

        Returns:
            float: Delay between shots in seconds.
        """
        return 1.7 + random.uniform(0.1, 0.9)

    @property
    def clear_delay(self):
        """Delay between this character's death and clearing.

        Returns:
            int: Seconds to hold the unit before delete.
        """
        return 15

    def _move(self, period, new_pos):
        """Run a new movement interval with the given parameters.

        Args:
            period (tuple): Interval duration bounds.
            new_pos (tuple): New enemy position.
        """
        if self._move_int is not None:
            self._move_int.pause()

        self._move_int = LerpPosInterval(
            self.node, period, new_pos, blendType="easeInOut"
        )
        self._move_int.start()

    def _float_move(self, task):
        """Make enemy floatly move along Train."""
        if chance(80):
            shift = random.choice((-0.05, 0.05))
            if self._y_pos + shift in self._y_positions:
                self._y_positions.append(self._y_pos)
                self._y_pos = self._y_pos + shift
                self._y_positions.remove(self._y_pos)

        self._move(
            random.randint(3, 6), (self._y_pos, random.uniform(*self._x_range), 0)
        )
        task.delayTime = random.randint(7, 9)
        return task.again

    def get_damage(self, damage):
        """Take damage points and change model color.

        Args:
            damage (int): Damage points to get.
        """
        Unit.get_damage(self, damage)
        self.model.setColorScale(self.model.getColorScale()[0] + 0.018, 1, 1, 1)

    def _die(self):
        """Make this enemy die.

        Play death sequence of movements and sounds,
        stop all the tasks for this enemy, plan clearing.

        Returns:
            bool: True, if enemy dies in the first time.
        """
        if not Unit._die(self):
            return False

        self.model.setColorScale(1, 1, 1, 1)
        self._stop_tasks("_float_move")
        self._move_int.pause()

        self.model.play("die")
        if self.id in base.world.enemy.active_units:  # noqa: F821
            base.world.enemy.active_units.pop(self.id)  # noqa: F821
            if self.current_part:
                self.current_part.enemies.remove(self)

        self._explode()
        self._y_positions.append(self._y_pos)

    def _explode(self):
        """Set physics for this enemy and explode."""
        self._explosion.play()

        rb_node = BulletRigidBodyNode(self.id + "_physics")
        rb_node.setMass(80)
        rb_node.addShape(BulletBoxShape(Vec3(0.005, 0.04, 0.028)))
        phys_node = self.node.attachNewNode(rb_node)  # noqa: F821

        self.model.reparentTo(phys_node)
        self.model.setPos(0, -0.01, -0.025)
        base.world.phys_mgr.attachRigidBody(rb_node)  # noqa: F821

        # boom impulse
        angle = self.model.getH(render)  # noqa: F821
        x = 0
        y = 0
        if angle == 0:
            y = random.randint(6000, 8000)
        elif angle == 90:
            x = -random.randint(6000, 8000)
        elif angle == -90:
            x = random.randint(6000, 8000)

        rb_node.applyForce(Vec3(x, y, random.randint(1500, 2500)), Point3(0))
        rb_node.applyTorque(
            Vec3(
                random.randint(-45, 45),
                random.randint(-45, 45),
                random.randint(-45, 45),
            )
        )

    def stop(self):
        """Smoothly stop this unit following Train."""
        self._stop_tasks("_float_move")
        self._move(random.randint(9, 11), (self._io_dist, -7, 0))
        self._y_positions.append(self._y_pos)

    def stop_ride(self):
        """Stop riding actions."""
        self.transport_snd.stop()

    def clear(self, task=None):
        """Clear all the graphical data of this unit."""
        base.sound_mgr.detach_sound(self.transport_snd)  # noqa: F821

        self._move_int.finish()
        self.model.cleanup()
        self.node.removeNode()

        if task is not None:
            return task.done


class MotoShooter(EnemyUnit, Shooter):
    """Shooter-motorcyclist unit.

    Includes character and his transport.

    Args:
        model (actor.Actor): Enemy character model.
        id_ (int): Enemy unit id.
        y_positions (list): Free positions along Y.
        enemy_handler (CollisionHandlerEvent): Enemy collisions handler.
        class_data (dict): Enemy class description.
    """

    def __init__(self, model, id_, y_positions, enemy_handler, class_data):
        EnemyUnit.__init__(
            self, id_, "Moto Shooter", class_data, model, y_positions, enemy_handler
        )
        Shooter.__init__(self)

        self.damage = (2, 3)

        self.model.setPlayRate(0.6, "aim_left")
        self.model.setPlayRate(0.6, "aim_right")

        self.shot_snd = self._set_shoot_snd("smg_shot1")

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
        targets = self.current_part.chars + [base.train]  # noqa: F821

        if self._target not in targets or chance(5):
            self._target = random.choice(targets)

            self._stop_tasks("_shoot")
            base.taskMgr.doMethodLater(  # noqa: F821
                0.5, self._shoot, self.id + "_shoot"
            )
        task.delayTime = 0.5
        return task.again

    def enter_the_part(self, part):
        """Start fighting in the given part.

        Args:
            part (train_part.TrainPart): Train part this enemy entered.
        """
        self.current_part = part
        self._aim(False)

        base.taskMgr.doMethodLater(  # noqa: F821
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

    def _detach(self):
        """Reparent this enemy to the render to left behind."""
        self.model.wrtReparentTo(render)  # noqa: F821

    def _missed_shot(self):
        """Calculate if enemy missed the current shot.

        Returns:
            bool: True if enemy missed, False otherwise.
        """
        return False

    def _die(self):
        """Die actions for this shooter.

        Returns:
            bool: True, if this shooter dies for the first time.
        """
        if not Shooter._die(self):
            return False

        EnemyUnit._die(self)

    def clear(self, task=None):
        """Clear all the graphical data of this unit."""
        EnemyUnit.clear(self, task)
        base.sound_mgr.detach_sound(self.shot_snd)  # noqa: F821

        if task is not None:
            return task.done


class BrakeDropper(EnemyUnit):
    """Brake shoes dropper unit.

    Args:
        model (actor.Actor): Enemy character model.
        id_ (int): Enemy unit id.
        y_positions (list): Free positions along Y.
        enemy_handler (CollisionHandlerEvent): Enemy collisions handler.
    """

    def __init__(self, model, id_, y_positions, enemy_handler, class_data):
        EnemyUnit.__init__(
            self, id_, "Braker", class_data, model, y_positions, enemy_handler
        )
        self.is_jumping = False

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

        self._jump_snd = base.sound_mgr.loadSfx("sounds/moto_jump1.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(self._jump_snd, self.model)  # noqa: F821

        self._fall_snd = base.sound_mgr.loadSfx("sounds/moto_fall1.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(self._fall_snd, self.model)  # noqa: F821

    def _jump_and_brake(self, task):
        """Jump over the railway and drop brake."""
        if not self._brakes or self.current_part is None:
            return task.done

        for char in base.world.enemy.active_units.values():  # noqa: F821
            # if someone is jumping now, don't jump
            if (
                type(char) == BrakeDropper and char.id != self.id and char.is_jumping
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

        base.taskMgr.doMethodLater(  # noqa: F821
            0.15, self._jump_snd.play, self.id + "_jump_sound", extraArgs=[]
        )
        base.taskMgr.doMethodLater(  # noqa: F821
            1.5, self._fall_snd.play, self.id + "_fall_sound", extraArgs=[]
        )
        base.taskMgr.doMethodLater(  # noqa: F821
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

        base.taskMgr.doMethodLater(  # noqa: F821
            2, self._float_move, self.id + "_float_move"
        )

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

    def enter_the_part(self, part):
        """Start fighting in the given part.

        Args:
            part (train_part.TrainPart): Train part this enemy entered.
        """
        if not part.name.endswith("_front"):
            return

        self.current_part = part
        base.taskMgr.doMethodLater(  # noqa: F821
            15, self._jump_and_brake, self.id + "_jump_and_brake"
        )

    def stop(self):
        """Smoothly stop this unit following Train."""
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
