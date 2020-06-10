"""Enemy systems."""
import random
from direct.actor.Actor import Actor
from direct.interval.LerpInterval import LerpPosInterval
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
        task_mgr (direct.task.Task.TaskManager): Task manager.
        sound_mgr (direct.showbase.Audio3DManager.Audio3DManager): Sound manager.
    """

    def __init__(self, fraction, task_mgr, sound_mgr):
        self._sound_mgr = sound_mgr
        self._task_mgr = task_mgr
        self._unit_id = 0
        self._active_units = []
        self._is_cooldown = False

        self._y_positions = []
        for gain in range(1, 14):
            self._y_positions.append(round(0.15 + gain * 0.05, 2))
            self._y_positions.append(round(-0.15 - gain * 0.05, 2))

        self._models = FRACTIONS[fraction]["models"]
        self._attack_chances = FRACTIONS[fraction]["attack_chances"]

        self._motocycle1_model = Actor(address("motocycle1"))
        self._motocycle1_model.setPlayRate(1.5, "ride")

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
            self._task_mgr.doMethodLater(
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
            self._task_mgr.doMethodLater(
                delay,
                self._load_enemy,
                "load_enemy_" + str(self._unit_id),
                extraArgs=[train_mod, self._unit_id],
            )
            delay += 0.035

    def stop_attack(self):
        """Make all the unit smoothly stop following Train."""
        for enemy in self._active_units:
            enemy.stop(self._task_mgr)

        self._task_mgr.doMethodLater(12, self._clear_enemies, "clear_enemies")

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
            self._task_mgr,
            Actor(address(random.choice(self._models))),
            id_,
            self._y_positions,
            self._motocycle1_model,
        )
        enemy.model.reparentTo(train_mod)
        self._active_units.append(enemy)

        # load sounds asynchronously
        self._task_mgr.doMethodLater(
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
        sound = self._sound_mgr.loadSfx("sounds/moto_moves1.ogg")
        self._sound_mgr.attachSoundToObject(sound, enemy.transport)
        enemy.set_sounds(sound)
        return task.done

    def _clear_enemies(self, task):
        """Delete all enemy units to release memory."""
        for enemy in self._active_units:
            self._sound_mgr.detach_sound(enemy.transport_snd)
            enemy.clear()

        self._active_units.clear()
        self._motocycle1_model.stop()
        return task.done


class EnemyUnit:
    """Single enemy unit.

    Includes character and his transport.

    Args:
        taskMgr (direct.task.Task.TaskManager): Task manager.
        model (actor.Actor): Enemy character model.
        id_ (int): Enemy unit id.
        y_positions (list): Free positions along Y.
        moto (actor.Actor): Motocycle model.
    """

    def __init__(self, taskMgr, model, id_, y_positions, moto_mod):
        self._move_int = None

        self._y_positions = y_positions
        self._y_pos = random.choice(self._y_positions)
        self._y_positions.remove(self._y_pos)

        self.id = "enemy_" + str(id_)

        self.model = model
        self.model.setPos(self._io_dist, -7, 0)
        self.model.pose("ride", 1)
        self.model.setPlayRate(0.6, "aim_left")
        self.model.setPlayRate(0.6, "aim_right")

        self.transport = self.model.attachNewNode("moto_" + self.id)
        moto_mod.instanceTo(self.transport)
        self.transport_snd = None

        time_to_overtake = random.randint(30, 47)
        self._move(time_to_overtake, (self._y_pos, random.uniform(-0.05, 0.4), 0))
        taskMgr.doMethodLater(
            time_to_overtake + 2, self._float_move, self.id + "_float_move"
        )
        taskMgr.doMethodLater(time_to_overtake - 2, self._aim, self.id + "_aim")

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

    def _aim(self, task):
        """Aim to Train when got close enough."""
        if self._y_pos < 0:
            self.model.play("aim_right")
        else:
            self.model.play("aim_left")

        return task.done

    def set_sounds(self, transport_snd):
        """Set sounds for this unit.

        Args:
            transport_snd (panda3d.core.AudioSound): Transport sound.
        """
        self.transport_snd = transport_snd
        self.transport_snd.setLoop(True)
        self.transport_snd.setPlayRate(random.uniform(0.8, 1))
        self.transport_snd.setVolume(0.4)
        self.transport_snd.play()

    def stop(self, taskMgr):
        """Smoothly stop this unit following Train."""
        taskMgr.remove(self.id + "_float_move")

        self._move(random.randint(9, 11), (self._io_dist, -7, 0))
        self._y_positions.append(self._y_pos)

        self.model.setPlayRate(-0.6, "aim_left")
        self.model.setPlayRate(-0.6, "aim_right")

        taskMgr.doMethodLater(2, self._aim, self.id + "_unaim")

    def clear(self):
        """Clear all the graphical data of this unit."""
        self._move_int.finish()
        self.model.cleanup()
        self.model.removeNode()
        self.transport.removeNode()
