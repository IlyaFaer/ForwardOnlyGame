"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Railways path generator.
"""
import random
from utils import chance


class Bound:
    """Represents a bound value for a sin-like function.

    When path generator made a step, which crosses this
    bound, turn should be made to realize arc.

    Args:
        value (int): Bound value.
        s_range (tuple): Bounds for step value generation.
        model (str): Name of the model related to this bound.
    """

    def __init__(self, value, s_range, model):
        self._s_range = s_range
        self._model = model
        self.value = value

    def _change_direction(self, prev_value):
        """Mirror turn direction.

        Bound can be crossed from two sides. In one of
        these cases we should mirror turn.
        """
        if self._model == "direct":
            return "l90_turn" if prev_value < 0 else "r90_turn"

        direction = "r" if self._model[0] == "l" else "l"

        return direction + self._model[1:]

    def is_crossed(self, prev, current):
        """Check if this bound crossed.

        Args:
            prev (float): Previous func value.
            current (float): Current func value.

        Returns:
            bool: True if bound crossed, False otherwise.
        """
        return (prev <= self.value <= current) or (prev >= self.value >= current)

    def make_turn(self, prev_bound):
        """Calculate railway turn and new generator step.

        Args:
            prev_bound (Bound): Previous crossed bound object.

        Returns:
            (float, str): New step value, turn model name.
        """
        step = random.uniform(*self._s_range)
        if self.value == 0:
            step *= random.choice((1, -1))

        prev_value = prev_bound.value if prev_bound else 0

        if abs(prev_value) > abs(self.value):
            model = self._change_direction(prev_value)
            return -1 * step, model

        return step, self._model


class RailwayGenerator:
    """Generates a path, using function similar to sin.

    Sin-like function is used to make path elongated -
    it'll have main direction and a lot of arcs. Length of
    arcs and straight paths is generated with random portion.
    """

    def __init__(self):
        self._prev_bound = None
        self._prev = 0
        self._step = random.uniform(0.025, 0.05) * random.choice((1, -1))
        self._current = self._step
        self._station_threshold = 90
        self._city_threshold = 400

        self._bounds = (
            Bound(-1, (0.08, 0.12), "r90_turn"),
            Bound(-0.5, (-0.08, -0.12), "l90_turn"),
            Bound(0, (0.025, 0.05), "direct"),
            Bound(0.5, (0.08, 0.12), "r90_turn"),
            Bound(1, (-0.08, -0.12), "l90_turn"),
        )

    @property
    def current(self):
        """Current function value."""
        return self._current

    @current.setter
    def current(self, value):
        """While setting current function value set previous as well.

        Args:
            value (float): New current function value.
        """
        self._prev = self._current
        self._current = value

    def _choose_block(self):
        """Choose the next block for the path.

        If any bound has been crosed, make a turn. Return
        straight block otherwise.

        Returns:
            str: Chosen block name.
        """
        for bound in self._bounds:
            if self._prev_bound != bound:
                if bound.is_crossed(self._prev, self.current):
                    self._step, model = bound.make_turn(self._prev_bound)
                    self._prev_bound = bound
                    return model

        if self._station_threshold <= 0 and chance(30):
            self._station_threshold = 90
            return "station"

        if self._city_threshold <= 0 and chance(30):
            self._city_threshold = 400
            return "city"

        if chance(10):
            return random.choice(("rs", "ls"))

        return "direct"

    def _choose_branch_block(self):
        """Generate a world block for a branch.

        There are no turns, nor cities on branch railways.
        """
        if self._station_threshold <= 0 and chance(30):
            self._station_threshold = 90
            return "station"

        if chance(10):
            return random.choice(("rs", "ls"))

        return "direct"

    def generate_main_line(self, size):
        """Generate the main railway line according to sin-like function.

        Args:
            size (int): The main line length

        Returns:
            list: List of block names.
        """
        main_line = []
        for _ in range(size):
            main_line.append(self._choose_block())

            self.current += self._step
            self._station_threshold -= 1
            self._city_threshold -= 1

        return main_line

    def intersects_branch(self, br_ends, start):
        """Check if the block can't be used as a branch start.

        Branches should not be mixed chaotically, so they can
        start only at some distance from each others' beginnings.

        Args:
            br_ends (list):
                List of the branches' starts indexes.
            start (int):
                The index of the block, which is
                considered as a branch start.

        Returns:
            bool:
                True, if the given block can't be used as a
                branch start; False otherwise.
        """
        for br_end in br_ends:
            if start in range(br_end - 3, br_end + 4):
                return True

        return False

    def find_straight(self, world_map, branches, ind):
        """Searh for a straight part of the main railway.

        To ensure all the branches are merged back to the main
        railway line, every branch should start and end at the
        horizontal parts of the main railway.

        Args:
            world_map (list): All the world blocks list.
            branches (list): Branches' descriptions.
            ind (int): An assumed index of the branch start/end.

        Returns
            int:
                The given index shifted along the main railway line
                enough to be on the horizontal part of the main railway.
        """
        br_ends = []
        for branch in branches:
            br_ends.append(branch["start"])
            br_ends.append(branch["end"])

        while (
            world_map[ind].z_dir != 0
            or self.intersects_branch(br_ends, ind)
            or world_map[ind].name in ("r90_turn", "l90_turn", "l_fork", "r_fork")
            or world_map[ind].is_city
        ):
            ind += 1

        return ind

    def generate_branches(self, world_map):
        """Generate railway branches.

        Every branch must be merged back to the main railway line
        to ensure players won't ride into a dead end/get into circle.

        Args:
            world_map (list): The main railway line blocks.

        Returns:
            list:
                Branches' short descriptions: start,
                end, side and structure.
        """
        branches = []
        # generate branches' descriptions
        for side in ("l", "r"):
            cursor = 0
            while cursor < len(world_map):
                try:
                    start = self.find_straight(
                        world_map,
                        branches,
                        cursor
                        + random.randint(*random.choice(((150, 250), (300, 350)))),
                    )
                except IndexError:
                    break

                try:
                    end = self.find_straight(
                        world_map, branches, start + random.randint(90, 130)
                    )
                except IndexError:
                    break

                branches.append({"side": side, "start": start, "end": end})
                cursor = end

        # generate branches' structures
        for branch in branches:
            branch_blocks = []

            branch_blocks.append(branch["side"] + "_fork")

            z_shift = random.randint(35, 50)

            # generate the part of the branch from
            # the fork start to the first turn
            for _ in range(z_shift):
                branch_blocks.append(self._choose_branch_block())

            if branch["side"] == "l":
                branch_blocks.append("r90_turn")
            else:
                branch_blocks.append("l90_turn")

            # generate the straight part of the branch
            # parallel to the main railway line
            for num in range(branch["end"] - branch["start"] - 2):
                branch_blocks.append(self._choose_branch_block())

            if branch["side"] == "l":
                branch_blocks.append("r90_turn")
            else:
                branch_blocks.append("l90_turn")

            end_z = world_map[branch["start"] - 1].z_coor + z_shift * (
                -1 if branch["side"] == "r" else 1
            )

            # generate the straight part of the branch
            # from the last turn to the end fork
            for num in range(
                abs(abs(end_z) - abs(world_map[branch["end"] - 1].z_coor))
            ):
                branch_blocks.append(self._choose_branch_block())

            branch_blocks.append(branch["side"] + "_fork")
            branch["blocks"] = branch_blocks

        return branches
