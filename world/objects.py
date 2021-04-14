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

    Deals damage to the Train on a hit.

    Args:
        block (world.block.Block): Block to set this barrier on.
    """

    def __init__(self, block):
        id_ = "barrier_" + str(random.randint(1, 10000))
        y_coor = random.randint(8, 16)
        self._rb_nodes = []

        self._prepare_physics(
            id_, block, 0.07, y_coor,
        )
        self._prepare_physics(
            id_, block, -0.07, y_coor,
        )

    def _prepare_physics(self, id_, block, x_coor, y_coor):
        """Prepare physics for the given model.

        Args:
            id_ (str):
                Barrier id. Used as a prefix in rigid body id.
            block (world.block.Block):
                Block to set barrier on.
            x_coor (float): X axis coordinate to set block on.
            y_coor (float): Y axis coordinate to set block on.
        """
        rb_node = BulletRigidBodyNode(id_ + str(x_coor))
        rb_node.setMass(150)
        rb_node.addShape(BulletBoxShape(Vec3(0.05, 0.005, 0.05)))

        phys_np = block.rails_mod.attachNewNode(rb_node)
        phys_np.setPos(x_coor, y_coor, 0.07)
        phys_np.setH(random.randint(-20, 20))
        loader.loadModel(address("barrier1")).reparentTo(phys_np)  # noqa: F821

        base.world.phys_mgr.attachRigidBody(rb_node)  # noqa: F821
        self._rb_nodes.append(rb_node)

    def clear(self):
        """Clear physical shapes."""
        for rb_node in self._rb_nodes:
            base.world.phys_mgr.removeRigidBody(rb_node)  # noqa: F821

        self._rb_nodes.clear()


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

        self._hiss_snd = base.sound_mgr.loadSfx("sounds/rocket_fly.ogg")  # noqa: F821
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
