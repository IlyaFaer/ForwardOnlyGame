"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The Train upgrades API.
"""
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import (
    Parallel,
    Sequence,
    SoundInterval,
)
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import Point3, CollisionNode, CollisionPolygon, CollisionSphere

from const import MOUSE_MASK, NO_MASK, SHOT_RANGE_MASK
from utils import address

UPGRADES_DESC = {
    "Ram": {
        "name": "Ram",
        "desc": """With this ram your locomotive
will be breaking road barriers
without getting damage""",
        "cost": "160$",
        "model": "ram1",
    },
    "Floodlights": {
        "name": "Floodlights",
        "desc": """All the negative darkness
factors are no more actual
with these floodlights on""",
        "cost": "190$",
        "model": "floodlights1",
    },
    "Armor Plate": {
        "name": "Armor Plate",
        "desc": """An active shield which can
cover one of the Train sides.
Press 4, 5, 6 keys to move it.""",
        "cost": "70$",
        "model": "armor_plate",
    },
    "Fire Extinguishers": {
        "name": "Fire Extinguishers",
        "desc": """Gradually restores locomotive
durability up to 400 points
in case of a big damage""",
        "cost": "190$",
        "model": "fire_extinguishers",
    },
    "Grenade Launcher": {
        "name": "Grenade Launcher",
        "desc": """Active gun, which can do a
lot of damage on a small area.
Press 1 key to aim and shoot.""",
        "cost": "180$",
        "model": "grenade_launcher",
    },
    "Sleeper": {
        "name": "Sleeper",
        "desc": """Add one more character cell
into the locomotive rest zone""",
        "cost": "140$",
        "model": "sleeper1",
    },
    "Window Frames": {
        "name": "Window Frames",
        "desc": """With this window frames
