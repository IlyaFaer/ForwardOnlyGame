"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Transport control API.
"""
import random
from direct.actor.Actor import Actor
from utils import address


class TransportManager:
    """Transport manager rules a transport loading and preparing.

    It prepares transport models and then propagates
    its instances to the given units.
    """

    def __init__(self):
        self._models = {
            "moto1": Actor(address("motocycle1")),
            "moto2": Actor(address("motocycle2")),
        }
        self._models["moto1"].setPlayRate(1.5, "ride")
        self._models["moto2"].setPlayRate(1.5, "ride")

    def make_motorcyclist(self, unit):
        """Make the given unit motorcyclist.

        Args:
            unit (enemy_unit.EnemyUnit): Unit to make motorcyclist.
        """
        moto_model = unit.class_data["moto_model"]

        unit.transport = unit.model.attachNewNode("moto_" + unit.id)
        self._models[moto_model].instanceTo(unit.transport)

        if not self._models[moto_model].getCurrentAnim():
            self._models[moto_model].loop("ride")

        base.taskMgr.doMethodLater(  # noqa: F821
            4,
            self._load_snd,
            "load_transport_sound_" + unit.id,
            extraArgs=[unit],
            appendTask=True,
        )

    def _load_snd(self, unit, task):
        """Load transport sound.

        Args:
            unit (enemy_unit.EnemyUnit): Unit to make motorcyclist.
        """
        unit.transport_snd = base.sound_mgr.loadSfx(  # noqa: F821
            "sounds/moto_moves1.ogg"
        )
        unit.transport_snd.setLoop(True)
        unit.transport_snd.setPlayRate(random.uniform(0.7, 1))
        unit.transport_snd.setVolume(0.5)
        unit.transport_snd.play()
        base.sound_mgr.attachSoundToObject(  # noqa: F821
            unit.transport_snd, unit.transport
        )
        return task.done

    def stop(self):
        """Stop all the transport animations."""
        for model in self._models.values():
            model.stop()
