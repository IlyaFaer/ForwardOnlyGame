"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The Train parts API.
"""
from panda3d.core import CollisionBox, CollisionNode, CollisionPolygon, Point3
from const import MOUSE_MASK, NO_MASK, SHOT_RANGE_MASK
from utils import address, take_random


class TrainPart:
    """A Train part where characters can be set.

    Contains characters set to this part and enemies
    within its shooting range. Has a manipulating arrow,
    which can be used to move a character to this part.
    Also includes a "shooting range" collider - area,
    on which characters can choose their targets.

    Args:
        parent (panda3d.core.NodePath):
                Model, to which arrow sprite of this part
                must be parented. Characters will be
                parented to this model as well.
        name (str): This unique part name.
        positions (list):
            Dicts describing possible positions on this part.
        angle (int): Character's angle on this part.
        arrow_pos (dict): Arrow position and angle.
    """

    def __init__(self, parent, name, positions, angle, arrow_pos):
        self.parent = parent
        self.name = name
        self.chars = []
        self.is_covered = False
        # enemies within shooting range of this part
        self.enemies = []
        self.angle = angle
        self._cells = positions

        self._arrow = self._prepare_arrow(name, arrow_pos)

        # shooting zone for this TrainPart
        col_node = CollisionNode("shoot_zone_" + name)
        col_node.setFromCollideMask(NO_MASK)
        col_node.setIntoCollideMask(SHOT_RANGE_MASK)
        col_node.addSolid(CollisionBox(Point3(-0.4, -0.06, 0), Point3(0.4, 1, 0.08)))
        col_np = self.parent.attachNewNode(col_node)
        col_np.setPos(arrow_pos[0], arrow_pos[1], 0)
        col_np.setH(angle)

        base.accept("into-shoot_zone_" + name, self.enemy_came)  # noqa: F821
        base.accept("out-shoot_zone_" + name, self.enemy_leave)  # noqa: F821

    @property
    def free_cells(self):
        """The number of free cells on this part.

        Returns:
            int: The number of free cells.
        """
        return len(self._cells)

    def _prepare_arrow(self, name, arrow_pos):
        """Prepare a manipulating arrow for this part.

        Args:
            name (str): Name of the part.
            arrow_pos (dict): Arrows position.

        Returns:
            panda3d.core.NodePath: Arrow node.
        """
        arrow = loader.loadModel(address("train_part_arrow"))  # noqa: F821
        arrow.setPos(*arrow_pos)
        arrow.setH(self.angle)
        arrow.clearLight()

        # set manipulating arrow collisions
        col_node = CollisionNode(name)
        col_node.setFromCollideMask(NO_MASK)
        col_node.setIntoCollideMask(MOUSE_MASK)
        col_node.addSolid(
            CollisionPolygon(
                Point3(-0.06, -0.06, 0),
                Point3(-0.06, 0.06, 0),
                Point3(0.06, 0.06, 0),
                Point3(0.06, -0.06, 0),
            )
        )
        arrow.attachNewNode(col_node)
        return arrow

    def enemy_came(self, event):
        """Enemy unit entered this part shooting range."""
        enemy = base.world.enemy.active_units.get(  # noqa: F821
            event.getFromNodePath().getName()
        )
        if enemy is not None:
            self.enemies.append(enemy)
            enemy.enter_the_part(self)

    def enemy_leave(self, event):
        """Enemy unit leaved this part shooting range."""
        enemy = base.world.enemy.active_units.get(  # noqa: F821
            event.getFromNodePath().getName()
        )
        if enemy is not None:
            self.enemies.remove(enemy)
            enemy.leave_the_part(self)

    def give_cell(self, character):
        """Choose a non taken cell.

        Args:
            character (personage.character.Character):
                Unit to set to this part.

        Returns:
            dict: Position and rotation to set character.
        """
        if not self._cells:
            return

        self.chars.append(character)
        return take_random(self._cells)

    def hide_arrow(self):
        """Hide manipulating arrow of this TrainPart."""
        self._arrow.detachNode()

    def release_cell(self, position, character):
        """Release a cell taken earlier.

        Args:
            position (dict):
                Position and rotation of the taken cell.
            character (personage.character.Character):
                Character to remove from this part.
        """
        self._cells.append(position)
        self.chars.remove(character)

    def show_arrow(self):
        """Show manipulating arrow of this TrainPart."""
        self._arrow.reparentTo(self.parent)


class RestPart:
    """Part of the Train on which characters can rest.

    Rest helps to regain energy and heal wounds.

    Args:
        parent (panda3d.core.NodePath):
            Model, to which characters will be
            reparented while on this part.
        name (str): Part name.
    """

    def __init__(self, parent, name):
        self.chars = []
        self.enemies = []
        self.parent = parent
        self.name = name
        self.angle = 0
        self.cells = 2

        # rest zone collisions
        col_node = CollisionNode(name)
        col_node.setFromCollideMask(NO_MASK)
        col_node.setIntoCollideMask(MOUSE_MASK)
        col_node.addSolid(
            CollisionBox(Point3(-0.09, -0.36, 0.15), Point3(0.09, -0.17, 0.27))
        )
        parent.attachNewNode(col_node)

    @property
    def free_cells(self):
        """The number of free cells on this part.

        Returns:
            int: The number of free cells.
        """
        return self.cells - len(self.chars)

    def give_cell(self, character):
        """Check if there is a free cell.

        Args:
            character (personage.character.Character):
                Character to move to this part.

        Returns:
            dict: Dict with position to move character to.
        """
        if len(self.chars) >= self.cells:
            return None

        self.chars.append(character)
        return (0, 0, 0)

    def hide_arrow(self):
        """Rest parts doesn't have manipulating arrows."""
        pass

    def release_cell(self, position, character):
        """Release one cell on this part.

        Args:
            position (dict):
                Position and rotation of the taken cell.
            character (personage.character.Character):
                Character to remove from this part.
        """
        self.chars.remove(character)

    def show_arrow(self):
        """Rest parts doesn't have manipulating arrows."""
        pass
