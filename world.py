"""Game world systems."""
import random

from direct.directutil import Mopath
from panda3d.core import DirectionalLight, AmbientLight

from railway_generator import RailwayGenerator

ANGLES = (0, 90, 180, 270)
MOD_DIR = "models/bam/"
SURFACES = {"direct": ("surface1", "surface2", "surface3")}


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

        if self.name == "direct":
            self._l_surface, self._l_turn = self._generate_surface()
            self._r_surface, self._r_turn = self._generate_surface()

    def _generate_surface(self):
        """Generate surface block.

        Randomly choose one of the surface blocks proper for this
        rails block. Randomly rotate it.
        """
        surface = MOD_DIR + random.choice(SURFACES[self.name]) + ".bam"
        turn = random.choice(ANGLES)
        return surface, turn

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

        if self.name == "direct":
            l_surf = loader.loadModel(self._l_surface)
            l_surf.reparentTo(self.rails_mod)
            l_surf.setPos(-4, 4, 0)
            l_surf.setH(self._l_turn)

            r_surf = loader.loadModel(self._r_surface)
            r_surf.reparentTo(self.rails_mod)
            r_surf.setPos(4, 4, 0)
            r_surf.setH(self._l_turn)

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
