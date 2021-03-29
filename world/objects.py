"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Active world objects API.
"""
import random

from direct.actor.Actor import Actor
from direct.directutil import Mopath
from direct.interval.IntervalGlobal import (
    Func,
    LerpPosInterval,
    Parallel,
    Sequence,
    SoundInterval,
    Wait,
)
from direct.interval.MopathInterval import MopathInterval
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.bullet import BulletBoxShape, BulletRigidBodyNode
from panda3d.core import Vec3


from utils import address

BARRIER_THRESHOLD = 8
ROCKET_THRESHOLD = 16


class Barrier:
    """Enemy barrier.

    Deals damage to the Train on hit.

    Args:
        block (world.block.Block): Block to set this barrier on.
    """

    def __init__(self, block):
        id_ = "barrier_" + str(random.randint(1, 10000))
        y_coor = random.randint(8, 16)
        self._rb_nodes = []

        self._prepare_physics(
            id_,
            block,
            loader.loadModel(address("barrier1")),  # noqa: F821
            0.07,
            y_coor,
        )
        self._prepare_physics(
            id_,
            block,
            loader.loadModel(address("barrier1")),  # noqa: F821
            -0.07,
            y_coor,
        )

    def _prepare_physics(self, id_, block, model, x_coor, y_coor):
        """Prepare physics for the given model.

        Args:
            id_ (str):
                Barrier id. Used as a prefix in rigid body id.
            block (world.block.Block):
                Block to set barrier on.
            model (panda3d.core.NodePath): Barrier model.
            x_coor (float): X axis coordinate to set block on.
            y_coor (float): Y axis coordinate to set block on.
        """
        rb_node = BulletRigidBodyNode(id_ + str(x_coor))
        rb_node.setMass(150)
        rb_node.addShape(BulletBoxShape(Vec3(0.05, 0.005, 0.05)))

        phys_np = block.rails_mod.attachNewNode(rb_node)
        phys_np.setPos(x_coor, y_coor, 0.07)
        phys_np.setH(random.randint(-20, 20))
        model.reparentTo(phys_np)

        base.world.phys_mgr.attachRigidBody(rb_node)  # noqa: F821
        self._rb_nodes.append(rb_node)

    def clear(self):
        """Clear physical shapes."""
        for rb_node in self._rb_nodes:
            base.world.phys_mgr.removeRigidBody(rb_node)  # noqa: F821

        self._rb_nodes.clear()


class ArmorPlate:
    """An active shield Train upgrade.

    Represents an active defense upgrade - plate, which
    can cover one of Train sides: left, right, top.

    Args:
        train_model (panda3d.core.NodePath):
            The Train model - parent for the plate.
    """

    def __init__(self, train_model):
        self._is_on_move = False
        self.cur_position = "top"

        self._snd = base.sound_mgr.loadSfx("sounds/armor_plate_move.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(self._snd, train_model)  # noqa: F821

        self._model = Actor(address("armor_plate"))
        self._model.reparentTo(train_model)

        self._right_to_left = Sequence(
            Parallel(
                self._model.actorInterval("right", playRate=-2.5),
                SoundInterval(self._snd),
            ),
            Parallel(
                self._model.actorInterval("left", playRate=2.5),
                SoundInterval(self._snd),
            ),
        )
        self._left_to_right = Sequence(
            Parallel(
                self._model.actorInterval("left", playRate=-2.5),
                SoundInterval(self._snd),
            ),
            Parallel(
                self._model.actorInterval("right", playRate=2.5),
                SoundInterval(self._snd),
            ),
        )
        base.accept("5", self._turn_left)  # noqa: F821
        base.accept("6", self._turn_top)  # noqa: F821
        base.accept("7", self._turn_right)  # noqa: F821

    def _cover_side(self, side):
        """Actually change the plate position.

        Args:
            side (str):
                Side of the train, which is
                now covered by the plate.
        """
        self.cur_position = side

    def _stop_move(self, task):
        """Release the plate moving block."""
        self._is_on_move = False
        return task.done

    def _turn_left(self):
        """Cover the left side of the Train with the plate."""
        if self.cur_position == "left" or self._is_on_move:
            return

        if self.cur_position == "top":
            self._model.actorInterval("left", playRate=2.5).start()
            delay = 0.9
            cover_delay = 0.45
            self._snd.play()
        else:
            self._right_to_left.start()
            delay = 1.8
            cover_delay = 1.35

        self._is_on_move = True
        taskMgr.doMethodLater(delay, self._stop_move, "stop_move_plate")  # noqa: F821
        taskMgr.doMethodLater(  # noqa: F821
            cover_delay, self._cover_side, "cover_side", extraArgs=["left"]
        )
        taskMgr.doMethodLater(  # noqa: F821
            cover_delay,
            base.train.cover_part,  # noqa: F821
            "cover_part",
            extraArgs=["part_locomotive_left"],
        )
        taskMgr.doMethodLater(  # noqa: F821
            0.5,
            base.train.uncover_part,  # noqa: F821
            "uncover_part",
            extraArgs=[self.cur_position],
        )

    def _turn_right(self):
        """Cover the right side of the Train with the plate."""
        if self.cur_position == "right" or self._is_on_move:
            return

        if self.cur_position == "top":
            self._model.actorInterval("right", playRate=2.5).start()
            delay = 0.9
            cover_delay = 0.45
            self._snd.play()
        else:
            self._left_to_right.start()
            delay = 1.8
            cover_delay = 1.35

        self._is_on_move = True
        taskMgr.doMethodLater(delay, self._stop_move, "stop_move_plate")  # noqa: F821
        taskMgr.doMethodLater(  # noqa: F821
            cover_delay, self._cover_side, "cover_side", extraArgs=["right"]
        )
        taskMgr.doMethodLater(  # noqa: F821
            cover_delay,
            base.train.cover_part,  # noqa: F821
            "cover_part",
            extraArgs=["part_locomotive_right"],
        )
        taskMgr.doMethodLater(  # noqa: F821
            0.5,
            base.train.uncover_part,  # noqa: F821
            "uncover_part",
            extraArgs=[self.cur_position],
        )

    def _turn_top(self):
        """Cover the top side of the Train with the plate."""
        if self.cur_position == "top" or self._is_on_move:
            return

        if self.cur_position == "left":
            self._snd.play()
            self._model.actorInterval("left", playRate=-2.5).start()
        elif self.cur_position == "right":
            self._snd.play()
            self._model.actorInterval("right", playRate=-2.5).start()

        self._is_on_move = True
        taskMgr.doMethodLater(0.9, self._stop_move, "stop_move_plate")  # noqa: F821
        taskMgr.doMethodLater(  # noqa: F821
            0.45, self._cover_side, "cover_side", extraArgs=["top"]
        )
        taskMgr.doMethodLater(  # noqa: F821
            0.5,
            base.train.uncover_part,  # noqa: F821
            "uncover_part",
            extraArgs=[self.cur_position],
        )


class Rocket:
    """An enemy rocket object.

    A rocket is overtaking the locomotive
    from behind and making a hit at it.
    """

    def __init__(self):
        x_coor, side = random.choice(((0.553, "left"), (-0.553, "right"), (0, "top")))

        self._model = Actor(address("rocket1"))
        self._model.reparentTo(base.train.model)  # noqa: F821
        self._model.setPos(x_coor, -7, 0.5)

        self._smoke = ParticleEffect()
        self._smoke.loadConfig("effects/smoke_tail.ptf")
        self._smoke.start(self._model, render)  # noqa: F821

        path = Mopath.Mopath(
            objectToLoad=loader.loadModel(  # noqa: F821
                address("rocket_{}_path".format(side))
            )
        )
        path.fFaceForward = True

        self._hiss_snd = base.sound_mgr.loadSfx("sounds/rocket_fly1.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(self._hiss_snd, self._model)  # noqa: F821

        self._hiss_snd2 = base.sound_mgr.loadSfx("sounds/rocket_hiss.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(self._hiss_snd2, self._model)  # noqa: F821

        self._hiss_snd.play()
        seq = Sequence(
            LerpPosInterval(
                self._model, 7, (x_coor, -0.627, 0.561), blendType="easeOut"
            ),
            Wait(0.3),
            Parallel(
                SoundInterval(self._hiss_snd2),
                MopathInterval(
                    path, self._model, duration=0.5, name="rocket_current_path"
                ),
            ),
            Func(self._explode, side),
        )
        seq.start()

    def _explode(self, side):
        """Explode the rocket.

        Args:
            side (str):
                Locomotive's side where the rocket is exploded.
        """
        self._model.cleanup()
        self._model.removeNode()
        self._smoke.softStop()

        self._hiss_snd.stop()
        base.sound_mgr.detach_sound(self._hiss_snd)  # noqa: F821
        base.sound_mgr.detach_sound(self._hiss_snd2)  # noqa: F821

        base.train.explode_rocket(side)  # noqa: F821
        taskMgr.doMethodLater(  # noqa: F821
            2,
            self._smoke.disable,
            "disable_rocket_smoke",
            extraArgs=[],
            appendTask=False,
        )
