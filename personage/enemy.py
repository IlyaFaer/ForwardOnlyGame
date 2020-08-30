"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Enemy systems.
"""
import random

from direct.actor.Actor import Actor
from panda3d.core import CollisionHandlerEvent

from utils import address, chance
from .enemy_unit import BrakeDropper, MotoShooter
from .transport import TransportManager

FRACTIONS = {
    "Skinheads": {
        "classes": (
            {
                "class": MotoShooter,
                "model": "skinhead_shooter1",
                "score": 3,
                "part": "side",
                "health": 100,
            },
            {
                "class": BrakeDropper,
                "model": "skinhead_shooter1",
                "score": 6,
                "part": "front",
                "health": 50,
            },
        ),
        "attack_chances": {"morning": 15, "noon": 20, "evening": 25, "night": 18},
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
        self._front_y_positions = []
        self._side_y_positions = []
        self.score = 3

        for gain in range(1, 14):
            self._side_y_positions.append(round(0.15 + gain * 0.05, 2))
            self._side_y_positions.append(round(-0.15 - gain * 0.05, 2))

        for gain in range(1, 7):
            self._front_y_positions.append(round(0.1 + gain * 0.05, 2))
            self._front_y_positions.append(round(-0.1 - gain * 0.05, 2))

        self._classes = FRACTIONS[fraction]["classes"]
        self._attack_chances = FRACTIONS[fraction]["attack_chances"]

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
        if self._is_cooldown:
            return False

        if chance(self._attack_chances[day_part] + 5 if lights_on else 0):
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
        available = [
            en_class for en_class in self._classes if en_class["score"] <= self.score
        ]

        delay = 0
        wave_score = 0
        brakers = 0
        while wave_score < self.score:
            unit_class = random.choice(available)

            if unit_class["class"] == BrakeDropper:
                brakers += 1
                if brakers == 3:
                    available.remove(unit_class)

            self._unit_id += 1
            base.taskMgr.doMethodLater(  # noqa: F821
                delay,
                self._load_enemy,
                "load_enemy_" + str(self._unit_id),
                extraArgs=[train_mod, unit_class, self._unit_id],
            )
            delay += 0.035
            wave_score += unit_class["score"]

    def stop_attack(self):
        """Make all the unit smoothly stop following Train."""
        self.score += 1
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

        self._transport_mgr.stop()
        return task.done

    def _stop_cooldown(self, task):
        """Ends cool down period."""
        self._is_cooldown = False
        return task.done

    def _load_enemy(self, train_mod, class_, id_):
        """Load single enemy unit.

        Args:
            train_mod (panda3d.core.NodePath): Train model to move.
            class_ (dict): Enemy class.
            id_ (int): Unit id.
        """
        y_poss = (
            self._side_y_positions
            if class_["part"] == "side"
            else self._front_y_positions
        )
        enemy = class_["class"](
            Actor(address(class_["model"])), id_, y_poss, self._handler, class_
        )
        self._transport_mgr.make_motorcyclist(enemy)

        enemy.node.reparentTo(train_mod)
        self.active_units[enemy.id] = enemy

    def _clear_enemies(self, task):
        """Delete all enemy units to release memory."""
        for enemy in self.active_units.values():
            enemy.clear()

        self.active_units.clear()
        self._transport_mgr.stop()
        return task.done
