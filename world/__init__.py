"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Game world systems.
"""
import glob
import random
import shelve

from direct.directutil import Mopath
from panda3d.bullet import BulletPlaneShape, BulletRigidBodyNode, BulletWorld
from panda3d.core import AudioSound, GeomVertexReader, PerspectiveLens, Spotlight, Vec3

from const import MOD_DIR
from gui import CityGUI, RailsScheme
from personage.enemy import Enemy
from utils import address, chance

from .block import Block
from .locations import LOCATION_CONF
from .outing import OutingsManager
from .railway_generator import RailwayGenerator
from .sun import Sun


class World:
    """Object which represents the Game world.

    Consists of blocks and is randomly generated.

    Args:
        day_part_desc (dict): Day part description.
    """

    def __init__(self, day_part_desc=None):
        self.enemy = None
        self.outings_mgr = None

        self._disease_threshold = 25
        self._noon_ambient_snd = None
        self._night_ambient_snd = None
        self._map = []  # all the world blocks
        self._branches = []
        self._block_coor = 0
        self._block_coor_step = 0
        self._loaded_blocks = []  # currently loaded world blocks
        self._last_angle = 0
        # index of the block, which is
        # processed by World now
        self._block_num = -1
        self._et_blocks = 0
        self._stench_step = 0

        self._prev_block = None
        self._cur_block = None
        self._exiting_et = False

        self._surf_vertices = self._cache_warmup()
        self._paths = self._load_motion_paths()
        self._inversions = self._prepare_inversions()
        self._hangar = None
        self._is_in_city = False
        self._et_rusty_blocks = 0
        self._et_stench_blocks = 0

        self.sun = Sun(day_part_desc)
        self.city_gui = CityGUI()
        self.rails_scheme = RailsScheme(self._map)

        self.phys_mgr = self._set_physics()
        taskMgr.add(  # noqa: F821
            self.update_physics, "update_physics", extraArgs=[0], appendTask=True
        )

    @property
    def branches(self):
        """Railway branches list.

        Returns:
            list: Branches list.
        """
        return self._branches

    @property
    def current_blocks(self):
        """The currently loaded blocks' ids.

        Returns:
            tuple: The currently loaded blocks' ids.
        """
        if len(self._loaded_blocks) < 3:
            return ()

        return (
            self._loaded_blocks[0].id,
            self._loaded_blocks[1].id,
            self._loaded_blocks[2].id,
        )

    @property
    def disease_threshold(self):
        """Return the current disease score value.

        Returns:
            int: Disease activity score.
        """
        return self._disease_threshold

    @property
    def is_in_city(self):
        """Indicates if the Train is near a city.

        Returns:
            bool: True if the Train is near a city.
        """
        factor = -1 if self._loaded_blocks[-2].id < self._loaded_blocks[-1].id else 1
        return (
            self._is_in_city
            or self._map[self._block_num + 1 * factor].is_city
            or self._map[self._block_num + 2 * factor].is_city
            or self._map[self._block_num + 3 * factor].is_city
        )

    @property
    def is_near_fork(self):
        """Indicates if the Train is near a railway fork.

        Returns:
            bool: True if the Train is near a fork.
        """
        if len(self._loaded_blocks) > 2:
            return self._loaded_blocks[1].name in (
                "r_fork",
                "l_fork",
                "exit_from_fork",
            ) or self._loaded_blocks[0].name in ("r_fork", "l_fork", "exit_from_fork")

    @property
    def is_on_et(self):
        """Indicates if the Train is near enemy territory.

        Returns:
            bool: True if the Train is near enemy territory.
        """
        for block in self._loaded_blocks:
            if block.enemy_territory:
                return True
        return False

    @property
    def last_cleared_block_angle(self):
        """The last cleared block angle.

        Need to be saved to reproduce part of
        the path on loading a saved game.

        Returns:
            int: The block angle.
        """
        return self._last_angle

    @property
    def stench_step(self):
        """The block number, where the edge of the Stench is."""
        return self._stench_step

    def _cache_warmup(self):
        """Load all the game resources once to cache them.

        When a resource is loaded for the first time,
        render can twitch a little. This can be avoid by
        loading models before the game actually started
        and caching them.

        Returns:
            dict: Index of vertices of every surface model.
        """
        for path in glob.glob("just_tex/*.png"):
            loader.loadTexture(path)  # noqa: F821

        all_surf_vertices = {}
        for path in glob.glob(MOD_DIR + "*.bam"):
            dont_load = False
            for name in (
                "locomotive",
                "train_part_arrow",
                "soldier",
                "raider",
                "anarchist",
                "character_pointer",
                "city_hangar",
                "sun_path",
                "relation_ball",
                "tree",
            ):
                if name in path:
                    dont_load = True
                    break

            if dont_load:
                continue

            mod = loader.loadModel(path)  # noqa: F821
            mod.setZ(-20)
            mod.reparentTo(render)  # noqa: F821

            # remember surface models vertices coordinates,
            # later they will be used to positionate
            # environment models
            if "surface" in path:
                all_surf_vertices[path.replace("\\", "/")] = self._read_vertices(
                    mod, path
                )

        for path in glob.glob("sounds/*.ogg"):
            base.sound_mgr.loadSfx(path)  # noqa: F821

        return all_surf_vertices

    def _make_stench_step(self, task):
        """Move the Stench edge one block further."""
        self._map[self._stench_step].is_stenchy = True
        self._stench_step += 1

        if self._stench_step == self._block_num:
            base.effects_mgr.stench_effect.play_clouds()  # noqa: F821
            base.effects_mgr.stench_effect.play()  # noqa: F821

            base.team.start_stench_activity()  # noqa: F821

        return task.again

    def _prepare_inversions(self):
        """Prepare inversion variants."""
        inversions = {
            "r90_turn": (
                "l90_turn",
                self._paths["l90_turn"],
                self._paths["cam_l90_turn"],
            ),
            "l90_turn": (
                "r90_turn",
                self._paths["r90_turn"],
                self._paths["cam_r90_turn"],
            ),
            "l_fork": ("r_fork", self._paths["r_fork"], self._paths["cam_r_fork"]),
            "r_fork": ("l_fork", self._paths["l_fork"], self._paths["cam_l_fork"]),
        }
        return inversions

    def _set_physics(self):
        """Set the world physics.

        Returns:
            panda3d.bullet.BulletWorld: Physical world.
        """
        world = BulletWorld()
        world.setGravity(Vec3(0, 0, -0.5))

        shape = BulletPlaneShape(Vec3(0, 0, 1), 0.02)
        node = BulletRigidBodyNode("Ground")
        node.addShape(shape)

        render.attachNewNode(node)  # noqa: F821
        world.attachRigidBody(node)

        base.train.set_physics(world)  # noqa: F821
        return world

    def update_physics(self, y_coor, task):
        """Update physics calculations.

        Args:
            y_coor (float):
                Y coordinate for the main
                Train physical shape.
        """
        self.phys_mgr.doPhysics(globalClock.getDt())  # noqa: F821

        base.train.update_physics(y_coor)  # noqa: F821
        return task.cont

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
                abs(pos.getX()) < 3.99
                and abs(pos.getY()) < 3.99
                and not ("turn" in path and abs(pos.getZ()) < 0.0001)
                and not ("fork" in path and abs(pos.getZ()) < 0.02)
                # don't remember vertices of station and city models
                and not ("station" in path and abs(pos.getY()) < 2.1)
                and not ("city" in path and abs(pos.getY()) < 2.1)
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

        # every fork has two paths
        paths["r_fork"] = (paths["direct"], paths["r90_turn"])
        paths["cam_r_fork"] = (paths["cam_direct"], paths["cam_r90_turn"])

        paths["l_fork"] = (paths["direct"], paths["l90_turn"])
        paths["cam_l_fork"] = (paths["cam_direct"], paths["cam_l90_turn"])

        paths["exit_from_fork"] = (paths["l90_turn"], paths["r90_turn"])
        paths["cam_exit_from_fork"] = (paths["cam_l90_turn"], paths["cam_r90_turn"])

        return paths

    def _prepare_et_block(self):
        """Prepare enemy territory block.

        Returns:
            world.block.Block: Prepared enemy territory block.
        """
        if self._et_blocks > 8:
            if not self._et_rusty_blocks and chance(3):
                self._et_rusty_blocks = random.randint(4, 8)

            if not self._et_stench_blocks and chance(2):
                self._et_stench_blocks = random.randint(4, 8)

        block = Block(
            name="direct",
            z_coor=0,
            z_dir=0,
            id_=-1,
            directions={},
            path=self._paths["direct"],
            cam_path=self._paths["cam_" + "direct"],
            surf_vertices=self._surf_vertices,
            enemy_territory=True,
            is_rusty=self._et_rusty_blocks > 0,
            is_stenchy=self._et_stench_blocks > 0,
        ).prepare()

        self._loaded_blocks.append(block)

        if self._et_rusty_blocks:
            self._et_rusty_blocks -= 1

        if self._et_stench_blocks:
            self._et_stench_blocks -= 1

        self._map.insert(self._block_num, block)
        return block

    def _track_amb_snd(self, task):
        """Check if current ambient sound should be changed."""
        if self.sun.day_part in ("evening", "night"):
            taskMgr.doMethodLater(  # noqa: F821
                2,
                self._change_amb_snd,
                "change_ambient_sound",
                extraArgs=[self._noon_ambient_snd, self._night_ambient_snd]
                if self.sun.day_part == "evening"
                else [self._night_ambient_snd, self._noon_ambient_snd],
                appendTask=True,
            )
        return task.again

    def _change_amb_snd(self, from_snd, to_snd, task):
        """Make smooth change between two ambient sounds.

        Args:
            from_snd (panda3d.core.AudioSound):
                Sound to fade.
            to_snd (panda3d.core.AudioSound):
                Sound to make main.
        """
        from_volume = from_snd.getVolume()

        if from_volume > 0:
            if to_snd.status() != AudioSound.PLAYING:
                to_snd.play()

            from_snd.setVolume(from_volume - 0.05)
            to_snd.setVolume(to_snd.getVolume() + 0.05)

            return task.again

        from_snd.stop()
        return task.done

    def drop_outing_ability(self):
        """Drop the current block outing ability."""
        self._loaded_blocks[-2].outing_available = None

    def start_outing(self, type_):
        """Start an outing with the given type.

        Args:
            type_ (str): Outing type.
        """
        self.outings_mgr.start_outing(type_)

    def generate_location(self, location, size):
        """Generate game location.

        Location consists of blocks, enemy and
        a list of available outings.

        Args:
            location (str): Location name.
            size (int): Quantity of blocks to generate.
        """
        rails_gen = RailwayGenerator()
        self.outings_mgr = OutingsManager()
        rusty_blocks = 0
        stench_blocks = 0

        # generating the main railway line
        for num, rails_block in enumerate(rails_gen.generate_main_line(size)):

            if not rusty_blocks and chance(2):
                rusty_blocks = random.randint(4, 8)

            if num > 100:
                if not stench_blocks and chance(2):
                    stench_blocks = random.randint(6, 10)

            is_city = False
            is_station = False

            if rails_block == "station":
                rails_block = "direct"
                is_station = True
            elif rails_block == "city":
                rails_block = "direct"
                is_city = True

            if rusty_blocks:
                is_rusty = True
                rusty_blocks -= 1
            else:
                is_rusty = False

            if stench_blocks and not is_city:
                is_stenchy = True
                stench_blocks -= 1
            else:
                is_stenchy = False

            self._block_coor += self._block_coor_step

            if rails_block == "r90_turn":
                self._block_coor_step -= 1
            elif rails_block == "l90_turn":
                self._block_coor_step += 1

            self._map.append(
                Block(
                    name=rails_block,
                    id_=num,
                    z_coor=self._block_coor,
                    z_dir=self._block_coor_step,
                    directions={num - 1: num + 1, num + 1: num - 1} if num > 0 else {},
                    path=self._paths[rails_block],
                    cam_path=self._paths["cam_" + rails_block],
                    surf_vertices=self._surf_vertices,
                    is_station=is_station,
                    is_city=is_city,
                    is_rusty=is_rusty,
                    is_stenchy=is_stenchy,
                    outing_available=None
                    if is_city
                    else self.outings_mgr.plan_outing(),
                )
            )

        # generating branches
        self._branches = rails_gen.generate_branches(self._map)
        for branch in self._branches:
            br_start_block = Block(
                name=branch["blocks"][0],
                id_=branch["start"],
                branch=branch["side"],
                z_coor=self._block_coor,
                z_dir=self._block_coor_step,
                directions={
                    branch["start"] - 1: (branch["start"] + 1, len(self._map)),
                    len(self._map): (branch["start"] + 1, branch["start"] - 1),
                    branch["start"] + 1: (branch["start"] - 1, len(self._map)),
                },
                path=self._paths[branch["blocks"][0]],
                cam_path=self._paths["cam_" + branch["blocks"][0]],
                surf_vertices=self._surf_vertices,
                is_station=is_station,
                is_city=False,
                is_rusty=is_rusty,
                is_stenchy=is_stenchy,
                outing_available=self.outings_mgr.plan_outing(),
            )

            self._map[branch["start"]] = br_start_block

            is_first = True
            index = 1
            for rails_block in branch["blocks"][1:-1]:
                if not rusty_blocks and chance(2):
                    rusty_blocks = random.randint(4, 8)

                if num > 100:
                    if not stench_blocks and chance(2):
                        stench_blocks = random.randint(6, 10)

                is_station = False

                if rails_block == "station":
                    rails_block = "direct"
                    is_station = True

                if rusty_blocks:
                    is_rusty = True
                    rusty_blocks -= 1
                else:
                    is_rusty = False

                if stench_blocks:
                    is_stenchy = True
                    stench_blocks -= 1
                else:
                    is_stenchy = False

                if rails_block == "r90_turn":
                    self._block_coor_step -= 1
                elif rails_block == "l90_turn":
                    self._block_coor_step += 1

                self._block_coor += self._block_coor_step

                num += 1
                self._map.append(
                    Block(
                        name=rails_block,
                        id_=num,
                        branch=branch["side"],
                        z_coor=self._block_coor,
                        z_dir=self._block_coor_step,
                        directions={
                            branch["start"]: len(self._map) + 1,
                            len(self._map) + 1: branch["start"],
                        }
                        if is_first
                        else {
                            len(self._map) - 1: len(self._map) + 1,
                            len(self._map) + 1: len(self._map) - 1,
                        },
                        path=self._paths[rails_block],
                        cam_path=self._paths["cam_" + rails_block],
                        surf_vertices=self._surf_vertices,
                        is_station=is_station,
                        is_city=False,
                        is_rusty=is_rusty,
                        is_stenchy=is_stenchy,
                        outing_available=self.outings_mgr.plan_outing(),
                    )
                )
                # replace the block name with the block object
                branch["blocks"][index] = self._map[-1]
                index += 1
                is_first = False

            self._map[-1].directions = {
                branch["end"]: len(self._map) - 2,
                len(self._map) - 2: branch["end"],
            }

            br_end_block = Block(
                name=branch["blocks"][-1],
                branch=branch["side"],
                id_=branch["end"],
                z_coor=self._block_coor,
                z_dir=self._block_coor_step,
                directions={
                    branch["end"] - 1: (branch["end"] + 1, len(self._map) - 1),
                    len(self._map) - 1: (branch["end"] + 1, branch["end"] - 1),
                    branch["end"] + 1: (branch["end"] - 1, len(self._map) - 1),
                },
                path=self._paths[branch["blocks"][-1]],
                cam_path=self._paths["cam_" + branch["blocks"][-1]],
                surf_vertices=self._surf_vertices,
                is_station=is_station,
                is_city=False,
                is_rusty=is_rusty,
                is_stenchy=is_stenchy,
                outing_available=self.outings_mgr.plan_outing(),
            )

            self._map[branch["end"]] = br_end_block

        self._set_sounds()
        self.enemy = Enemy()
        taskMgr.doMethodLater(23, self._make_stench_step, "stench_step")  # noqa: F821

    def invert(self, block):
        """Invert the given block.

        While the Train is moving along the main railway line, every
        turn is correct, but when the Train is moving in opposite
        direction, every turn must be mirrored.
        """
        if block.name in self._inversions:
            block.name, block.path, block.cam_path = self._inversions[block.name]

    def save_map(self, num):
        """Save the world map.

        Args:
            num (int): The number of save slot.
        """
        map_to_save = []

        for block in self._map:
            map_to_save.append(block.description())

        world_save = shelve.open("saves/world{}".format(str(num)), "n")
        world_save["Plains"] = map_to_save
        world_save["Plains_branches"] = self.branches
        world_save.close()

    def show_scheme(self):
        """Show railways scheme GUI."""
        self.rails_scheme.show()

    def load_location(self, location, num, enemy_score, disease_threshold, stench_step):
        """Load the given location from the last save.

        Args:
            location (str): Location name.
            num (int): The save slot number.
            enemy_score (int): Enemy score.
            disease_threshold (int): Disease activity score.
            stench_step (int):
                Number of the block, where the Stench edge is located.
        """
        self._disease_threshold = disease_threshold

        self._stench_step = stench_step
        taskMgr.doMethodLater(30, self._make_stench_step, "stench_step")  # noqa: F821

        self.outings_mgr = OutingsManager()

        world_save = shelve.open("saves/world{}".format(str(num)))
        for desc in world_save[location]:
            block = Block(
                name=desc["name"],
                id_=desc["id"],
                directions=desc["directions"],
                branch=desc["branch"],
                z_coor=None,
                z_dir=None,
                path=self._paths[desc["name"]],
                cam_path=self._paths["cam_" + desc["name"]],
                surf_vertices=self._surf_vertices,
                is_station=desc["station_side"] is not None,
                is_city=desc["is_city"],
                is_rusty=desc["is_rusty"],
                is_stenchy=desc["is_stenchy"],
                outing_available=desc["outing_available"],
                desc=desc,
            )
            self._map.append(block)

        self._set_sounds()
        self.enemy = Enemy()
        self.enemy.score = enemy_score

        self._branches = world_save[location + "_branches"]

    def load_blocks(self, cur_blocks, angle):
        """Load blocks around player to continue the saved game.

        Args:
            cur_block (int): The current block number.
            angle (int): The current - 2 block angle.
        """
        block = self._map[cur_blocks[0]].prepare()
        block.rails_mod.reparentTo(render)  # noqa: F821
        block.rails_mod.setH(angle)
        self._loaded_blocks.append(block)

        base.train.root_node.setH(angle)  # noqa: F821

        final_pos = block.path.getFinalState()[0]
        base.train.root_node.setPos(base.train.root_node, final_pos)  # noqa: F821

        if block.name == "r90_turn":
            base.train.root_node.setH(base.train.root_node, -90)  # noqa: F821
        elif block.name == "l90_turn":
            base.train.root_node.setH(base.train.root_node, 90)  # noqa: F821

        cur_block = self.prepare_next_block(cur_blocks[1])
        return cur_block

    def _set_sounds(self):
        """Configure the location sounds."""
        self._noon_ambient_snd = loader.loadSfx(  # noqa: F821
            "sounds/{name}.ogg".format(name=LOCATION_CONF["ambient_sounds"][0])
        )
        self._noon_ambient_snd.setLoop(True)
        self._noon_ambient_snd.setVolume(1)
        self._noon_ambient_snd.play()

        self._night_ambient_snd = loader.loadSfx(  # noqa: F821
            "sounds/{name}.ogg".format(name=LOCATION_CONF["ambient_sounds"][1])
        )
        self._night_ambient_snd.setVolume(0)
        self._night_ambient_snd.setLoop(True)

        taskMgr.doMethodLater(  # noqa: F821
            300, self._track_amb_snd, "track_ambient_sounds"
        )

    def _track_outings(self):
        """Track outing abilities."""
        if len(self._loaded_blocks) < 2:
            return

        current_block = self._loaded_blocks[-2]
        if current_block.enemy_territory:
            self.outings_mgr.hide_outing()
            return

        new_block = self._loaded_blocks[-1].directions[current_block.id]
        if isinstance(new_block, tuple):
            return

        if self._map[new_block].outing_available:
            self.outings_mgr.show_upcoming(self._map[new_block].outing_available)

        elif self._map[self._loaded_blocks[-1].id].outing_available:
            self.outings_mgr.show_upcoming_closer()

        elif self._map[current_block.id].outing_available:
            self.outings_mgr.show_can_start()

        elif not self._is_in_city:
            self.outings_mgr.hide_outing()

    def _track_cities(self):
        """Track upcoming cities.

        Slow down and stop the Train when
        approaching to a city.
        """
        if len(self._loaded_blocks) < 2:
            return

        current_block = self._loaded_blocks[-2]
        if current_block.enemy_territory:
            return

        new_block = self._loaded_blocks[-1].directions[current_block.id]
        if isinstance(new_block, tuple):
            return

        if self._map[new_block].is_city:
            self._is_in_city = True
            base.train.ctrl.unset_controls()  # noqa: F821
            base.train.slow_down_to(0.7)  # noqa: F821
            self.outings_mgr.show_city()

        elif self._map[self._loaded_blocks[-1].id].is_city:
            base.train.slow_down_to(0.5)  # noqa: F821

        elif self._map[current_block.id].is_city:
            base.train.slow_down_to(0)  # noqa: F821
            base.notes.stop()  # noqa: F821
            taskMgr.doMethodLater(  # noqa: F821
                10, base.effects_mgr.fade_out_screen, "fade_screen"  # noqa: F821
            )
            # disable camera movement to avoid flying
            # camera away while loading a hangar scene
            taskMgr.doMethodLater(  # noqa: F821
                10,
                taskMgr.remove,  # noqa: F821
                "stop_moving_camera_with_mouse",
                extraArgs=["move_camera_with_mouse"],
            )
            taskMgr.doMethodLater(  # noqa: F821
                13, self._load_hangar_scene, "load_hangar_scene"
            )

    def _track_forks(self):
        """Track approaching forks and notify the player."""
        if len(self._loaded_blocks) < 2:
            return

        current_block = self._loaded_blocks[-2]
        if current_block.enemy_territory:
            return

        new_block = self._loaded_blocks[-1].directions[current_block.id]

        if isinstance(new_block, tuple):
            return

        if self._map[new_block].name in ("l_fork", "r_fork", "exit_from_fork"):
            base.train.show_turning_ability(  # noqa: F821
                self._map[new_block],
                current_block.branch,
                new_block < current_block.id,
            )

        if current_block.name in ("l_fork", "r_fork", "exit_from_fork"):
            base.train.hide_turning_ability()  # noqa: F821

    def _load_hangar_scene(self, task):
        """Load the city hangar scene.

        Load the scene, move the Train into the hangar,
        build interface and hide the team.
        """
        self.outings_mgr.hide_outing()  # noqa: F821

        self._hangar = Hangar()

        self.stop_ambient_snd()
        self.city_gui.show()
        base.train.move_to_hangar()  # noqa: F821
        base.team.rest_all()  # noqa: F821

        taskMgr.doMethodLater(  # noqa: F821
            2, base.effects_mgr.fade_in_screen, "fade_in_screen"  # noqa: F821
        )
        return task.done

    def unload_hangar_scene(self, turn_around):
        """Clear the current hangar scene.

        Args:
            turn_around (bool): True, if the Train should be turned around.
        """
        self._hangar.clear(turn_around)
        self._hangar = None

        self.resume_ambient_snd()
        base.train.ctrl.set_controls(base.train)  # noqa: F821
        base.camera_ctrl.enable_ctrl_keys()  # noqa: F821
        base.team.stop_rest_all()  # noqa: F821
        base.notes.resume()  # noqa: F821
        self._is_in_city = False

    def prepare_next_block(self, block_num=None, from_city=False):
        """Prepare the next world block.

        Args:
            block_num (int): Optional. Id of the block to prepare.
            from_city (bool):
                Optional. True if the next block is
                loaded to continue the way from a city.

        Block configurations will be taken from the generated
        world map. All of its environment models and
        textures will be loaded and placed on the block.

        Returns:
            block.Block: Prepared world block.
        """
        if block_num is not None:
            self._block_num = block_num
        else:
            self._block_num += 1

        if (
            len(self._loaded_blocks) > 2
            and self._loaded_blocks[-2].id >= 15
            and not self._et_blocks
            and self.enemy.going_to_attack(
                self.sun.day_part, base.train.lights_on  # noqa: F821
            )
        ):
            self._prev_block = self._loaded_blocks[-2].id
            self._cur_block = self._loaded_blocks[-1].id

            self._et_blocks = 30
            self.enemy.prepare(base.train.model)  # noqa: F821
            base.team.prepare_to_fight()  # noqa: F821
            base.train.ctrl.speed_to_min()  # noqa: F821

        if self._loaded_blocks:
            current_block = self._loaded_blocks[-1]

        if self._et_blocks:
            self._exiting_et = False
            block = self._prepare_et_block()

            self._map[self._block_num - 1].enemy_territory = True
            self._et_blocks -= 1
            if self._et_blocks == 0:
                self.enemy.stop_attack()

            # as enemy units are prepared async, wait for
            # five enemy territory blocks passed before
            # checking for enemy units activiness
            if self._et_blocks <= 25 and not self.enemy.active_units:
                self._et_blocks = min(2, self._et_blocks)
        else:
            if len(self._loaded_blocks) > 1:
                prev_block_num = self._loaded_blocks[-2].id

                # Enemy territory blocks are not considered in the world
                # map (they has id = -1). That creates a special case for
                # blocks loading system, when previous blocks are non-
                # -considered enemy blocks, which can't be routed to the
                # real blocks. Instead of enemy blocks - real blocks (which
                # were loaded before the enemy territory) must be used.
                if prev_block_num == -1:
                    inverse = self._prev_block > self._cur_block
                    prev_block_num = self._prev_block

                    if not current_block.directions:
                        current_block.directions = self._map[self._cur_block].directions

                    if inverse:
                        next_block = current_block.directions[prev_block_num]
                        if next_block == self._block_num:
                            next_block -= 1
                    else:
                        if self._exiting_et:
                            next_block = current_block.directions[prev_block_num] + 2
                        else:
                            next_block = current_block.directions[prev_block_num] + 3

                    self._prev_block = self._cur_block
                    self._cur_block = self._map[next_block].id

                    self._exiting_et = True
                else:
                    if self._prev_block is not None:
                        next_block = current_block.directions[prev_block_num]
                        if isinstance(next_block, tuple):
                            next_block = next_block[base.train.do_turn]  # noqa: F821

                        if self._prev_block < self._cur_block:
                            next_block += 1

                        self._prev_block = None
                    else:
                        next_block = current_block.directions[prev_block_num]

                if isinstance(next_block, tuple):
                    next_block = next_block[base.train.do_turn]  # noqa: F821

                cur_id = current_block.id if current_block.id != -1 else self._cur_block

                block = self._map[next_block].prepare(
                    invert=cur_id > self._map[next_block].id,
                    from_branch=current_block.branch,
                )
                self._block_num = block.id
            else:
                block = self._map[self._block_num].prepare()

            self._loaded_blocks.append(block)

        if self._block_num:  # reparent the next block to the current one
            block.rails_mod.reparentTo(current_block.rails_mod)
            block.prepare_physical_objects()

            path = (
                current_block.path[base.train.do_turn]  # noqa: F821
                if isinstance(current_block.path, tuple)
                else current_block.path
            )
            final_pos = path.getFinalState()[0]
            block.rails_mod.setPos(
                round(final_pos.getX()),
                round(final_pos.getY()),
                round(final_pos.getZ()),
            )
            if (
                current_block.name == "r90_turn"
                or (
                    current_block.name == "r_fork"
                    and base.train.do_turn == 1  # noqa: F821
                )
                or (
                    current_block.name == "exit_from_fork"
                    and current_block.branch == "r"
                    and base.train.do_turn == 0  # noqa: F821
                )
                or (
                    current_block.name == "exit_from_fork"
                    and current_block.branch == "l"
                    and base.train.do_turn == 1  # noqa: F821
                )
            ):
                block.rails_mod.setH(-90)

            if (
                current_block.name == "l90_turn"
                or (
                    current_block.name == "l_fork"
                    and base.train.do_turn == 1  # noqa: F821
                )
                or (
                    current_block.name == "exit_from_fork"
                    and current_block.branch == "l"
                    and base.train.do_turn == 0  # noqa: F821
                )
                or (
                    current_block.name == "exit_from_fork"
                    and current_block.branch == "r"
                    and base.train.do_turn == 1  # noqa: F821
                )
            ):
                block.rails_mod.setH(90)
        else:  # reparent the first block to the render
            block.rails_mod.reparentTo(render)  # noqa: F821

        if not from_city:
            self._track_cities()
            self._track_outings()
            self._track_forks()

        return block

    def clear_prev_block(self):
        """Clear the block to release memory."""
        if len(self._loaded_blocks) > 3:
            block_to_clear = self._loaded_blocks.pop(0)
            # blocks are reparented to each other, so
            # we need to reparent the block to the render
            # before clearing, to avoid chain reaction
            self._last_angle = block_to_clear.rails_mod.getH()

            self._loaded_blocks[0].rails_mod.wrtReparentTo(render)  # noqa: F821
            block_to_clear.clear()

            # don't keep enemy territory in the world
            if block_to_clear.id == -1:
                self._map.remove(block_to_clear)
                self._block_num -= 1

    def disease_activity(self, task):
        """Run a disease activity iteration.

        Activity includes getting characters
        diseased with some possibility.
        """
        self._disease_threshold -= 1

        if self._disease_threshold == 0:
            self._disease_threshold = 25

            for char in base.team.chars.values():  # noqa: F821
                char.get_sick()

        return task.again

    def stop_ambient_snd(self):
        """Stop all the ambient sounds."""
        self._noon_ambient_snd.stop()
        self._night_ambient_snd.stop()

    def resume_ambient_snd(self):
        """Continue playing the ambient sound."""
        if (
            self._noon_ambient_snd.getVolume() > 0
            and self._noon_ambient_snd.status() != AudioSound.PLAYING
        ):
            self._noon_ambient_snd.play()
        elif (
            self._night_ambient_snd.getVolume() > 0
            and self._night_ambient_snd.status() != AudioSound.PLAYING
        ):
            self._night_ambient_snd.play()

    def turn_around(self):
        """Turn the Train around.

        The next block will be the same as was previous.
        """
        prev_block = self._loaded_blocks[0]
        cur_block = self._loaded_blocks[1]
        next_block = self._loaded_blocks[2]

        next_block.rails_mod.wrtReparentTo(render)  # noqa: F821
        cur_block.rails_mod.wrtReparentTo(render)  # noqa: F821

        cur_block.turn_around()
        self._loaded_blocks.reverse()

        next_block.rails_mod.setPos(cur_block.rails_mod.getPos())
        next_block.rails_mod.setH(next_block.rails_mod, 180)

        cur_block.rails_mod.wrtReparentTo(next_block.rails_mod)

        prev_block.clear()
        self._loaded_blocks.pop(-1)
        self.prepare_next_block(from_city=True)

        base.current_block = self._loaded_blocks[-1]  # noqa: F821


class Hangar:
    """City hangar scene.

    Includes hangar models, lights, camera position.
    Remembers the last camera and Train positions
    to return them back correctly to the positions they
    were before moving to ther hangar.
    """

    def __init__(self):
        self._train_pos = base.train.root_node.getPos()  # noqa: F821

        self._mod = loader.loadModel(address("city_hangar"))  # noqa: F821

        base.camera_ctrl.set_hangar_pos(self._mod)  # noqa: F821

        self._mod.reparentTo(base.train.model)  # noqa: F821

        lens = PerspectiveLens()
        lens.setNearFar(0, 10)
        lens.setFov(100, 100)

        lighter = Spotlight("hangar_light")
        lighter.setColor((1, 1, 1, 1))
        lighter.setLens(lens)
        self._lighter_np = self._mod.attachNewNode(lighter)
        self._lighter_np.setPos(-0.3, 0.65, 4)
        self._lighter_np.lookAt(base.train.model)  # noqa: F821

        render.setLight(self._lighter_np)  # noqa: F821

    def clear(self, turn_around):
        """Clear this hangar.

        Remove this hangar models and lights, return
        Train and camera back to their original positions.

        Args:
            turn_around (bool): True, if the Train should be turned around.
        """
        base.camera_ctrl.unset_hangar_pos()  # noqa: F821
        render.clearLight(self._lighter_np)  # noqa: F821
        self._lighter_np.removeNode()
        self._mod.removeNode()

        base.train.root_node.setPos(self._train_pos)  # noqa: F821
        if turn_around:
            base.world.turn_around()  # noqa: F821

        taskMgr.doMethodLater(  # noqa: F821
            0.2, base.effects_mgr.fade_in_screen, "fade_in_screen"  # noqa: F821
        )
