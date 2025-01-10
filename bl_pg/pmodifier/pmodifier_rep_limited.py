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
        if pmd != None and pmd.name == 'RepLimited':
            pmd.set_dirty(True)

class ERNST_PG_PModifier_RepLimited(PropertyGroup):
    name: bpy.props.StringProperty(default = 'RepLimited')
    icon: bpy.props.StringProperty(default = 'MOD_ARRAY')
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

    margin: bpy.props.FloatProperty(name = 'Margin', min = 0.0, max = 1000.0, default = 1.0, update = force_dirty)
    repetation: bpy.props.IntProperty(name = 'Repetation', min = 1, max = 10000, default = 1, update = force_dirty)

    def get_uniform_names(self, target_cp_name, id):
        u_names = {}
        u_names['margin'] = f'{target_cp_name}_rep_limited{self.axis.upper()}_margin'
        u_names['repetation'] = f'{target_cp_name}_rep_limited{self.axis.upper()}_repetation'
        u_names['margin_repetation'] = f'{target_cp_name}_rep_limited{self.axis.upper()}_margin_repetation'
        return u_names

    def draw_gui(self, layout, obj, id, active):
        pmod_box = layout.box()
        pmod_box.active = active
        row = pmod_box.row(align=True)

        col = row.column(align=True)
        col.alignment = 'LEFT'
        col.prop(self, "axis")

        col = row.column(align=True)
        row = col.row(align=True)
        row.prop(self, 'repetation', text='Repetation')
        row.prop(self, 'margin', text='Margin')

    def get_uniform_dec_code(self, target_cp_name, id):
        if self.visible==False:
            return ''
        u_names = self.get_uniform_names(target_cp_name, id)
        if ubo.enabled:
            code_u_names = ''
            ubo.add_vec4(u_names['margin_repetation'])
        else:
            code_u_names = f'uniform float {u_names["margin"]};\n'
            code_u_names += f'uniform float {u_names["repetation"]};\n'
        return code_u_names

    def set_dirty(self, bool):
        obj = self.id_data
        is_dirty[obj.name] = bool

    def update_uniforms(self, shader, target_cp_name, id):
        if self.visible==False:
            return
        obj = self.id_data
        u_names = self.get_uniform_names(target_cp_name, id)
        if ubo.enabled:
            if not obj.name in is_dirty:
                self.set_dirty(True)
            if is_dirty[obj.name] or ubo.is_dirty:
                ubo.data[u_names['margin_repetation']] = (self.margin, self.repetation, 0, 0)
                self.set_dirty(False)
        else:
            uniform_float(shader, u_names['margin'], self.margin)
            uniform_float(shader, u_names['repetation'], self.repetation)

    def get_shader_code(self, obj, target_cp_name, id, is_fixed):
        if self.visible==False:
            return ''
        u_names = self.get_uniform_names(target_cp_name, id)
        v = ['']*2
        if is_fixed:
            v[0] = er_f(self.margin)
            v[1] = str(self.repetation)+'.'
        else:
            if ubo.enabled:
                v[0] = f'ubo.{u_names["margin_repetation"]}.x'
                v[1] = f'ubo.{u_names["margin_repetation"]}.y'
            else:
                v[0] = u_names['margin']
                v[1] = u_names['repetation']

        loader = sgd.module_lib.pmod['PMOD_REP_LIMITED']
        loader.used = True
        return '{0}({1}.{2}, {3}, {4});\n'.format(
            loader.fncname,
            target_cp_name,
            self.axis,
            v[0],
            v[1]
        )
