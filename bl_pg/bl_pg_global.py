import bpy
from bpy.types import PropertyGroup

class ERNST_PG_GlobalVariables(PropertyGroup):
    edit_in                   : bpy.props.StringProperty(default = 'SINGLE')
    blui_set_boolean_order    : bpy.props.IntProperty(name = 'Set orders', min = -30, max = 30, default = 0, options=set([]))
    blui_offset_boolean_order : bpy.props.IntProperty(name = 'offset orders', min = -15, max = 15, default = 0, options=set([]))
    enable_edit_trvs : bpy.props.BoolProperty(name='Enable Editting TRVs', default = True)
