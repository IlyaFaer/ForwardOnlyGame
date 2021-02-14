"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Transport control API.
"""
import random
from direct.actor.Actor import Actor
from utils import address


class TransportManager:
    """Transport manager rules transport loading and preparing.

    It prepares transport models and then propagates
    its instances to the given units.
    """

    def __init__(self):
        self._models = {
            "moto1": Actor(address("motocycle1")),
            "moto2": Actor(address("motocycle2")),
            "dodge": Actor(address("car1")),
        }
        self._models["moto1"].setPlayRate(1.5, "ride")
        self._models["moto2"].setPlayRate(1.5, "ride")
        self._models["dodge"].setPlayRate(2.5, "ride")

    def _load_snd(self, unit, type_, task):
        """Load transport sound.

        Args:
            unit (enemy_unit.EnemyUnit): Unit to make motorcyclist.
            type_ (str): The transport type: car or motorcycle.
        """
        unit.transport_snd = base.sound_mgr.loadSfx(  # noqa: F821
            "sounds/{type}_moves1.ogg".format(type=type_)
        )
        unit.transport_snd.setLoop(True)
        unit.transport_snd.setPlayRate(random.uniform(0.7, 1))
        unit.transport_snd.setVolume(0.5)
        unit.transport_snd.play()
        base.sound_mgr.attachSoundToObject(  # noqa: F821
            unit.transport_snd, unit.transport
        )
        return task.done

    def load_transport(self, unit):
        """Load transport for the given unit.

        Args:
            unit (enemy_unit.EnemyUnit): The unit to set onto transport.
        """
        transport_model = unit.class_data["transport_model"]

        unit.transport = unit.model.attachNewNode("transport_" + unit.id)
        self._models[transport_model].instanceTo(unit.transport)

        if not self._models[transport_model].getCurrentAnim():
            self._models[transport_model].loop("ride")

        taskMgr.doMethodLater(  # noqa: F821
            4,
            self._load_snd,
            "load_transport_sound_" + unit.id,
            extraArgs=[unit, "moto" if transport_model.startswith("moto") else "car"],
            appendTask=True,
        )

    def stop(self):
        """Stop all the transport animations."""
        for model in self._models.values():
            model.stop()
