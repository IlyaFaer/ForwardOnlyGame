"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Active world objects API.
"""
import random

from direct.actor.Actor import Actor
from panda3d.bullet import BulletBoxShape, BulletRigidBodyNode
from panda3d.core import Vec3
from direct.interval.IntervalGlobal import Sequence

from utils import address


class Barrier:
    """Enemy barrier.

    Deals damage to the Train on hit.

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


class ArmorPlate:
    """An active shield Train upgrade.

    Represents an active defense upgrade - plate, which
    can cover one of three Train sides: left, right, top.

    Args:
        train_model (panda3d.core.NodePath):
            The Train model - parent for the plate.
    """

    def __init__(self, train_model):
        self._is_on_move = False
        self._cur_position = "top"

        self._model = Actor(address("armor_plate"))
        self._model.reparentTo(train_model)

        self._right_to_left = Sequence(
            self._model.actorInterval("right", playRate=-1.5),
            self._model.actorInterval("left", playRate=1.5),
        )
        self._left_to_right = Sequence(
            self._model.actorInterval("left", playRate=-1.5),
            self._model.actorInterval("right", playRate=1.5),
        )

        base.accept("5", self._turn_left)  # noqa: F821
        base.accept("6", self._turn_top)  # noqa: F821
        base.accept("7", self._turn_right)  # noqa: F821

    def _turn_right(self):
        """Cover the right side of the Train with the plate."""
        if self._cur_position == "right" or self._is_on_move:
            return

        if self._cur_position == "top":
            self._model.play("right")
            delay = 1.9
        else:
            self._left_to_right.start()
            delay = 3.3

        self._is_on_move = True
        base.taskMgr.doMethodLater(  # noqa: F821
            delay, self._stop_move, "stop_move_plate"
        )
        base.taskMgr.doMethodLater(  # noqa: F821
            delay - 0.9,
            base.train.cover_part,  # noqa: F821
            "cover_part",
            extraArgs=["part_locomotive_right"],
        )
        base.taskMgr.doMethodLater(  # noqa: F821
            0.5,
            base.train.uncover_part,  # noqa: F821
            "uncover_part",
            extraArgs=[self._cur_position],
        )
        self._cur_position = "right"

    def _turn_left(self):
        """Cover the left side of the Train with the plate."""
        if self._cur_position == "left" or self._is_on_move:
            return

        if self._cur_position == "top":
            self._model.play("left")
            delay = 1.9
        else:
            self._right_to_left.start()
            delay = 3.3

        self._is_on_move = True
        base.taskMgr.doMethodLater(  # noqa: F821
            delay, self._stop_move, "stop_move_plate"
        )
        base.taskMgr.doMethodLater(  # noqa: F821
            delay - 0.9,
            base.train.cover_part,  # noqa: F821
            "cover_part",
            extraArgs=["part_locomotive_left"],
        )
        base.taskMgr.doMethodLater(  # noqa: F821
            0.5,
            base.train.uncover_part,  # noqa: F821
            "uncover_part",
            extraArgs=[self._cur_position],
        )
        self._cur_position = "left"

    def _turn_top(self):
        """Cover the top side of the Train with the plate."""
        if self._cur_position == "top" or self._is_on_move:
            return

        if self._cur_position == "left":
            self._model.actorInterval("left", playRate=-1.5).start()
        elif self._cur_position == "right":
            self._model.actorInterval("right", playRate=-1.5).start()

        self._is_on_move = True
        base.taskMgr.doMethodLater(  # noqa: F821
            1.9, self._stop_move, "stop_move_plate"
        )
        base.taskMgr.doMethodLater(  # noqa: F821
            0.5,
            base.train.uncover_part,  # noqa: F821
            "uncover_part",
            extraArgs=[self._cur_position],
        )
        self._cur_position = "top"

    def _stop_move(self, task):
        """Release the plate moving block."""
        self._is_on_move = False
        return task.done
