"""Camera configuring and controls."""
from direct.interval.LerpInterval import LerpPosInterval
from panda3d.core import Vec3


class CameraController:
    """Object to configure camera and its controls."""

    def __init__(self):
        self._target = Vec3(2, 0, 3)  # final pos of the current movement
        self._move_int = None  # current move interval

    def set_camera_controls(self, game, cam, train_node, train_mod):
        """Configure camera, its node and set keyboard keys to control the camera.

        Args:
            game (ForwardOnly): Game object.
            cam (panda3d.core.NodePath): Main camera object.
            train_node (panda3d.core.NodePath): Train node.
            train_mod (panda3d.core.NodePath): Train model

        Returns:
            panda3d.core.NodePath: Camera node.
        """
        cam_np = game.render.attachNewNode("camera_node")
        cam_np.reparentTo(train_node)

        cam.reparentTo(cam_np)
        cam.setPos(self._target)
        cam.lookAt(train_mod)

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
        return cam_np

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

    def _stop(self, cam_np, cam, stop_x):
        """Stop moving camera (on key release).

        Args:
            cam_np (panda3d.core.NodePath): Camera node.
            cam (panda3d.core.NodePath): Camera object.
            stop_x (bool):
                True - movement along x axis should be stopped.
                False - movement along y axis should be stopped.
        """
        self._move_int.pause()
        if stop_x:
            self._target.setX(cam.getX())
        else:
            self._target.setY(cam.getY())

        self._move_int = LerpPosInterval(cam, 0.75, self._target, other=cam_np)
        self._move_int.start()
