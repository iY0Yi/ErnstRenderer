import bpy
from bpy.types import Menu

from ..bl_ot.bl_ot_boolean import *
from ..bl_ot.shadergen import shadergen_data as sgd
from ..util.util import *

class ERNST_MT_BoolCodeName(Menu):
    bl_idname = 'ERNST_MT_Objects'
    bl_label = 'List scene objects'

    def draw(self, context):
        layout = self.layout
        for o in bpy.data.objects:
            layout.prop(o.name)
