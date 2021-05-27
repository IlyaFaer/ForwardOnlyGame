"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

World blocks API.
"""
import copy
import random

from panda3d.core import TextureStage, Texture, TransparencyAttrib

from utils import address, chance, take_random
from .location import LOCATION_CONF
from .objects import BARRIER_THRESHOLD, ROCKET_THRESHOLD, Barrier, Rocket

ANGLES = (0, 90, 180, 270)
SURFACES = {
    "direct": ("surface1", "surface2", "surface3"),
    "l90_turn": ("l90_turn_surface1", "l90_turn_surface2"),
    "r90_turn": ("r90_turn_surface1", "r90_turn_surface2"),
    "ls": ("surface1", "surface2", "surface3"),
    "rs": ("surface1", "surface2", "surface3"),
    "l_fork": ("surface_exit_from_fork",),
    "r_fork": ("surface_exit_from_fork",),
    "exit_from_fork": ("surface_exit_from_fork",),
}
FLOWER_RANGES = {
    (0, "l"): {"u": (20, 40), "v": (-55, 35)},
    (90, "l"): {"u": (-55, 35), "v": (-60, -35)},
    (180, "l"): {"u": (-55, -35), "v": (-60, 350)},
    (270, "l"): {"u": (-55, 35), "v": (15, 35)},
    (0, "r"): {"u": (-55, -35), "v": (-60, 35)},
    (90, "r"): {"u": (-55, 35), "v": (15, 35)},
    (180, "r"): {"u": (20, 40), "v": (-55, 35)},
    (270, "r"): {"u": (-55, 35), "v": (-60, -35)},
}


class Block:
    """Single world block.

    Consists of railway block, path for the Train to
    move along, environment models and two surface blocks.

    On creation it chooses surface models and arranges
    environment models, but only coordinates and model names
    are generated. All of that content will be loaded on
    Block.prepare() call.

    Args:
        path (Mopath.Mopath): Motion path.
        cam_path (Mopath.Mopath): Motion path for camera.
        name (str): Block path name.
        z_coor (int): Coordinate of the block.
        z_dir (int): Direction of the block along Z-axis.
        id_ (int): The block id.
        direction (dict): Possible movement directions on this block.
        surf_vertices (dict): Vertices index of every surface model.
        branch (str): Branch direction indicator: "l" or "r".
        enemy_territory (bool): This block is an enemy territory.
        is_station (bool): Station must be set on this block.
        is_city (bool): This is a city block.
        is_rusty (bool): Rails on this block are deteriorated.
        is_stenchy (bool): This block is covered with the Stench clouds.
        outing_available (str): An outing type available on this block.
        desc (dict): Block description.
    """

    def __init__(
        self,
        path,
        cam_path,
        name,
        z_coor,
        z_dir,
        id_,
        directions,
        surf_vertices,
        branch=None,
        enemy_territory=False,
        is_station=False,
        is_city=False,
        is_rusty=False,
        is_stenchy=False,
        outing_available=None,
        desc=None,
    ):

        self._surfs = []
        self._phys_objs = []
        self.rails_mod = None
        self._req_add_surface = False
        self._old_values = None

        self.name = name
        self.path = path
        self.cam_path = cam_path
        self.enemy_territory = enemy_territory
        self.outing_available = outing_available
        self.is_city = is_city
        self.is_rusty = is_rusty
        self.is_stenchy = is_stenchy
        self.id = id_
        self.z_coor = z_coor
        self.z_dir = z_dir
        self.directions = directions
        self.branch = branch

        if desc:  # loading block
            self._station_side = desc["station_side"]
            self._l_surface = desc["l_surface"]
            self._r_surface = desc["r_surface"]
            self._l_angle = desc["l_angle"]
            self._r_angle = desc["r_angle"]
            self._env_mods = desc["env_mods"]
            self._railways_model = desc["railways_model"]
            self.id = desc["id"]
            self.branch = desc["branch"]
            self.directions = desc["directions"]
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

        for models_conf in LOCATION_CONF[et_suf + "with_quantity"]:
            for _ in range(random.randint(*models_conf["quantity"])):
                models.append(
                    (
                        random.choice(models_conf["models"]),
                        take_random(vertices[models_conf["square"]]),
                    )
                )
        for models_conf in LOCATION_CONF[et_suf + "with_chance"]:
            if chance(models_conf["chance"]):
                models.append(
                    (
                        random.choice(models_conf["models"]),
                        take_random(vertices[models_conf["square"]]),
                    )
                )
        return models

    def _gen_railways_model(self):
        """Select railways model and generate its coordinates.

        Returns:
            list: Railways model name, x and y coords, angle.
        """
        if self.name != "direct" or chance(85) or self.enemy_territory:
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
            return address("surface_en1"), random.choice(ANGLES)

        if self.is_city:
            return address("surface_with_" + side + "_city"), 180 if side == "r" else 0

        if side == self._station_side:
            surface = address(
                random.choice(
                    (
                        "surface_with_station1",
                        "surface_with_station2",
                        "surface_with_station3",
                        "surface_with_station4",
                    )
                )
            )
            return surface, (180 if side == "r" else 0)

        surface = address(random.choice(SURFACES[self.name]))
        if self.name == "direct":
            return surface, random.choice(ANGLES)

        return surface, 0

    def _load_surface_block(self, name, x_pos, y_pos, angle, side=None, invert=False):
        """Load surface model and set it to the given coords.

        Surface model will be reparented to the rails model
        of this Block. Models are loaded asynchronous to
        avoid freezing.

        Args:
            name (str): Surface model name.
            x_pos (int): Position on X axis.
            y_pos (int): Position on Y axis.
            angle (int): Angle to rotate the model.
            side (str): Left or right side.
            invert (bool):
                True if the Train is moving in the direction
                opposite to the main railway line.
        """
        # load surface
        surf_mod = loader.loadModel(name)  # noqa: F821
        surf_mod.reparentTo(self.rails_mod)
        surf_mod.setPos(x_pos, y_pos, 0)
        surf_mod.setH(angle)

        self._surfs.append(surf_mod)

        if not side:
            return

        # load environment models asynchronous
        delay = 0
        for env_mod in self._env_mods[side]:
            taskMgr.doMethodLater(  # noqa: F821
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
            taskMgr.doMethodLater(  # noqa: F821
                2.5,
                self._gen_flowers,
                "generate_flowers",
                extraArgs=[surf_mod, angle, side],
            )

        if invert:
            if self.name in ("r_fork", "r90_turn"):
                surf_mod.setH(surf_mod, 90)
            elif self.name in ("l_fork", "l90_turn"):
                surf_mod.setH(surf_mod, -90)

    def turn_around(self):
        """Turn the surfaces of the block around."""
        l_surf, r_surf = self._surfs

        l_pos = l_surf.getPos()

        l_surf.setPos(r_surf.getPos())
        l_surf.setH(l_surf, 180)

        r_surf.setPos(l_pos)
        r_surf.setH(r_surf, 180)

    def _load_env_model(self, surf_mod, env_mod):
        """Helper to load a model asynchronous.

        Args:
            surf_mod (panda3d.core.NodePath): Surface model.
            env_mod (str): Name of the model to load and its position.
        """
        mod = loader.loadModel(address(env_mod[0]))  # noqa: F821
        if "grass" in env_mod[0]:
            mod.setTransparency(TransparencyAttrib.M_binary)
            mod.setShaderOff()

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

    def prepare(self, invert=False, from_branch=False):
        """Load models, which represents this block content.

        Args:
            invert (bool):
                True if the Train is moving in the direction
                opposite to the main railway line.
            from_branch (str): Branch direction indicator: "l" or "r".

        Returns:
            Block: Returns self object.
        """
        if self.name in ("l_fork", "r_fork") and from_branch:
            self._old_values = (self.name, self.path, self.cam_path)
            self.name, self.path, self.cam_path = (
                "exit_from_fork",
                (
                    base.world._paths["r90_turn"],  # noqa: F821
                    base.world._paths["l90_turn"],  # noqa: F821
                )
                if self.branch == "r"
                else (
                    base.world._paths["l90_turn"],  # noqa: F821
                    base.world._paths["r90_turn"],  # noqa: F821
                ),
                (
                    base.world._paths["cam_r90_turn"],  # noqa: F821
                    base.world._paths["cam_l90_turn"],  # noqa: F821
                )
                if self.branch == "r"
                else (
                    base.world._paths["cam_l90_turn"],  # noqa: F821
                    base.world._paths["cam_r90_turn"],  # noqa: F821
                ),
            )

        if invert:
            self._old_values = (self.name, self.path, self.cam_path)
            base.world.invert(self)  # noqa: F821

        self.rails_mod = loader.loadModel(  # noqa: F821
            address(self.name + "_rails" + ("_rusty" if self.is_rusty else ""))
        )

        self._load_surface_block(
            self._l_surface, -4, 4, self._l_angle, "l", invert=invert
        )
        self._load_surface_block(
            self._r_surface, 4, 4, self._r_angle, "r", invert=invert
        )

        if self.name == "l90_turn" or (
            self.name == "exit_from_fork"
            and self.branch == "l"
            and base.train.do_turn == 0  # noqa: F821
        ):
            self._load_surface_block(self._r_surface, -4, 12, self._l_angle)
            self._load_surface_block(self._r_surface, 4, 12, self._l_angle)

        elif self.name == "r90_turn" or (
            self.name == "exit_from_fork"
            and self.branch == "r"
            and base.train.do_turn == 0  # noqa: F821
        ):
            self._load_surface_block(self._l_surface, 4, 12, self._r_angle)
            self._load_surface_block(self._l_surface, -4, 12, self._r_angle)

        if self._req_add_surface:
            self.load_additional_surface()
            self._req_add_surface = False

        if self.id == 0:
            surf_mod = loader.loadModel(address("surface1"))  # noqa: F821
            surf_mod.reparentTo(self.rails_mod)
            surf_mod.setPos(-4, -4, 0)

            surf_mod = loader.loadModel(address("surface1"))  # noqa: F821
            surf_mod.reparentTo(self.rails_mod)
            surf_mod.setPos(4, -4, 0)

            rails_mod = loader.loadModel(address("direct_rails"))  # noqa: F821
            rails_mod.reparentTo(self.rails_mod)
            rails_mod.setPos(0, -8, 0)

        return self

    def load_additional_surface(self):
        """Load the additional surface models for this block."""
        # the rails model isn't prepared yet - delay the additional
        # surfaces loading until the rails model loading
        if self.rails_mod is None:
            self._req_add_surface = True
            return

        if self.name == "l_fork" or (
            self.name == "exit_from_fork" and self.branch == "r"
        ):
            self._load_surface_block(self._r_surface, -4, 12, self._l_angle)
            self._load_surface_block(self._r_surface, 4, 12, self._l_angle)

        elif self.name == "r_fork" or (
            self.name == "exit_from_fork" and self.branch == "l"
        ):
            self._load_surface_block(self._l_surface, 4, 12, self._r_angle)
            self._load_surface_block(self._l_surface, -4, 12, self._r_angle)

    def prepare_physical_objects(self):
        """Prepare physical objects on this block.

        This method must be called only after reparenting
        the main rails_mod node of the block. Otherwise
        all the children physical nodes will be positioned
        relative to the game render.
        """
        if (
            self.enemy_territory
            and base.world.enemy.score >= BARRIER_THRESHOLD  # noqa: F821
            and chance(2)
        ):
            self._phys_objs.append(Barrier(self))

        if (
            self.enemy_territory
            and base.world.enemy.score >= ROCKET_THRESHOLD  # noqa: F821
            and chance(2)
        ):
            Rocket()

    def description(self):
        """Build block description.

        Used to save the game world.

        Returns:
            dict: Block description.
        """
        desc = {
            "name": self.name,
            "id": self.id,
            "branch": self.branch,
            "directions": self.directions,
            "outing_available": self.outing_available,
            "is_city": self.is_city,
            "is_rusty": self.is_rusty,
            "is_stenchy": self.is_stenchy,
            "station_side": self._station_side,
            "l_surface": self._l_surface,
            "r_surface": self._r_surface,
            "l_angle": self._l_angle,
            "r_angle": self._r_angle,
            "env_mods": self._env_mods,
            "railways_model": self._railways_model,
        }
        return desc

    def clear(self):
        """Clear this block and revert its inversion."""
        if self._old_values:
            self.name, self.path, self.cam_path = self._old_values
            self._old_values = None

        for obj in self._phys_objs:
            obj.clear()

        self._surfs.clear()
        self.rails_mod.removeNode()
        self.rails_mod = None
