import bpy
from bpy.types import PropertyGroup
from ..bl_ot.shadergen.shaderizer import shaderizer_watcher
from ..bl_ot.shadergen.shadergen_util import *

class ERNST_PG_CollectionProperties(PropertyGroup):
    is_ernst_obj : bpy.props.BoolProperty(default = False)
    type                   : bpy.props.StringProperty(default = '')
    enable_bounding : bpy.props.BoolProperty(name='Enable', default = False, update=shaderizer_watcher.check)
    bounding_offset : bpy.props.FloatVectorProperty(name='Offset', subtype='TRANSLATION', size = 3, min = -25000.0, max = 25000.0, default=(0,0,0), update=shaderizer_watcher.check)
    bounding_sphere_radius : bpy.props.FloatProperty(name='Radius', min = 0.01, max = 50000.0, default = 1.0, update=shaderizer_watcher.check)
    bounding_box_size : bpy.props.FloatVectorProperty(name='Offset', subtype='XYZ', size = 3, min = 0.01, max = 50000.0, default=(1,1,1), update=shaderizer_watcher.check)
    bounding_type: bpy.props.EnumProperty(
        name = 'Bounding Type',
        default = 'sphere',
        items = (
            ("sphere", "Bounding Sphere", "Bounding Type"),
            ("box", "Bounding Box", "Bounding Type")
        ), update=shaderizer_watcher.check)
    enable_cache : bpy.props.BoolProperty(name='Distance Caching', default=False, update=shaderizer_watcher.check)
    force_export_function : bpy.props.BoolProperty(name='Force Export', default = False, update=shaderizer_watcher.check)

    def get_cached_name(self):
        collection = self.id_data
        return f'cache_{er_var(collection.name)}'

    def get_cached_dec_code(self):
        if self.enable_cache:
            return f'vec4 {self.get_cached_name()};\n'
        else:
            return ''

    def draw_gui(self, context, layout):
        layout.use_property_split = False

        col = layout.column(align = True)
        col.prop(self, 'force_export_function', text='Force Export')
        col = layout.column(align = True)
        col.prop(self, 'enable_bounding', text='Bounding:')
        col = layout.column(align = True)
        type_icon = 'MESH_UVSPHERE' if self.bounding_type == 'sphere' else 'MESH_CUBE'
        col.prop(self, 'bounding_type', text='', icon = type_icon)
        col = layout.column(align = True)
        col.active = self.enable_bounding
        col.prop(self, 'bounding_offset', text='')
        if self.bounding_type == 'sphere':
            col.prop(self, 'bounding_sphere_radius', text='Radius')
        else:
            col.prop(self, 'bounding_box_size', text='Size')

        col = layout.column(align = True)
        col.prop(self, 'enable_cache', text='Enable Distance Caching')
