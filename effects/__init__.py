"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The game visual effects API.
"""
from direct.filter.CommonFilters import CommonFilters
from direct.particles.ParticleEffect import ParticleEffect
from direct.showbase.Transitions import Transitions
from panda3d.core import (
    Fog,
    GraphicsOutput,
    NodePath,
    PointLight,
    Texture,
)

from utils import drown_snd


class EffectsManager:
    """Manager to control the game visual effects."""

    def __init__(self):
        base.enableParticles()  # noqa: F821
        render.setShaderAuto()  # noqa: F821

        self._explosion_lights = self._set_explosion_lights()

        self._transition = Transitions(loader)  # noqa: F821
        self._transition.setFadeColor(0, 0, 0)

        self.stench_effect = Stench()
        self.love_fog = LoveFog()

        filters = CommonFilters(base.win, base.cam)  # noqa: F821
        filters.setBloom(size="large", mintrigger=0.8, intensity=2.1)

    def _set_explosion_lights(self):
        """Prepare three explosion lights.

        Build a list-pool of light objects to
        be used in different explosions.

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

    def bomb_explosion(self, parent):
        """Prepare a bomb explosion effect for the given object.

        Args:
            parent (object): Must include "model" property.

        Returns:
            BombExplosion: Hand bomb explosion effect object.
        """
        return BombExplosion(parent)

    def burn_smoke(self, parent):
        """Prepare a burning object smoke effect.

        Args:
            parent (object): Must include "id" and "model" properties.

        Returns:
            BurnSmoke: Burning object smoke effect.
        """
        return BurnSmoke(parent)

    def explosion(self, parent):
        """Prepare an explosion effect for the given object.

        Args:
            parent (object): Must include "id" and "model" properties.

        Returns:
            Explosion: Explosion effect object.
        """
        return Explosion(self._explosion_lights, parent, "explode_fire", 1.5)

    def explosion_big(self, parent):
        """Prepare a big explosion effect for the given object.

        Args:
            parent (object): Must include "id" and "model" properties.

        Returns:
            Explosion: Explosion effect object.
        """
        return Explosion(self._explosion_lights, parent, "explode_fire2", 2.1)

    def fade_in_screen(self, task):
        """Smoothly fill the screen with natural colors."""
        self._transition.fadeIn(3)
        return task.done

    def fade_out_screen(self, task):
        """Smoothly fill the screen with black color."""
        self._transition.fadeOut(3)
        return task.done


