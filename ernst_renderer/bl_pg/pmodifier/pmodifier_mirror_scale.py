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
        if pmd != None and pmd.name == 'Mirror Scale':
            pmd.set_dirty(True)

class ERNST_PG_PModifier_MirrorScale(PropertyGroup):
    name: bpy.props.StringProperty(default = 'Mirror Scale')
    icon: bpy.props.StringProperty(default = 'CON_SIZELIMIT')
    visible: bpy.props.BoolProperty(default = True, update=shaderizer_watcher.check)
    expanded : bpy.props.BoolProperty(default=True)

    target_axis: bpy.props.EnumProperty(
        name = '',
        default = '+x',
        items = (
            ("+x", "+X", "+X"),
            ("+y", "+Y", "+Y"),
            ("+z", "+Z", "+Z"),
            ("-x", "-X", "-X"),
            ("-y", "-Y", "-Y"),
            ("-z", "-Z", "-Z")
        ),
        update=shaderizer_watcher.check)

    value: bpy.props.FloatProperty(name = 'value', min = 0.001, max = 2.0, default = 1, update = force_dirty)

    def get_uniform_names(self, target_cp_name, id):
        side = 'P' if self.target_axis[0] == '+' else 'N'
        target_axis_elem = self.target_axis[1:].upper()
        u_name = f'{target_cp_name}_mirror{id}{target_axis_elem}_{side}_scale'
        return u_name

    def draw_gui(self, layout, obj, id, active):
        pmod_box = layout.box()
        pmod_box.active = active
        row = pmod_box.row(align=True)
        row.label(text = 'Target Side:')
        col = row.column(align=True)
        col.alignment = 'LEFT'
        col.prop(self, "target_axis", expand=False)

        row = pmod_box.row(align=True)
        row.prop(self, 'value', text='Scale')

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
                ubo.data[u_name] = (self.value, 0, 0, 0)
                self.set_dirty(False)
        else:
            uniform_float(shader, u_name, self.value)

    def get_shader_code(self, obj, target_cp_name, id, is_fixed):
        if self.visible==False:
            return ''
        mirror_id = id
        u_name = self.get_uniform_names(target_cp_name, mirror_id)
        if is_fixed:
            v = er_f(self.value)
        else:
            if ubo.enabled:
                v = f'ubo.{u_name}.x'
            else:
                v = u_name

        side = f'{target_cp_name}_mir{mirror_id}_Pos' if self.target_axis[0] == '+' else f'{target_cp_name}_mir{mirror_id}_Neg'
        target_axis_elem = self.target_axis[1:]

        code = 'float {0}_scale = ({1}.{2}>0.) ? {3} : 1.;'.format(
            target_cp_name,
            side,
            target_axis_elem,
            v
        )
        code += f'{target_cp_name} /= {target_cp_name}_scale;\n'

        ### Additional code for finish scaling in
        ### "shaderizer_material.py"

        return code
