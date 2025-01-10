import bpy
from bpy.props import *
from bpy.types import PropertyGroup

class ERNST_PG_RenderProperties(PropertyGroup):
    tile_grid     : bpy.props.IntProperty(name = 'Tile Grid', min = 1, max = 100, default = 4, options=set([]))
    file_grid     : bpy.props.IntProperty(name = 'File Grid', min = 1, max = 10, default = 2, options=set([]))
    anti_aliasing : bpy.props.IntProperty(name = 'Anti-Aliasing', min = 1, max = 16, default = 1, options=set([]))
    target_mode : bpy.props.EnumProperty(
        name="Render Mode",
        description="Full / File / Tile",
        default='0',
        items=[
            ('0', "Full", "Render Full Image"),
            ('1', "File", "Render a File"),
            ('2', "Tile", "Render a Tile"),
        ],
        options=set([])
    )
    target_tile : bpy.props.IntProperty(name = 'Target Tile ID', min = 0, max = 10000, default = 0, options=set([]))
    target_file : bpy.props.IntProperty(name = 'Target File ID', min = 0, max = 100, default = 0, options=set([]))
 
