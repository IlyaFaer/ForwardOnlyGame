"""Lighting system."""
import copy
import itertools
from direct.directutil import Mopath
from direct.interval.MopathInterval import MopathInterval
from panda3d.core import AmbientLight, Spotlight, Vec4, PerspectiveLens

MOD_DIR = "models/bam/"
SUN_COLORS = itertools.cycle(
    (
        {
            "name": "morning",
            "dir": Vec4(0.34, 0.45, 0.5, 1),
            "amb": Vec4(0.4, 0.4, 0.4, 1),
        },
        {
            "name": "noon",
            "dir": Vec4(0.79, 0.76, 0.35, 1),
            "amb": Vec4(0.6, 0.6, 0.6, 1),
        },
        {
            "name": "evening",
            "dir": Vec4(0.7, 0.43, 0.15, 1),
            "amb": Vec4(0.35, 0.35, 0.35, 1),
        },
        {
            "name": "night",
            "dir": Vec4(0.05, 0.05, 0.05, 1),
            "amb": Vec4(0.1, 0.1, 0.1, 1),
        },
    )
)


class Sun:
    """Game Sun. Includes ambient and directional lights.

    Sun changes its color according to game day time.
    It simulates real Sun movement as well.

    Args:
        game (ForwardOnly): The game object.
        train (train.Train): Train object.
    """

    def __init__(self, game, train):
        self._color = copy.deepcopy(next(SUN_COLORS))
        self._next_color = copy.deepcopy(next(SUN_COLORS))
        self._path = Mopath.Mopath(objectToLoad=MOD_DIR + "sun_path.bam")

        self._color_step = 0
        # day duration = 90 steps * 10 sec/step = 15 min/part
        self._day_part_duration = 90
        self._step_duration = 10

        self._color_vec = self._calc_color_vec(
            self._color, self._next_color, self._day_part_duration
        )

        self._amb_light, self._dir_light, sun_np = self._set_general_lights(
            game.render, train.node
        )
        self._set_day_night_cycle(sun_np, game.taskMgr, train.model)

    def _set_general_lights(self, render, train_np):
        """Set initial Sun lights.

        Args:
            render (panda3d.core.NodePath): Game render.
            train_np (panda3d.core.NodePath): Train node.

        Returns:
            panda3d.core.AmbientLight: World ambient light.
            panda3d.core.DirectionalLight: World directional light.
            panda3d.core.NodePath: NodePath of the Sun.
        """
        amb_light = AmbientLight("sun_amb")
        amb_light.setColor(self._color["amb"])
        render.setLight(render.attachNewNode(amb_light))

        lens = PerspectiveLens()
        lens.setNearFar(1, 100)
        lens.setFov(70, 70)

        sun_light = Spotlight("sun_dir")
        sun_light.setColor(self._color["dir"])
        sun_light.setShadowCaster(True, 8192, 8192)
        sun_light.setLens(lens)
        sun_light.setExponent(0.5)
        sun_np = train_np.attachNewNode(sun_light)

        render.setShaderAuto()
        render.setLight(sun_np)

        return amb_light, sun_light, sun_np

    def _set_day_night_cycle(self, sun_np, taskMgr, train_mod):
        """Set intervals and methods for day-night cycle.

        Args:
            sun_np (panda3d.core.NodePath): Sun node path.
            taskMgr (direct.task.Task.TaskManager): Task manager.
            train_mod (panda3d.core.NodePath): Train model.
        """
        taskMgr.doMethodLater(
            self._step_duration,
            self._change_sun_state,
            "change_sun_color",
            extraArgs=[sun_np, train_mod],
            appendTask=True,
        )
        MopathInterval(
            self._path,
            sun_np,
            duration=self._day_part_duration * self._step_duration * 2,
            name="sun_interval",
        ).start()

        taskMgr.doMethodLater(
            0.1, sun_np.lookAt, extraArgs=[train_mod], name="turn_sun"
        )

    def _change_sun_state(self, sun_np, train_mod, task):
        """Change Sun color and angle with a small step.

        Args:
            sun_np (panda3d.core.NodePath): Sun node path.
            task (panda3d.core.PythonTask): Task object.
        """
        if self._color_step == self._day_part_duration:
            self._color_step = 0

            self._color = self._next_color
            self._next_color = copy.deepcopy(next(SUN_COLORS))

            self._color_vec = self._calc_color_vec(
                self._color, self._next_color, self._day_part_duration
            )
            # start Sun movement interval
            if self._color["name"] == "night":
                MopathInterval(
                    self._path,
                    sun_np,
                    duration=self._day_part_duration * self._step_duration * 3,
                    name="sun_interval",
                ).start()

        # do color changing step
        for field in ("dir", "amb"):
            for i in range(3):
                self._color[field][i] += self._color_vec[field][i]

        self._dir_light.setColor(self._color["dir"])
        self._amb_light.setColor(self._color["amb"])
        self._color_step += 1

        sun_np.lookAt(train_mod)
        return task.again

    def _calc_color_vec(self, color, next_color, steps):
        """Calculate vector to change color in given steps number.

        Args:
            color (dict): Ambient and directional current colors.
            next_color (Vec4): Next ambient and directional colors.
            steps (int): Number of steps to change color.

        Returns:
            dict: Directonal and ambient lights change vector.
        """
        vects = {}
        for field in ("dir", "amb"):
            vects[field] = Vec4(
                (next_color[field][0] - color[field][0]) / steps,
                (next_color[field][1] - color[field][1]) / steps,
                (next_color[field][2] - color[field][2]) / steps,
                1,
            )
        return vects
