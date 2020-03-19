"""Game world systems."""
import random

from direct.directutil import Mopath
from panda3d.core import (
    DirectionalLight,
    AmbientLight,
    TextureStage,
    Texture,
    GeomVertexReader,
)
from railway_generator import RailwayGenerator

ANGLES = (0, 90, 180, 270)
MOD_DIR = "models/bam/"
SURFACES = {
    "direct": ("surface1", "surface2", "surface3"),
    "l90_turn": ("l90_turn_surface1", "l90_turn_surface2"),
    "r90_turn": ("r90_turn_surface1", "r90_turn_surface2"),
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

    Consists of railway block, path for Train to move along, and two surface blocks.

    Args:
        rails_mod_name (str): Name of the rails block model.
        path (Mopath.Mopath): Motion path model.
        cam_path (Mopath.Mopath): Motion path model for camera.
        name (str): Block path name.
    """

    def __init__(self, rails_mod_name, path, cam_path, name):
        self._rails_mod_name = rails_mod_name

        self.rails_mod = None
        self.path = path
        self.name = name
        self.cam_path = cam_path

        self._l_surface, self._l_turn = self._generate_surface()
        self._r_surface, self._r_turn = self._generate_surface()

        self._env_mods = {"l": self._gen_env_mods(), "r": self._gen_env_mods()}

    def _gen_env_mods(self):
        """Select and arrange environment models.

        Every surface have 1024 vertices. Choose on which
        vertex to positionate an environment model.

        Returns:
            dict: Numbers of vertices to set models on, and models names themselves.
        """
        points = set()
        for _ in range(random.randint(0, 30)):
            points.add(random.randint(0, 1023))

        models = {}
        for point in points:
            models[point] = MOD_DIR + "sp_grass{}.bam".format(random.randint(1, 7))

        return models

    def _generate_surface(self):
        """Generate surface block.

        Randomly choose one of the surface blocks proper for this
        rails block. Randomly rotate it.

        Returns:
            str, int: Surface model name, angle.
        """
        surface = MOD_DIR + random.choice(SURFACES[self.name]) + ".bam"
        if self.name == "direct":
            return surface, random.choice(ANGLES)

        return surface, 0

    def _load_surface_block(self, loader, name, x_pos, y_pos, angle, side=None):
        """Load surface model and set it to the given coords.

        Surface model will be reparented to the rails model of this Block.

        Args:
            loader (direct.showbase.Loader.Loader): Panda3d models loader.
            name (str): Surface model name.
            x_pos (int): Position on X axis.
            y_pos (int): Position on Y axis.
            angle (int): Angle to rotate the model.
            side (str): Left or right side.
        """
        # load surface
        surf_mod = loader.loadModel(name)
        surf_mod.reparentTo(self.rails_mod)
        surf_mod.setPos(x_pos, y_pos, 0)
        surf_mod.setH(angle)

        if not side:
            return

        # load environment models
        env_mods = self._env_mods[side]
        if env_mods:
            v_reader = GeomVertexReader(
                surf_mod.findAllMatches("**/+GeomNode")[0]
                .node()
                .getGeom(0)
                .getVertexData(),
                "vertex",
            )
            for i in range(max(env_mods.keys())):
                pos = v_reader.getData3()
                if i in env_mods.keys():
                    if pos.is_nan():
                        continue

                    # don't set a model onto rails
                    if (
                        pos.getX() != 4
                        and pos.getY() != 4
                        and not ("turn" in name and abs(pos.getZ()) < 0.0001)
                    ):
                        env_mod = loader.loadModel(env_mods[i])
                        env_mod.reparentTo(surf_mod)
                        env_mod.setPos(pos)
                        env_mod.setH(random.randint(1, 359))

        # generate texture flowers
        for i in range(random.randint(0, 3)):
            ts = TextureStage("ts_flower{}".format(str(i)))
            ts.setMode(TextureStage.MDecal)

            tex = loader.loadTexture(
                MOD_DIR + "tex/flower{}.png".format(str(random.randint(1, 5)))
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

    def prepare(self, loader, current_block):
        """Load models, which represents this block content.

        Args:
            loader (direct.showbase.Loader.Loader): Panda3d models loader.
            current_block (Block): Block on which Train currently stands.

        Returns:
            Block: Return self object.
        """
        self.rails_mod = loader.loadModel(self._rails_mod_name)

        if current_block:
            self.rails_mod.reparentTo(current_block.rails_mod)

            final_pos = current_block.path.getFinalState()[0]
            self.rails_mod.setPos(
                round(final_pos.getX()),
                round(final_pos.getY()),
                round(final_pos.getZ()),
            )
            if current_block.name == "r90_turn":
                self.rails_mod.setH(-90)
            elif current_block.name == "l90_turn":
                self.rails_mod.setH(90)

        self._load_surface_block(loader, self._l_surface, -4, 4, self._l_turn, "l")
        self._load_surface_block(loader, self._r_surface, 4, 4, self._r_turn, "r")

        if self.name == "l90_turn":
            self._load_surface_block(loader, self._r_surface, -4, 12, self._l_turn)
        elif self.name == "r90_turn":
            self._load_surface_block(loader, self._l_surface, 4, 12, self._r_turn)

        return self


class World:
    """Object which represents the game world.

    Consists of blocks and is randomly generated.

    Args:
        render (panda3d.core.NodePath): Game render.
        loader (direct.showbase.Loader.Loader): Panda3d models loader.
    """

    def __init__(self, render, loader):
        self._loader = loader
        self._world_map = []  # this world blocks

        self._set_general_lights(render)

    def _set_general_lights(self, render):
        """Set general world lights.

        Args:
            render (panda3d.core.NodePath): Game render.
        """
        ambient = AmbientLight("main_amb_light")
        ambient.setColor((0.5, 0.5, 0.5, 1))
        render.setLight(render.attachNewNode(ambient))

        directional = DirectionalLight("main_dir_light")
        directional.setColor((0.7, 0.7, 0.7, 1))
        dlnp = render.attachNewNode(directional)
        dlnp.setHpr(150, 190, 0)
        render.setLight(dlnp)

    def _load_rails_models(self):
        """Load all rails models and paths.

        Returns:
            (dict, dict): Index of paths, index of rails models.
        """
        paths = {}
        rails = {}

        for name, path, model in {
            ("direct", "direct_path.bam", "direct_rails.bam"),
            ("l90_turn", "l90_turn_path.bam", "l90_turn_rails.bam"),
            ("r90_turn", "r90_turn_path.bam", "r90_turn_rails.bam"),
        }:
            path_mod = self._loader.loadModel(MOD_DIR + path)

            # path for Train
            paths[name] = Mopath.Mopath(objectToLoad=path_mod)
            paths[name].fFaceForward = True

            # path for camera
            paths["cam_" + name] = Mopath.Mopath(objectToLoad=path_mod)
            rails[name] = MOD_DIR + model

        return paths, rails

    def generate_location(self, name, size):
        """Generate game location.

        Location consists of blocks.

        Args:
            name (str):
                Location name. Used to get the right location
                configurations (models, lights).
            size (int): Quantity of blocks to generate.
        """
        rails_gen = RailwayGenerator()
        paths, rails = self._load_rails_models()

        for _ in range(size):
            rails_block = rails_gen.generate_block()

            self._world_map.append(
                Block(
                    name=rails_block,
                    rails_mod_name=rails[rails_block],
                    path=paths[rails_block],
                    cam_path=paths["cam_" + rails_block],
                )
            )

    def prepare_block(self, num):
        """Prepare block with the given num.

        Block will be taken from the generated world map.

        Args:
            num (int): World map index of the block to be prepared.

        Returns:
            Block: Prepared world block.
        """
        return self._world_map[num].prepare(
            self._loader, current_block=self._world_map[num - 1] if num else None
        )
