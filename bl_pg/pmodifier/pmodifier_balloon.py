import bpy
from bpy.types import PropertyGroup

from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen.shaderizer import shaderizer_watcher
from ...bl_ot.shadergen.shaderizer.shaderizer_object import *
from ...bl_ot.shadergen import shadergen_ubo as ubo

is_dirty = {}

def force_dirty(self, context):
    pmods = self.id_data.ernst.pmods.pmod
    for pmod in pmods.values():
        pmd = pmod.get_pmod()
        if pmd != None and pmd.name == 'Balloon':
            pmd.set_dirty(True)

class ERNST_PG_PModifier_Balloon(PropertyGroup):
    name: bpy.props.StringProperty(default = 'Balloon')
    icon: bpy.props.StringProperty(default = 'NODE_MATERIAL')
    visible: bpy.props.BoolProperty(default = True, update=shaderizer_watcher.check)
    expanded : bpy.props.BoolProperty(default=True)

    axis : bpy.props.EnumProperty(
        name = '',
        default = 'xyz',
        items = (
            ("xyz", "XYZ", "XYZ"),
            ("x", "X", "X"),
            ("y", "Y", "Y"),
            ("z", "Z", "Z")
        ),
        update=shaderizer_watcher.check)

    strength: bpy.props.FloatProperty(name = 'Strength', min = -10, max = 10, default = 0, update = force_dirty)

    def get_uniform_names(self, target_cp_name, id):
        u_name = f'{target_cp_name}_balloon{self.axis.upper()}'
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
        if ubo.enabled:
            code_u_names = ''
            ubo.add_vec4(u_name)
        else:
            code_u_names = f'uniform float {u_name};\n'
        return code_u_names

    def set_dirty(self, bool):
        obj = self.id_data
        is_dirty[obj.name] = bool

    def update_uniforms(self, shader, target_cp_name, id):
        if self.visible==False:
            return
        obj = self.id_data
        u_name = self.get_uniform_names(target_cp_name, id)
        if ubo.enabled:
            if not obj.name in is_dirty:
                self.set_dirty(True)
            if is_dirty[obj.name] or ubo.is_dirty:
                ubo.data[u_name] = (self.strength, 0, 0, 0)
                self.set_dirty(False)
        else:
            uniform_float(shader, u_name, self.strength)

    def get_shader_code(self, obj, target_cp_name, id, is_fixed):
        if self.visible==False:
            return ''
        u_name = self.get_uniform_names(target_cp_name, id)
        if is_fixed:
            v = er_f(self.strength)
        else:
            if ubo.enabled:
                v = f'ubo.{u_name}.x'
            else:
                v = u_name

        elem = 'xyz'
        v_name = 'V3'
        if self.axis == 'x':
            elem = 'yz'
            v_name = 'V2'
        elif self.axis == 'y':
            elem = 'xz'
            v_name = 'V2'
        elif self.axis == 'z':
            elem = 'xy'
            v_name = 'V2'

        module_name = 'PMOD_BALLOON_V2'
        if v_name == 'V3': module_name = 'PMOD_BALLOON_V3'
        loader = sgd.module_lib.pmod[module_name]
        loader.used = True
        return '{0}({1}.{2}, {3});\n'.format(
            loader.fncname,
            target_cp_name,
            elem,
            v
        )
