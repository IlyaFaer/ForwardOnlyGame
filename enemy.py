"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Enemy systems.
"""
import random

from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence, Parallel
from direct.interval.LerpInterval import LerpPosInterval, LerpScaleInterval
from direct.interval.SoundInterval import SoundInterval
from panda3d.core import CollisionHandlerEvent, CollisionNode, CollisionSphere

from const import MOUSE_MASK, SHOT_RANGE_MASK
from utils import address, chance

FRACTIONS = {
    "Skinheads": {
        "models": ("skinhead_shooter1",),
        "attack_chances": {"morning": 0, "noon": 3, "evening": 5, "night": 2},
    }
}


class Enemy:
    """Class to hold an enemy fraction.

    Includes all the currently active enemies.

    Args:
        fraction (str): Enemy fraction name.
        sound_mgr (direct.showbase.Audio3DManager.Audio3DManager): Sound manager.
    """

    def __init__(self, fraction, sound_mgr):
        self.active_units = {}
        self._unit_id = 0
        self._is_cooldown = False
        self._y_positions = []

        self._sound_mgr = sound_mgr

        for gain in range(1, 14):
            self._y_positions.append(round(0.15 + gain * 0.05, 2))
            self._y_positions.append(round(-0.15 - gain * 0.05, 2))

        self._models = FRACTIONS[fraction]["models"]
        self._attack_chances = FRACTIONS[fraction]["attack_chances"]

        self._motocycle1_model = Actor(address("motocycle1"))
        self._motocycle1_model.setPlayRate(1.5, "ride")

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
        self._motocycle1_model.loop("ride")

        delay = 0
        for _ in range(random.randint(2, 10)):
            self._unit_id += 1
            base.taskMgr.doMethodLater(  # noqa: F821
                delay,
                self._load_enemy,
                "load_enemy_" + str(self._unit_id),
                extraArgs=[train_mod, self._unit_id],
            )
            delay += 0.035

    def stop_attack(self):
        """Make all the unit smoothly stop following Train."""
        for enemy in self.active_units.values():
            enemy.stop()

        base.taskMgr.doMethodLater(  # noqa: F821
            12, self._clear_enemies, "clear_enemies"
        )

    def _stop_cooldown(self, task):
        """Ends cool down period."""
        self._is_cooldown = False
        return task.done

    def _load_enemy(self, train_mod, id_):
        """Load single enemy unit.

        Args:
            train_mod (panda3d.core.NodePath): Train model to move.
            id_ (int): Unit id.
        """
        enemy = EnemyUnit(
            Actor(address(random.choice(self._models))),
            id_,
            self._y_positions,
            self._motocycle1_model,
            self._handler,
        )
        enemy.model.reparentTo(train_mod)
        self.active_units[enemy.id] = enemy

        # load sounds asynchronously
        base.taskMgr.doMethodLater(  # noqa: F821
            4,
            self._add_enemy_sounds,
            "load_enemy_sounds_" + str(id_),
            extraArgs=[enemy],
            appendTask=True,
        )

    def _add_enemy_sounds(self, enemy, task):
        """Load and attach enemy sounds asynchronous.

        Args:
            enemy (EnemyUnit): Enemy unit object.
        """
        transport_snd = self._sound_mgr.loadSfx("sounds/moto_moves1.ogg")
        shot_snd = self._sound_mgr.loadSfx("sounds/smg_shot1.ogg")

        self._sound_mgr.attachSoundToObject(transport_snd, enemy.transport)
        self._sound_mgr.attachSoundToObject(shot_snd, enemy.model)

        enemy.set_sounds(transport_snd, shot_snd)
        return task.done

    def _clear_enemies(self, task):
        """Delete all enemy units to release memory."""
        for enemy in self.active_units.values():
            self._sound_mgr.detach_sound(enemy.transport_snd)
            self._sound_mgr.detach_sound(enemy.shot_snd)
            enemy.clear()

        self.active_units.clear()
        self._motocycle1_model.stop()
        return task.done


class EnemyUnit:
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
        self._move_int = None
        self._shoot_anim = None

        self._y_positions = y_positions
        self._y_pos = random.choice(self._y_positions)
        self._y_positions.remove(self._y_pos)

        self.id = "enemy_" + str(id_)

        self.model = model
        self.model.setPos(self._io_dist, -7, 0)
        self.model.pose("ride", 1)
        self.model.setPlayRate(0.6, "aim_left")
        self.model.setPlayRate(0.6, "aim_right")

        en_col_node = CollisionNode(self.id)
        en_col_node.setIntoCollideMask(MOUSE_MASK)
        en_col_node.setFromCollideMask(SHOT_RANGE_MASK)
        en_col_node.addSolid(CollisionSphere(0, 0, 0.05, 0.05))
        col_np = self.model.attachNewNode(en_col_node)
        base.traverser.addCollider(col_np, enemy_handler)  # noqa: F821

        # prepare transport
        self.transport = self.model.attachNewNode("moto_" + self.id)
        moto_mod.instanceTo(self.transport)
        self.transport_snd = None

        # organize movement and aiming tasks
        time_to_overtake = random.randint(30, 47)
        self._move(time_to_overtake, (self._y_pos, random.uniform(-0.05, 0.4), 0))
        base.taskMgr.doMethodLater(  # noqa: F821
            time_to_overtake + 2, self._float_move, self.id + "_float_move"
        )
        base.taskMgr.doMethodLater(  # noqa: F821
            time_to_overtake - 2,
            self._aim,
            self.id + "_aim",
            extraArgs=[False],
            appendTask=True,
        )
        base.taskMgr.doMethodLater(  # noqa: F821
            time_to_overtake, self._shoot, self.id + "_shoot"
        )

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
            self.model, period, new_pos, blendType="easeInOut"
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

    def _aim(self, back, task):
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
            # prepare gun fire sequence
            fire = loader.loadModel(address("gun_fire1"))  # noqa: F821
            fire.reparentTo(self.model)
            fire.setScale(1, 0.0001, 1)

            shoot_seq = Parallel(
                Sequence(
                    LerpScaleInterval(fire, 0.12, (1, 1, 1)),
                    LerpScaleInterval(fire, 0.12, (1, 0.0001, 1)),
                ),
                SoundInterval(self.shot_snd, duration=0.3),
            )
            self._shoot_anim = Sequence(shoot_seq, shoot_seq)

            fire.setPos(*pos)
            fire.setH(h)

        return task.done

    def _shoot(self, task):
        """Play shooting animation and sound."""
        self._shoot_anim.start()
        task.delayTime = 1.7 + random.uniform(0.1, 0.9)
        return task.again

    def set_sounds(self, transport_snd, shot_snd):
        """Set sounds for this unit.

        Args:
            transport_snd (panda3d.core.AudioSound): Transport sound.
            shot_snd (panda3d.core.AudioSound): Shooting sound.
        """
        self.transport_snd = transport_snd
        self.transport_snd.setLoop(True)
        self.transport_snd.setPlayRate(random.uniform(0.8, 1))
        self.transport_snd.setVolume(0.4)
        self.transport_snd.play()

        self.shot_snd = shot_snd

    def stop(self):
        """Smoothly stop this unit following Train."""
        base.taskMgr.remove(self.id + "_float_move")  # noqa: F821

        self._move(random.randint(9, 11), (self._io_dist, -7, 0))
        self._y_positions.append(self._y_pos)

        self.model.setPlayRate(-0.6, "aim_left")
        self.model.setPlayRate(-0.6, "aim_right")

        base.taskMgr.doMethodLater(  # noqa: F821
            2, self._aim, self.id + "_unaim", extraArgs=[True], appendTask=True
        )
        base.taskMgr.remove(self.id + "_shoot")  # noqa: F821

    def clear(self):
        """Clear all the graphical data of this unit."""
        self._move_int.finish()
        self.model.cleanup()
        self.model.removeNode()
        self.transport.removeNode()
