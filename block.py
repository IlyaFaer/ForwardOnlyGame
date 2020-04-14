"""World blocks API."""
import copy
import random

from panda3d.core import TextureStage, Texture

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
        self._railways_model = self._gen_railways_model()

    def _gen_env_mods(self):
        """Select environment models.

        Returns:
            list: Environment models names.
        """
        models = []
        for _ in range(random.randint(10, 40)):
            models.append(MOD_DIR + "sp_grass{}.bam".format(random.randint(1, 7)))

        for _ in range(random.randint(10, 20)):
            models.append(MOD_DIR + "tree{}.bam".format(random.randint(1, 3)))

        for _ in range(random.randint(2, 8)):
            models.append(MOD_DIR + "stone1.bam")

        if random.randint(1, 100) <= 7:
            models.append(MOD_DIR + "grave{}.bam".format(random.randint(1, 2)))

        return models

    def _gen_railways_model(self):
        """Select railways model and generate its coordinates.

        Returns:
            list: Railways model name, x and y coords.
        """
        if self.name != "direct" or random.randint(1, 100) < 87:
            return None

        model = "light_post{}.bam".format(random.randint(1, 2))
        return (
            MOD_DIR + model,
            (random.choice((0.15, -0.15)), random.randint(0, 8)),
        )

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

    def _load_surface_block(
        self, loader, taskMgr, name, x_pos, y_pos, angle, surface_vertices, side=None
    ):
        """Load surface model and set it to the given coords.

        Surface model will be reparented to the rails model of this Block.
        Models are loaded asynchronous to avoid freezing.

        Args:
            loader (direct.showbase.Loader.Loader): Panda3D models loader.
            taskMgr (direct.task.Task.TaskManager): Task manager.
            name (str): Surface model name.
            x_pos (int): Position on X axis.
            y_pos (int): Position on Y axis.
            angle (int): Angle to rotate the model.
            surface_vertices (dict): Index of vertices of every surface model.
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
        vertices = copy.copy(surface_vertices[name])
        delay = 0
        for mod_name in self._env_mods[side]:
            # every surface model have 1024 vertices. Choose on
            # which vertex to positionate an environment model.
            pos = random.choice(vertices)
            vertices.remove(pos)

            taskMgr.doMethodLater(
                delay,
                self._load_env_model,
                "load_tree",
                extraArgs=[loader, surf_mod, mod_name, pos],
            )
            delay += 0.03

        # load railways models
        if self._railways_model:
            railways_mod = loader.loadModel(self._railways_model[0])
            railways_mod.reparentTo(self.rails_mod)
            railways_mod.setX(self._railways_model[1][0])
            railways_mod.setY(self._railways_model[1][1])

        taskMgr.doMethodLater(
            3,
            self._generate_flowers,
            "generate_flowers",
            extraArgs=[loader, surf_mod, angle, side],
        )

    def _load_env_model(self, loader, surf_mod, mod_name, pos):
        """Helper to load a model asinchronous.

        Args:
            loader (direct.showbase.Loader.Loader): Panda3D models loader.
            surf_mod (panda3d.core.NodePath): Surface model.
            mod_name (str): Name of the model to load.
            pos (list): Position to set model on.
        """
        env_mod = loader.loadModel(mod_name)
        env_mod.reparentTo(surf_mod)
        env_mod.setPos(pos)
        env_mod.setH(random.randint(1, 359))

    def _generate_flowers(self, loader, surf_mod, angle, side):
        """Generate texture flowers.

        Args:
            loader (direct.showbase.Loader.Loader): Panda3D models loader.
            surf_mod (panda3d.core.NodePath): Surface model.
            angle (int): Surface model angle.
            side (str): Surface model side.
        """
        for i in range(random.randint(0, 3)):
            ts = TextureStage("ts_flower{}".format(str(i)))
            ts.setMode(TextureStage.MDecal)

            tex = loader.loadTexture(
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

    def prepare(self, loader, taskMgr, current_block, surf_vertices):
        """Load models, which represents this block content.

        Args:
            loader (direct.showbase.Loader.Loader): Panda3d models loader.
            taskMgr (direct.task.Task.TaskManager): Task manager.
            current_block (Block): Block on which Train currently stands.
            surf_vertices (dict): Index of vertices of every surface model.

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

        self._load_surface_block(
            loader, taskMgr, self._l_surface, -4, 4, self._l_turn, surf_vertices, "l"
        )
        self._load_surface_block(
            loader, taskMgr, self._r_surface, 4, 4, self._r_turn, surf_vertices, "r"
        )

        if self.name == "l90_turn":
            self._load_surface_block(
                loader, taskMgr, self._r_surface, -4, 12, self._l_turn, surf_vertices
            )
        elif self.name == "r90_turn":
            self._load_surface_block(
                loader, taskMgr, self._l_surface, 4, 12, self._r_turn, surf_vertices
            )
        return self
