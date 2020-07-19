"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Visual effects API.
"""
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import PointLight


class EffectsManager:
    """Manager to control visual effects."""

    def __init__(self):
        self._explosion_lights = self._set_explosion_lights()

    def _set_explosion_lights(self):
        """Prepare three explosion lights.

        Returns:
            list: List of lights to be used for explosions.
        """
        lights = []
        for num in range(3):
            light = PointLight("explosion_light_" + str(num))
            light.setColor((1, 0.9, 0.55, 1))
            light.setAttenuation((0, 0, 1))
            light_np = render.attachNewNode(light)  # noqa: F821
            light_np.setPos(0, 0, -5)
            render.setLight(light_np)  # noqa: F821
            lights.append(light_np)

        return lights

    def explosion(self, parent):
        """Prepare an explosion effect for the given object.

        Args:
            parent (object):
                Must include "id" and "model" properties.
        """
        return Explosion(self._explosion_lights, parent)


class Explosion:
    """An explosion effect.

    Includes sound and particle effects.

    Args:
        explode_lights (list): List of explosion lights
        parent (object): Object to explode.
    """

    def __init__(self, explode_lights, parent):
        self._lights = explode_lights
        self._light_coef = 1.5
        self._parent = parent

        self._sparks = ParticleEffect()
        self._sparks.loadConfig("effects/explode_sparks.ptf")
        self._sparks.setY(0.2)

        self._fire = ParticleEffect()
        self._fire.loadConfig("effects/explode_fire.ptf")
        self._fire.setY(0.1)

        self._snd = base.sound_mgr.loadSfx("sounds/explosion1.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(self._snd, parent.model)  # noqa: F821

    def play(self):
        """Make actual explosion and plan its clearing."""
        self._snd.play()
        self._sparks.start(self._parent.model, render)  # noqa: F821
        self._fire.start(self._parent.model, render)  # noqa: F821

        if self._lights:
            light = self._lights.pop()
            light.reparentTo(self._parent.model)
            light.setPos(0, 0, 0)

            base.taskMgr.doMethodLater(  # noqa: F821
                0.02,
                self._light_change,
                self._parent.id + "_explosion_light",
                extraArgs=[light],
                appendTask=True,
            )

        base.taskMgr.doMethodLater(  # noqa: F821
            0.9, self._stop_fire, self._parent.id + "_disable_exlode_fire"
        )
        base.taskMgr.doMethodLater(  # noqa: F821
            4.95, self._stop_sparks, self._parent.id + "_disable_exlode_sparks"
        )
        base.taskMgr.doMethodLater(  # noqa: F821
            5.05, self._clear, self._parent.id + "_clear_explode"
        )

    def _light_change(self, light, task):
        """Change explosion light attenuation.

        Args:
            light (panda3d.core.NodePath): Explosion lights.
        """
        self._light_coef += 0.1

        if self._light_coef >= 10:
            self._lights.append(light)
            light.detachNode()
            light.node().setAttenuation((0, 0, 1))
            return task.done

        light.node().setAttenuation((self._light_coef - 1, 0, self._light_coef))
        return task.again

    def _stop_sparks(self, task):
        """Disable explosion effect."""
        self._sparks.disable()
        return task.done

    def _stop_fire(self, task):
        """Disable explosion effect."""
        self._fire.disable()
        return task.done

    def _clear(self, task):
        """Clear this explosion effect."""
        self._sparks.cleanup()
        self._fire.cleanup()
        base.sound_mgr.detach_sound(self._snd)  # noqa: F821
        return task.done
