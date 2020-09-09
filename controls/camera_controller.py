"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Game main camera configuring and controls.
"""
from direct.interval.LerpInterval import LerpHprInterval, LerpPosInterval
from panda3d.core import Vec3

MAX_Z = 3
MAX_UP_MOVE = [1, None, 1.5]
MAX_DOWN_MOVE = [2.5, None, 0.75]
MAX_LEFT_MOVE = [None, -1.1, 0.9]
MAX_RIGHT_MOVE = [None, 1.1, 0.9]


class CameraController:
    """Object to configure camera and its controls."""

    def __init__(self):
        self._cam_np = None
        self._target = Vec3(2, 0, MAX_Z)  # the current movement final pos
        self._move_int = None  # current move interval
        self._turn_int = None  # current rotation interval
        self._with_mouse_move = None  # camera is in move by mouse
        self._with_mouse_move_x = None

        # camera position before toggling centered view
        self._last_cam_pos = None
        self._last_cam_hpr = None
        self._last_cam_np_pos = None
        self._last_cam_np_hpr = None
        self._is_centered = False

        base.camLens.setNear(0.25)  # noqa: F821

    def set_controls(self, train):
        """Configure camera and its controls.

        Args:
            train (train.Train): Train object.
        """
        base.disableMouse()  # noqa: F821

        self._cam_np = train.node.attachNewNode("camera_node")
        base.cam.reparentTo(self._cam_np)  # noqa: F821
        base.cam.setPos(self._target)  # noqa: F821
        base.cam.lookAt(train.model)  # noqa: F821

        self._set_move_keys()
        base.accept("c", self._toggle_centered_view)  # noqa: F821
        base.taskMgr.doMethodLater(  # noqa: F821
            0.2, self._move_with_mouse, "move_camera_with_mouse", appendTask=True
        )

    def _move_with_mouse(self, task):
        """Implement moving camera with mouse.

        If mouse pointer touches a screen edge, move
        camera in this direction.
        """
        x = round(base.mouseWatcherNode.getMouseX(), 2)  # noqa: F821
        z = round(base.mouseWatcherNode.getMouseY(), 2)  # noqa: F821

        if x == 1:
            self._with_mouse_move = True
            self._move(*MAX_RIGHT_MOVE)
            self._with_mouse_move_x = False
            return task.again
        if x == -1:
            self._with_mouse_move = True
            self._move(*MAX_LEFT_MOVE)
            self._with_mouse_move_x = False
            return task.again
        if z == 1:
            self._with_mouse_move = True
            self._move(*MAX_UP_MOVE)
            self._with_mouse_move_x = True
            return task.again
        if z == -1:
            self._with_mouse_move = True
            self._move(*MAX_DOWN_MOVE)
            self._with_mouse_move_x = True
            return task.again

        if self._with_mouse_move:
            self._stop(self._with_mouse_move_x)
            self._with_mouse_move = False

        return task.again

    def _move(self, x, y, time):
        """Start camera movement with an interval (on key press).

        Args:
            x (float): Translation along x axis.
            y (float): Translation along y axis.
            time (float): Interval length.
        """
        if self._move_int is not None:
            self._move_int.pause()

        if x:
            # if camera moves forward, consider Z coordinate
            # to calibrate move limits when zoomed
            if x == 1:
                x -= MAX_Z - base.cam.getZ()  # noqa: F821

            self._target.setX(x)
        else:
            self._target.setY(y)

        self._move_int = LerpPosInterval(
            base.cam, time, self._target, other=self._cam_np  # noqa: F821
        )
        self._move_int.start()

    def _zoom_timed(self, x, z):
        """Zoom camera for some time.

        Args:
            x (float): Translation along x axis.
            z (float): Translation along z axis.
        """
        base.taskMgr.doMethodLater(  # noqa: F821
            0.12, self._stop, "zoom_stop", extraArgs=[False, True, True]
        )
        self._zoom(x, z, 0.2)

    def _zoom(self, x, z, zoom_time):
        """Zoom camera.

        Args:
            x (float): Translation along x axis.
            z (float): Translation along z axis.
            zoom_time (float): Time to zoom.
        """
        if self._move_int is not None:
            self._move_int.pause()

        self._target.setX(x)
        self._target.setZ(z)

        self._move_int = LerpPosInterval(
            base.cam, zoom_time, self._target, other=self._cam_np  # noqa: F821
        )
        self._move_int.start()

    def _turn(self, h, r):
        """Turn camera with a single interval (on key press).

        Args:
            h (int): Translation for camera heading, angle.
            r (int): Translation for camera rolling, angle.
        """
        if self._turn_int is not None and self._turn_int.isPlaying():
            return

        self._turn_int = LerpHprInterval(
            self._cam_np, 4, (self._cam_np.getH() + h, 0, r)
        )
        self._turn_int.start()

    def _stop(self, stop_x, stop_zoom=False, is_hard=False):
        """Stop moving and rotating camera (on key release).

        Args:
            stop_x (bool):
                True - movement along x axis should be stopped.
                False - movement along y axis should be stopped.
            stop_zoom (bool):
                True if camera stopped zoom movement.
            is_hard (bool):
                If False, camera will be stopped with an deceleration
                interval. If True, stopping will be immediate.
        """
        if self._move_int is not None:
            self._move_int.pause()

        if self._turn_int is not None:
            self._turn_int.pause()

        if stop_zoom:
            self._target = base.cam.getPos()  # noqa: F821
        elif stop_x:
            self._target.setX(base.cam.getX())  # noqa: F821
        else:
            self._target.setY(base.cam.getY())  # noqa: F821

        if not is_hard:
            self._move_int = LerpPosInterval(
                base.cam, 0.75, self._target, other=self._cam_np  # noqa: F821
            )
            self._move_int.start()

    def _set_move_keys(self):
        """Set camera move and rotate keys."""
        # key pressed - start movement
        base.accept("arrow_up", self._move, MAX_UP_MOVE)  # noqa: F821
        base.accept("arrow_down", self._move, MAX_DOWN_MOVE)  # noqa: F821
        base.accept("arrow_left", self._move, MAX_LEFT_MOVE)  # noqa: F821
        base.accept("arrow_right", self._move, MAX_RIGHT_MOVE)  # noqa: F821

        # key released - stop
        base.accept("arrow_up-up", self._stop, [True])  # noqa: F821
        base.accept("arrow_down-up", self._stop, [True])  # noqa: F821
        base.accept("arrow_left-up", self._stop, [False])  # noqa: F821
        base.accept("arrow_right-up", self._stop, [False])  # noqa: F821

        # key pressed - start turning
        base.accept("alt-arrow_left", self._turn, [-360, 0])  # noqa: F821
        base.accept("alt-arrow_right", self._turn, [360, 0])  # noqa: F821
        base.accept("alt-arrow_up", self._turn, [0, -60])  # noqa: F821
        base.accept("alt-arrow_down", self._turn, [0, 25])  # noqa: F821

        # camera zooming controls
        base.accept("+", self._zoom, [0.7, 1.2, 1.75])  # noqa: F821
        base.accept("-", self._zoom, [2, 3, 1.75])  # noqa: F821
        base.accept("+-up", self._stop, [False, True, True])  # noqa: F821
        base.accept("--up", self._stop, [False, True, True])  # noqa: F821

        base.accept("wheel_up", self._zoom_timed, [0.7, 1.2])  # noqa: F821
        base.accept("wheel_down", self._zoom_timed, [2, 3])  # noqa: F821

    def _toggle_centered_view(self):
        """Set camera onto default position.

        Centered position is optimal for characters
        manipulations. Press repeating returns camera to
        the previous position.
        """
        if not self._is_centered:
            self._stop(False, is_hard=True)

            self._last_cam_pos = base.cam.getPos()  # noqa: F821
            self._last_cam_hpr = base.cam.getHpr()  # noqa: F821
            self._last_cam_np_hpr = self._cam_np.getHpr()

            base.cam.wrtReparentTo(base.train.model)  # noqa: F821
            base.cam.setPos(0, 0, 1.8)  # noqa: F821
            base.cam.setHpr(90, -90, 0)  # noqa: F821
            self._cam_np.setHpr(0, 0, 0)

            self._disable_ctrl_keys()
            base.taskMgr.remove("move_camera_with_mouse")  # noqa: F821
        else:
            base.cam.wrtReparentTo(self._cam_np)  # noqa: F821
            self._set_move_keys()

            base.cam.setPos(*self._last_cam_pos)  # noqa: F821
            base.cam.setHpr(*self._last_cam_hpr)  # noqa: F821
            self._cam_np.setHpr(*self._last_cam_np_hpr)

            base.taskMgr.doMethodLater(  # noqa: F821
                0.2, self._move_with_mouse, "move_camera_with_mouse", appendTask=True
            )

        self._is_centered = not self._is_centered

    def _disable_ctrl_keys(self):
        """Ignore all the camera control keys."""
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
            "+",
            "-",
            "+-up",
            "--up",
            "wheel_up",
            "wheel_down",
        ):
            base.ignore(key)  # noqa: F821

    def set_hangar_pos(self, hangar):
        """Set camera to hangar position.

        Args:
            hangar (panda3d.core.NodePath): Hangar model.
        """
        self._disable_ctrl_keys()
        base.ignore("c")  # noqa: F821

        self._last_cam_pos = base.cam.getPos()  # noqa: F821
        self._last_cam_hpr = base.cam.getHpr()  # noqa: F821
        self._last_cam_np_pos = self._cam_np.getPos()
        self._last_cam_np_hpr = self._cam_np.getHpr()

        base.cam.setPos(0)  # noqa: F821
        base.cam.setHpr(0)  # noqa: F821

        self._cam_np.reparentTo(hangar)
        self._cam_np.setPos(-0.35, 1.36, 0.12)
        self._cam_np.setHpr(-163, 5, 0)

    def enable_ctrl_keys(self):
        """Enable all the camera control keys."""
        self._set_move_keys()
        base.accept("c", self._toggle_centered_view)  # noqa: F821
        base.taskMgr.doMethodLater(  # noqa: F821
            0.2, self._move_with_mouse, "move_camera_with_mouse", appendTask=True
        )

    def unset_hangar_pos(self):
        """Return camera back to normal position."""
        base.cam.setPos(self._last_cam_pos)  # noqa: F821
        base.cam.setHpr(self._last_cam_hpr)  # noqa: F821

        self._cam_np.reparentTo(base.train.node)  # noqa: F821
        self._cam_np.setPos(self._last_cam_np_pos)
        self._cam_np.setHpr(self._last_cam_np_hpr)
