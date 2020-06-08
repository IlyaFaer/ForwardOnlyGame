"""Enemy systems."""
import random
from direct.actor.Actor import Actor
from direct.interval.LerpInterval import LerpPosInterval
from utils import address, chance

FRACTIONS = {"Skinheads": ("skinhead_shooter1",)}


class Enemy:
    """Class to hold an enemy fraction.

    Includes all the currently active enemies.

    Args:
        fraction (str): Enemy fraction name.
        taskMgr (direct.task.Task.TaskManager): Task manager.
    """

    def __init__(self, fraction, taskMgr):
        self._task_mgr = taskMgr
        self._unit_id = 0
        self._active_units = []

        self._y_positions = []
        for gain in range(1, 14):
            self._y_positions.append(round(0.15 + gain * 0.05, 2))
            self._y_positions.append(round(-0.15 - gain * 0.05, 2))

        self._models = FRACTIONS[fraction]
        self._motocycle1_model = Actor(address("motocycle1"))
        self._motocycle1_model.setPlayRate(1.5, "ride")

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

    def _clear_enemies(self, task):
        """Delete all enemy units to release memory."""
        for enemy in self._active_units:
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

        self.transport = self.model.attachNewNode("moto_" + self.id)
        moto_mod.instanceTo(self.transport)

        self._move((30, 47), (self._y_pos, random.uniform(-0.05, 0.4), 0))
        taskMgr.doMethodLater(49, self._float_move, self.id + "_float_move")

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
            self.model, random.randint(*period), new_pos, blendType="easeInOut"
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

        self._move((3, 6), (self._y_pos, random.uniform(-0.25, 0.35) + 0.05, 0))

        task.delayTime = random.randint(7, 9)
        return task.again

    def stop(self, taskMgr):
        """Smoothly stop this unit following Train."""
        taskMgr.remove(self.id + "_float_move")

        self._move((9, 11), (self._io_dist, -7, 0))
        self._y_positions.append(self._y_pos)

    def clear(self):
        """Clear all the graphical data of this unit."""
        self._move_int.finish()
        self.model.cleanup()
        self.model.removeNode()
        self.transport.removeNode()
