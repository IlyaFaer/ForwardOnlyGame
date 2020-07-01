"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

API to control Train and its movement.
"""
from direct.interval.IntervalGlobal import Parallel
from direct.interval.MopathInterval import MopathInterval

MIN_SPEED = 0.5


class TrainController:
    """Object to control Train.

    Implements changing Train speed and animation.
    Also manages moving Train along motion paths.

    Args:
        model (panda3d.core.NodePath): Train model.
        move_snd (panda3d.core.AudioSound): Train movement sound.
    """

    def __init__(self, model, move_snd):
        self._model = model
        self._move_snd = move_snd

        self._move_anim_int = model.actorInterval("move_forward", playRate=14)
        self._move_anim_int.loop()
        # parallel with train model and camera move intervals
        self._move_par = None
        self._is_stopped = False
        self._on_et = False

        self.critical_damage = False

    def set_controls(self, train):
        """Configure Train control keys.

        Args:
            train (train.Train): Train object.
        """
        # speed smoothly changes with holding w/s keys pressed
        base.accept("w", self._change_speed_delayed, [0.05])  # noqa: F821
        base.accept("s", self._change_speed_delayed, [-0.05])  # noqa: F821
        base.accept("w-up", base.taskMgr.remove, ["change_train_speed"])  # noqa: F821
        base.accept("s-up", base.taskMgr.remove, ["change_train_speed"])  # noqa: F821

        base.accept("f", train.toggle_lights)  # noqa: F821

    def move_along_block(self, block, train_np):
        """Start Train move intervals for the given block.

        There are two intervals: Train movement and
        synchronous camera movement.

        Args:
            block (world.block.Block): World block to move along.
            train_np (panda3d.core.NodePath): Train node.
        """
        self._on_et = block.enemy_territory
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
        self._move_par.pause()
        self._move_anim_int.pause()
        self._move_snd.stop()
        self._is_stopped = True

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
            self._on_et  # don't stop on enemy territory
            and new_rate <= MIN_SPEED
            and diff < 0
            # stop on enemy territory only
            # in case of critical damage
            and not self.critical_damage
        ):
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
            0.6 * (speed / 0.05) + 0.8,
            base.taskMgr.remove,  # noqa: F821
            "finish_stopping",
            extraArgs=["stop_train"],
        )
        base.taskMgr.doMethodLater(  # noqa: F821
            0.6 * (speed / 0.05) + 0.2,
            base.world.enemy.stop_ride_anim,  # noqa: F821
            "stop_riding",
        )
