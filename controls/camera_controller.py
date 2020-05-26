"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Camera configuring and controls.
"""
from direct.interval.LerpInterval import LerpPosInterval, LerpHprInterval
from panda3d.core import Vec3


class CameraController:
    """Object to configure camera and its controls."""

    def __init__(self):
        self._target = Vec3(2, 0, 3)  # final pos of the current movement
        self._move_int = None  # current move interval
        self._turn_int = None  # current rotation interval
        self._is_centered = False

        # camera position before toggling centered view
        self._last_cam_pos = None
        self._last_cam_hpr = None
        self._last_cam_np_hpr = None

    def set_controls(self, game, cam, train):
        """Configure camera, its node and set keyboard keys to control the camera.

        Args:
            game (ForwardOnly): Game object.
            cam (panda3d.core.NodePath): Main camera object.
            train (train.Train): Train object.
        """
        cam_np = train.node.attachNewNode("camera_node")
        cam.reparentTo(cam_np)
        cam.setPos(self._target)
        cam.lookAt(train.model)

        self._set_move_keys(game, cam_np, cam)
        game.accept("c", self._toggle_centered_view, [game, cam_np, cam])

    def _move(self, cam_np, cam, x, y, time):
        """Start camera movement with a single interval (on key press).

        Args:
            cam_np (panda3d.core.NodePath): Camera node.
            cam (panda3d.core.NodePath): Camera object.
            x (float): Translation along x axis.
            y (float): Translation along y axis.
            time (float): Interval length.
        """
        if self._move_int is not None:
            self._move_int.pause()

        if x:
            self._target.setX(x)
        else:
            self._target.setY(y)

        self._move_int = LerpPosInterval(cam, time, self._target, other=cam_np)
        self._move_int.start()

    def _turn(self, cam_np, h, r):
        """Turn camera with a single interval (on key press).

        Args:
            cam_np (panda3d.core.NodePath): Camera node.
            h (int): Translation for camera heading, angle.
            r (int): Translation for camera rolling, angle.
        """
        if self._turn_int is not None and self._turn_int.isPlaying():
            return

        self._turn_int = LerpHprInterval(cam_np, 4, (cam_np.getH() + h, 0, r))
        self._turn_int.start()

    def _stop(self, cam_np, cam, stop_x, is_hard=False):
        """Stop moving and rotating camera (on key release).

        Args:
            cam_np (panda3d.core.NodePath): Camera node.
            cam (panda3d.core.NodePath): Camera object.
            stop_x (bool):
                True - movement along x axis should be stopped.
                False - movement along y axis should be stopped.
            is_hard (bool):
                If False, camera will be stopped with an deceleration
                interval. If True, stopping will be immediate.
        """
        if self._move_int is not None:
            self._move_int.pause()

        if self._turn_int is not None:
            self._turn_int.pause()

        if stop_x:
            self._target.setX(cam.getX())
        else:
            self._target.setY(cam.getY())

        if not is_hard:
            self._move_int = LerpPosInterval(cam, 0.75, self._target, other=cam_np)
            self._move_int.start()

    def _set_move_keys(self, game, cam_np, cam):
        """Set camera move and rotate keys.

        Args:
            game (ForwardOnly): Game object.
            cam_np (panda3d.core.NodePath): Camera node object.
            cam (panda3d.core.NodePath): Main camera object.
        """
        # key pressed - start movement
        game.accept("arrow_up", self._move, [cam_np, cam, 1, None, 1.5])
        game.accept("arrow_down", self._move, [cam_np, cam, 2, None, 0.75])
        game.accept("arrow_left", self._move, [cam_np, cam, None, -1.1, 0.9])
        game.accept("arrow_right", self._move, [cam_np, cam, None, 1.1, 0.9])

        # key released - stop
        game.accept("arrow_up-up", self._stop, [cam_np, cam, True])
        game.accept("arrow_down-up", self._stop, [cam_np, cam, True])
        game.accept("arrow_left-up", self._stop, [cam_np, cam, False])
        game.accept("arrow_right-up", self._stop, [cam_np, cam, False])

        # key pressed - start turning
        game.accept("alt-arrow_left", self._turn, [cam_np, -360, 0])
        game.accept("alt-arrow_right", self._turn, [cam_np, 360, 0])
        game.accept("alt-arrow_up", self._turn, [cam_np, 0, -60])
        game.accept("alt-arrow_down", self._turn, [cam_np, 0, 25])

    def _toggle_centered_view(self, game, cam_np, cam):
        """Set camera onto default position.

        Centered position is optimal for characters
        manipulations. Press repeating returns camera to
        the previous position.

        Args:
            game (ForwardOnly): Game object.
            cam_np (panda3d.core.NodePath): Camera node object.
            cam (panda3d.core.NodePath): Main camera object.
        """
        if not self._is_centered:
            self._stop(cam_np, cam, False, is_hard=True)

            self._last_cam_pos = cam.getPos()
            self._last_cam_hpr = cam.getHpr()
            self._last_cam_np_hpr = cam_np.getHpr()

            cam.wrtReparentTo(game.train.model)
            cam.setPos(0, 0, 1.8)
            cam.setHpr(90, -90, 0)
            cam_np.setHpr(0, 0, 0)

            for key in (
                "arrow_up",
                "arrow_down",
                "arrow_left",
                "arrow_right",
                "arrow_up-up",
                "arrow_down-up",
                "arrow_left-up",
                "arrow_right-up",
                "alt-arrow_left",
                "alt-arrow_right",
                "alt-arrow_up",
                "alt-arrow_down",
            ):
                game.ignore(key)
        else:
            cam.wrtReparentTo(cam_np)
            self._set_move_keys(game, cam_np, cam)

            cam.setPos(*self._last_cam_pos)
            cam.setHpr(*self._last_cam_hpr)
            cam_np.setHpr(*self._last_cam_np_hpr)

        self._is_centered = not self._is_centered
