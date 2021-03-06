"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Enemy systems.
"""
import random

from direct.actor.Actor import Actor
from panda3d.core import CollisionHandlerEvent

from utils import address, chance
from .enemy_unit import BrakeDropper, DodgeShooter, MotoShooter, StunBombThrower
from .transport import TransportManager

CLASSES = {
    "classes": (
        {
            "class": MotoShooter,
            "model": "skinhead_shooter1",
            "score": 3,
            "threshold": 0,
            "part": "side",
            "health": 100,
            "transport_model": "moto1",
        },
        {
            "class": BrakeDropper,
            "model": "skinhead_shooter1",
            "score": 4,
            "threshold": 6,
            "part": "front",
            "health": 50,
            "transport_model": "moto1",
        },
        {
            "class": StunBombThrower,
            "model": "skinhead_thrower1",
            "score": 5,
            "threshold": 9,
            "part": "side",
            "health": 90,
            "transport_model": "moto2",
        },
        {
            "class": DodgeShooter,
            "model": "dodge_gun",
            "score": 8,
            "threshold": 12,
            "part": "side",
            "health": 100,
            "transport_model": "dodge",
        },
    ),
    "attack_chances": {"morning": 6, "noon": 20, "evening": 35, "night": 20},
}


class Enemy:
    """Class to hold an enemy fraction overall.

    Includes all the currently active enemies.
    """

    def __init__(self):
        self.active_units = {}
        self.score = 3

        self._unit_id = 0
        self._is_cooldown = False
        self._front_y_positions = []
        self._side_y_positions = []

        for gain in range(1, 14):
            self._side_y_positions.append(round(0.15 + gain * 0.075, 2))
            self._side_y_positions.append(round(-0.15 - gain * 0.075, 2))

        for gain in range(1, 7):
            self._front_y_positions.append(round(0.1 + gain * 0.05, 2))
            self._front_y_positions.append(round(-0.1 - gain * 0.05, 2))

        self._transport_mgr = TransportManager()

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
        if (
            self._is_cooldown
            or base.world.is_in_city  # noqa: F821
            or base.train.smoke_filtered  # noqa: F821
        ):
            return False

        if chance(CLASSES["attack_chances"][day_part] + (15 if lights_on else 0)):
            self._is_cooldown = True
            taskMgr.doMethodLater(  # noqa: F821
                480, self._stop_cooldown, "stop_attack_cooldown"
            )
            return True

        return False

    def prepare(self, train_mod):
        """Load enemy units and make them follow the Train.

        Method asynchronously loads every enemy unit to avoid freezing.

        Args:
            train_mod (panda3d.core.NodePath): Train model.
        """
        available = [
            en_class
            for en_class in CLASSES["classes"]
            if en_class["threshold"] <= self.score
        ]

        delay = 0
        wave_score = 0
        brakers = 0
        throwers = 0
        cars = 0
        while wave_score < self.score:
            unit_class = random.choice(available)

            if unit_class["class"] == BrakeDropper:
                brakers += 1
                if brakers == 2:
                    available.remove(unit_class)

            if unit_class["class"] == StunBombThrower:
                throwers += 1
                if throwers == 3:
                    available.remove(unit_class)

            if unit_class["class"] == DodgeShooter:
                cars += 1
                if cars == 2:
                    available.remove(unit_class)

            self._unit_id += 1
            taskMgr.doMethodLater(  # noqa: F821
                delay,
                self._load_enemy,
                "load_enemy_" + str(self._unit_id),
                extraArgs=[train_mod, unit_class, self._unit_id],
            )
            delay += 0.035
            wave_score += unit_class["score"]

    def stop_attack(self):
        """Make all the unit smoothly stop following the Train."""
        self.score += 1
        for enemy in self.active_units.values():
            enemy.stop()

        taskMgr.doMethodLater(12, self._clear_enemies, "clear_enemies")  # noqa: F821

    def capture_train(self):
        """The Train got critical damage - stop near it."""
        for enemy in self.active_units.values():
            enemy.capture_train()

    def stop_ride_anim(self, task):
        """Stop riding animation and sounds."""
        for enemy in self.active_units.values():
            enemy.stop_ride()

        self._transport_mgr.stop()
        return task.done

    def _stop_cooldown(self, task):
        """Ends enemy attack cool down period."""
        self._is_cooldown = False
        return task.done

    def _load_enemy(self, train_mod, class_data, id_):
        """Load single enemy unit.

        Args:
            train_mod (panda3d.core.NodePath): Train model to move.
            class_data (dict): Enemy class description.
            id_ (int): Unit id.
        """
        y_poss = (
            self._side_y_positions
            if class_data["part"] == "side"
            else self._front_y_positions
        )
        enemy = class_data["class"](
            Actor(address(class_data["model"])), id_, y_poss, self._handler, class_data
        )
        self._transport_mgr.load_transport(enemy)

        enemy.node.reparentTo(train_mod)
        self.active_units[enemy.id] = enemy

    def _clear_enemies(self, task):
        """Delete all enemy units to release memory."""
        for enemy in self.active_units.values():
            enemy.clear()

        self.active_units.clear()
        self._transport_mgr.stop()
        return task.done
