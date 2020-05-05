"""Lighting system."""
import copy
import itertools
from panda3d.core import DirectionalLight, AmbientLight, Vec3, Vec4


SUN_COLORS = itertools.cycle(
    (
        {
            "name": "morning",
            "dir": Vec4(0.76, 0.87, 0.89, 1),
            "amb": Vec4(0.3, 0.3, 0.3, 1),
        },
        {
            "name": "noon",
            "dir": Vec4(0.99, 0.96, 0.6, 1),
            "amb": Vec4(0.5, 0.5, 0.5, 1),
        },
        {
            "name": "evening",
            "dir": Vec4(0.9, 0.63, 0.35, 1),
            "amb": Vec4(0.25, 0.25, 0.25, 1),
        },
        {"name": "night", "dir": Vec4(0.25, 0.25, 0.25, 1), "amb": Vec4(0, 0, 0, 1)},
    )
)


class Sun:
    """Game Sun. Includes ambient and directional lights.

    Sun changes its color according to game day time.
    It simulates real Sun movement as well.

    Args:
        game (ForwardOnly): The game object.
    """

    def __init__(self, game):
        self._sun_color = copy.deepcopy(next(SUN_COLORS))
        self._next_sun_color = copy.deepcopy(next(SUN_COLORS))
        self._color_step = 0
        # day duration = 90 steps * 10 sec/step = 1h
        self._day_part_duration = 90

        self._color_vec = self._calc_color_vec(
            self._sun_color, self._next_sun_color, self._day_part_duration
        )

        self._amb_light, self._dir_light, sun_np = self._set_general_lights(game.render)
        self._set_day_night_cycle(sun_np, game.taskMgr)

    def _set_general_lights(self, render):
        """Set initial Sun lights.

        Args:
            render (panda3d.core.NodePath): Game render.

        Returns:
            panda3d.core.AmbientLight: World ambient light.
            panda3d.core.DirectionalLight: World directional light.
            panda3d.core.NodePath: NodePath of the Sun.
        """
        amb_light = AmbientLight("sun_amb")
        amb_light.setColor(self._sun_color["amb"])
        render.setLight(render.attachNewNode(amb_light))

        dir_light = DirectionalLight("sun_dir")
        dir_light.setColor(self._sun_color["dir"])
        sun_np = render.attachNewNode(dir_light)
        sun_np.setHpr(80, 0, 0)
        render.setLight(sun_np)

        return amb_light, dir_light, sun_np

    def _set_day_night_cycle(self, sun_np, taskMgr):
        """Set intervals and methods for day-night cycle.

        Args:
            sun_np (panda3d.core.NodePath): Sun node path.
            taskMgr (direct.task.Task.TaskManager): Task manager.
        """
        taskMgr.doMethodLater(
            10,
            self._change_sun_color,
            "change_sun_color",
            extraArgs=[sun_np],
            appendTask=True,
        )
        sun_np.hprInterval(self._day_part_duration * 30, Vec3(110, -175, 0)).start()

    def _change_sun_color(self, sun_np, task):
        """Change Sun color with a small step.

        Args:
            sun_np (panda3d.core.NodePath): Sun node path.
            task (panda3d.core.PythonTask): Task object.
        """
        if self._color_step == self._day_part_duration:
            self._color_step = 0

            self._sun_color = self._next_sun_color
            self._next_sun_color = copy.deepcopy(next(SUN_COLORS))

            self._color_vec = self._calc_color_vec(
                self._sun_color, self._next_sun_color, self._day_part_duration
            )
            # start Sun movement interval
            if self._sun_color["name"] == "night":
                sun_np.setHpr(135, 0, -45)
                sun_np.hprInterval(
                    self._day_part_duration * 40, Vec3(110, -175, 0)
                ).start()

        # do color changing step
        for field in ("dir", "amb"):
            for i in range(3):
                self._sun_color[field][i] += self._color_vec[field][i]

        self._dir_light.setColor(self._sun_color["dir"])
        self._amb_light.setColor(self._sun_color["amb"])
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
