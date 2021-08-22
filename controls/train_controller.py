"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

API to control the locomotive and its movement.
"""
from direct.interval.IntervalGlobal import Parallel
from direct.interval.MopathInterval import MopathInterval
from panda3d.core import AudioSound

from utils import drown_snd

MIN_SPEED = 0.5  # minimum speed on enemy territory


class TrainController:
    """Object to control the locomotive.

    Implements changing the locomotive speed and animation.
    Also manages moving the locomotive along motion paths.

    Args:
        model (panda3d.core.NodePath): The locomotive model.
    """

    def __init__(self, model):
        self._model = model
        self._move_snd, self._stop_snd, self._brake_snd = self._set_sounds(model)

        self._move_anim_int = model.actorInterval("move_forward", playRate=14)
        self._move_anim_int.loop()
        # parallel with the Train model and camera move intervals
        self._move_par = Parallel()
        self._is_stopped = False
        self._outing_available = None
        self._move_snd_volume = 1

        self.on_et = False
        self.critical_damage = False
        self.max_speed = 1

    @property
    def current_speed(self):
        """Current locomotive speed.

        Returns
            float: Current locomotive speed (play rate).
        """
        return 0 if self._is_stopped else self._move_anim_int.getPlayRate()

    def _change_speed(self, diff, task):
        """Actually change the locomotive speed.

        Args:
            diff (float): Coefficient to change the Train speed.
        """
        if self._is_stopped and diff > 0:
            self.start_move()

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

    def _change_speed_delayed(self, diff):
        """Start changing the locomotive speed.

        To make speed changing smoother delayed task is used.

        Args:
            diff (float): Coefficient to change speed.
        """
        taskMgr.doMethodLater(  # noqa: F821
            0.6,
            self._change_speed,
            "change_train_speed",
            extraArgs=[diff],
            appendTask=True,
        )

    def _finish_stopping(self, task):
        """Finish stopping the damaged Train."""
        taskMgr.remove("stop_train")  # noqa: F821
        base.train.stop_sparks()  # noqa: F821

        base.main_menu.show(is_game_over=True)  # noqa: F821
        return task.done

    def _set_sounds(self, model):
        """Set interactive locomotive sounds.

        Args:
            model (panda3d.core.NodePath): The locomotive model.

        Returns:
            (panda3d.core.AudioSound...):
                Interactive locomotive sounds.
        """
        move_snd = base.sound_mgr.loadSfx("sounds/train/ride.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(move_snd, model)  # noqa: F821
        move_snd.setLoop(True)
        move_snd.play()

        stop_snd = base.sound_mgr.loadSfx("sounds/train/stop.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(stop_snd, model)  # noqa: F821

        brake_snd = base.sound_mgr.loadSfx("sounds/train/brake.ogg")  # noqa: F821
        brake_snd.setLoop(True)
        base.sound_mgr.attachSoundToObject(brake_snd, model)  # noqa: F821
        return move_snd, stop_snd, brake_snd

    def _stop_move(self):
        """Stop the Train movement."""
        taskMgr.doMethodLater(  # noqa: F821
            0.6, self._stop_snd.play, "train_stop_snd", extraArgs=[]
        )
        base.train.stop_sparks()  # noqa: F821
        self._move_par.pause()
        self._move_anim_int.pause()
        taskMgr.doMethodLater(  # noqa: F821
            0.7, base.train.stop, "release_steam", extraArgs=[]  # noqa: F821
        )

        self._is_stopped = True
        taskMgr.doMethodLater(  # noqa: F821
            0.07,
            drown_snd,
            "drown_move_snd",
            extraArgs=[self._move_snd],
            appendTask=True,
        )
        if self._outing_available:
            base.world.start_outing(self._outing_available)  # noqa: F821
            self._outing_available = None

    def brake_down_to(self, target):
        """Slow down the Train to the given speed.

        Args:
            target (float): Target speed.
        """
        if self._brake_snd.status() == AudioSound.PLAYING:
            self._brake_snd.setVolume(1)
        else:
            self._brake_snd.play()
            taskMgr.doMethodLater(  # noqa: F821
                3,
                drown_snd,
                "drown_brake_snd",
                extraArgs=[self._brake_snd],
                appendTask=True,
            )
        self.slow_down_to(target)

    def drown_move_snd(self):
        """Reduce the main move sound volume."""
        if self._move_snd_volume == 1:
            self._move_snd.setVolume(0.5)
            self._move_snd_volume = 0.5

    def move_along_block(self, block, train_np, do_turn):
        """Start the locomotive move intervals for the given block.

        There are two intervals: the locomotive movement
        and synchronous camera movement.

        Args:
            block (world.block.Block):
                The World block to move along.
            train_np (panda3d.core.NodePath): Train node.
            do_turn (int):
                0 if default direction was chosen,
                1 if a turn is needed.
        """
        self.on_et = block.enemy_territory
        self._outing_available = block.outing_available
        # use speed value from the last block
        rate = self._move_par.getPlayRate() if self._move_par else 1

        is_fork = block.name in ("r_fork", "l_fork", "exit_from_fork")

        self._move_par = Parallel(
            MopathInterval(  # locomotive movement
                block.path[do_turn] if is_fork else block.path,
                self._model,
                duration=4.4,
                name="current_path",
            ),
            MopathInterval(  # camera movement
                block.cam_path[do_turn] if is_fork else block.cam_path,
                train_np,
                duration=4.4,
                name="current_camera_path",
            ),
        )
        self._move_par.setDoneEvent("block_finished")
        self._move_par.start()
        self._move_par.setPlayRate(rate)

    def load_speed(self, speed):
        """Load previously saved locomotive speed.

        Args:
            speed (float): Rate to set for animation, move and sounds.
        """
        self._move_par.setPlayRate(speed)
        self._move_anim_int.setPlayRate(speed)
        self._move_snd.setPlayRate(min(max(0.25, speed * 1.2), 1))
        if not speed:
            self._move_snd.stop()
            self._is_stopped = True

    def pause_movement(self):
        """Make a movement pause (used when a tutorial page is shown)."""
        self._move_par.pause()
        self._move_anim_int.pause()
        self._move_snd.stop()

    def set_controls(self, train):
        """Configure the locomotive control keys.

        Args:
            train (train.Train): The locomotive object.
        """
        # speed smoothly changes while holding w/s keys
        base.accept("w", self._change_speed_delayed, [0.05])  # noqa: F821
        base.accept("s", self._change_speed_delayed, [-0.05])  # noqa: F821
        base.accept("w-up", taskMgr.remove, ["change_train_speed"])  # noqa: F821
        base.accept("s-up", taskMgr.remove, ["change_train_speed"])  # noqa: F821

        base.accept("f", train.toggle_lights)  # noqa: F821

    def start_move(self):
        """Start the Train movement."""
        self._move_par.resume()
        self._move_anim_int.resume()
        self._move_snd.play()
        self._is_stopped = False

    def speed_to_min(self):
        """Accelerate to minimum speed.

        Used when locomotive got on enemy territory.
        """
        taskMgr.remove("change_train_speed")  # noqa: F821
        speed = self._move_anim_int.getPlayRate()
        if speed >= MIN_SPEED:
            return

        # calculate acceleration length
        acc_steps = (MIN_SPEED - speed) / 0.05

        # start accelerating
        taskMgr.doMethodLater(  # noqa: F821
            0.6, self._change_speed, "speed_up_train", extraArgs=[0.05], appendTask=True
        )
        # stop accelerating
        taskMgr.doMethodLater(  # noqa: F821
            0.6 * acc_steps + 0.2,
            taskMgr.remove,  # noqa: F821
            "stop_speedind_up",
            extraArgs=["speed_up_train"],
        )

    def slow_down_to(self, target):
        """Slow down the locomotive to the given speed.

        Args:
            target (float): Target speed.
        """
        taskMgr.remove("change_train_speed")  # noqa: F821

        speed = self._move_anim_int.getPlayRate()
        if speed <= target:
            return

        # calculate deceleration length
        acc_steps = (speed - target) / 0.05

        # start decelerating
        taskMgr.doMethodLater(  # noqa: F821
            0.6,
            self._change_speed,
            "slow_down_train",
            extraArgs=[-0.05],
            appendTask=True,
        )
        # stop decelerating
        taskMgr.doMethodLater(  # noqa: F821
            0.6 * acc_steps + 0.2,
            taskMgr.remove,  # noqa: F821
            "stop_slowing_down",
            extraArgs=["slow_down_train"],
        )

    def stop(self, urgent=False, place_of_interest=False):
        """Completely stop the locomotive.

        Args:
            urgent (bool):
                If True, deceleration speed will be much higher.
                Used for stopping in places of interest and cities.
            place_of_interest (bool):
                If True, that means the stop is
                initiated by a place of interest.
        """
        base.ignore("w")  # noqa: F821
        base.ignore("s")  # noqa: F821
        taskMgr.remove("change_train_speed")  # noqa: F821

        delay = 0.25 if urgent else 0.6

        # calculate deceleration length
        speed = self._move_anim_int.getPlayRate()
        taskMgr.doMethodLater(  # noqa: F821
            delay, self._change_speed, "stop_train", extraArgs=[-0.05], appendTask=True
        )

        if urgent:
            if place_of_interest:
                taskMgr.doMethodLater(  # noqa: F821
                    delay * (speed / 0.05) + 0.8,
                    base.scenario.start_chapter,  # noqa: F821
                    "start_scenario_chapter",
                )
        else:
            # stop decelerating
            taskMgr.doMethodLater(  # noqa: F821
                delay * (speed / 0.05) + 0.8, self._finish_stopping, "finish_stopping"
            )
            taskMgr.doMethodLater(  # noqa: F821
                delay * (speed / 0.05) + 0.2,
                base.world.enemy.stop_ride_anim,  # noqa: F821
                "stop_riding",
            )

    def raise_move_snd(self):
        """Restore full volume of the main move sound."""
        if self._move_snd_volume == 0.5:
            self._move_snd.setVolume(1)
            self._move_snd_volume = 1

    def unset_controls(self):
        """Disable all the locomotive controls."""
        for key in ("w", "s", "w-up", "s-up", "f"):
            base.ignore(key)  # noqa: F821
