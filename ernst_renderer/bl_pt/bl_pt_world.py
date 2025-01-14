from bpy.types import Panel

from ..bl_pg.bl_pg_world import *


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class WorldButtonsPanel:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "world"
    # COMPAT_ENGINES must be defined in each subclass, external engines can add themselves here

    @classmethod
    def poll(cls, context):
        return (context.world and context.engine in cls.COMPAT_ENGINES)

class ERNST_PT_WorldProps(WorldButtonsPanel, Panel):
    bl_label = "Ambient"
    bl_order = 1
    # bl_options = {'DEFAULT_CLOSED'}
    COMPAT_ENGINES = {'ERNST'}

    @classmethod
    def poll(cls, context):
        return context.world

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        world = context.world.ernst

        box = layout.box()
        row = box.row()
        row.prop(world, "amb_col")
        row = box.row()
        row.prop(world, "amb_strength")

        box = layout.box()
        row = box.row()
        row.prop(world, "fog_col")
        row = box.row()
        row.prop(world, "fog_start")
        row = box.row()
        row.prop(world, "fog_pow")
