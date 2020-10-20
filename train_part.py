"""
Copyright (C) 2020 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Train parts API.
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
            Dicts describing possible positions and
            rotations on this part.
        arrow_pos (dict): Arrow position and angle.
    """

    def __init__(self, parent, name, positions, arrow_pos):
        self.parent = parent
        self.name = name
        self.chars = []
        # enemies within shooting range of this part
        self.enemies = []
        self._cells = positions

        # organize a manipulating arrow
        self._arrow = loader.loadModel(address("train_part_arrow"))  # noqa: F821
        self._arrow.setPos(*arrow_pos["pos"])
        self._arrow.setH(arrow_pos["angle"])
        self._arrow.clearLight()

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
        self._arrow.attachNewNode(col_node)

        # shooting zone for this TrainPart
        col_node = CollisionNode("shoot_zone_" + name)
        col_node.setFromCollideMask(NO_MASK)
        col_node.setIntoCollideMask(SHOT_RANGE_MASK)
        col_node.addSolid(CollisionBox(Point3(-0.4, -0.06, 0), Point3(0.4, 0.8, 0.08)))
        col_np = self.parent.attachNewNode(col_node)
        col_np.setPos(arrow_pos["pos"][0], arrow_pos["pos"][1], 0)
        col_np.setH(arrow_pos["angle"])

        base.accept("into-shoot_zone_" + name, self.enemy_came)  # noqa: F821
        base.accept("out-shoot_zone_" + name, self.enemy_leave)  # noqa: F821

    @property
    def free_cells(self):
        """The number of free cells on this part.

        Returns:
            int: The number of free cells
        """
        return len(self._cells)

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

    def hide_arrow(self):
        """Hide manipulating arrow of this TrainPart."""
        self._arrow.detachNode()


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
        return 2 - len(self.chars)

    def give_cell(self, character):
        """Check if there is a free cell.

        Args:
            character (personage.character.Character):
                Character to move to this part.

        Returns:
            dict: Dict with position to move character to.
        """
        if len(self.chars) >= 2:
            return None

        self.chars.append(character)
        return {"pos": (0, 0, 0), "angle": 0}

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

    def hide_arrow(self):
        """Rest parts doesn't have manipulating arrows."""
        pass
