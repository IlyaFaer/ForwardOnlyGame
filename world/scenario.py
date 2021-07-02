"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The main game scenario.
"""


class Scenario:
    """The game scenario orchestrator.

    Tracks on which part of the scenario the player is, controls
    the next scenario steps and performs choice consequences effects.
    """

    def __init__(self):
        self.current_chapter = -1

    def start_chapter(self, task):
        """Start a new scenario chapter."""
        self.current_chapter += 1

        base.train.ctrl.set_controls(base.train)  # noqa: F821
        base.camera_ctrl.enable_ctrl_keys()  # noqa: F821

        base.world.outings_mgr.hide_outing()  # noqa: F821
        return task.done
