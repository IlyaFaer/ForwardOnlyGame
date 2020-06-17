"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Game world systems.
"""
import glob

from direct.directutil import Mopath
from panda3d.core import GeomVertexReader

from .block import Block
from .railway_generator import RailwayGenerator
from .sun import Sun
from .locations import LOCATIONS
from personage.enemy import Enemy
from utils import address, MOD_DIR


class World:
    """Object which represents the game world.

    Consists of blocks and is randomly generated.

    Args:
        game (ForwardOnly): Game object.
        train (train.Train): Train object.
        team (personage.character.Team): Player units.
    """

    def __init__(self, game, train, team):
        self._game = game
        self._train = train
        self._team = team
        self._enemy = None
        self._map = []  # all the generated world blocks
        # index of the block, which is
        # processed by World now
        self._block_num = -1
        self._et_blocks = 0

        self._surf_vertices = self._cache_warmup(game.sound_mgr)
        self._paths = self._load_motion_paths()
        self._sun = Sun(game, train)

    def _cache_warmup(self, sound_mgr):
        """Load all the game resources once to cache them.

        When a resource is loaded for the first time,
        render can twitch a little. This can be avoid by
        loading models before the game actually started
        and caching them.

        Args:
            sound_mgr (direct.showbase.Audio3DManager.Audio3DManager): Sound manager.

        Returns:
            dict: Index of vertices of every surface model.
        """
        for path in glob.glob("just_tex/*.png"):
            loader.loadTexture(path)  # noqa: F821

        all_surf_vertices = {}
        for path in glob.glob(MOD_DIR + "*.bam"):
            mod = loader.loadModel(path)  # noqa: F821

            # remember surface models vertices coordinates,
            # later they will be used to positionate
            # environment models
            if "surface" in path:
                all_surf_vertices[path.replace("\\", "/")] = self._read_vertices(
                    mod, path
                )

        for path in glob.glob("sounds/*.ogg"):
            sound_mgr.loadSfx(path)

        return all_surf_vertices

    def _read_vertices(self, mod, path):
        """Read the model vertices and return their positions.

        Args:
            mod (panda3d.core.NodePath): Model to read vertices from.
            path (str): Model filename.

        Returns:
            dict:
                Dict with two lists of points: "wide" - most
                part of the block, and "narrow" - smaller
                part of the block with big paddings on
                every side.
        """
        v_reader = GeomVertexReader(
            mod.findAllMatches("**/+GeomNode")[0].node().getGeom(0).getVertexData(),
            "vertex",
        )
        surf_vertices = {"wide": [], "narrow": []}

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
                surf_vertices["wide"].append(pos)

                if abs(pos.getX()) < 3 and abs(pos.getY()) < 3:
                    surf_vertices["narrow"].append(pos)

        return surf_vertices

    def _load_motion_paths(self):
        """Load all motion path models into index.

        Returns:
            dict: Index of paths.
        """
        paths = {}

        for name in ("direct", "l90_turn", "r90_turn", "ls", "rs"):
            path_mod = loader.loadModel(address(name + "_path"))  # noqa: F821

            # motion path for Train
            paths[name] = Mopath.Mopath(objectToLoad=path_mod)
            paths[name].fFaceForward = True
            # motion path for camera
            paths["cam_" + name] = Mopath.Mopath(objectToLoad=path_mod)

        return paths

    def _prepare_et_block(self):
        """Prepare enemy territory block.

        Returns:
            world.block.Block: Prepared enemy territory block.
        """
        block = Block(
            name="direct",
            path=self._paths["direct"],
            cam_path=self._paths["cam_" + "direct"],
            surf_vertices=self._surf_vertices,
            enemy_territory=True,
        ).prepare(self._game.taskMgr)

        self._map.insert(self._block_num, block)
        return block

    def generate_location(self, location, size):
        """Generate game location.

        Location consists of blocks and enemy fraction.

        Args:
            location (str): Location name.
            size (int): Quantity of blocks to generate.
        """
        rails_gen = RailwayGenerator()
        for _ in range(size):
            rails_block = rails_gen.generate_block()

            if rails_block == "station":
                rails_block = "direct"
                is_station = True
            else:
                is_station = False

            self._map.append(
                Block(
                    name=rails_block,
                    path=self._paths[rails_block],
                    cam_path=self._paths["cam_" + rails_block],
                    surf_vertices=self._surf_vertices,
                    is_station=is_station,
                )
            )
        self._enemy = Enemy(LOCATIONS[location]["enemy"])

    def prepare_next_block(self):
        """Prepare the next world block.

        Block configurations will be taken from the generated
        world map. All of its environment models and
        textures will be loaded and placed on the block.

        Returns:
            block.Block: Prepared world block.
        """
        self._block_num += 1

        if not self._et_blocks and self._enemy.going_to_attack(
            self._sun.day_part, self._train.lights_on
        ):
            self._et_blocks = 20
            self._enemy.prepare(self._train.model)
            self._team.prepare_to_fight(self._enemy.active_units)
            self._train.speed_to_min()

        if self._et_blocks:
            block = self._prepare_et_block()
            self._et_blocks -= 1
            if self._et_blocks == 0:
                self._enemy.stop_attack()
        else:
            block = self._map[self._block_num].prepare(self._game.taskMgr)

        if self._block_num:  # reparent the next block to the current one
            current_block = self._map[self._block_num - 1]
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

    def clear_prev_block(self):
        """Clear models from old block to release memory."""
        num = self._block_num - 3
        if num >= 0:
            # blocks are reparented to each other, so
            # we need to reparent the block to the render
            # before clearing, to avoid chain reaction
            self._map[num + 1].rails_mod.wrtReparentTo(self._game.render)
            self._map[num].rails_mod.removeNode()

            # don't keep enemy territory in the world
            if self._map[num].enemy_territory:
                self._map.pop(num)
                self._block_num -= 1
