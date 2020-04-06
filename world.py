"""Game world systems."""
import glob

from direct.directutil import Mopath
from panda3d.core import DirectionalLight, AmbientLight, GeomVertexReader
from railway_generator import RailwayGenerator

from block import Block

MOD_DIR = "models/bam/"


class World:
    """Object which represents the game world.

    Consists of blocks and is randomly generated.

    Args:
        render (panda3d.core.NodePath): Game render.
        loader (direct.showbase.Loader.Loader): Panda3d models loader.
    """

    def __init__(self, render, loader):
        self._world_map = []  # world blocks
        self._loader = loader

        self._surf_vertices = self._cache_warmup(loader)
        self._set_general_lights(render)

    def _set_general_lights(self, render):
        """Set general world lights.

        Args:
            render (panda3d.core.NodePath): Game render.
        """
        ambient = AmbientLight("main_amb_light")
        ambient.setColor((0.6, 0.6, 0.6, 1))
        render.setLight(render.attachNewNode(ambient))

        directional = DirectionalLight("main_dir_light")
        directional.setColor((0.8, 0.8, 0.8, 1))
        dlnp = render.attachNewNode(directional)
        dlnp.setHpr(150, 190, 0)
        render.setLight(dlnp)

    def _cache_warmup(self, loader):
        """Load all of the game models and textures once to cache them.

        Args:
            loader (direct.showbase.Loader.Loader): Panda3d loader.

        Returns:
            dict: Index of vertices of every surface model.
        """
        for path in glob.glob("just_tex/*.png"):
            loader.loadTexture(path)

        all_surf_vertices = {}
        for path in glob.glob("models/bam/*.bam"):
            mod = loader.loadModel(path)

            # read and remember surface vertices
            if "surface" in path:
                all_surf_vertices[path.replace("\\", "/")] = self._read_vertices(
                    mod, path
                )

        return all_surf_vertices

    def _read_vertices(self, mod, path):
        """Read model vertices and build a list of their positions.

        Args:
            mod (panda3d.core.NodePath): Model to read vertices from.
            path (str): Model filename.

        Returns:
            list: List of vertices positions.
        """
        v_reader = GeomVertexReader(
            mod.findAllMatches("**/+GeomNode")[0].node().getGeom(0).getVertexData(),
            "vertex",
        )
        surf_vertices = []

        while not v_reader.isAtEnd():
            pos = v_reader.getData3()
            if pos.is_nan():
                continue

            # don't set a model onto rails
            if (
                pos.getX() not in (-4, 4)
                and pos.getY() not in (-4, 4)
                and not ("turn" in path and abs(pos.getZ()) < 0.0001)
            ):
                surf_vertices.append(pos)

        return surf_vertices

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
            self._loader,
            current_block=self._world_map[num - 1] if num else None,
            surf_vertices=self._surf_vertices,
        )
