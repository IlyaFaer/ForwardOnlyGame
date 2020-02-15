"""Main game file. Starts the game itself."""
from direct.directutil import Mopath
from direct.interval.MopathInterval import MopathInterval
from direct.interval.IntervalGlobal import Sequence, Func
from direct.showbase.ShowBase import ShowBase


class ForwardOnly(ShowBase):
    """Object, which represents the game itself."""

    def __init__(self):
        ShowBase.__init__(self)

        # load dummy model
        box = self.loader.loadModel("models/bam/box.bam")
        box.reparentTo(self.render)
        box.setPos(0)

        # create first motion path object and interval of moving box along it
        path = Mopath.Mopath(objectToLoad="models/bam/direct_path.bam")
        path_int = MopathInterval(path, box, duration=2, name="start_path")

        seq = Sequence(path_int, Func(self._move_along_next, box))
        seq.start()

        self.cam.setPos(0, 0, 50)
        self.cam.lookAt(box)

    def _move_along_next(self, box):
        # create motion path object and interval of moving box along it
        path = Mopath.Mopath(objectToLoad="models/bam/l90_turn_path.bam")
        path.fFaceForward = True

        path_node = self.render.attachNewNode("path_mo")
        path_node.setPos(8, 0, 0)
        path_node.setHpr(-90, 0, 0)

        box.wrtReparentTo(path_node)

        path_int2 = MopathInterval(path, box, duration=2, name="Name2")
        path_int2.start()


ForwardOnly().run()
