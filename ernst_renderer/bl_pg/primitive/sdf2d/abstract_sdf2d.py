import bpy
from bpy.types import PropertyGroup

from ..abstract_sdf import ERNST_PG_SDF_Abstract
from ....bl_ot.shadergen.shaderizer import shaderizer_watcher

def get_name_axis():
    return 'axis'

def get_dafault_axis():
    return 'y'

def get_component_axis():
    return (
        ("x", "X", "X"),
        ("y", "Y", "Y"),
        ("z", "Z", "Z")
    )

def update_geometry(self, context):
    last_axis = self.id_data.ernst.shader_proxy.props.last_axis
    if last_axis == self.axis: return
    
    bpy.ops.object.select_all(action='DESELECT')
    self.id_data.select_set(True)
    bpy.ops.view3d.snap_cursor_to_selected()
    bpy.ops.object.rotation_clear(clear_delta=False)

    if self.axis == 'x':
        if last_axis=='y': 
            bpy.ops.transform.rotate(value=1.5708, orient_axis='X')
            bpy.ops.transform.rotate(value=1.5708, orient_axis='Z')

        if last_axis=='z':
            bpy.ops.transform.rotate(value=1.5708, orient_axis='Z')

    if self.axis == 'y':
        if last_axis=='x':
            bpy.ops.transform.rotate(value=1.5708, orient_axis='Z')
            bpy.ops.transform.rotate(value=1.5708, orient_axis='X')

        if last_axis=='z':
            bpy.ops.transform.rotate(value=1.5708, orient_axis='X')

    if self.axis == 'z':
        if last_axis=='x':
            bpy.ops.transform.rotate(value=1.5708, orient_axis='Z')

        if last_axis=='y':
            bpy.ops.transform.rotate(value=1.5708, orient_axis='X')

    bpy.ops.object.transform_apply(rotation=True)
    self.id_data.ernst.shader_proxy.props.last_axis = self.axis
    
    shaderizer_watcher.need_analyze = True

class ERNST_PG_SDF_2D_Abstract(ERNST_PG_SDF_Abstract):
    axis : bpy.props.EnumProperty(
    name = get_name_axis(),
    default = get_dafault_axis(),
    items = get_component_axis(),
    update=update_geometry)
    last_axis : bpy.props.StringProperty(default = 'y')
    
    def get_code_plane_axis(self):
        code = 'xy'
        if self.axis == 'x':
            code = 'yz'
        elif self.axis == 'y':
            code = 'xz'
        elif self.axis == 'z':
            code = 'xy'
        return code

