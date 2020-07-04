"""Base API for all the Game units."""
import abc

from panda3d.core import CollisionNode


class Unit(metaclass=abc.ABCMeta):
    """Base unit class.

    Args:
        id_ (str): Unit id.
        health (int): Health points.
        class_ (str): Unit class.
    """

    def __init__(self, id_, health, class_):
        self.id = id_
        self.health = health
        self.is_dead = False
        self.model = None
        self.class_ = class_

    def get_damage(self, damage):
        """Getting damage.

        Start dying if needed.

        Args:
            damage (int): Damage points to get.
        """
        self.health -= damage
        if self.health <= 0:
            self._die()

    def _init_col_node(self, from_mask, into_mask, solid):
        """Initialize this unit collision node.

        Args:
            from_mask (panda3d.core.BitMask_uint32_t_32):
                FROM collision mask.
            into_mask (panda3d.core.BitMask_uint32_t_32):
                INTO collision mask.
            solid (panda3d.core.CollisionSolid):
                Collision solid for this unit.
        """
        col_node = CollisionNode(self.id)
        col_node.setFromCollideMask(from_mask)
        col_node.setIntoCollideMask(into_mask)
        col_node.addSolid(solid)
        return self.model.attachNewNode(col_node)

    def _die(self):
        """Actions on this unit death.

        Returns:
            bool: True, if enemy dies in the first time.
        """
        if self.is_dead:
            return False

        self.is_dead = True
        self._col_node.removeNode()

        base.taskMgr.doMethodLater(  # noqa: F821
            self.clear_delay, self.clear, self.id + "_clear"
        )
        return True

    @abc.abstractproperty
    def tooltip(self):
        """This unit tooltip.

        Returns:
            str: This unit tooltip.
        """
        raise NotImplementedError("Every unit must have a tooltip property.")

    @abc.abstractproperty
    def clear_delay(self):
        """Time to keep this character in the Game after his death.

        Returns:
            float: Seconds of the delay before deleting this character.
        """
        raise NotImplementedError("Every unit must have a clear_delay property.")

    @abc.abstractmethod
    def clear(self):
        """Deleting this unit from the Game method."""
        raise NotImplementedError("Every unit class must have clear() method.")
