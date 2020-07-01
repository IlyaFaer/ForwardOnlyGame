"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Camera configuring and controls.
"""
from direct.interval.LerpInterval import LerpPosInterval, LerpHprInterval
from panda3d.core import Vec3

MAX_Z = 3


class CameraController:
    """Object to configure camera and its controls."""

    def __init__(self):
        self._target = Vec3(2, 0, MAX_Z)  # final pos of the current movement
        self._move_int = None  # current move interval
        self._turn_int = None  # current rotation interval
        self._with_mouse_move = None  # camera is in move by mouse
        self._with_mouse_move_x = None
        self._is_centered = False

        # camera position before toggling centered view
        self._last_cam_pos = None
        self._last_cam_hpr = None
        self._last_cam_np_hpr = None

        base.camLens.setNear(0.5)  # noqa: F821

    def set_controls(self, train):
        """Configure camera and its controls.

        Args:
            train (train.Train): Train object.
        """
        base.disableMouse()  # noqa: F821

        cam_np = train.node.attachNewNode("camera_node")
        base.cam.reparentTo(cam_np)  # noqa: F821
        base.cam.setPos(self._target)  # noqa: F821
        base.cam.lookAt(train.model)  # noqa: F821

        self._set_move_keys(cam_np)
        base.accept("c", self._toggle_centered_view, [cam_np])  # noqa: F821
        base.taskMgr.doMethodLater(  # noqa: F821
            0.2,
            self._move_with_mouse,
            "move_camera_with_mouse",
            extraArgs=[cam_np],
            appendTask=True,
        )

    def _move_with_mouse(self, cam_np, task):
        """Implement moving camera with mouse.

        If mouse pointer touches a screen edge, move
        camera in this direction.

        Args:
            cam_np (panda3d.core.NodePath): Camera node.
        """
        x = round(base.mouseWatcherNode.getMouseX(), 2)  # noqa: F821
        z = round(base.mouseWatcherNode.getMouseY(), 2)  # noqa: F821

        if x == 1:
            self._with_mouse_move = True
            self._move(cam_np, None, 1.1, 0.9)
            self._with_mouse_move_x = False
            return task.again
        if x == -1:
            self._with_mouse_move = True
            self._move(cam_np, None, -1.1, 0.9)
            self._with_mouse_move_x = False
            return task.again
        if z == 1:
            self._with_mouse_move = True
            self._move(cam_np, 1, None, 1.5)
            self._with_mouse_move_x = True
            return task.again
        if z == -1:
            self._with_mouse_move = True
            self._move(cam_np, 2, None, 0.75)
            self._with_mouse_move_x = True
            return task.again

        if self._with_mouse_move:
            self._stop(cam_np, self._with_mouse_move_x)
            self._with_mouse_move = False

        return task.again

    def _move(self, cam_np, x, y, time):
        """Start camera movement with an interval (on key press).

        Args:
            cam_np (panda3d.core.NodePath): Camera node.
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
            base.cam, time, self._target, other=cam_np  # noqa: F821
        )
        self._move_int.start()

    def _zoom_timed(self, cam_np, x, z):
        """Zoom camera for some time.

        Args:
            cam_np (panda3d.core.NodePath): Camera node.
            x (float): Translation along x axis.
            z (float): Translation along z axis.
        """
        base.taskMgr.doMethodLater(  # noqa: F821
            0.12, self._stop, "zoom_stop", extraArgs=[cam_np, False, True, True]
        )
        self._zoom(cam_np, x, z, 0.2)

    def _zoom(self, cam_np, x, z, zoom_time):
        """Zoom camera.

        Args:
            cam_np (panda3d.core.NodePath): Camera node.
            x (float): Translation along x axis.
            z (float): Translation along z axis.
            zoom_time (float): Time to zoom.
        """
        if self._move_int is not None:
            self._move_int.pause()

        self._target.setX(x)
        self._target.setZ(z)

        self._move_int = LerpPosInterval(
            base.cam, zoom_time, self._target, other=cam_np  # noqa: F821
        )
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

    def _stop(self, cam_np, stop_x, stop_zoom=False, is_hard=False):
        """Stop moving and rotating camera (on key release).

        Args:
            cam_np (panda3d.core.NodePath): Camera node.
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
                base.cam, 0.75, self._target, other=cam_np  # noqa: F821
            )
            self._move_int.start()

    def _set_move_keys(self, cam_np):
        """Set camera move and rotate keys.

        Args:
            cam_np (panda3d.core.NodePath): Camera node object.
        """
        # key pressed - start movement
        base.accept("arrow_up", self._move, [cam_np, 1, None, 1.5])  # noqa: F821
        base.accept("arrow_down", self._move, [cam_np, 2, None, 0.75])  # noqa: F821
        base.accept("arrow_left", self._move, [cam_np, None, -1.1, 0.9])  # noqa: F821
        base.accept("arrow_right", self._move, [cam_np, None, 1.1, 0.9])  # noqa: F821

        # key released - stop
        base.accept("arrow_up-up", self._stop, [cam_np, True])  # noqa: F821
        base.accept("arrow_down-up", self._stop, [cam_np, True])  # noqa: F821
        base.accept("arrow_left-up", self._stop, [cam_np, False])  # noqa: F821
        base.accept("arrow_right-up", self._stop, [cam_np, False])  # noqa: F821

        # key pressed - start turning
        base.accept("alt-arrow_left", self._turn, [cam_np, -360, 0])  # noqa: F821
        base.accept("alt-arrow_right", self._turn, [cam_np, 360, 0])  # noqa: F821
        base.accept("alt-arrow_up", self._turn, [cam_np, 0, -60])  # noqa: F821
        base.accept("alt-arrow_down", self._turn, [cam_np, 0, 25])  # noqa: F821

        # camera zooming controls
        base.accept("+", self._zoom, [cam_np, 0.7, 1.2, 1.75])  # noqa: F821
        base.accept("-", self._zoom, [cam_np, 2, 3, 1.75])  # noqa: F821
        base.accept("+-up", self._stop, [cam_np, False, True, True])  # noqa: F821
        base.accept("--up", self._stop, [cam_np, False, True, True])  # noqa: F821

        base.accept("wheel_up", self._zoom_timed, [cam_np, 0.7, 1.2])  # noqa: F821
        base.accept("wheel_down", self._zoom_timed, [cam_np, 2, 3])  # noqa: F821

    def _toggle_centered_view(self, cam_np):
        """Set camera onto default position.

        Centered position is optimal for characters
        manipulations. Press repeating returns camera to
        the previous position.

        Args:
            cam_np (panda3d.core.NodePath): Camera node object.
        """
        if not self._is_centered:
            self._stop(cam_np, False, is_hard=True)

            self._last_cam_pos = base.cam.getPos()  # noqa: F821
            self._last_cam_hpr = base.cam.getHpr()  # noqa: F821
            self._last_cam_np_hpr = cam_np.getHpr()

            base.cam.wrtReparentTo(base.train.model)  # noqa: F821
            base.cam.setPos(0, 0, 1.8)  # noqa: F821
            base.cam.setHpr(90, -90, 0)  # noqa: F821
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
                base.ignore(key)  # noqa: F821
        else:
            base.cam.wrtReparentTo(cam_np)  # noqa: F821
            self._set_move_keys(cam_np)

            base.cam.setPos(*self._last_cam_pos)  # noqa: F821
            base.cam.setHpr(*self._last_cam_hpr)  # noqa: F821
            cam_np.setHpr(*self._last_cam_np_hpr)

        self._is_centered = not self._is_centered
