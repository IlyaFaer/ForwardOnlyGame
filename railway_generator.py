"""Railways path generator."""
import random

# set minimal step not less than 0.025
BOUND_PARAMS = (
    (-1, (0.08, 0.12), "r90_turn"),
    (-0.5, (-0.08, -0.12), "l90_turn"),
    (0, (-0.05, 0.05), "direct"),
    (0.5, (0.08, 0.12), "r90_turn"),
    (1, (-0.08, -0.12), "l90_turn"),
)


class Bound:
    """Represents a bound value for a sin-like function.

    When path generator made a step, which crosses this
    bound, turn should be made to realize arcs.

    Args:
        value (int): Bound value.
        s_range (tuple): Bounds to generate step value.
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

        first = "r" if self._model[0] == "l" else "l"

        return first + self._model[1:]

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
        self._prev = None
        self._current = 0
        self._step = random.uniform(-0.05, 0.05)

        self._bounds = [
            Bound(value, s_range, model) for value, s_range, model in BOUND_PARAMS
        ]

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
        """Choose next block for the path.

        Returns:
            str: Current block model name.
        """
        for bound in self._bounds:
            if self._prev_bound != bound:
                if bound.is_crossed(self._prev, self.current):
                    self._step, model = bound.make_turn(self._prev_bound)
                    self._prev_bound = bound
                    return model

        return "direct"

    def generate_path(self, size):
        """Generate sin-like path of the given size.

        Args:
            size (int): Blocks number.

        Returns:
            path (list): Names of motion paths.
        """
        path = []
        self.current = self._step

        for _ in range(size):
            path.append(self._choose_block())
            self.current += self._step

        return path
