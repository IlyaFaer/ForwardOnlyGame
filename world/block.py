"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

World blocks API.
"""
import copy
import random

from panda3d.core import TextureStage, Texture

from utils import address, chance, take_random
from .locations import LOCATIONS
from .objects import Barrier

ANGLES = (0, 90, 180, 270)
SURFACES = {
    "direct": ("surface1", "surface2", "surface3"),
    "l90_turn": ("l90_turn_surface1", "l90_turn_surface2"),
    "r90_turn": ("r90_turn_surface1", "r90_turn_surface2"),
    "ls": ("surface1", "surface2", "surface3"),
    "rs": ("surface1", "surface2", "surface3"),
}
FLOWER_RANGES = {
    (0, "l"): {"u": (45, 65), "v": (-80, 60)},
    (90, "l"): {"u": (-80, 60), "v": (-85, -60)},
    (180, "l"): {"u": (-80, -60), "v": (-85, 60)},
    (270, "l"): {"u": (-80, 60), "v": (40, 60)},
    (0, "r"): {"u": (-80, -60), "v": (-85, 60)},
    (90, "r"): {"u": (-80, 60), "v": (40, 60)},
    (180, "r"): {"u": (45, 65), "v": (-80, 60)},
    (270, "r"): {"u": (-80, 60), "v": (-85, -60)},
}


class Block:
    """Single world block.

    Consists of railway block, path for Train to
    move along, environment models and two surface blocks.

    On creation it chooses surface models and arranges
    environment models, but only coordinates and model names
    are generated. All of that content will be loaded on
    Block.prepare() call.

    Args:
        path (Mopath.Mopath): Motion path.
        cam_path (Mopath.Mopath): Motion path for camera.
        name (str): Block path name.
        surf_vertices (dict): Vertices index of every surface model.
        enemy_territory (bool): This block is an enemy territory.
        is_station (bool): Station must be set on this block.
        is_city (bool): This is a city block.
        outing_available (str): An outing type available on this block.
        desc (dict): Block description.
    """

    def __init__(
        self,
        path,
        cam_path,
        name,
        surf_vertices,
        enemy_territory=False,
        is_station=False,
        is_city=False,
        outing_available=None,
        desc=None,
    ):
        self.rails_mod = None

        self.name = name
        self.path = path
        self.cam_path = cam_path
        self.enemy_territory = enemy_territory
        self.outing_available = outing_available
        self.is_city = is_city

        if desc:  # loading block
            self._station_side = desc["station_side"]
            self._l_surface = desc["l_surface"]
            self._r_surface = desc["r_surface"]
            self._l_angle = desc["l_angle"]
            self._r_angle = desc["r_angle"]
            self._env_mods = desc["env_mods"]
            self._railways_model = desc["railways_model"]
            return

        # generating block
        self._station_side = random.choice(("l", "r")) if is_station else None

        self._l_surface, self._l_angle = self._gen_surface("l")
        self._r_surface, self._r_angle = self._gen_surface("r")

        self._env_mods = {
            "l": self._gen_env_mods(copy.deepcopy(surf_vertices[self._l_surface])),
            "r": self._gen_env_mods(copy.deepcopy(surf_vertices[self._r_surface])),
        }
        self._railways_model = self._gen_railways_model()

    def _gen_env_mods(self, vertices):
        """Randomly select and arrange environment models.

        Args:
            vertices (list): Vertices of the surface model.

        Returns:
            list:
                Lists in which the first element is an
                environment model name, and the second is
                its position.
        """
        models = []
        et_suf = "et_" if self.enemy_territory else ""

        for models_conf in LOCATIONS["Plains"][et_suf + "with_quantity"]:
            for _ in range(random.randint(*models_conf["quantity"])):
                models.append(
                    (
                        address(random.choice(models_conf["models"])),
                        take_random(vertices[models_conf["square"]]),
                    )
                )
        for models_conf in LOCATIONS["Plains"][et_suf + "with_chance"]:
            if chance(models_conf["chance"]):
                models.append(
                    (
                        address(random.choice(models_conf["models"])),
                        take_random(vertices[models_conf["square"]]),
                    )
                )
        return models

    def _gen_railways_model(self):
        """Select railways model and generate its coordinates.

        Returns:
            list: Railways model name, x and y coords, angle.
        """
        if self.name != "direct" or chance(85):
            return

        model = random.choice(
            (
                "arch1",
                "light_post{}".format(random.randint(1, 2)),
                "lamp_post1",
                "transparant1",
            )
        )
        if model in ("arch1", "transparant1"):
            coor = 0
        else:
            coor = random.choice((0.15, -0.15))

        if model == "lamp_post1" and coor > 0:
            angle = 180
        else:
            angle = 0

        return (address(model), (coor, random.randint(0, 8)), angle)

    def _gen_surface(self, side):
        """Generate surface block.

        Randomly choose one of the surface blocks proper for
        this rails block. Randomly rotate it. Use special
        surface blocks for enemy territory.

        Args:
            side (str): Side of the surface block.

        Returns:
            str, int: Surface model name, angle.
        """
        if self.enemy_territory:
            surface = address("surface_en1")
            return surface, random.choice(ANGLES)

        if self.is_city:
            surface = address("surface_with_" + side + "_city")
            if side == "r":
                return surface, 180
            return surface, 0

        if side == self._station_side:
            surface = address(
                random.choice(
                    (
                        "surface_with_station1",
                        "surface_with_station2",
                        "surface_with_station3",
                    )
                )
            )
            if side == "r":
                return surface, 180
            return surface, 0

        surface = address(random.choice(SURFACES[self.name]))
        if self.name == "direct":
            return surface, random.choice(ANGLES)

        return surface, 0

    def _load_surface_block(self, taskMgr, name, x_pos, y_pos, angle, side=None):
        """Load surface model and set it to the given coords.

        Surface model will be reparented to the rails model
        of this Block. Models are loaded asynchronous to
        avoid freezing.

        Args:
            taskMgr (direct.task.Task.TaskManager): Task manager.
            name (str): Surface model name.
            x_pos (int): Position on X axis.
            y_pos (int): Position on Y axis.
            angle (int): Angle to rotate the model.
            side (str): Left or right side.
        """
        # load surface
        surf_mod = loader.loadModel(name)  # noqa: F821
        surf_mod.reparentTo(self.rails_mod)
        surf_mod.setPos(x_pos, y_pos, 0)
        surf_mod.setH(angle)

        if not side:
            return

        # load environment models asynchronous
        delay = 0
        for env_mod in self._env_mods[side]:
            taskMgr.doMethodLater(
                delay,
                self._load_env_model,
                "load_env_model",
                extraArgs=[surf_mod, env_mod],
            )
            delay += 0.0275

        # load railways model
        if self._railways_model:
            railways_mod = loader.loadModel(self._railways_model[0])  # noqa: F821
            railways_mod.reparentTo(self.rails_mod)

            railways_mod.setX(self._railways_model[1][0])
            railways_mod.setY(self._railways_model[1][1])
            railways_mod.setH(self._railways_model[2])

        if not base.world.sun.is_dark:  # noqa: F821
            # generate texture flowers
            taskMgr.doMethodLater(
                2.5,
                self._gen_flowers,
                "generate_flowers",
                extraArgs=[surf_mod, angle, side],
            )

    def _load_env_model(self, surf_mod, env_mod):
        """Helper to load a model asynchronous.

        Args:
            surf_mod (panda3d.core.NodePath): Surface model.
            env_mod (str): Name of the model to load and its position.
        """
        mod = loader.loadModel(env_mod[0])  # noqa: F821
        mod.reparentTo(surf_mod)
        mod.setPos(env_mod[1])
        mod.setH(random.randint(1, 359))

    def _gen_flowers(self, surf_mod, angle, side):
        """Generate texture flowers.

        Args:
            surf_mod (panda3d.core.NodePath): Surface model.
            angle (int): Surface model angle.
            side (str): Surface model side.
        """
        for i in range(random.randint(0, 3)):
            ts = TextureStage("ts_flower{}".format(str(i)))
            ts.setMode(TextureStage.MDecal)

            tex = loader.loadTexture(  # noqa: F821
                "just_tex/flower{}.png".format(str(random.randint(1, 5)))
            )
            tex.setWrapU(Texture.WMClamp)
            tex.setWrapV(Texture.WMClamp)

            surf_mod.setTexture(ts, tex)
            surf_mod.setTexPos(
                ts,
                random.randint(*FLOWER_RANGES[(angle, side)]["u"]),
                random.randint(*FLOWER_RANGES[(angle, side)]["v"]),
                0,
            )
            surf_mod.setTexScale(ts, 20, 20)

    def prepare(self):
        """Load models, which represents this block content.

        Returns:
            Block: Returns self object.
        """
        if self.is_city:
            self.rails_mod = loader.loadModel(address("city1_rails"))  # noqa: F821
        else:
            self.rails_mod = loader.loadModel(  # noqa: F821
                address(self.name + "_rails")
            )

        self._load_surface_block(
            base.taskMgr, self._l_surface, -4, 4, self._l_angle, "l"  # noqa: F821
        )
        self._load_surface_block(
            base.taskMgr, self._r_surface, 4, 4, self._r_angle, "r"  # noqa: F821
        )

        if self.name == "l90_turn":
            self._load_surface_block(
                base.taskMgr, self._r_surface, -4, 12, self._l_angle  # noqa: F821
            )
            self._load_surface_block(
                base.taskMgr, self._r_surface, 4, 12, self._l_angle  # noqa: F821
            )
        elif self.name == "r90_turn":
            self._load_surface_block(
                base.taskMgr, self._l_surface, 4, 12, self._r_angle  # noqa: F821
            )
            self._load_surface_block(
                base.taskMgr, self._l_surface, -4, 12, self._r_angle  # noqa: F821
            )
        return self

    def prepare_physical_objects(self):
        """Prepare physical objects on this block.

        This method must be called only after reparenting
        the main rails_mod node of the block. Otherwise
        all the children physical nodes will be positioned
        relative to the game render.
        """
        if self.enemy_territory and chance(10):
            Barrier(self)

    def description(self):
        """Build block description.

        Used to save the game world.

        Returns:
            dict: Block description.
        """
        desc = {
            "name": self.name,
            "outing_available": self.outing_available,
            "is_city": self.is_city,
            "station_side": self._station_side,
            "l_surface": self._l_surface,
            "r_surface": self._r_surface,
            "l_angle": self._l_angle,
            "r_angle": self._r_angle,
            "env_mods": self._env_mods,
            "railways_model": self._railways_model,
        }
        return desc
