"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

Game configurations API.
"""
import os.path


class Config:
    """Includes and orchestrates all the game configurations."""

    opts_file = "options.cfg"

    def __init__(self):
        if not os.path.exists(self.opts_file):
            self._create_default()

        with open(self.opts_file, "r") as opts_file:
            self.resolution, lang, tutorial_on, fps = opts_file.readlines()

        self.resolution = self.resolution.strip()
        self.tutorial_enabled = tutorial_on.strip() == "True"
        self.language = lang.strip()
        self.fps_limit = int(fps)

    def _create_default(self):
        """Create default game configurations file.

        Defaults:
            Screen resolution: player's monitor size.
            Language: English
            Turorial: enabled
        """
        with open(self.opts_file, "w") as opts_file:
            opts_file.write(
                str(base.pipe.getDisplayWidth())  # noqa: F82
                + "x"
                + str(base.pipe.getDisplayHeight())  # noqa: F82
                + "\nEN\nTrue\n60"
            )

    def update(self, resolution, lang, tutorial, fps_limit):
        """Update the game configurations with new values.

        Args:
            resolution (str): New screen resolution.
            lang (str): New language code.
            tutorial (str): New value for Tutorial Enabled option.
            fps_limit (int): Framerate limit.
        """
        with open(self.opts_file, "w") as opts_file:
            opts_file.write(
                resolution + "\n" + lang + "\n" + tutorial + "\n" + fps_limit
            )
