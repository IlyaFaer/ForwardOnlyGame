"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Visual effects API.
"""
from direct.particles.ParticleEffect import ParticleEffect
from direct.showbase.Transitions import Transitions
from panda3d.core import (
    Fog,
    GraphicsOutput,
    NodePath,
    PointLight,
    Texture,
)


class EffectsManager:
    """Manager to control game visual effects."""

    def __init__(self):
        self._explosion_lights = self._set_explosion_lights()

        self._transition = Transitions(loader)  # noqa: F821
        self._transition.setFadeColor(0, 0, 0)

        self.stench_effect = Stench()

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

    def fade_out_screen(self, task):
        """Smoothly fill the screen with black color."""
        self._transition.fadeOut(3)
        return task.done

    def fade_in_screen(self, task):
        """Smoothly fill the screen with natural colors."""
        self._transition.fadeIn(3)
        return task.done

    def explosion(self, parent):
        """Prepare an explosion effect for the given object.

        Args:
            parent (object):
                Must include "id" and "model" properties.

        Returns:
            Explosion: Explosion effect object.
        """
        return Explosion(self._explosion_lights, parent)

    def bomb_explosion(self, parent):
        """Prepare a bomb explosion effect for the given object.

        Args:
            parent (object):
                Must include "model" property.

        Returns:
            BombExplosion: Hand bomb explosion effect object.
        """
        return BombExplosion(parent)


class Explosion:
    """An explosion effect.

    Includes sound, light and particle effects.

    Args:
        explode_lights (list): List of explosion lights.
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
            light.setPos(0)

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
        """Change the explosion light attenuation.

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
        """Disable sparks particle effect."""
        self._sparks.disable()
        return task.done

    def _stop_fire(self, task):
        """Disable fire particle effect."""
        self._fire.disable()
        return task.done

    def _clear(self, task):
        """Clear this explosion effect."""
        self._sparks.cleanup()
        self._fire.cleanup()
        base.sound_mgr.detach_sound(self._snd)  # noqa: F821
        return task.done


class BombExplosion:
    """A hand bomb explosion effect.

    Includes sound and particle effects.

    Args:
        parent (object): Object to explode.
    """

    def __init__(self, parent):
        self._parent = parent

        self._smoke = ParticleEffect()
        self._smoke.loadConfig("effects/bomb_smoke1.ptf")

        self._sparks = ParticleEffect()
        self._sparks.loadConfig("effects/white_sparks1.ptf")

        self._snd = base.sound_mgr.loadSfx("sounds/bomb_explosion1.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(self._snd, parent.model)  # noqa: F821

    def play(self):
        """Make actual explosion and plan its stop."""
        self._snd.play()
        self._smoke.start(self._parent.model, render)  # noqa: F821
        self._sparks.start(self._parent.model, render)  # noqa: F821
        self._smoke.softStart()
        self._sparks.softStart()

        base.taskMgr.doMethodLater(  # noqa: F821
            2.49, self._stop_explosion, "train_disable_bomb_explosion"
        )

    def _stop_explosion(self, task):
        """Disable explosion effect."""
        self._smoke.softStop()
        self._sparks.softStop()
        return task.done

    def setPos(self, x, y, z):
        """Set explosion position.

        Args:
            x (float): X coordinate.
            y (float): Y coordinate.
            z (float): Z coordinate.
        """
        self._smoke.setPos(x, y, z)
        self._sparks.setPos(x, y, z)


class Stench:
    """All the Stench visual effects and sounds as an object."""

    def __init__(self):
        background = NodePath("background")
        background.setDepthTest(0)
        background.setDepthWrite(0)

        tex = Texture()
        tex.setMinfilter(Texture.FTLinear)
        base.win.addRenderTexture(  # noqa: F821
            tex, GraphicsOutput.RTMTriggeredCopyTexture
        )
        tex.setClearColor((0, 0, 0, 1))
        tex.clearImage()

        bcard = base.win.getTextureCard()  # noqa: F821
        bcard.reparentTo(background)  # noqa: F821
        bcard.setTransparency(1)
        bcard.show()
        bcard.setColor(1, 1, 1, 1)
        bcard.setScale(1.0)

        fcard = base.win.getTextureCard()  # noqa: F821
        fcard.reparentTo(base.render2d)  # noqa: F821
        fcard.setTransparency(1)
        fcard.show()
        fcard.setColor(1, 1, 1, 0.4)
        fcard.setScale(1.08)

        self._nextclick = 0

        self._snd1 = loader.loadSfx("sounds/hollow1.ogg")  # noqa: F821
        self._snd1.setLoop(True)
        self._snd2 = loader.loadSfx("sounds/creepy1.ogg")  # noqa: F821
        self._snd2.setLoop(True)
        self._snd3 = loader.loadSfx("sounds/breathing1.ogg")  # noqa: F821
        self._snd3.setLoop(True)
        self._snd4 = loader.loadSfx("sounds/teeth.ogg")  # noqa: F821
        self._snd4.setLoop(True)

    def play(self):
        """Start playing the Stench effects and sounds."""
        fog = Fog("Stench")
        fog.setColor(1, 0.64, 0)
        fog.setExpDensity(0.1)
        render.setFog(fog)  # noqa: F821

        base.taskMgr.add(self._snapshot, "_snapshot")  # noqa: F821
        self._snd1.play()
        self._snd2.play()
        self._snd3.play()
        self._snd4.play()

    def _snapshot(self, task):
        """Make snapshot of the screen."""
        if task.time > self._nextclick:
            self._nextclick += 1.0 / 1000
            if self._nextclick < task.time:
                self._nextclick = task.time
            base.win.triggerCopy()  # noqa: F821

        return task.cont
