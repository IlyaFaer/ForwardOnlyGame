"""World blocks API."""
import copy
import random
from panda3d.core import TextureStage, Texture
from utils import chance

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

    Consists of railway block, path for Train to
    move along, environment models and two surface blocks.

    On creation it chooses surface models and arranges
    environment models, but only coordinates and model names
    are generated. All of that content will be loaded on
    Block.prepare() call.

    Args:
        rails_mod_name (str): Rails block model name.
        path (Mopath.Mopath): Motion path.
        cam_path (Mopath.Mopath): Motion path for camera.
        name (str): Block path name.
        surf_vertices (dict): Vertices index of every surface model.
    """

    def __init__(self, rails_mod_name, path, cam_path, name, surf_vertices):
        self._rails_mod_name = rails_mod_name

        self.path = path
        self.name = name
        self.cam_path = cam_path

        self._l_surface, self._l_turn = self._gen_surface("l")
        self._r_surface, self._r_turn = self._gen_surface("r")

        self._env_mods = {
            "l": self._gen_env_mods(copy.copy(surf_vertices[self._l_surface])),
            "r": self._gen_env_mods(copy.copy(surf_vertices[self._r_surface])),
        }
        self._railways_model = self._gen_railways_model()

    def _choose_pos(self, vertices):
        """
        Every surface model have 1024 vertices - choose on
        which of them to positionate an environment model.

        Args:
            vertices (list): List of vertices.

        Returns:
            list: Vertex position.
        """
        pos = random.choice(vertices)
        vertices.remove(pos)
        return pos

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

        for _ in range(random.randint(10, 40)):
            models.append(
                (
                    MOD_DIR + "sp_grass{}.bam".format(random.randint(1, 7)),
                    self._choose_pos(vertices),
                )
            )
        for _ in range(random.randint(10, 20)):
            models.append(
                (
                    MOD_DIR + "tree{}.bam".format(random.randint(1, 3)),
                    self._choose_pos(vertices),
                )
            )
        for _ in range(random.randint(2, 8)):
            models.append((MOD_DIR + "stone1.bam", self._choose_pos(vertices)))

        if chance(7):
            models.append(
                (
                    MOD_DIR + "grave{}.bam".format(random.randint(1, 2)),
                    self._choose_pos(vertices),
                )
            )
        if chance(8):
            models.append(
                (
                    MOD_DIR + random.choice(("fireplace1.bam", "tent.bam")),
                    self._choose_pos(vertices),
                )
            )
        return models

    def _gen_railways_model(self):
        """Select railways model and generate its coordinates.

        Returns:
            list: Railways model name, x and y coords, angle.
        """
        if self.name != "direct" or chance(85):
            return None

        model = random.choice(
            (
                "light_post{}.bam".format(random.randint(1, 2)),
                "lamp_post1.bam",
                "arch1.bam",
            )
        )
        if model != "arch1.bam":
            coor = random.choice((0.15, -0.15))
        else:
            coor = 0

        if model == "lamp_post1.bam" and coor > 0:
            angle = 180
        else:
            angle = 0

        return (
            MOD_DIR + model,
            (coor, random.randint(0, 8)),
            angle,
        )

    def _gen_surface(self, side):
        """Generate surface block.

        Randomly choose one of the surface blocks proper for
        this rails block. Randomly rotate it.

        Args:
            side (str): Side of the surface block.

        Returns:
            str, int: Surface model name, angle.
        """
        if chance(1) and self.name == "direct":
            surface = MOD_DIR + "surface_with_station1.bam"
            if side == "r":
                return surface, 180
            return surface, 0

        surface = MOD_DIR + random.choice(SURFACES[self.name]) + ".bam"
        if self.name == "direct":
            return surface, random.choice(ANGLES)

        return surface, 0

    def _load_surface_block(
        self, loader, taskMgr, name, x_pos, y_pos, angle, side=None
    ):
        """Load surface model and set it to the given coords.

        Surface model will be reparented to the rails model
        of this Block. Models are loaded asynchronous to
        avoid freezing.

        Args:
            loader (direct.showbase.Loader.Loader): Panda3D models loader.
            taskMgr (direct.task.Task.TaskManager): Task manager.
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

        # load environment models asynchronous
        delay = 0
        for env_mod in self._env_mods[side]:
            taskMgr.doMethodLater(
                delay,
                self._load_env_model,
                "load_env_model",
                extraArgs=[loader, surf_mod, env_mod],
            )
            delay += 0.03

        # load railways model
        if self._railways_model:
            railways_mod = loader.loadModel(self._railways_model[0])
            railways_mod.reparentTo(self.rails_mod)

            railways_mod.setX(self._railways_model[1][0])
            railways_mod.setY(self._railways_model[1][1])
            railways_mod.setH(self._railways_model[2])

        # generate texture flowers
        taskMgr.doMethodLater(
            3,
            self._generate_flowers,
            "generate_flowers",
            extraArgs=[loader, surf_mod, angle, side],
        )

    def _load_env_model(self, loader, surf_mod, env_mod):
        """Helper to load a model asynchronous.

        Args:
            loader (direct.showbase.Loader.Loader): Panda3D loader.
            surf_mod (panda3d.core.NodePath): Surface model.
            env_mod (str): Name of the model to load and its position.
        """
        mod = loader.loadModel(env_mod[0])
        mod.reparentTo(surf_mod)
        mod.setPos(env_mod[1])
        mod.setH(random.randint(1, 359))

    def _generate_flowers(self, loader, surf_mod, angle, side):
        """Generate texture flowers.

        Args:
            loader (direct.showbase.Loader.Loader): Panda3D loader.
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

    def prepare(self, loader, taskMgr):
        """Load models, which represents this block content.

        Args:
            loader (direct.showbase.Loader.Loader): Panda3d models loader.
            taskMgr (direct.task.Task.TaskManager): Task manager.

        Returns:
            Block: Returns self object.
        """
        self.rails_mod = loader.loadModel(self._rails_mod_name)

        self._load_surface_block(
            loader, taskMgr, self._l_surface, -4, 4, self._l_turn, "l"
        )
        self._load_surface_block(
            loader, taskMgr, self._r_surface, 4, 4, self._r_turn, "r"
        )

        if self.name == "l90_turn":
            self._load_surface_block(
                loader, taskMgr, self._r_surface, -4, 12, self._l_turn
            )
        elif self.name == "r90_turn":
            self._load_surface_block(
                loader, taskMgr, self._l_surface, 4, 12, self._r_turn
            )
        return self
