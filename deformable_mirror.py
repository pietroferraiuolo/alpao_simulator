from base_deformable_mirror import BaseDeformableMirror

class AlpaoDm(BaseDeformableMirror):

    def __init__(self, nActs):
        super(AlpaoDm, self).__init__(nActs)

    def set_shape(self, command, differential=False):
        pass

    def get_shape(self):
        pass