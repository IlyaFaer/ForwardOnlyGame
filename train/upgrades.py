"""
Copyright (C) 2021 Ilya "Faer" Gurov (ilya.faer@mail.ru)
License: https://github.com/IlyaFaer/ForwardOnlyGame/blob/master/LICENSE.md

The locomotive upgrades API.

Upgrades can be active and passive. Passive upgrades give some permanent
effects. Acitve uprades (weapons mostly) are manually controlled by
player, otherwise doesn't give any effects.
"""
import random

from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import (
    Func,
    LerpHprInterval,
    LerpPosInterval,
    LerpScaleInterval,
    Parallel,
    Sequence,
    SoundInterval,
)
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import (
    CollisionNode,
    CollisionPolygon,
    CollisionSphere,
    Point3,
    TransparencyAttrib,
)

from const import MOUSE_MASK, NO_MASK, SHOT_RANGE_MASK
from utils import address

UPGRADES_DESC = {
    "Ram": {
        "name": "Ram",
        "desc": """With this ram your locomotive
will be breaking road barriers
without getting damage""",
        "cost": "120$",
        "model": "ram1",
        "threshold": 1,
    },
    "Floodlights": {
        "name": "Floodlights",
        "desc": """All the negative darkness
factors are no more actual
with these floodlights on""",
        "cost": "190$",
        "model": "floodlights1",
        "threshold": 2,
    },
    "Armor Plate": {
        "name": "Armor Plate",
        "desc": """An active shield which can
cover one of the Train sides.
Press 4, 5, 6 keys to move it.""",
        "cost": "70$",
        "model": "armor_plate",
        "threshold": 1,
    },
    "Fire Extinguishers": {
        "name": "Fire Extinguishers",
        "desc": """Gradually restores locomotive
durability up to 400 points
in case of a big damage""",
        "cost": "190$",
        "model": "fire_extinguishers",
        "threshold": 2,
    },
    "Grenade Launcher": {
        "name": "Grenade Launcher",
        "desc": """Active gun, which can do a
lot of damage on a small area.
Press 1 key to aim and shoot.""",
        "cost": "180$",
        "model": "grenade_launcher",
        "threshold": 1,
    },
    "Sleeper": {
        "name": "Sleeper",
        "desc": """Add one more character cell
into the locomotive rest zone""",
        "cost": "140$",
        "model": "sleeper1",
        "threshold": 1,
    },
    "Window Frames": {
        "name": "Window Frames",
        "desc": """With this window frames
characters in the rest zone are
protected from the Stench""",
        "cost": "150$",
        "model": "isolation",
        "threshold": 2,
    },
    "Cluster Howitzer": {
        "name": "Cluster Howitzer",
        "desc": """Shots a cluster rocket, which
splits to four grenades, doing
damage on several circles.
Press 3 to aim and shoot.""",
        "cost": "200$",
        "model": "cluster_bomb_launcher",
        "threshold": 2,
    },
    "Machine Gun": {
        "name": "Machine Gun",
        "desc": """Fires aiming burst. Better be
used for a single target.
Press 2 to aim and shoot.""",
        "cost": "160$",
        "model": "machine_gun",
        "threshold": 2,
    },
}


