"""Game world systems."""
import glob

from direct.directutil import Mopath
from panda3d.core import GeomVertexReader

from .block import Block
from .railway_generator import RailwayGenerator
from .sun import Sun

MOD_DIR = "models/bam/"


class World:
    """Object which represents the game world.

    Consists of blocks and is randomly generated.

    Args:
        game (ForwardOnly): Game object.
        train (train.Train): Train object.
    """

    def __init__(self, game, train):
        self._game = game
        self._world_map = []  # generated world blocks

        self._surf_vertices = self._cache_warmup(game.loader)
        Sun(game, train)

    def _cache_warmup(self, loader):
        """Load all the game models and textures to cache them.

        When model is loaded for the first time, render
        can twitch a little. This can be avoid by loading
        models before the game actually started and
        caching them.

        Args:
            loader (direct.showbase.Loader.Loader): Panda3d loader.

        Returns:
            dict: Index of vertices of every surface model.
        """
        for path in glob.glob("just_tex/*.png"):
            loader.loadTexture(path)

        all_surf_vertices = {}
        for path in glob.glob(MOD_DIR + "*.bam"):
            mod = loader.loadModel(path)

            # remember surface models vertices coordinates,
            # later they will be used to positionate
            # environment models
            if "surface" in path:
                all_surf_vertices[path.replace("\\", "/")] = self._read_vertices(
                    mod, path
                )

        return all_surf_vertices

    def _read_vertices(self, mod, path):
        """Read the model vertices and return their positions.

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

            if (
                # don't remember coordinates of vertices
                # on which rails will be set
                pos.getX() not in (-4, 4)
                and pos.getY() not in (-4, 4)
                and not ("turn" in path and abs(pos.getZ()) < 0.0001)
                # don't remember vertices of station models
                and not ("station" in path and abs(pos.getY()) < 2.1)
            ):
                surf_vertices.append(pos)

        return surf_vertices

    def _load_rails_models(self):
        """Load all rails models and motion paths.

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
            path_mod = self._game.loader.loadModel(MOD_DIR + path)

            # motion path for Train
            paths[name] = Mopath.Mopath(objectToLoad=path_mod)
            paths[name].fFaceForward = True

            # motion path for camera
            paths["cam_" + name] = Mopath.Mopath(objectToLoad=path_mod)
            rails[name] = MOD_DIR + model

        return paths, rails

    def generate_location(self, size):
        """Generate game location.

        Location consists of blocks.

        Args:
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
                    surf_vertices=self._surf_vertices,
                )
            )

    def prepare_block(self, num):
        """Prepare world block with the given num.

        Block configurations will be taken from the generated
        world map. All of its environment models and
        textures will be loaded and placed on the block.

        Args:
            num (int): World map index of the block to be prepared.

        Returns:
            block.Block: Prepared world block.
        """
        block = self._world_map[num].prepare(self._game.loader, self._game.taskMgr)

        if num:  # reparent the next block to the current one
            current_block = self._world_map[num - 1]
            block.rails_mod.reparentTo(current_block.rails_mod)

            final_pos = current_block.path.getFinalState()[0]
            block.rails_mod.setPos(
                round(final_pos.getX()),
                round(final_pos.getY()),
                round(final_pos.getZ()),
            )
            if current_block.name == "r90_turn":
                block.rails_mod.setH(-90)
            elif current_block.name == "l90_turn":
                block.rails_mod.setH(90)
        else:  # reparent the first world block to the render
            block.rails_mod.reparentTo(self._game.render)

        return block

    def clear_block(self, num):
        """Clear models from old block to release memory.

        Args:
            num (int): World map index of the block to be cleared.
        """
        if num >= 0:
            # blocks are reparented to each other, so
            # we need to reparent the block to the render
            # before clearing, to avoid chain reaction
            self._world_map[num + 1].rails_mod.wrtReparentTo(self._game.render)
            self._world_map[num].rails_mod.removeNode()
