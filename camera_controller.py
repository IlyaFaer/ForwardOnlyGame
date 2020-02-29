"""Camera configuring and controls."""
from direct.interval.LerpInterval import LerpPosInterval


class CameraController:
    """Object to configure camera and camera controls."""

    def __init__(self):
        self._move_int = None

    def set_camera_controls(self, game, cam, train_node, train_mod):
        """Configure camera, its node and set keyboard keys to control the camera

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
        cam.setPos(2, 0, 3)
        cam.lookAt(train_mod)

        # set controls
        game.accept("arrow_up", self._move, [cam_np, cam, 1, None, 1.5])
        game.accept("arrow_down", self._move, [cam_np, cam, 2, None, 0.75])
        game.accept("arrow_left", self._move, [cam_np, cam, None, -1.1, 0.9])
        game.accept("arrow_right", self._move, [cam_np, cam, None, 1.1, 0.9])

        game.accept("arrow_up-up", self._stop)
        game.accept("arrow_down-up", self._stop)
        game.accept("arrow_left-up", self._stop)
        game.accept("arrow_right-up", self._stop)
        return cam_np

    def _move(self, cam_np, cam, x, y, time):
        """Start camera movement with single interval (on key press).

        Args:
            cam_np (panda3d.core.NodePath): Camera node.
            cam (panda3d.core.NodePath): Camera object.
            x (float): Translation along x axis.
            y (float): Translation along y axis.
            time (float): Interval length.
        """
        if self._move_int is not None:
            self._move_int.pause()

        self._move_int = LerpPosInterval(
            cam, time, (x or cam.getX(), y or cam.getY(), 3), other=cam_np
        )
        self._move_int.start()

    def _stop(self):
        """Stop moving camera (on key release)."""
        self._move_int.pause()
