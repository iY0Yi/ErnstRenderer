import math

from bpy.types import Panel

from ..bl_pg.bl_pg_render import *


class RenderOutputButtonsPanel:
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    @classmethod
    def poll(cls, context):
        return (context.engine in cls.COMPAT_ENGINES)

class ERNST_PT_RenderProps(RenderOutputButtonsPanel, Panel):
    bl_label = "Performance"
    bl_order = 1
    COMPAT_ENGINES = {'ERNST'}

    @classmethod
    def poll(cls, context):
        return context.scene

    def draw(self, context):
        layout = self.layout
        layout.use_property_decorate = False
        scene = context.scene
        render_ernst = scene.render_ernst
        col = layout.column(align=True)
        tx = math.floor(scene.render.resolution_x * scene.render.resolution_percentage/100) / render_ernst.tile_grid / render_ernst.file_grid
        ty = math.floor(scene.render.resolution_y * scene.render.resolution_percentage/100) / render_ernst.tile_grid / render_ernst.file_grid
        num = render_ernst.tile_grid*render_ernst.tile_grid*render_ernst.file_grid*render_ernst.file_grid
        col.label(text=f'Render Grid ( {tx} x {ty} px * {num} tiles )')
        row = col.row(align=True)
        row.prop(render_ernst, "tile_grid")
        row = col.row(align=True)
        row.prop(render_ernst, "file_grid")
        col = layout.column(align=True)
        col.prop(render_ernst, "anti_aliasing")

        col = layout.column(align=True)
        col.label(text='Render Mode')
        row = col.row(align=True)
        row.prop(render_ernst, "target_mode", expand=True)
        row = col.row(align=True)
        row.prop(render_ernst, "target_file")
        row.enabled = int(render_ernst.target_mode) >= 1
        row = col.row(align=True)
        row.prop(render_ernst, "target_tile")
        row.enabled = int(render_ernst.target_mode) == 2
