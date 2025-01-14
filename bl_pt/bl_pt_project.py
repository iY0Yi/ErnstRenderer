from bpy.types import Panel

from ..bl_ot.bl_ot_export_shader import *
from ..bl_ot.shadergen import shadergen_data as sgd

class ERNST_PT_Project(Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_label = 'Project'
    bl_order = 0
    COMPAT_ENGINES = {'ERNST'}

    @classmethod
    def poll(cls, context):
        return (context.engine in cls.COMPAT_ENGINES)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False

        col = layout.column(align = True)
        col.label(text='Buffers:')
        box = layout.box()
        col = box.column(align = True)
        context.workspace.ernst.image.draw_gui(context, col)
        context.workspace.ernst.buffer_a.draw_gui(context, col)
        context.workspace.ernst.buffer_b.draw_gui(context, col)
        context.workspace.ernst.buffer_c.draw_gui(context, col)
        context.workspace.ernst.buffer_d.draw_gui(context, col)

        col = layout.column(align = True)
        row = col.row(align = True)
        row.label(text='Resolution Scale:')
        row.prop(context.workspace.ernst, 'resolution_scale', text='')

        col = layout.column(align = True)
        row = col.row(align = True)
        row.label(text='Hit Distance:')
        row.prop(context.workspace.ernst, 'hit_distance', text='')

        col = layout.column(align = True)
        row = col.row(align = True)
        row.label(text='End Distance:')
        row.prop(context.workspace.ernst, 'end_distance', text='')

        col = layout.column(align = True)
        row = col.row(align = True)
        row.label(text='Max Marching Steps:')
        row.prop(context.workspace.ernst, 'max_marching_steps', text='')

        col = layout.column(align = True)
        row = col.row(align = True)
        row.label(text='Matcap:')
        row.prop(context.workspace.ernst, 'matcap', text='')

        col = layout.column(align = True)
        row = col.row(align = True)
        row.label(text='Print the generated code:')
        row.prop(context.workspace.ernst, 'print_code', text='')

        col = layout.column(align = True)
        row = col.row(align = True)
        row.operator(ERNST_OT_Export_JSON.bl_idname, text = 'Export JSON', icon='EXPORT')



