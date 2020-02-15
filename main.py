"""Main game file. Starts the game itself."""
from direct.directutil import Mopath
from direct.interval.MopathInterval import MopathInterval
from direct.showbase.ShowBase import ShowBase


class ForwardOnly(ShowBase):
    """Object, which represents the game itself."""

    def __init__(self):
        ShowBase.__init__(self)

        # load motion path
        dir_path = self.loader.loadModel("models/bam/direct_path.bam")
        dir_path.reparentTo(self.render)
        dir_path.setPos(0)

        # load dummy model
        box = self.loader.loadModel("models/bam/box.bam")
        box.reparentTo(self.render)
        box.setPos(0)

        # create motion path object and interval of moving box along it
        path_name = Mopath.Mopath()
        path_name.loadNodePath(dir_path)
        path_int = MopathInterval(path_name, box, duration=2, name="Name")

        path_int.start()

        self.cam.setPos(0, 25, 0)
        self.cam.lookAt(box)


fo_app = ForwardOnly()
fo_app.run()