characters in the rest zone are
protected from the Stench""",
        "cost": "150$",
        "model": "isolation",
    },
}


class ArmorPlate:
    """An active shield Train upgrade.

    Represents an active defense upgrade - plate, which
    can cover one of Train sides: left, right, top.

    Args:
        train_model (panda3d.core.NodePath):
            The Train model - parent for the plate.
    """

    def __init__(self, train_model):
        self._is_on_move = False
        self.cur_position = "top"

        self._snd = base.sound_mgr.loadSfx(  # noqa: F821
            "sounds/train/armor_plate_move.ogg"
        )
        base.sound_mgr.attachSoundToObject(self._snd, train_model)  # noqa: F821

        self._model = Actor(address("armor_plate"))
        self._model.reparentTo(train_model)

        self._right_to_left = Sequence(
            Parallel(
                self._model.actorInterval("right", playRate=-2.5),
                SoundInterval(self._snd),
            ),
            Parallel(
                self._model.actorInterval("left", playRate=2.5),
                SoundInterval(self._snd),
            ),
        )
        self._left_to_right = Sequence(
            Parallel(
                self._model.actorInterval("left", playRate=-2.5),
                SoundInterval(self._snd),
            ),
            Parallel(
                self._model.actorInterval("right", playRate=2.5),
                SoundInterval(self._snd),
            ),
        )
        base.accept("4", self._turn_left)  # noqa: F821
        base.accept("5", self._turn_top)  # noqa: F821
        base.accept("6", self._turn_right)  # noqa: F821

    def _cover_side(self, side):
        """Actually change the plate position.

        Args:
            side (str):
                Side of the train, which is
                now covered by the plate.
        """
        self.cur_position = side

    def _stop_move(self, task):
        """Release the plate moving block."""
        self._is_on_move = False
        return task.done

    def _turn_left(self):
        """Cover the left side of the Train with the plate."""
        if self.cur_position == "left" or self._is_on_move:
            return

        if self.cur_position == "top":
            self._model.actorInterval("left", playRate=2.5).start()
            delay = 0.9
            cover_delay = 0.45
            self._snd.play()
        else:
            self._right_to_left.start()
            delay = 1.8
            cover_delay = 1.35

        self._is_on_move = True
        taskMgr.doMethodLater(delay, self._stop_move, "stop_move_plate")  # noqa: F821
        taskMgr.doMethodLater(  # noqa: F821
            cover_delay, self._cover_side, "cover_side", extraArgs=["left"]
        )
        taskMgr.doMethodLater(  # noqa: F821
            cover_delay,
            base.train.cover_part,  # noqa: F821
            "cover_part",
            extraArgs=["part_left"],
        )
        taskMgr.doMethodLater(  # noqa: F821
            0.5,
            base.train.uncover_part,  # noqa: F821
            "uncover_part",
            extraArgs=[self.cur_position],
        )

    def _turn_right(self):
        """Cover the right side of the Train with the plate."""
        if self.cur_position == "right" or self._is_on_move:
            return

        if self.cur_position == "top":
            self._model.actorInterval("right", playRate=2.5).start()
            delay = 0.9
            cover_delay = 0.45
            self._snd.play()
        else:
            self._left_to_right.start()
            delay = 1.8
            cover_delay = 1.35

        self._is_on_move = True
        taskMgr.doMethodLater(delay, self._stop_move, "stop_move_plate")  # noqa: F821
        taskMgr.doMethodLater(  # noqa: F821
            cover_delay, self._cover_side, "cover_side", extraArgs=["right"]
        )
        taskMgr.doMethodLater(  # noqa: F821
            cover_delay,
            base.train.cover_part,  # noqa: F821
            "cover_part",
            extraArgs=["part_right"],
        )
        taskMgr.doMethodLater(  # noqa: F821
            0.5,
            base.train.uncover_part,  # noqa: F821
            "uncover_part",
            extraArgs=[self.cur_position],
        )

    def _turn_top(self):
        """Cover the top side of the Train with the plate."""
        if self.cur_position == "top" or self._is_on_move:
            return

        if self.cur_position == "left":
            self._snd.play()
            self._model.actorInterval("left", playRate=-2.5).start()
        elif self.cur_position == "right":
            self._snd.play()
            self._model.actorInterval("right", playRate=-2.5).start()

        self._is_on_move = True
        taskMgr.doMethodLater(0.9, self._stop_move, "stop_move_plate")  # noqa: F821
        taskMgr.doMethodLater(  # noqa: F821
            0.45, self._cover_side, "cover_side", extraArgs=["top"]
        )
        taskMgr.doMethodLater(  # noqa: F821
            0.5,
            base.train.uncover_part,  # noqa: F821
            "uncover_part",
            extraArgs=[self.cur_position],
        )


class GrenadeLauncher:
    """Grenade launcher Train upgrade.

    Represents an active weapon, which can
    do a lot of damage on some radius.

    Args:
        train_model (panda3d.core.NodePath): The Train model.
    """

    def __init__(self, train_model):
        self._is_up = False
        # flag, which indicates if the launcher
        # is in (un-)loading process
        self._is_loading = False

        self._range_col_np = None

        self._model = Actor(address("grenade_launcher"))
        self._model.reparentTo(train_model)

        self._sight = loader.loadModel(address("grenade_sight"))  # noqa: F821
        self._sight.reparentTo(train_model)
        self._sight.hide()

        self._grenade_explosion = ParticleEffect()
        self._grenade_explosion.loadConfig("effects/grenade_explode.ptf")

        self._grenade_smoke = ParticleEffect()
        self._grenade_smoke.loadConfig("effects/bomb_smoke1.ptf")

        base.accept("1", self.change_state)  # noqa: F821

        self._shot_snd = loader.loadSfx(  # noqa: F821
            "sounds/combat/grenade_launcher_shot.ogg"
        )
        self._explosion_snd = loader.loadSfx(  # noqa: F821
            "sounds/combat/bomb_explosion1.ogg"
        )
        self._explosion_snd.setVolume(0.15)

    def _change_mode(self, task):
        """Change controls mode - common or grenade launcher shooting."""
        if self._is_up:
            self._sight.hide()
            self._end_aiming()
        else:
            self._smoke = ParticleEffect()
            self._smoke.loadConfig("effects/grenade_launcher_smoke.ptf")
            self._smoke.setPos(0.026, -0.15, 0.35)

            taskMgr.doMethodLater(  # noqa: F821
                0.05, self._sight.show, "show_sight", extraArgs=[]
            )
            base.common_ctrl.deselect()  # noqa: F821
            self._start_aiming()

        self._is_up = not self._is_up
        self._is_loading = False
        return task.done

    def change_state(self):
        """Change the launcher state."""
        if not base.world.is_on_et or self._is_loading:  # noqa: F821
            return

        self._is_loading = True
        self._model.setPlayRate(-4 if self._is_up else 4, "gun_up")
        self._model.play("gun_up")

        taskMgr.doMethodLater(  # noqa: F821
            0.2, self._change_mode, "grenade_launcher_aim"
        )

    def _do_grenade_damage(self, event):
        """Event which is called by the grenade explosion.

        The method do damage to the enemy units, which
        were in the grenade explosion area.
        """
        base.world.enemy.active_units[  # noqa: F821
            event.getFromNodePath().getName()
        ].get_damage(40)

    def _end_aiming(self):
        """Stop aiming and disable aiming GUI."""
        self._range_col_np.removeNode()
        base.common_ctrl.set_mouse_events()  # noqa: F82

    def _explode_grenade(self, grenade_pos):
        """Explode the grenade, shot from the launcher.

        Args:
            grenade_pos (panda3d.core.Point3):
                The position, where the sight was
                when player made the shot.
        """
        col_node = CollisionNode("grenade_explosion")
        col_node.setFromCollideMask(NO_MASK)
        col_node.setIntoCollideMask(SHOT_RANGE_MASK)
        col_node.addSolid(CollisionSphere(0, 0, 0, 0.096))

        base.accept("into-grenade_explosion", self._do_grenade_damage)  # noqa: F821

        col_np = self._model.attachNewNode(col_node)
        col_np.setPos(grenade_pos)

        self._grenade_explosion.setPos(grenade_pos)
        self._grenade_explosion.start(self._model, render)  # noqa: F821
        self._grenade_explosion.softStart()

        self._grenade_smoke.setPos(grenade_pos)
        self._grenade_smoke.start(self._model, render)  # noqa: F82
        self._grenade_smoke.softStart()

        self._explosion_snd.play()

        taskMgr.doMethodLater(  # noqa: F821
            1, self._grenade_explosion.softStop, "stop_grenade_explosion", extraArgs=[]
        )
        taskMgr.doMethodLater(  # noqa: F821
            2.5, self._grenade_smoke.softStop, "stop_grenade_smoke", extraArgs=[]
        )
        taskMgr.doMethodLater(  # noqa: F821
            0.1, col_np.removeNode, "remove_grenade_solid", extraArgs=[]
        )

    def _move_sight(self, event):
        """Move the launcher sight sprite.

        The launcher sight can be moved only
        within the Train part shooting range.
        """
        if event.getIntoNodePath().getName() != "grenade_launcher_range":
            return

        point = event.getSurfacePoint(base.train.model)  # noqa: F821
        self._sight.setPos(point.getX(), point.getY(), 0.01)

    def _shot(self):
        """Make a shot."""
        self._shot_snd.play()
        self.change_state()
        base.ignore("1")  # noqa: F82

        self._smoke.start(self._model, render)  # noqa: F82
        self._smoke.softStart()

        taskMgr.doMethodLater(  # noqa: F82
            0.5,
            self._explode_grenade,
            "explode_grenade",
            extraArgs=[self._sight.getPos()],
        )
        taskMgr.doMethodLater(  # noqa: F82
            1.45, self._stop_smoke, "stop_launcher_smoke"
        )
        taskMgr.doMethodLater(  # noqa: F82
            20,
            base.accept,  # noqa: F82
            "unblock_launcher",
            extraArgs=["1", self.change_state],
        )
        base.train.make_shot("Grenade Launcher")  # noqa: F82

    def _start_aiming(self):
        """Show aiming GUI and tweak shooting events."""
        col_node = CollisionNode("grenade_launcher_range")
        col_node.setFromCollideMask(NO_MASK)
        col_node.setIntoCollideMask(MOUSE_MASK)

        col_node.addSolid(
            CollisionPolygon(
                Point3(-1.2, -0.3, 0),
                Point3(-1.2, 1.5, 0),
                Point3(1.2, 1.5, 0),
                Point3(1.2, -0.3, 0),
            )
        )
        self._range_col_np = base.train.model.attachNewNode(col_node)  # noqa: F821

        base.accept("mouse1", self._shot)  # noqa: F821
        base.accept("mouse_ray-into", self._move_sight)  # noqa: F821
        base.accept("mouse_ray-again", self._move_sight)  # noqa: F82

    def _stop_smoke(self, task):
        """Stop the launcher shot smoke."""
        self._smoke.disable()
        self._smoke.cleanup()
        return task.done