class Explosion:
    """An explosion effect.

    Includes sound, light and particle effects.

    Args:
        explode_lights (list): Explosion lights pool.
        parent (object): Object to explode.
        ptf (str): Name of the particles file to use.
        length (float): The length of the effect.
    """

    def __init__(self, explode_lights, parent, ptf, length):
        self._length = length
        self._parent = parent

        self._lights = explode_lights
        self._light_coef = 1.5

        self._sparks = ParticleEffect()
        self._sparks.loadConfig("effects/explode_sparks.ptf")
        self._sparks.setY(0.2)

        self._fire = ParticleEffect()
        self._fire.loadConfig("effects/{}.ptf".format(ptf))
        self._fire.setY(0.1)

        self._snd = base.sound_mgr.loadSfx("sounds/combat/explosion1.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(self._snd, parent.model)  # noqa: F821

    def _clear(self, task):
        """Clear this explosion effect."""
        self._sparks.cleanup()
        self._fire.cleanup()
        base.sound_mgr.detach_sound(self._snd)  # noqa: F821
        return task.done

    def _light_change(self, light, task):
        """Change the explosion light attenuation.

        Implements a gradual (but fast) fall off of the light power.

        Args:
            light (panda3d.core.NodePath): Explosion light object.
        """
        self._light_coef += 0.1

        if self._light_coef >= 10:
            self._lights.append(light)
            light.detachNode()
            light.node().setAttenuation((0, 0, 1))
            return task.done

        light.node().setAttenuation((self._light_coef - 1, 0, self._light_coef))
        return task.again

    def play(self):
        """Do the actual explosion and plan its clearing."""
        self._snd.play()
        self._sparks.start(self._parent.model, render)  # noqa: F821
        self._fire.start(self._parent.model, render)  # noqa: F821

        if self._lights:
            light = self._lights.pop()
            light.reparentTo(self._parent.model)
            light.setPos(0)

            taskMgr.doMethodLater(  # noqa: F821
                0.02,
                self._light_change,
                self._parent.id + "_explosion_light",
                extraArgs=[light],
                appendTask=True,
            )

        taskMgr.doMethodLater(  # noqa: F821
            0.8,
            self._fire.softStop,
            self._parent.id + "_disable_exlode_fire",
            extraArgs=[],
        )

        taskMgr.doMethodLater(  # noqa: F821
            self._length,
            self._fire.disable,
            self._parent.id + "_disable_exlode_fire",
            extraArgs=[],
        )
        taskMgr.doMethodLater(  # noqa: F821
            4.95,
            self._sparks.disable,
            self._parent.id + "_disable_exlode_sparks",
            extraArgs=[],
        )
        taskMgr.doMethodLater(  # noqa: F821
            5.05, self._clear, self._parent.id + "_clear_explode"
        )


class BurnSmoke:
    """Smoke from a burning object effect.

    Args:
        parent (object): Object to parent the effect to.
    """

    def __init__(self, parent):
        self._parent = parent
        self._smoke = ParticleEffect()
        self._smoke.loadConfig("effects/after_explode_smoke1.ptf")

    def _clear_smoke(self, task):
        """Clear the smoke effect."""
        self._smoke.softStop()
        self._smoke.cleanup()
        return task.done

    def play(self):
        """Start playing the particle effect."""
        self._smoke.start(self._parent.model, render)  # noqa: F821
        taskMgr.doMethodLater(  # noqa: F821
            11, self._clear_smoke, self._parent.id + "_stop_smoke"
        )


class BombExplosion:
    """A hand bomb explosion reusable effect.

    Includes sound and particle effects.

    Args:
        parent (object): Object to explode. Must include "model" property.
    """

    def __init__(self, parent):
        self._parent = parent

        self._smoke = ParticleEffect()
        self._smoke.loadConfig("effects/bomb_smoke1.ptf")

        self._sparks = ParticleEffect()
        self._sparks.loadConfig("effects/white_sparks1.ptf")

        self._snd = base.sound_mgr.loadSfx(  # noqa: F821
            "sounds/combat/bomb_explosion1.ogg"
        )
        base.sound_mgr.attachSoundToObject(self._snd, parent.model)  # noqa: F821

    def _stop_explosion(self, task):
        """Disable explosion effect."""
        self._smoke.softStop()
        self._sparks.softStop()
        return task.done

    def play(self):
        """Make actual explosion and plan its stop."""
        self._snd.play()
        self._smoke.start(self._parent.model, render)  # noqa: F821
        self._sparks.start(self._parent.model, render)  # noqa: F821
        self._smoke.softStart()
        self._sparks.softStart()

        taskMgr.doMethodLater(  # noqa: F821
            2.49, self._stop_explosion, "train_disable_bomb_explosion"
        )

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
    """All the Stench visual effects and sounds as a single object."""

    def __init__(self):
        self._is_playing = False
        self._nextclick = 0

        background = NodePath("background")
        background.setDepthTest(0)
        background.setDepthWrite(0)

        self._snd1 = loader.loadSfx("sounds/Stench/hollow.ogg")  # noqa: F821
        self._snd1.setLoop(True)
        self._snd2 = loader.loadSfx("sounds/Stench/creepy.ogg")  # noqa: F821
        self._snd2.setLoop(True)
        self._snd3 = loader.loadSfx("sounds/Stench/breathing.ogg")  # noqa: F821
        self._snd3.setLoop(True)
        self._snd4 = loader.loadSfx("sounds/Stench/teeth.ogg")  # noqa: F821
        self._snd4.setLoop(True)

        self._stench = ParticleEffect()
        self._stench.loadConfig("effects/stench.ptf")
        self._stench.setPos(0, 3.5, 0.3)

        self._fog = Fog("Stench")
        self._fog.setColor(1, 0.69, 0)
        self._fog.setExpDensity(0.1)

        tex = Texture()
        tex.setMinfilter(Texture.FTLinear)
        base.win.addRenderTexture(  # noqa: F821
            tex, GraphicsOutput.RTMTriggeredCopyTexture
        )
        taskMgr.add(self._snapshot, "tex_snapshot")  # noqa: F821

        self._bcard = base.win.getTextureCard()  # noqa: F821
        self._bcard.reparentTo(background)  # noqa: F821
        self._bcard.setTransparency(1)
        self._bcard.setColor(1, 1, 1, 1)
        self._bcard.setScale(1)
        self._bcard.hide()

        self._fcard = base.win.getTextureCard()  # noqa: F821
        self._fcard.reparentTo(base.render2d)  # noqa: F821
        self._fcard.setTransparency(1)
        self._fcard.setColor(1, 1, 1, 0.4)
        self._fcard.setScale(1.08)
        self._fcard.hide()

    @property
    def is_playing(self):
        """Flag indicating if the Stench effect is playing.

        Returns:
            bool:
                True, if the Stench effect is playing, False otherwise.
        """
        return self._is_playing

    def _snapshot(self, task):
        """Make snapshot of the screen."""
        if task.time > self._nextclick:
            self._nextclick += 0.001
            if self._nextclick < task.time:
                self._nextclick = task.time
            base.win.triggerCopy()  # noqa: F821

        return task.cont

    def set_fog(self):
        """Turn on fog."""
        render.setFog(self._fog)  # noqa: F821

    def play(self):
        """Start playing the Stench visual effects and sounds."""
        if self._is_playing:
            return

        self._is_playing = True

        render.setFog(self._fog)  # noqa: F821
        self._bcard.show()
        self._fcard.show()

        self._snd1.play()
        self._snd2.play()
        self._snd3.play()
        self._snd4.play()
        base.effects_mgr.love_fog.switch()  # noqa: F821
        base.effects_mgr.love_fog.switch()  # noqa: F821

    def play_clouds(self):
        """Start playing the Stench particle effect."""
        if self._is_playing:
            return

        self._stench.start(base.train.model, render)  # noqa: F821
        self._stench.softStart()

    def stop(self):
        """Stop playing the Stench effects and sounds."""
        if not self._is_playing:
            return

        self._is_playing = False

        taskMgr.doMethodLater(  # noqa: F821
            0.2, drown_snd, "drown_stench_snd1", extraArgs=[self._snd1], appendTask=True
        )
        taskMgr.doMethodLater(  # noqa: F821
            0.2, drown_snd, "drown_stench_snd2", extraArgs=[self._snd2], appendTask=True
        )
        taskMgr.doMethodLater(  # noqa: F821
            0.2, drown_snd, "drown_stench_snd3", extraArgs=[self._snd3], appendTask=True
        )
        taskMgr.doMethodLater(  # noqa: F821
            0.2, drown_snd, "drown_stench_snd4", extraArgs=[self._snd4], appendTask=True
        )
        self._stench.softStop()

        self._fcard.hide()
        self._bcard.hide()

        render.clearFog()  # noqa: F821

        if base.effects_mgr.love_fog.is_on:  # noqa: F821
            base.effects_mgr.love_fog.is_on = False  # noqa: F821
            base.effects_mgr.love_fog.switch()  # noqa: F821


class LoveFog:
    """St. Valentines Day mode effect."""

    def __init__(self):
        self.is_on = False
        self._love_fog = Fog("Love")
        self._love_fog.setColor(0.7, 0.42, 0.49)
        self._love_fog.setExpDensity(0.25)

    def switch(self):
        """Switch on/off the effect."""
        if self.is_on:
            render.clearFog()  # noqa: F821
            base.train.love_particles(False)  # noqa: F821
            if base.effects_mgr.stench_effect.is_playing:  # noqa: F821
                base.effects_mgr.stench_effect.set_fog()  # noqa: F821
        else:
            render.setFog(self._love_fog)  # noqa: F821
            base.train.love_particles(True)  # noqa: F821

        self.is_on = not self.is_on
