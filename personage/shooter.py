"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Base API for shooting units.
"""
import abc

from direct.interval.IntervalGlobal import (
    LerpScaleInterval,
    Parallel,
    Sequence,
    SoundInterval,
)

from utils import address


class Shooter(metaclass=abc.ABCMeta):
    """Base class for all shooters."""

    def __init__(self):
        self._shoot_anim = None
        self._target = None

        self.current_part = None
        self.shot_snd = None

    @abc.abstractmethod
    def _missed_shot(self):
        """Method to calculate if shooter missed the shot.

        Returns:
            bool: True, if this shooter missed the shot.
        """
        raise NotImplementedError(
            "Every shooter class must have _missed_shot() method."
        )

    @abc.abstractproperty
    def shooting_speed(self):
        raise NotImplementedError(
            "Every shooter class must have shooting_speed property."
        )

    def _die(self):
        """Die actions for this shooter.

        Returns:
            bool: True, if this shooter dies for the first time.
        """
        if self.is_dead:
            return False

        self._stop_tasks("_aim", "_shoot", "_choose_target")
        self._shoot_anim.finish()
        return True

    def _shoot(self, task):
        """Play shooting animation and sound, make damage."""
        self._shoot_anim.start()
        if not self._missed_shot():
            self._target.get_damage(self.damage)

        task.delayTime = self.shooting_speed
        return task.again

    def _set_shoot_anim(self, pos, angle, shots):
        """Prepare gun fire animation and sounds.

        Args:
            pos (tuple): Position to set fire.
            angle (int): Angle to set fire.
            shots (int): Number of shots in animation.

        Returns:
            direct.interval.MetaInterval.Sequence:
                Shooting sequence.
        """
        fire = loader.loadModel(address("gun_fire1"))  # noqa: F821
        fire.reparentTo(self.model)
        fire.setScale(1, 0.0001, 1)
        fire.setPos(*pos)
        fire.setH(angle)

        shoot_seq = Parallel(
            Sequence(
                LerpScaleInterval(fire, 0.12, (1, 1, 1)),
                LerpScaleInterval(fire, 0.12, (1, 0.0001, 1)),
            ),
            SoundInterval(self.shot_snd, duration=0.3),
        )
        return Sequence(*(shoot_seq,) * shots)

    def _set_shoot_snd(self, name):
        """Attach the shooting sound to the model.

        Args:
            name (str): Name of the shooting sound.

        Returns:
            panda3d.core.AudioSound: Shooting sound.
        """
        shot_snd = base.sound_mgr.loadSfx(  # noqa: F821
            "sounds/{name}.ogg".format(name=name)
        )
        base.sound_mgr.attachSoundToObject(shot_snd, self.model)  # noqa: F821
        return shot_snd
