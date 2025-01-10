import bpy
from bpy.types import PropertyGroup

from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen.shaderizer import shaderizer_watcher
from ...bl_ot.shadergen.shaderizer.shaderizer_object import *

class ERNST_PG_PModifier_Spin(PropertyGroup):
    name: bpy.props.StringProperty(default = 'Spin')
    icon: bpy.props.StringProperty(default = 'MOD_SCREW')
    visible: bpy.props.BoolProperty(default = True, update=shaderizer_watcher.check)
    expanded : bpy.props.BoolProperty(default=True)

    axis : bpy.props.EnumProperty(
        name = '',
        default = 'x',
        items = (
            ("x", "X", "X"),
            ("y", "Y", "Y"),
            ("z", "Z", "Z")
        ),
        update=shaderizer_watcher.check)

    def get_uniform_names(self, target_cp_name, id):
        pass

    def draw_gui(self, layout, obj, id, active):
        pmod_box = layout.box()
        pmod_box.active = active
        row = pmod_box.row(align=True)

        col = row.column(align=True)
        col.alignment = 'LEFT'
        col.prop(self, "axis", expand=False)

    def get_uniform_dec_code(self, target_cp_name, id):
        return ''

    def update_uniforms(self, shader, target_cp_name, id):
        pass

    def get_shader_code(self, obj, target_cp_name, id, is_fixed):
        if self.visible==False:
            return ''
        loader = sgd.module_lib.pmod['PMOD_SPIN']
        loader.used = True
        elem = 'xy'
        if self.axis == 'x':
            elem = 'yxz'
        elif self.axis == 'y':
            elem = 'xyz'
        elif self.axis == 'z':
            elem = 'xzy'
        code = '{0}({1}.{2});\n'.format(
                loader.fncname,
                target_cp_name,
                elem
            )
        return code
