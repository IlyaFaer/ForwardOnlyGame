"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Base enemy unit API.
"""
import abc
import random

from direct.interval.IntervalGlobal import LerpPosInterval

from utils import chance, take_random
from .unit import Unit


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

        # organize movement and aiming tasks
        time_to_overtake = random.randint(33, 50)

        self._move(time_to_overtake, (self._y_pos, random.uniform(*self._x_range), 0))
        taskMgr.doMethodLater(  # noqa: F821
            time_to_overtake + 2, self._float_move, self.id + "_float_move"
        )

    @abc.abstractmethod
    def _explode(self):
        raise NotImplementedError(
            "Every enemy unit class must implement _explode() method."
        )

    @property
    def _io_dist(self):
        """Enemy Y-distance for approach and back off."""
        if self._y_pos > 0:
            return self._y_pos + 0.45
        return self._y_pos - 0.45

    @property
    def clear_delay(self):
        """Delay between this character's death and clearing.

        Returns:
            int: Seconds to hold the unit before delete.
        """
        return 15

    @property
    def shooting_speed(self):
        """Delay between shots of this unit.

        Returns:
            float: Delay between shots in seconds.
        """
        return 1.7 + random.uniform(0.1, 0.9)

    @property
    def tooltip(self):
        """Tooltip to show on mouse pointing to this enemy.

        Returns:
            str: This unit fraction and class.
        """
        return self._tooltip

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

    def capture_train(self):
        """The Train got critical damage - stop near it."""
        self._stop_tasks("_float_move")

    def get_damage(self, damage):
        """Take damage points and change model color.

        Args:
            damage (int): Damage points to get.
        """
        Unit.get_damage(self, damage)
        self.model.setColorScale(self.model.getColorScale()[0] + 0.018, 1, 1, 1)

    def _die(self):
        """Make this enemy unit die.

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
        return True

    def stop(self):
        """Smoothly stop this unit following the Train."""
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
