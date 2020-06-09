"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

API to control Train.
"""
from direct.interval.IntervalGlobal import Parallel
from direct.interval.MopathInterval import MopathInterval


class TrainController:
    """Object to control Train.

    Implements changing Train speed and animation.
    Also manages moving Train along motion paths.

    Args:
        train_mod (panda3d.core.NodePath): Train model.
    """

    def __init__(self, train_mod):
        self._train_mod = train_mod
        self._move_anim_int = None
        # parallel with train model and camera move intervals
        self._move_par = None
        self._is_stopped = False
        self._on_et = False

    def set_controls(self, game, train, train_move_sound):
        """Configure Train control keys and animation.

        Args:
            game (ForwardOnly): The game object.
            train (train.Train): Train object.
            train_move_sound (panda3d.core.AudioSound): Train movement sound.
        """
        self._move_anim_int = self._train_mod.actorInterval("move_forward", playRate=10)
        self._move_anim_int.loop()

        # speed smoothly changes with holding w/s keys pressed
        game.accept(
            "w", self._change_speed_delayed, [game.taskMgr, train_move_sound, 0.05]
        )
        game.accept(
            "s", self._change_speed_delayed, [game.taskMgr, train_move_sound, -0.05]
        )
        game.accept("w-up", self._stop_speed_change, [game.taskMgr])
        game.accept("s-up", self._stop_speed_change, [game.taskMgr])

        game.accept("f", train.toggle_lights, [game.render])

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
                block.path, self._train_mod, duration=4, name="current_path"
            ),
            MopathInterval(  # camera movement
                block.cam_path, train_np, duration=4, name="current_camera_path"
            ),
        )
        self._move_par.setDoneEvent("block_finished")
        self._move_par.start()
        self._move_par.setPlayRate(rate)

    def _stop_speed_change(self, taskMgr):
        """Stop the task which is changing Train speed.

        Args:
            taskMgr (direct.task.Task.TaskManager): Task manager.
        """
        taskMgr.remove("change_train_speed")

    def _change_speed_delayed(self, taskMgr, train_move_sound, diff):
        """Start changing Train speed.

        To make speed changing smoother delayed task is used.

        Args:
            taskMgr (direct.task.Task.TaskManager): Task manager.
            train_move_sound (panda3d.core.AudioSound): Train movement sound.
            diff (float): Coefficient to change Train speed.
        """
        taskMgr.doMethodLater(
            0.6,
            self._change_speed,
            "change_train_speed",
            extraArgs=[train_move_sound, diff],
            appendTask=True,
        )

    def _change_speed(self, train_move_sound, diff, task):
        """Actually change Train speed.

        Args:
            train_move_sound (panda3d.core.AudioSound): Train movement sound.
            diff (float): Coefficient to change Train speed.
            task (panda3d.core.PythonTask): Task object.
        """
        # start movement
        if self._is_stopped and diff > 0:
            self._move_par.resume()
            self._move_anim_int.resume()

            train_move_sound.play()

            self._is_stopped = False

        new_rate = round(self._move_anim_int.getPlayRate() + diff, 2)
        # don't stop on enemy territory
        if self._on_et and new_rate <= 0.35:
            return task.again

        # change speed
        if 0 < new_rate <= 1:
            self._move_anim_int.setPlayRate(new_rate)
            self._move_par.setPlayRate(new_rate)

            new_sound_rate = new_rate * 1.2
            if 0.25 <= new_sound_rate <= 1:
                train_move_sound.setPlayRate(new_sound_rate)

            return task.again

        # stop
        if new_rate == 0:
            self._move_par.pause()
            self._move_anim_int.pause()

            train_move_sound.stop()

            self._is_stopped = True

        return task.done