class ArmorPlate:
    """An active shield locomotive upgrade.

    Represents an active defense upgrade - plate, which can
    cover one of the locomotive sides: left, right, top.

    Args:
        loc_model (panda3d.core.NodePath):
            The locomotive model - parent for the plate.
    """

    def __init__(self, loc_model):
        self._is_on_move = False
        self.cur_position = "top"

        self._snd = base.sound_mgr.loadSfx(  # noqa: F821
            "sounds/train/armor_plate_move.ogg"
        )
        base.sound_mgr.attachSoundToObject(self._snd, loc_model)  # noqa: F821

        self._model = Actor(address("armor_plate"))
        self._model.reparentTo(loc_model)

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
                Side of the locomotive, which is now covered by the plate.
        """
        self.cur_position = side

    def _stop_move(self, task):
        """Release the plate moving block."""
        self._is_on_move = False
        return task.done

    def _turn_left(self):
        """Cover the left side of the locomotive with the plate."""
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
        """Cover the right side of the locomotive with the plate."""
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
    """Grenade launcher locomotive upgrade.

    Represents an active weapon, which can
    do a lot of damage on some radius.

    Args:
        loc_model (panda3d.core.NodePath): The locomotive model.
    """

    def __init__(self, loc_model):
        self.is_up = False
        # flag, which indicates if the launcher
        # is in (un-)loading process
        self._is_loading = False
        self._range_col_np = None

        self._loc_model = loc_model

        self._model = Actor(address("grenade_launcher"))
        self._model.reparentTo(loc_model)

        self._sight = loader.loadModel(address("grenade_sight"))  # noqa: F821
        self._sight.reparentTo(loc_model)
        self._sight.hide()

        self._grenade_explosion = ParticleEffect()
        self._grenade_explosion.loadConfig("effects/grenade_explode.ptf")

        self._grenade_smoke = ParticleEffect()
        self._grenade_smoke.loadConfig("effects/bomb_smoke1.ptf")

        self._hole_sprite = loader.loadModel(address("ground_hole"))  # noqa: F821
        self._hole_sprite.reparentTo(loc_model)
        self._hole_sprite.setTransparency(TransparencyAttrib.MAlpha)
        self._hole_sprite.hide()

        base.accept("1", self.change_state)  # noqa: F821

        self._shot_snd = loader.loadSfx(  # noqa: F821
            "sounds/combat/grenade_launcher_shot.ogg"
        )
        self._explosion_snd = loader.loadSfx(  # noqa: F821
            "sounds/combat/bomb_explosion1.ogg"
        )
        self._explosion_snd.setVolume(0.15)

        self._load_snd = loader.loadSfx(  # noqa: F821
            "sounds/combat/grenade_launcher_load.ogg"
        )

    def _change_mode(self, task):
        """Change controls mode - common or grenade launcher shooting."""
        if self.is_up:
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

        self.is_up = not self.is_up
        self._is_loading = False
        return task.done

    def change_state(self):
        """Change the launcher state."""
        if not base.world.is_on_et or self._is_loading:  # noqa: F821
            return

        base.train.disable_enabled_weapon(self)  # noqa: F821

        self._is_loading = True
        self._model.setPlayRate(-4 if self.is_up else 4, "gun_up")
        self._model.play("gun_up")

        if not self.is_up:
            self._load_snd.play()

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

        self._hole_sprite.setPos(grenade_pos)
        self._hole_sprite.wrtReparentTo(
            base.world.current_block.rails_mod  # noqa: F821
        )
        self._hole_sprite.show()

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
        taskMgr.doMethodLater(  # noqa: F821
            4, self._return_hole_sprite, "hide_ground_hole",
        )

    def _return_hole_sprite(self, task):
        """Return the hole sprite to the grenade launcher model."""
        self._hole_sprite.hide()
        self._hole_sprite.reparentTo(self._loc_model)
        return task.done

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


class ClusterHowitzer:
    """Cluster bombs launcher locomotive upgrade.

    Args:
        loc_model (panda3d.core.NodePath): The locomotive model.
    """

    def __init__(self, loc_model):
        self._is_loading = False
        self.is_up = False

        self._coors = [None, None, None, None]
        self._sights = []
        self._explosions = []
        self._ground_holes = []
        self._smokes = []
        self._bombs = []
        self._explosion_snds = []

        self._train_mod = loc_model
        self._model = Actor(address("cluster_bomb_launcher"))
        self._model.reparentTo(loc_model)

        for _ in range(4):
            sight = loader.loadModel(address("grenade_sight"))  # noqa: F82
            sight.reparentTo(loc_model)
            sight.hide()
            self._sights.append(sight)

            explosion = ParticleEffect()
            explosion.loadConfig("effects/grenade_explode.ptf")
            self._explosions.append(explosion)

            smoke = ParticleEffect()
            smoke.loadConfig("effects/bomb_smoke1.ptf")
            self._smokes.append(smoke)

            snd = loader.loadSfx("sounds/combat/bomb_explosion1.ogg")  # noqa: F821
            snd.setVolume(random.uniform(0.1, 0.15))
            snd.setPlayRate(random.uniform(0.8, 1))
            self._explosion_snds.append(snd)

            hole = loader.loadModel(address("ground_hole"))  # noqa: F821
            hole.reparentTo(loc_model)
            hole.setTransparency(TransparencyAttrib.MAlpha)
            hole.hide()
            self._ground_holes.append(hole)

        self._load_snd = loader.loadSfx("sounds/combat/howitzer_load.ogg")  # noqa: F821
        self._load_snd.setPlayRate(0.8)

        base.accept("3", self.change_state)  # noqa: F82

    def _change_mode(self, task):
        """Change the launcher mode: aiming or idle."""
        if self.is_up:
            self._end_aiming()
        else:
            taskMgr.doMethodLater(0.05, self._show_sights, "show_sights")  # noqa: F82
            base.common_ctrl.deselect()  # noqa: F82
            base.accept("mouse1", self._shot)  # noqa: F821

        self.is_up = not self.is_up
        self._is_loading = False
        return task.done

    def _show_sights(self, task):
        """Show four aiming sights."""
        self._move_sights()
        for sight in self._sights:
            sight.show()

        taskMgr.doMethodLater(1, self._move_sights, "move_cluster_sights")  # noqa: F82
        return task.done

    def _end_aiming(self):
        """End aiming mode, hide sights."""
        for sight in self._sights:
            sight.hide()

        taskMgr.remove("move_cluster_sights")  # noqa: F82
        base.common_ctrl.set_mouse_events()  # noqa: F82

    def _shot(self):
        """Make a cluster howitzer shot."""
        self.change_state()
        base.ignore("3")  # noqa: F82

        rocket = loader.loadModel(address("cluster_rocket"))  # noqa: F82
        rocket.reparentTo(self._model)
        rocket.setPos(0, -0.325, 0.3)
        rocket.setP(20)

        smoke = ParticleEffect()
        smoke.loadConfig("effects/smoke_tail.ptf")
        smoke.start(rocket, render)  # noqa: F821

        hiss_snd = base.sound_mgr.loadSfx("sounds/rocket_fly.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(hiss_snd, rocket)  # noqa: F821
        hiss_snd.play()

        open_snd = base.sound_mgr.loadSfx("sounds/cluster_open.ogg")  # noqa: F821
        base.sound_mgr.attachSoundToObject(open_snd, rocket)  # noqa: F821

        Sequence(
            Parallel(
                LerpPosInterval(rocket, 2, (0, 1.8, 3)),
                LerpHprInterval(rocket, 2, (0, 80, 0)),
            ),
            SoundInterval(open_snd),
            Func(self._clear_rocket, rocket, smoke, hiss_snd),
            Func(self._bombs_down),
        ).start()

        taskMgr.doMethodLater(  # noqa: F82
            60,
            base.accept,  # noqa: F82
            "unblock_cluster_launcher",
            extraArgs=["3", self.change_state],
        )
        base.train.make_shot("Cluster Howitzer")  # noqa: F82

    def _bombs_down(self):
        """Move bombs down to the ground and do explosion."""
        move_par = Parallel()
        for num in range(4):
            bomb = loader.loadModel(address("hand_bomb1"))  # noqa: F82
            bomb.reparentTo(self._train_mod)
            bomb.setPos(*self._coors[num], 2)
            bomb.setScale(2)

            self._bombs.append(bomb)
            move_par.append(
                LerpPosInterval(
                    bomb, random.uniform(0.5, 0.65), (*self._coors[num], 0)
                ),
            )

        Sequence(
            move_par, Func(self._clear_grenades), Func(self._explode_grenades),
        ).start()

    def _clear_grenades(self):
        """Delete bomb models."""
        for bomb in self._bombs:
            bomb.removeNode()

        self._bombs.clear()

    def _do_grenade_damage(self, event):
        """Event which is called by a grenade explosion.

        The method do damage to the enemy units, which
        were in the grenade explosion area.
        """
        base.world.enemy.active_units[  # noqa: F821
            event.getFromNodePath().getName()
        ].get_damage(50)

    def _explode_grenades(self):
        """Organize grenades explosion effects and damaging."""
        col_nps = []
        for num, coor in enumerate(self._coors):
            col_node = CollisionNode("grenade_explosion{}".format(num))
            col_node.setFromCollideMask(NO_MASK)
            col_node.setIntoCollideMask(SHOT_RANGE_MASK)
            col_node.addSolid(CollisionSphere(0, 0, 0, 0.096))

            col_np = self._model.attachNewNode(col_node)
            col_np.setPos(*coor, 0.1)
            col_nps.append(col_np)

            base.accept(  # noqa: F821
                "into-grenade_explosion{}".format(num), self._do_grenade_damage
            )
            self._explosions[num].setPos(*coor, 0.1)
            self._explosions[num].start(self._model, render)  # noqa: F82
            self._explosions[num].softStart()

            self._smokes[num].setPos(*coor, 0.1)
            self._smokes[num].start(self._model, render)  # noqa: F82
            self._smokes[num].softStart()

            taskMgr.doMethodLater(  # noqa: F82
                random.uniform(0, 0.5),
                self._explosion_snds[num].play,
                "play_explosion_snd",
                extraArgs=[],
            )

            self._ground_holes[num].setPos(*coor, 0.05)
            self._ground_holes[num].wrtReparentTo(
                base.world.current_block.rails_mod  # noqa: F82
            )
            self._ground_holes[num].show()

        taskMgr.doMethodLater(  # noqa: F821
            1, self._grenade_explosions_stop, "stop_grenade_explosions"
        )
        taskMgr.doMethodLater(  # noqa: F821
            2.5, self._grenade_smokes_stop, "stop_grenade_smokes"
        )
        taskMgr.doMethodLater(  # noqa: F821
            0.1, self._clear_grenade_solids, "clear_grenade_solid", extraArgs=[col_nps]
        )
        taskMgr.doMethodLater(  # noqa: F821
            4, self._return_hole_sprites, "hide_ground_hole",
        )

    def _return_hole_sprites(self, task):
        """Return groun hole sprites to the howitzer model."""
        for hole in self._ground_holes:
            hole.hide()
            hole.reparentTo(self._train_mod)

        return task.done

    def _grenade_explosions_stop(self, task):
        """Stop grenade explosion effects."""
        for explosion in self._explosions:
            explosion.softStop()

        return task.done

    def _grenade_smokes_stop(self, task):
        """Stop explosion smoke effects."""
        for smoke in self._smokes:
            smoke.softStop()

        return task.done

    def _clear_grenade_solids(self, col_nps):
        """Delete explosion solids, which are dealing the damage to enemies.

        Args:
            col_nps (list): List of collision solids.
        """
        for col_np in col_nps:
            col_np.removeNode()

    def _clear_rocket(self, rocket, smoke, hiss_snd):
        """Clear the cluster rocket model and its effects.

        Args:
            rocket (panda3d.core.NodePath): The rocket model.
            smoke (direct.particles.ParticleEffect.ParticleEffect):
                The rocket smoke tail effect.
            hiss_snd (panda3d.core.AudioSound):
                The rocket hiss sound.
        """
        hiss_snd.stop()
        base.sound_mgr.detach_sound(hiss_snd)  # noqa: F82
        smoke.disable()
        rocket.removeNode()

    def _move_sights(self, task=None):
        """Randomly periodically move aiming sights within shoot-range."""
        for ind, sight in enumerate(self._sights):
            x = random.uniform(*random.choice(((-1.1, -0.15), (1.1, 0.15))))
            y = random.uniform(-0.11, 0.5)

            self._coors[ind] = (x, y)
            sight.setPos(x, y, 0.01)

        if task:
            return task.again

    def change_state(self):
        """Change the launcher mode."""
        if not base.world.is_on_et or self._is_loading:  # noqa: F82
            return

        base.train.disable_enabled_weapon(self)  # noqa: F821

        self._is_loading = True
        self._model.setPlayRate(-4 if self.is_up else 4, "gun_up")
        self._model.play("gun_up")

        if not self.is_up:
            self._load_snd.play()

        taskMgr.doMethodLater(  # noqa: F82
            0.2, self._change_mode, "cluster_bomb_launcher_aim"
        )


class MachineGun:
    """Machine gun locomotive upgrade, active weapon.

    Does a lot of damage on a narrow range, so
    usually harms only one enemy target.

    Args:
        loc_model (panda3d.core.NodePath): The locomotive model.
    """

    def __init__(self, loc_model):
        self.is_up = False
        # flag, which indicates if the launcher
        # is in (un-)loading process
        self._is_loading = False
        self._col_np = None

        self._model = loader.loadModel(address("machine_gun"))  # noqa: F821
        self._model.reparentTo(loc_model)
        self._model.setPos(-0.02, -0.27, 0.31)

        self._sight = loader.loadModel(address("machine_gun_sight"))  # noqa: F821
        self._sight.reparentTo(loc_model)
        self._sight.hide()

        self._shot_snd = base.sound_mgr.loadSfx(  # noqa: F82
            "sounds/combat/loc_machine_gun.ogg"
        )
        base.sound_mgr.attachSoundToObject(self._shot_snd, self._model)  # noqa: F82
        self._load_snd = loader.loadSfx(  # noqa: F82
            "sounds/combat/machine_gun_load.ogg"
        )

        fire = loader.loadModel(address("gun_fire2"))  # noqa: F821
        fire.reparentTo(self._model)
        fire.setScale(1, 0.0001, 1)
        fire.setPos(0, 0.095, 0.029)
        fire.setH(90)

        self._shoot_seq = Sequence(
            LerpScaleInterval(fire, 0.16, (1.3, 1, 1.3)),
            LerpScaleInterval(fire, 0.085, (1, 0.0001, 1)),
        )
        base.accept("2", self.change_state)  # noqa: F82

    def _aim_machine_gun(self, task):
        """Aim machine gun to the place pointed by the sight."""
        self._model.headsUp(self._sight)
        return task.again

    def _change_mode(self, task):
        """Change controls mode - aiming and shooting or passive."""
        if self.is_up:
            self._sight.hide()
            self._end_aiming()
        else:
            taskMgr.doMethodLater(  # noqa: F821
                0.05, self._sight.show, "show_sight", extraArgs=[]
            )
            base.common_ctrl.deselect()  # noqa: F821
            self._start_aiming()

        self.is_up = not self.is_up
        self._is_loading = False
        return task.done

    def _do_damage(self, event):
        """Do the machine gun damage."""
        base.world.enemy.active_units[  # noqa: F821
            event.getFromNodePath().getName()
        ].get_damage(7)

    def _end_aiming(self):
        """Stop aiming and disable aiming GUI."""
        base.ignore("mouse1-up")  # noqa: F82
        taskMgr.remove("aim_machine_gun")  # noqa: F82

        self._range_col_np.removeNode()
        base.common_ctrl.set_mouse_events()  # noqa: F82

        LerpHprInterval(self._model, 0.5, (0, 0, 0)).start()

    def _make_shot(self, task):
        """Make a single machine gun shot."""
        pos = self._sight.getPos()
        Parallel(
            Sequence(
                LerpPosInterval(
                    self._sight,
                    0.125,
                    (
                        pos.getX() + random.uniform(-0.05, 0.05),
                        pos.getY() + random.uniform(-0.05, 0.05),
                        0,
                    ),
                ),
                LerpPosInterval(self._sight, 0.125, pos, blendType="easeOut"),
            ),
            self._shoot_seq,
        ).start()
        return task.again

    def _move_sight(self, event):
        """Move the machine gun sight sprite.

        The machine gun sight can be moved only
        within the locomotive parts shooting range.
        """
        if event.getIntoNodePath().getName() != "machine_gun_range":
            return

        point = event.getSurfacePoint(base.train.model)  # noqa: F821
        self._sight.setPos(point.getX(), point.getY(), 0.01)

    def _start_aiming(self):
        """Show aiming GUI and tweak shooting events."""
        col_node = CollisionNode("machine_gun_range")
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

        base.accept("mouse1", self._start_shooting)  # noqa: F821
        base.accept("mouse1-up", self._stop_shooting)  # noqa: F821
        base.accept("mouse_ray-into", self._move_sight)  # noqa: F821
        base.accept("mouse_ray-again", self._move_sight)  # noqa: F82

        taskMgr.doMethodLater(  # noqa: F82
            0.05, self._aim_machine_gun, "aim_machine_gun"
        )

    def _start_shooting(self):
        """Start the machine gun shooting sequence."""
        self._shot_snd.play()
        taskMgr.doMethodLater(0.25, self._make_shot, "machine_gun_shoot")  # noqa: F82
        taskMgr.doMethodLater(  # noqa: F82
            4, self._stop_shooting, "stop_machine_gun_shooting"
        )

        col_node = CollisionNode("machine_gun_bullet")
        col_node.setFromCollideMask(NO_MASK)
        col_node.setIntoCollideMask(SHOT_RANGE_MASK)
        col_node.addSolid(CollisionSphere(0, 0, 0, 0.005))
        self._col_np = self._sight.attachNewNode(col_node)

        base.accept("into-machine_gun_bullet", self._do_damage)  # noqa: F82

    def _stop_shooting(self, task=None):
        """Stop machine gun shooting and start reloading."""
        taskMgr.remove("stop_machine_gun_shooting")  # noqa: F82
        taskMgr.remove("machine_gun_shoot")  # noqa: F82

        self._col_np.removeNode()
        self._col_np = None

        base.train.make_shot("Machine Gun")  # noqa: F82
        taskMgr.doMethodLater(  # noqa: F82
            0.05, self._change_mode, "change_machine_gun_mode"
        )

        base.ignore("2")  # noqa: F82
        taskMgr.doMethodLater(  # noqa: F82
            30,
            base.accept,  # noqa: F82
            "unblock_machine_gun",
            extraArgs=["2", self.change_state],
        )
        taskMgr.doMethodLater(  # noqa: F82
            2, self._shot_snd.setTime, "change_shooting_snd_time", extraArgs=[0]
        )

        if task is not None:
            return task.done
        else:
            self._shot_snd.setTime(4)

    def change_state(self):
        """Change the machine gun state: aiming and shooting or passive."""
        if not base.world.is_on_et or self._is_loading:  # noqa: F821
            return

        base.train.disable_enabled_weapon(self)  # noqa: F821

        self._is_loading = True
        if not self.is_up:
            self._load_snd.play()

        taskMgr.doMethodLater(0.2, self._change_mode, "machine_gun_aim")  # noqa: F821
