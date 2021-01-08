"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Includes game Sun systems.
"""
import copy
import itertools

from direct.directutil import Mopath
from direct.interval.MopathInterval import MopathInterval
from panda3d.core import AmbientLight, Spotlight, Vec4, PerspectiveLens

from utils import address

SUN_COLORS = itertools.cycle(
    (
        {
            "name": "morning",
            "dir": Vec4(0.34, 0.45, 0.5, 1),
            "amb": Vec4(0.4, 0.4, 0.4, 1),
        },
        {
            "name": "noon",
            "dir": Vec4(0.57, 0.54, 0.4, 1),
            "amb": Vec4(0.53, 0.53, 0.53, 1),
        },
        {
            "name": "evening",
            "dir": Vec4(0.7, 0.43, 0.15, 1),
            "amb": Vec4(0.35, 0.35, 0.35, 1),
        },
        {
            "name": "night",
            "dir": Vec4(0.05, 0.05, 0.05, 1),
            "amb": Vec4(0.14, 0.14, 0.14, 1),
        },
    )
)


class Sun:
    """Game Sun. Includes ambient and directional lights.

    Sun changes its color according to game day time.
    Simulates real Sun movement as well.

    Args:
        day_part_desc (dict): Day part description.
    """

    def __init__(self, day_part_desc):
        self._path = Mopath.Mopath(objectToLoad=address("sun_path"))

        self._color = copy.deepcopy(next(SUN_COLORS))
        self._next_color = copy.deepcopy(next(SUN_COLORS))
        self._color_step = 0

        if day_part_desc:
            while self._color["name"] != day_part_desc["name"]:
                self._color = self._next_color
                self._next_color = copy.deepcopy(next(SUN_COLORS))

            self._color = day_part_desc["time"]["color"]
            self._color_step = day_part_desc["time"]["step"]

        # day duration = 90 steps * 10 sec/step = 15 min/part
        # 15 min/part * 4 parts = 1 hour/day
        self._day_part_duration = 90
        self._step_duration = 10

        self._arch_int = None

        self._color_vec = self._calc_color_vec(
            self._color, self._next_color, self._day_part_duration
        )

        self._amb_light, self._dir_light, sun_np = self._set_general_lights(
            base.train.node  # noqa: F821
        )
        self._set_day_night_cycle(sun_np, base.train.model, day_part_desc)  # noqa: F821

    @property
    def day_part(self):
        """Day part name.

        Returns:
            str: day part name.
        """
        return self._color["name"]

    @property
    def day_part_time(self):
        """Exact day part step.

        Returns:
            int: Day part step.
        """
        return {
            "step": self._color_step,
            "duration": self._arch_int.getDuration(),
            "current": self._arch_int.getT(),
            "color": self._color,
        }

    @property
    def is_dark(self):
        """Returns True if it's too dark to shoot."""
        if self.day_part == "evening" and self._color_step > 45:
            return True

        if self.day_part == "night" and self._color_step < 45:
            return True

        return False

    def _set_general_lights(self, train_np):
        """Set initial Sun lights.

        Args:
            train_np (panda3d.core.NodePath): Train node.

        Returns:
            panda3d.core.AmbientLight: Sun ambient light.
            panda3d.core.DirectionalLight: Sun directional light.
            panda3d.core.NodePath: NodePath of the Sun.
        """
        amb_light = AmbientLight("sun_amb")
        amb_light.setColor(self._color["amb"])
        render.setLight(render.attachNewNode(amb_light))  # noqa: F821

        lens = PerspectiveLens()
        lens.setNearFar(1, 100)
        lens.setFov(70, 70)

        sun_light = Spotlight("sun_dir")
        sun_light.setColor(self._color["dir"])
        sun_light.setShadowCaster(True, 8192, 8192, sort=-2000)
        sun_light.setLens(lens)
        sun_light.setExponent(0.5)
        sun_np = train_np.attachNewNode(sun_light)

        render.setLight(sun_np)  # noqa: F821

        return amb_light, sun_light, sun_np

    def _set_day_night_cycle(self, sun_np, train_mod, day_time):
        """Set intervals and methods for day-night cycle.

        Args:
            sun_np (panda3d.core.NodePath): Sun node path.
            train_mod (panda3d.core.NodePath): Train model.
            day_time (dict): Day time description.
        """
        taskMgr.doMethodLater(  # noqa: F821
            self._step_duration,
            self._change_sun_state,
            "change_sun_color",
            extraArgs=[sun_np, train_mod],
            appendTask=True,
        )
        self._arch_int = MopathInterval(
            self._path,
            sun_np,
            duration=day_time["time"]["duration"]
            if day_time
            else self._day_part_duration * self._step_duration * 2,
            name="sun_interval",
        )

        self._arch_int.start(startT=day_time["time"]["current"] if day_time else 0)

        taskMgr.doMethodLater(  # noqa: F821
            0.01,
            self._sun_look_at_train,
            "sun_look_at_train",
            extraArgs=[sun_np],
            appendTask=True,
        )

    def _sun_look_at_train(self, sun_np, task):
        sun_np.lookAt(base.train.model)  # noqa: F821
        return task.again

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
                self._arch_int = MopathInterval(
                    self._path,
                    sun_np,
                    duration=self._day_part_duration * self._step_duration * 3,
                    name="sun_interval",
                )
                self._arch_int.start()

        # do color changing step
        for field in ("dir", "amb"):
            for i in range(3):
                self._color[field][i] += self._color_vec[field][i]

        self._dir_light.setColor(self._color["dir"])
        self._amb_light.setColor(self._color["amb"])
        self._color_step += 1

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
