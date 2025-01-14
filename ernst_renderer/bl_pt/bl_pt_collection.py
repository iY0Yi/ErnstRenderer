from bpy.types import Panel

from ..bl_ot.bl_ot_export_shader import *
from ..bl_ot.shadergen import shadergen_data as sgd

class CollectionButtonsPanel:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "collection"

    @classmethod
    def poll(cls, context):
        return (context.collection != context.scene.collection) and (context.engine in cls.COMPAT_ENGINES)

class ERNST_PT_ERNST_Collection_Instanccing(CollectionButtonsPanel, Panel):
    bl_label = 'Instancing'
    COMPAT_ENGINES = {'ERNST'}
    def draw(self, context):
        collection = context.collection.ernst
        collection.draw_gui(context, self.layout)
