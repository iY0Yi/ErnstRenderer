import bpy
from bpy.types import Panel

from ..bl_ot.bl_ot_gui_uniform import *


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_PT_Uniforms(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = 'Uniforms'
    bl_category = 'Ernst'
    COMPAT_ENGINES = {'ERNST'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False

        col = layout.column(align=False)
        GUI_NAME = 'BluGui_1f'
        if bpy.data.objects.find(GUI_NAME)==-1:
            row = col.row()
            row.operator(ERNST_OT_BLUGUI_1f.bl_idname, text = 'Build BLUGUI:1f', icon='TOOL_SETTINGS')
        else:
            box = col.box()
            row = box.row(align=True)
            row.label(text='BLUGUI:1f:', icon='TOOL_SETTINGS')
            row.operator('ernst.blugui1f_remove', text = '', icon = 'REMOVE')
            row.operator('ernst.blugui1f_add', text = '', icon = 'ADD')

        GUI_NAME = 'BluGui_2v'
        if bpy.data.objects.find(GUI_NAME)==-1:
            row = col.row()
            row.operator(ERNST_OT_BLUGUI_2v.bl_idname, text = 'Build BLUGUI:2v', icon='TOOL_SETTINGS')
        else:
            box = col.box()
            row = box.row(align=True)
            row.label(text='BLUGUI:2v:', icon='TOOL_SETTINGS')
            row.operator('ernst.blugui2v_remove', text = '', icon = 'REMOVE')
            row.operator('ernst.blugui2v_add', text = '', icon = 'ADD')

        GUI_NAME = 'BluGui_3v'
        if bpy.data.objects.find(GUI_NAME)==-1:
            row = col.row()
            row.operator(ERNST_OT_BLUGUI_3v.bl_idname, text = 'Build BLUGUI:3v', icon='TOOL_SETTINGS')
        else:
            box = col.box()
            row = box.row(align=True)
            row.label(text='BLUGUI:3v:', icon='TOOL_SETTINGS')
            row.operator('ernst.blugui3v_remove', text = '', icon = 'REMOVE')
            row.operator('ernst.blugui3v_add', text = '', icon = 'ADD')
