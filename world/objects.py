"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Active world objects API.
"""
import random

from panda3d.bullet import BulletBoxShape, BulletRigidBodyNode
from panda3d.core import Vec3

from utils import address


class Barrier:
    """Enemy barrier.

    Deals damage to Train on hit.

    Args:
        block (world.block.Block): Block to set this barrier on.
    """

    def __init__(self, block):
        id_ = "barrier_" + str(random.randint(1, 10000))
        y_coor = random.randint(8, 16)

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
