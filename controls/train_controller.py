"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

API to control Train and its movement.
"""
from direct.interval.IntervalGlobal import Parallel
from direct.interval.MopathInterval import MopathInterval
from panda3d.core import AudioSound

MIN_SPEED = 0.5


class TrainController:
    """Object to control Train.

    Implements changing Train speed and animation.
    Also manages moving Train along motion paths.

    Args:
        model (panda3d.core.NodePath): Train model.
        move_snd (panda3d.core.AudioSound): Train movement sound.
        stop_snd (panda3d.core.AudioSound): Train stopping sound.
        brake_snd (panda3d.core.AudioSound): Train braking sound.
    """

    def __init__(self, model, move_snd, stop_snd, brake_snd):
        self._model = model
        self._move_snd = move_snd
        self._stop_snd = stop_snd
        self._brake_snd = brake_snd

        self._move_anim_int = model.actorInterval("move_forward", playRate=14)
        self._move_anim_int.loop()
        # parallel with the Train model and camera move intervals
        self._move_par = None
        self._is_stopped = False
        self._outing_available = None

        self.on_et = False
        self.critical_damage = False
        self.max_speed = 1

    @property
    def current_speed(self):
        """Current Train speed.

        Returns
            float: Current Train speed.
        """
        return 0 if self._is_stopped else self._move_anim_int.getPlayRate()

    def set_controls(self, train):
        """Configure Train control keys.

        Args:
            train (train.Train): The Train object.
        """
        # speed smoothly changes with holding w/s keys pressed
        base.accept("w", self._change_speed_delayed, [0.05])  # noqa: F821
        base.accept("s", self._change_speed_delayed, [-0.05])  # noqa: F821
        base.accept("w-up", base.taskMgr.remove, ["change_train_speed"])  # noqa: F821
        base.accept("s-up", base.taskMgr.remove, ["change_train_speed"])  # noqa: F821

        base.accept("f", train.toggle_lights)  # noqa: F821

    def unset_controls(self):
        """Disable all the Train controls."""
        for key in ("w", "s", "w-up", "s-up", "f"):
            base.ignore(key)  # noqa: F821

    def move_along_block(self, block, train_np):
        """Start Train move intervals for the given block.

        There are two intervals: the Train movement and
        synchronous camera movement.

        Args:
            block (world.block.Block): World block to move along.
            train_np (panda3d.core.NodePath): Train node.
        """
        self.on_et = block.enemy_territory
        self._outing_available = block.outing_available
        # use speed value from the last block
        rate = self._move_par.getPlayRate() if self._move_par else 1

        self._move_par = Parallel(
            MopathInterval(  # Train movement
                block.path, self._model, duration=4, name="current_path"
            ),
            MopathInterval(  # camera movement
                block.cam_path, train_np, duration=4, name="current_camera_path"
            ),
        )
        self._move_par.setDoneEvent("block_finished")
        self._move_par.start()
        self._move_par.setPlayRate(rate)

    def load_speed(self, speed, task):
        """Load previously saved Train speed.

        Args:
            speed (float):
                Rate to set for animation, move and sound intervals.
        """
        self._move_par.setPlayRate(speed)
        self._move_anim_int.setPlayRate(speed)
        self._move_snd.setPlayRate(min(max(0.25, speed * 1.2), 1))
        if not speed:
            self._move_snd.stop()
            self._is_stopped = True

        return task.done

    def _change_speed_delayed(self, diff):
        """Start changing Train speed.

        To make speed changing smoother delayed task is used.

        Args:
            diff (float): Coefficient to change Train speed.
        """
        base.taskMgr.doMethodLater(  # noqa: F821
            0.6,
            self._change_speed,
            "change_train_speed",
            extraArgs=[diff],
            appendTask=True,
        )

    def _start_move(self):
        """Start Train movement."""
        self._move_par.resume()
        self._move_anim_int.resume()
        self._move_snd.play()
        self._is_stopped = False

    def _stop_move(self):
        """Stop Train movement."""
        base.taskMgr.doMethodLater(  # noqa: F821
            0.6, self._play_stop_snd, "train_stop_snd"
        )
        base.train.stop_sparks()  # noqa: F821
        self._move_par.pause()
        self._move_anim_int.pause()
        self._is_stopped = True
        base.taskMgr.doMethodLater(  # noqa: F821
            0.06,
            self._drown_snd,
            "drown_move_snd",
            extraArgs=[self._move_snd],
            appendTask=True,
        )
        if self._outing_available:
            base.world.start_outing(self._outing_available)  # noqa: F821

    def _play_stop_snd(self, task):
        """Play Train stop sound."""
        self._stop_snd.play()
        return task.done

    def _change_speed(self, diff, task):
        """Actually change Train speed.

        Args:
            diff (float): Coefficient to change Train speed.
            task (panda3d.core.PythonTask): Task object.
        """
        if self._is_stopped and diff > 0:
            self._start_move()

        new_rate = round(self._move_anim_int.getPlayRate() + diff, 2)
        if (
            self.on_et  # don't stop on enemy territory
            and diff < 0
            # stop on enemy territory only
            # in case of critical damage
            and not self.critical_damage
            and new_rate < MIN_SPEED
        ):
            return task.again

        if new_rate > self.max_speed and diff > 0:
            return task.again

        # change speed
        if 0 < new_rate <= 1:
            self._move_anim_int.setPlayRate(new_rate)
            self._move_par.setPlayRate(new_rate)

            new_snd_rate = new_rate * 1.2
            if 0.25 <= new_snd_rate <= 1:
                self._move_snd.setPlayRate(new_snd_rate)

            return task.again

        if new_rate == 0:
            self._stop_move()

        return task.done

    def speed_to_min(self):
        """Accelerate to minimum combat speed."""
        base.taskMgr.remove("change_train_speed")  # noqa: F821
        speed = self._move_anim_int.getPlayRate()
        if speed >= MIN_SPEED:
            return

        # calculate acceleration length
        acc_steps = (MIN_SPEED - speed) / 0.05

        # start accelerating
        base.taskMgr.doMethodLater(  # noqa: F821
            0.6, self._change_speed, "speed_up_train", extraArgs=[0.05], appendTask=True
        )
        # stop accelerating
        base.taskMgr.doMethodLater(  # noqa: F821
            0.6 * acc_steps + 0.2,
            base.taskMgr.remove,  # noqa: F821
            "stop_speedind_up",
            extraArgs=["speed_up_train"],
        )

    def brake_down_to(self, target):
        """Slow down the Train to the given speed.

        Args:
            target (float): Target speed.
        """
        if self._brake_snd.status() == AudioSound.PLAYING:
            self._brake_snd.setVolume(1)
        else:
            self._brake_snd.play()
            base.taskMgr.doMethodLater(  # noqa: F821
                3,
                self._drown_snd,
                "drown_brake_snd",
                extraArgs=[self._brake_snd],
                appendTask=True,
            )
        self.slow_down_to(target)

    def slow_down_to(self, target):
        """Slow down the Train to the given speed.

        Args:
            target (float): Target speed.
        """
        base.taskMgr.remove("change_train_speed")  # noqa: F821

        speed = self._move_anim_int.getPlayRate()
        if speed <= target:
            return

        # calculate deceleration length
        acc_steps = (speed - target) / 0.05

        # start decelerating
        base.taskMgr.doMethodLater(  # noqa: F821
            0.6,
            self._change_speed,
            "slow_down_train",
            extraArgs=[-0.05],
            appendTask=True,
        )
        # stop decelerating
        base.taskMgr.doMethodLater(  # noqa: F821
            0.6 * acc_steps + 0.2,
            base.taskMgr.remove,  # noqa: F821
            "stop_slowing_down",
            extraArgs=["slow_down_train"],
        )

    def _drown_snd(self, snd, task):
        """Drown the given sounds."""
        volume = snd.getVolume()
        if volume <= 0:
            snd.stop()
            snd.setVolume(1)
            return task.done

        snd.setVolume(volume - 0.1)
        return task.again

    def stop(self):
        """Completely stop Train."""
        base.ignore("w")  # noqa: F821
        base.ignore("s")  # noqa: F821

        base.taskMgr.remove("change_train_speed")  # noqa: F821

        # calculate deceleration length
        speed = self._move_anim_int.getPlayRate()
        base.taskMgr.doMethodLater(  # noqa: F821
            0.6, self._change_speed, "stop_train", extraArgs=[-0.05], appendTask=True
        )
        # stop decelerating
        base.taskMgr.doMethodLater(  # noqa: F821
            0.6 * (speed / 0.05) + 0.8, self._finish_stopping, "finish_stopping"
        )
        base.taskMgr.doMethodLater(  # noqa: F821
            0.6 * (speed / 0.05) + 0.2,
            base.world.enemy.stop_ride_anim,  # noqa: F821
            "stop_riding",
        )

    def _finish_stopping(self, task):
        """Finish stopping damaged Train."""
        base.taskMgr.remove("stop_train")  # noqa: F821
        base.train.stop_sparks()  # noqa: F821
        return task.done
