"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Base API for all the Game units, both characters and enemies.
"""
import abc
from panda3d.core import CollisionNode


class Unit(metaclass=abc.ABCMeta):
    """Base game unit class.

    Args:
        id_ (str): This unit id.
        class_ (str): This unit class.
        class_data (dict):
            This unit class definition, including
            max health points.
    """

    def __init__(self, id_, class_, class_data):
        self.id = id_
        self.class_data = class_data
        self.class_ = class_
        self.is_dead = False
        self.model = None

        self._health = class_data["health"]

    @property
    def health(self):
        """This unit health.

        Returns:
            int: This unit health points.
        """
        return self._health

    @health.setter
    def health(self, value):
        """Health setter.

        Limits health points to [0: class_max_health]

        Args:
            value (int): New health value.
        """
        self._health = min(max(value, 0), self.class_data["health"])

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

    def _stop_tasks(self, *names):
        """Stop this unit related tasks.

        Args:
            names (tuple): Tasks names to stop.
        """
        for name in names:
            base.taskMgr.remove(self.id + name)  # noqa: F821

    def get_damage(self, damage):
        """Getting damage.

        Start dying if needed.

        Args:
            damage (int): Damage points to get.
        """
        self.health -= damage
        if self.health <= 0:
            self._die()

    @abc.abstractmethod
    def clear(self):
        """Deleting this unit from the Game method."""
        raise NotImplementedError("Every unit class must have clear() method.")

    @abc.abstractproperty
    def clear_delay(self):
        """Time to keep this character in the Game after his death.

        Returns:
            float: Seconds of the delay before deleting this character.
        """
        raise NotImplementedError("Every unit must have a clear_delay property.")

    @abc.abstractproperty
    def tooltip(self):
        """This unit tooltip.

        Returns:
            str: This unit tooltip.
        """
        raise NotImplementedError("Every unit must have a tooltip property.")
