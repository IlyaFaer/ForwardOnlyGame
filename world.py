from panda3d.core import DirectionalLight, AmbientLight


class World:
    """Object which represents the game world."""

    def __init__(self, render):
        self._render = render
        self._set_general_lights()

    def _set_general_lights(self):
        """Set general world lights."""
        ambient = AmbientLight("main_amb_light")
        ambient.setColor((0.5, 0.5, 0.5, 1))
        self._render.setLight(self._render.attachNewNode(ambient))

        directional = DirectionalLight("main_dir_light")
        directional.setColor((0.7, 0.7, 0.7, 1))
        dlnp = self._render.attachNewNode(directional)
        dlnp.setHpr(180, 0, 0)
        self._render.setLight(dlnp)
