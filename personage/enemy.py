"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Enemy systems.
"""
import random

from direct.actor.Actor import Actor
from direct.interval.LerpInterval import LerpPosInterval
from panda3d.bullet import BulletBoxShape, BulletRigidBodyNode
from panda3d.core import CollisionHandlerEvent, CollisionSphere, Point3, Vec3

from const import MOUSE_MASK, SHOT_RANGE_MASK
from .shooter import Shooter
from utils import address, chance

FRACTIONS = {
    "Skinheads": {
        "classes": ({"model": "skinhead_shooter1", "score": 3},),
        "attack_chances": {"morning": 0, "noon": 3, "evening": 5, "night": 2},
    }
}


class Enemy:
    """Class to hold an enemy fraction.

    Includes all the currently active enemies.

    Args:
        fraction (str): Enemy fraction name.
    """

    def __init__(self, fraction):
        self.active_units = {}
        self._unit_id = 0
        self._is_cooldown = False
        self._y_positions = []
        self._score = 3

        for gain in range(1, 14):
            self._y_positions.append(round(0.15 + gain * 0.05, 2))
            self._y_positions.append(round(-0.15 - gain * 0.05, 2))

        self._classes = FRACTIONS[fraction]["classes"]
        self._attack_chances = FRACTIONS[fraction]["attack_chances"]

        self._motocycle_model = Actor(address("motocycle1"))
        self._motocycle_model.setPlayRate(1.5, "ride")

        # set enemy collisions handler
        self._handler = CollisionHandlerEvent()
        self._handler.addInPattern("into-%in")
        self._handler.addOutPattern("out-%in")

    def going_to_attack(self, day_part, lights_on):
        """Checks if enemy is going to attack.

        Args:
            day_part (str): Day part name.
            lights_on (bool): True if Train lights are on.

        Returns:
            bool: True if enemy is going to attack, False otherwise.
        """
        if self._is_cooldown:
            return False

        if chance(self._attack_chances[day_part] + 2 if lights_on else 0):
            self._is_cooldown = True
            base.taskMgr.doMethodLater(  # noqa: F821
                600, self._stop_cooldown, "stop_attack_cooldown"
            )
            return True

        return False

    def prepare(self, train_mod):
        """Load all the enemies and make them follow Train.

        Method asynchronously loads every enemy unit
        to avoid freezing.

        Args:
            train_mod (panda3d.core.NodePath): Train model.
        """
        self._motocycle_model.loop("ride")

        available = [
            en_class for en_class in self._classes if en_class["score"] <= self._score
        ]

        delay = 0
        wave_score = 0
        while wave_score < self._score:
            unit_class = random.choice(available)

            self._unit_id += 1
            base.taskMgr.doMethodLater(  # noqa: F821
                delay,
                self._load_enemy,
                "load_enemy_" + str(self._unit_id),
                extraArgs=[train_mod, unit_class["model"], self._unit_id],
            )
            delay += 0.035
            wave_score += unit_class["score"]

    def stop_attack(self):
        """Make all the unit smoothly stop following Train."""
        self._score += 1
        for enemy in self.active_units.values():
            enemy.stop()

        base.taskMgr.doMethodLater(  # noqa: F821
            12, self._clear_enemies, "clear_enemies"
        )

    def capture_train(self):
        """Train got critical damage - stop near it."""
        for enemy in self.active_units.values():
            base.taskMgr.remove(enemy.id + "_float_move")  # noqa: F821
            base.taskMgr.remove(enemy.id + "_shoot")  # noqa: F821
            base.taskMgr.remove(enemy.id + "_choose_target")  # noqa: F821

    def stop_ride_anim(self, task):
        """Stop riding animation and sounds."""
        for enemy in self.active_units.values():
            enemy.stop_ride()

        self._motocycle_model.stop()
        return task.done

    def _stop_cooldown(self, task):
        """Ends cool down period."""
        self._is_cooldown = False
        return task.done

    def _load_enemy(self, train_mod, model, id_):
        """Load single enemy unit.

        Args:
            train_mod (panda3d.core.NodePath): Train model to move.
            model (panda3d.core.NodePath): Unit model.
            id_ (int): Unit id.
        """
        enemy = EnemyUnit(
            Actor(address(model)),
            id_,
            self._y_positions,
            self._motocycle_model,
            self._handler,
        )
        enemy.node.reparentTo(train_mod)
        self.active_units[enemy.id] = enemy

        # load sounds asynchronously
        base.taskMgr.doMethodLater(  # noqa: F821
            4, enemy.set_sounds, "load_enemy_sounds_" + str(id_)
        )

    def _clear_enemies(self, task):
        """Delete all enemy units to release memory."""
        for enemy in self.active_units.values():
            enemy.clear()

        self.active_units.clear()
        self._motocycle_model.stop()
        return task.done


class EnemyUnit(Shooter):
    """Single enemy unit.

    Includes character and his transport.

    Args:
        model (actor.Actor): Enemy character model.
        id_ (int): Enemy unit id.
        y_positions (list): Free positions along Y.
        moto (actor.Actor): Motocycle model.
        enemy_handler (CollisionHandlerEvent): Enemy collisions handler.
    """

    def __init__(self, model, id_, y_positions, moto_mod, enemy_handler):
        super().__init__("enemy_" + str(id_), "Shooter", {"health": 100})
        self._tooltip = "Skinhead - " + self.class_
        self._move_int = None

        self._y_positions = y_positions
        self._y_pos = random.choice(self._y_positions)
        self._y_positions.remove(self._y_pos)

        self.damage = (2, 3)

        self.model = model
        self.model.pose("ride", 1)
        self.model.setPlayRate(0.6, "aim_left")
        self.model.setPlayRate(0.6, "aim_right")

        self.node = render.attachNewNode(self.id + "_node")  # noqa: F821
        self.node.setPos(self._io_dist, -7, 0)
        self.model.reparentTo(self.node)

        self.transport_snd = None

        self._col_node = self._init_col_node(
            SHOT_RANGE_MASK, MOUSE_MASK, CollisionSphere(0, 0, 0.05, 0.05)
        )
        base.common_ctrl.traverser.addCollider(  # noqa: F821
            self._col_node, enemy_handler
        )

        # prepare transport
        self.transport = self.model.attachNewNode("moto_" + self.id)
        moto_mod.instanceTo(self.transport)

        self._explosion = base.effects_mgr.explosion(self)  # noqa: F821

        # organize movement and aiming tasks
        time_to_overtake = random.randint(33, 50)
        self._move(time_to_overtake, (self._y_pos, random.uniform(-0.05, 0.4), 0))
        base.taskMgr.doMethodLater(  # noqa: F821
            time_to_overtake + 2, self._float_move, self.id + "_float_move"
        )

    @property
    def tooltip(self):
        """Tooltip to show on mouse pointing to this enemy.

        Returns:
            str: This unit fraction and class.
        """
        return self._tooltip

    @property
    def clear_delay(self):
        """Delay between this character's death and clearing.

        Returns:
            int: Seconds to hold the unit before delete.
        """
        return 15

    @property
    def _io_dist(self):
        """Enemy Y-distance for approach and back off."""
        if self._y_pos > 0:
            return self._y_pos + 0.45
        return self._y_pos - 0.45

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
            random.randint(3, 6), (self._y_pos, random.uniform(-0.25, 0.35) + 0.05, 0)
        )
        task.delayTime = random.randint(7, 9)
        return task.again

    def _aim(self, back):
        """Aim to Train when got close enough.

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
            self._shoot_anim = self._set_shoot_anim(pos, h)

    def _choose_target(self, task):
        """Choose a character/Train as a target.

        Character will be chosen from the list of
        characters set to the TrainPart, in which
        range this enemy is now.
        """
        targets = self.current_part.chars + [base.train]  # noqa: F821

        if self._target not in targets:
            self._target = random.choice(targets)
            base.taskMgr.doMethodLater(  # noqa: F821
                0.5, self._shoot, self.id + "_shoot"
            )

        task.delayTime = 0.5
        return task.again

    def set_sounds(self, task):
        """Set sounds for this unit."""
        self.transport_snd = base.sound_mgr.loadSfx(  # noqa: F821
            "sounds/moto_moves1.ogg"
        )
        self.transport_snd.setLoop(True)
        self.transport_snd.setPlayRate(random.uniform(0.8, 1))
        self.transport_snd.setVolume(0.5)
        self.transport_snd.play()
        base.sound_mgr.attachSoundToObject(  # noqa: F821
            self.transport_snd, self.transport
        )

        self.shot_snd = self._set_shoot_snd("smg_shot1")
        return task.done

    def enter_the_part(self, part):
        """Start fighting in the given part.

        Args:
            part (train.TrainPart): Train part this enemy entered.
        """
        self.current_part = part
        self._aim(False)

        base.taskMgr.doMethodLater(  # noqa: F821
            1.5, self._choose_target, self.id + "_choose_target"
        )

    def leave_the_part(self):
        """Stop fighting in the current part."""
        base.taskMgr.remove(self.id + "_shoot")  # noqa: F821
        base.taskMgr.remove(self.id + "_choose_target")  # noqa: F821

        self.model.setPlayRate(-0.6, "aim_left")
        self.model.setPlayRate(-0.6, "aim_right")

        self._aim(True)

        self.current_part = None
        self._target = None

    def get_damage(self, damage):
        """Take damage points and change model color.

        Args:
            damage (int): Damage points to get.
        """
        super().get_damage(damage)
        self.model.setColorScale(self.model.getColorScale()[0] + 0.018, 1, 1, 1)

    def _die(self):
        """Make this enemy die.

        Play death sequence of movements and sounds,
        stop all the tasks for this enemy, plan clearing.
        """
        if not super()._die():
            return

        self.model.setColorScale(1, 1, 1, 1)
        base.taskMgr.remove(self.id + "_float_move")  # noqa: F821
        self._move_int.pause()

        self.model.play("die")
        if self.id in base.world.enemy.active_units:  # noqa: F821
            base.world.enemy.active_units.pop(self.id)  # noqa: F821
            self.current_part.enemies.remove(self)

        self._explode()

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
            y = random.randint(5000, 7000)
        elif angle == 90:
            x = -random.randint(5000, 7000)
        elif angle == -90:
            x = random.randint(5000, 7000)

        rb_node.applyForce(Vec3(x, y, random.randint(1500, 2500)), Point3(0))
        rb_node.applyTorque(
            Vec3(
                random.randint(-45, 45),
                random.randint(-45, 45),
                random.randint(-45, 45),
            )
        )

    def _detach(self):
        """Reparent this enemy to the render to left behind."""
        self.model.wrtReparentTo(render)  # noqa: F821

    def _missed_shot(self):
        """Calculate if enemy missed the current shot.

        Returns:
            bool: True if enemy missed, False otherwise.
        """
        return False

    def stop(self):
        """Smoothly stop this unit following Train."""
        base.taskMgr.remove(self.id + "_float_move")  # noqa: F821

        self._move(random.randint(9, 11), (self._io_dist, -7, 0))
        self._y_positions.append(self._y_pos)

    def stop_ride(self):
        self.transport_snd.stop()

    def clear(self, task=None):
        """Clear all the graphical data of this unit."""
        base.sound_mgr.detach_sound(self.transport_snd)  # noqa: F821
        base.sound_mgr.detach_sound(self.shot_snd)  # noqa: F821

        self._move_int.finish()
        self.model.cleanup()
        self.node.removeNode()

        if task is not None:
            return task.done
