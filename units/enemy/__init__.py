"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Enemy systems.
"""
import random

from direct.actor.Actor import Actor
from panda3d.core import CollisionHandlerEvent

from gui.teaching import EnemyDesc
from utils import address, chance
from world.objects import (
    BARRIER_THRESHOLD,
    ROCKET_THRESHOLD,
    Barrier,
    Rocket,
    SCPInstance,
)
from .enemy_unit import (
    BrakeThrower,
    DodgeShooter,
    Kamikaze,
    MotoShooter,
    StunBombThrower,
)
from .transport import TransportManager

# enemy classes description
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
            "class": BrakeThrower,
            "model": "skinhead_shooter1",
            "score": 3,
            "threshold": 6,
            "part": "front",
            "health": 55,
            "transport_model": "moto1",
        },
        {
            "class": StunBombThrower,
            "model": "skinhead_thrower1",
            "score": 3,
            "threshold": 10,
            "part": "side",
            "health": 90,
            "transport_model": "moto2",
        },
        {
            "class": DodgeShooter,
            "model": "dodge_gun",
            "score": 5,
            "threshold": 13,
            "part": "side",
            "health": 100,
            "transport_model": "dodge",
        },
        {
            "class": Kamikaze,
            "model": "skinhead_kamikaze",
            "score": 6,
            "threshold": 19,
            "part": "side",
            "health": 50,
            "transport_model": "moto3",
        },
    ),
    "attack_chances": {"morning": 8, "noon": 20, "evening": 35, "night": 20},
}

# enemy objects
NOT_TRANSPORT_CLASSES = (
    {"class": Barrier, "threshold": BARRIER_THRESHOLD},
    {"class": Rocket, "threshold": ROCKET_THRESHOLD},
)


class Enemy:
    """Class to hold an enemy fraction overall.

    Includes all the currently active enemy units/objects.
    """

    def __init__(self):
        self.active_units = {}
        self.score = 3

        self._unit_id = 0
        self._is_cooldown = False
        self._is_first_attack = True
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
        self.handler = CollisionHandlerEvent()
        self.handler.addInPattern("into-%in")
        self.handler.addOutPattern("out-%in")

    def _clear_enemies(self, task):
        """Delete all enemy units to release memory."""
        for enemy in self.active_units.values():
            enemy.clear()

        self.active_units.clear()
        self._transport_mgr.stop()

        for part in base.train.parts.values():  # noqa: F821
            part.enemies = []

        return task.done

    def _load_enemy(self, train_mod, class_data, id_):
        """Load single enemy unit.

        Args:
            train_mod (panda3d.core.NodePath): Train model to overtake.
            class_data (dict): Enemy class description.
            id_ (int): Unit id.
        """
        y_poss = (
            self._side_y_positions
            if class_data["part"] == "side"
            else self._front_y_positions
        )
        enemy = class_data["class"](
            Actor(address(class_data["model"])), id_, y_poss, self.handler, class_data
        )
        self._transport_mgr.load_transport(enemy)

        enemy.node.reparentTo(train_mod)
        self.active_units[enemy.id] = enemy

    def _stop_cooldown(self, task):
        """Ends enemy attack cool down period."""
        self._is_cooldown = False
        return task.done

    def capture_train(self):
        """The Train got critical damage - stop near it."""
        for enemy in self.active_units.values():
            enemy.capture_train()

    def going_to_attack(self, day_part, lights_on):
        """Checks if enemy is going to attack.

        Args:
            day_part (str): Day part name.
            lights_on (bool): True if Train lights are on.

        Returns:
            bool: True if enemy is going to attack, False otherwise.
        """
        if self._is_first_attack and self.score == 3:
            self._is_first_attack = False
            EnemyDesc("MotoShooter")

        if (
            self._is_cooldown
            or base.world.is_in_city  # noqa: F821
            or base.train.smoke_filtered  # noqa: F821
            or base.world.is_near_fork  # noqa: F821
            or base.world.meet_scp  # noqa: F821
        ):
            return False

        if chance(CLASSES["attack_chances"][day_part] + (15 if lights_on else 0)):
            self._is_cooldown = True
            taskMgr.doMethodLater(  # noqa: F821
                290, self._stop_cooldown, "stop_attack_cooldown"
            )
            return True

        return False

    def prepare_scp_instance(self, scp_train, positions, char, id_):
        """Prepare an SCP enemy instance.

        Args:
            scp_train (world.objects.SCPTrain): SCP train object.
            positions (dict):
                A list of currently free unit position on SCP train.
            char (crew.character):
                An Adjutant crew member, whose copy the new
                instance must be.
            id_ (ind): Instance id.

        Returns:
            SCPInstance: An SCP enemy instance.
        """
        instance = SCPInstance(
            char.class_data,
            char.class_,
            char.sex,
            positions,
            scp_train,
            id_,
            self.handler,
        )
        self.active_units[instance.id] = instance

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
        kamikazes = 0
        while wave_score < self.score:
            unit_class = random.choice(available)

            if unit_class["class"] == BrakeThrower:
                brakers += 1
                if brakers == 2:
                    available.remove(unit_class)

            if unit_class["class"] == StunBombThrower:
                throwers += 1
                if throwers == 2:
                    available.remove(unit_class)

            if unit_class["class"] == DodgeShooter:
                cars += 1
                if cars == 2:
                    available.remove(unit_class)

            if unit_class["class"] == Kamikaze:
                kamikazes += 1
                if kamikazes == 2:
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

        for class_ in CLASSES["classes"] + NOT_TRANSPORT_CLASSES:
            if class_["threshold"] == self.score:
                EnemyDesc(class_["class"].__name__)

    def stop_ride_anim(self, task):
        """Stop riding animation and sounds."""
        for enemy in self.active_units.values():
            enemy.stop_ride()

        self._transport_mgr.stop()
        return task.done
