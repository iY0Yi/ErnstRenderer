# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Map function to access dict with dot syntax
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Map(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self
