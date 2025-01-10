import bpy
from bpy.types import PropertyGroup

from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen.shaderizer import shaderizer_watcher
from ...bl_ot.shadergen.shaderizer.shaderizer_object import *

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_PG_PModifier_CurvedElongate(PropertyGroup):
    name: bpy.props.StringProperty(default = 'CurvedElongate')
    icon: bpy.props.StringProperty(default = 'MOD_SIMPLEDEFORM')
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

    strength: bpy.props.FloatProperty(name = 'Strength', min = -10., max = 10, default = 0)

    def get_uniform_names(self, target_cp_name, id):
        u_name = f'{target_cp_name}_bend{self.axis.upper()}'
        return u_name

    def draw_gui(self, layout, obj, id, active):
        pmod_box = layout.box()
        pmod_box.active = active
        row = pmod_box.row(align=True)

        col = row.column(align=True)
        col.alignment = 'LEFT'
        col.prop(self, "axis", expand=False)

        col = row.column(align=True)
        col.prop(self, 'strength', text='Strength')

    def get_uniform_dec_code(self, target_cp_name, id):
        if self.visible==False:
            return ''
        u_name = self.get_uniform_names(target_cp_name, id)
        return 'uniform float {u_name};\n'

    def update_uniforms(self, shader, target_cp_name, id):
        if self.visible==False:
            return
        u_name = self.get_uniform_names(target_cp_name, id)
        # shader.uniform_float(u_name, self.strength)
        uniform_float(shader, u_name, self.strength)

    def get_shader_code(self, obj, target_cp_name, id, is_fixed):
        if self.visible==False:
            return ''
        u_name = self.get_uniform_names(target_cp_name, id)

        elem = 'xy'
        if self.axis == 'x':
            elem = 'yz'
        elif self.axis == 'y':
            elem = 'xz'
        elif self.axis == 'z':
            elem = 'xy'

        loader = sgd.module_lib.pmod['PMOD_CURVE_ELONGATE']
        loader.used = True
        return '{0}({1}.{2}, {3});\n'.format(
            loader.fncname,
            target_cp_name,
            elem,
            er_f(self.strength) if is_fixed else u_name
        )
