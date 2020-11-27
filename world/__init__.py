"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
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
from personage.enemy import Enemy
from utils import address, chance

from .block import Block
from .locations import LOCATIONS
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
        self._last_angle = 0
        # index of the block, which is
        # processed by World now
        self._block_num = -1
        self._et_blocks = 0

        self._surf_vertices = self._cache_warmup()
        self._paths = self._load_motion_paths()
        self._hangar = None
        self._is_in_city = False
        self._et_rusty_blocks = 0
        self._et_stench_blocks = 0

        self.sun = Sun(day_part_desc)

        self.phys_mgr = self._set_physics()
        base.taskMgr.add(  # noqa: F821
            self.update_physics, "update_physics", extraArgs=[0], appendTask=True
        )

    @property
    def current_block_number(self):
        """The current block index in the world map.

        Returns:
            int: The current block number.
        """
        return self._block_num

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
        return (
            self._is_in_city
            or self._map[self._block_num - 1].is_city
            or self._map[self._block_num - 2].is_city
            or self._map[self._block_num - 3].is_city
        )

    @property
    def last_cleared_block_angle(self):
        """The last cleared block angle.

        Need to be saved to reproduce part of
        the path on loading a saved game.

        Returns:
            int: The block angle.
        """
        return self._last_angle

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
            if "locomotive" in path:
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
            path=self._paths["direct"],
            cam_path=self._paths["cam_" + "direct"],
            surf_vertices=self._surf_vertices,
            enemy_territory=True,
            is_rusty=self._et_rusty_blocks > 0,
            is_stenchy=self._et_stench_blocks > 0,
        ).prepare()

        if self._et_rusty_blocks:
            self._et_rusty_blocks -= 1

        if self._et_stench_blocks:
            self._et_stench_blocks -= 1

        self._map.insert(self._block_num, block)
        return block

    def _track_amb_snd(self, task):
        """Check if current ambient sound should be changed."""
        if self.sun.day_part == "evening":
            base.taskMgr.doMethodLater(  # noqa: F821
                2,
                self._change_amb_snd,
                "change_ambient_sound",
                extraArgs=[self._noon_ambient_snd, self._night_ambient_snd],
                appendTask=True,
            )
        elif self.sun.day_part == "night":
            base.taskMgr.doMethodLater(  # noqa: F821
                2,
                self._change_amb_snd,
                "change_ambient_sound",
                extraArgs=[self._night_ambient_snd, self._noon_ambient_snd],
                appendTask=True,
            )
        return task.again

    def _change_amb_snd(self, from_snd, to_snd, task):
        """Make smooth change between two ambient sounds.

        Args:
            from_snd (panda3d.core.AudioSound):
                Sound to fade.
            from_snd (panda3d.core.AudioSound):
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
        self.outings_mgr = OutingsManager(location)
        map_to_save = []
        rusty_blocks = 0
        stench_blocks = 0

        for num in range(size):
            rails_block = rails_gen.generate_block()

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

            block = Block(
                name=rails_block,
                path=self._paths[rails_block],
                cam_path=self._paths["cam_" + rails_block],
                surf_vertices=self._surf_vertices,
                is_station=is_station,
                is_city=is_city,
                is_rusty=is_rusty,
                is_stenchy=is_stenchy,
                outing_available=None if is_city else self.outings_mgr.plan_outing(),
            )
            self._map.append(block)
            map_to_save.append(block.description())

        world_save = shelve.open("saves/world", "n")
        world_save[location] = map_to_save
        world_save.close()

        self._set_sounds(location)
        self.enemy = Enemy()

    def load_location(self, location, enemy_score, disease_threshold):
        """Load the given location from the last world save.

        Args:
            location (str): Location name.
            enemy_score (int): Enemy score.
            disease_threshold (int): Disease activity score.
        """
        self._disease_threshold = disease_threshold
        self.outings_mgr = OutingsManager(location)

        world_save = shelve.open("saves/world")
        for desc in world_save[location]:
            block = Block(
                name=desc["name"],
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

        self._set_sounds(location)
        self.enemy = Enemy()
        self.enemy.score = enemy_score

    def load_blocks(self, cur_block, angle):
        """Load four blocks to continue saved game.

        There will be prepared four blocks:
        current - 2: block to clear
        current - 1: previous block
        current: the current block
        current + 1: the next block

        Args:
            cur_block (int): The current block number.
            angle (int): The current - 2 block angle.
        """
        self._block_num = cur_block - 3

        block = self._map[self._block_num].prepare()
        block.rails_mod.reparentTo(render)  # noqa: F821
        block.rails_mod.setH(angle)

        base.train.root_node.setH(angle)  # noqa: F821

        final_pos = block.path.getFinalState()[0]
        base.train.root_node.setPos(base.train.root_node, final_pos)  # noqa: F821

        if block.name == "r90_turn":
            base.train.root_node.setH(base.train.root_node, -90)  # noqa: F821
        elif block.name == "l90_turn":
            base.train.root_node.setH(base.train.root_node, 90)  # noqa: F821

        prev_block = self.prepare_next_block()

        final_pos = prev_block.path.getFinalState()[0]
        base.train.root_node.setPos(base.train.root_node, final_pos)  # noqa: F821

        if prev_block.name == "r90_turn":
            base.train.root_node.setH(base.train.root_node, -90)  # noqa: F821
        elif prev_block.name == "l90_turn":
            base.train.root_node.setH(base.train.root_node, 90)  # noqa: F821

        return self.prepare_next_block()

    def _set_sounds(self, location):
        """Configure World sounds.

        Args:
            location (str):
                Location for which sounds must be loaded.
        """
        self._noon_ambient_snd = base.loader.loadSfx(  # noqa: F821
            "sounds/{name}.ogg".format(name=LOCATIONS[location]["ambient_sounds"][0])
        )
        self._noon_ambient_snd.setLoop(True)
        self._noon_ambient_snd.setVolume(1)
        self._noon_ambient_snd.play()

        self._night_ambient_snd = base.loader.loadSfx(  # noqa: F821
            "sounds/{name}.ogg".format(name=LOCATIONS[location]["ambient_sounds"][1])
        )
        self._night_ambient_snd.setVolume(0)
        self._night_ambient_snd.setLoop(True)

        base.taskMgr.doMethodLater(  # noqa: F821
            300, self._track_amb_snd, "track_ambient_sounds"
        )

    def _track_outings(self):
        """Track outing abilities."""
        if self._block_num < 2:
            return

        if (
            self._map[self._block_num + 1].outing_available
            and not self._map[self._block_num + 1].enemy_territory
        ):
            self.outings_mgr.show_upcoming(
                self._map[self._block_num + 1].outing_available
            )
        elif self._map[self._block_num].outing_available:
            self.outings_mgr.show_upcoming_closer()

        elif self._map[self._block_num - 1].outing_available:
            self.outings_mgr.show_can_start()

        elif self._map[self._block_num - 2].outing_available:
            self.outings_mgr.hide_outing()

    def _track_cities(self):
        """Track upcoming cities.

        Slow down and stop Train when approaching to a city.
        """
        if self._block_num < 1:
            return

        if self._map[self._block_num + 1].is_city:
            self._is_in_city = True
            base.train.ctrl.unset_controls()  # noqa: F821
            base.train.slow_down_to(0.7)  # noqa: F821
            self.outings_mgr.show_city()

        elif self._map[self._block_num].is_city:
            base.train.slow_down_to(0.5)  # noqa: F821

        elif self._map[self._block_num - 1].is_city:
            base.train.slow_down_to(0)  # noqa: F821
            base.notes.stop()  # noqa: F821
            base.taskMgr.doMethodLater(  # noqa: F821
                10, base.effects_mgr.fade_out_screen, "fade_screen"  # noqa: F821
            )
            # disable camera movement to avoid flying
            # camera away while loading a hangar scene
            base.taskMgr.doMethodLater(  # noqa: F821
                10,
                base.taskMgr.remove,  # noqa: F821
                "stop_moving_camera_with_mouse",
                extraArgs=["move_camera_with_mouse"],
            )
            base.taskMgr.doMethodLater(  # noqa: F821
                13, self._load_hangar_scene, "load_hangar_scene"
            )

    def _load_hangar_scene(self, task):
        """Load the city hangar scene.

        Load the scene, move Train into the hangar,
        build interface and hide the team.
        """
        self.outings_mgr.hide_outing()  # noqa: F821

        self._hangar = Hangar()

        base.city_interface.show()  # noqa: F821
        base.train.move_to_hangar()  # noqa: F821
        base.team.rest_all()  # noqa: F821

        base.taskMgr.doMethodLater(  # noqa: F821
            2, base.effects_mgr.fade_in_screen, "fade_in_screen"  # noqa: F821
        )
        return task.done

    def unload_hangar_scene(self):
        """Remove the current hangar scene."""
        self._hangar.clear()
        self._hangar = None

        base.train.ctrl.set_controls(base.train)  # noqa: F821
        base.camera_ctrl.enable_ctrl_keys()  # noqa: F821
        base.team.stop_rest_all()  # noqa: F821
        base.notes.resume()  # noqa: F821
        self._is_in_city = False

    def prepare_next_block(self):
        """Prepare the next world block.

        Block configurations will be taken from the generated
        world map. All of its environment models and
        textures will be loaded and placed on the block.

        Returns:
            block.Block: Prepared world block.
        """
        self._block_num += 1

        if not self._et_blocks and self.enemy.going_to_attack(
            self.sun.day_part, base.train.lights_on  # noqa: F821
        ):
            self._et_blocks = 30
            self.enemy.prepare(base.train.model)  # noqa: F821
            base.team.prepare_to_fight()  # noqa: F821
            base.train.ctrl.speed_to_min()  # noqa: F821

        if self._et_blocks:
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
            block = self._map[self._block_num].prepare()

        if self._block_num:  # reparent the next block to the current one
            current_block = self._map[self._block_num - 1]
            block.rails_mod.reparentTo(current_block.rails_mod)
            block.prepare_physical_objects()

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
        else:  # reparent the first block to the render
            block.rails_mod.reparentTo(render)  # noqa: F821

        self._track_outings()
        self._track_cities()
        return block

    def clear_prev_block(self):
        """Clear the block to release memory."""
        num = self._block_num - 3
        if num >= 0:
            # blocks are reparented to each other, so
            # we need to reparent the block to the render
            # before clearing, to avoid chain reaction
            self._last_angle = self._map[num].rails_mod.getH()

            self._map[num + 1].rails_mod.wrtReparentTo(render)  # noqa: F821
            self._map[num].rails_mod.removeNode()

            # don't keep enemy territory in the world
            if self._map[num].enemy_territory:
                self._map.pop(num)
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

    def clear(self):
        """Clear this hangar.

        Remove this hangar models and lights, return
        Train and camera back to their original positions.
        """
        base.camera_ctrl.unset_hangar_pos()  # noqa: F821
        render.clearLight(self._lighter_np)  # noqa: F821
        self._lighter_np.removeNode()
        self._mod.removeNode()

        base.train.root_node.setPos(self._train_pos)  # noqa: F821
        base.taskMgr.doMethodLater(  # noqa: F821
            0.2, base.effects_mgr.fade_in_screen, "fade_in_screen"  # noqa: F821
        )
