import bpy
from bpy.types import PropertyGroup

from ..abstract_sdf import ERNST_PG_SDF_Abstract
from ....bl_ot.shadergen.shadergen_util import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import is_renderable

from ....bl_ot.shadergen import shadergen_ubo as ubo

is_dirty = {}

class ERNST_PG_SDF3D_Box(PropertyGroup, ERNST_PG_SDF_Abstract):
    icon: bpy.props.StringProperty(default = 'MESH_CUBE')

    def get_uniform_names(self):
        obj = self.id_data
        u_names = {}
        u_names['dimensions'] = f'{er_var(obj.name)}_dimensions'
        self.get_round_uniform_name(u_names)
        self.get_shell_uniform_name(u_names)
        self.get_boolean_uniform_names(u_names)
        return u_names

    def draw_gui(self, context, layout):
        self.draw_mini_header(layout)
        box = self.draw_property_box(layout)

        if self.expanded:
            self.draw_parent(context, box)
            self.draw_pmods(box)

            row = box.row(align=True)
            row.prop(self, 'round_active', text='Round:')
            row.active = self.round_active
            row.prop(self, 'round_radius', text='')

            row = box.row(align=True)
            row.prop(self, 'shell_active', text='Shell:')
            row.active = self.shell_active
            row.prop(self, 'shell_tickness', text='')

            self.draw_inlines(box)

        self.draw_boolean(layout)

    def get_uniform_dec_code(self):
        obj = self.id_data
        if not is_renderable(obj):
           return ''
        u_names = self.get_uniform_names()
        if ubo.enabled:
            code_u_names  = ''
            ubo.add_vec4(u_names["dimensions"])
            self.add_ubo_shell()
            self.add_ubo_round()
            self.add_ubo_boolean()
        else:
            code_u_names = f'uniform vec3 {u_names["dimensions"]};\n'
            code_u_names += self.get_shell_uniform_dec_code()
            code_u_names += self.get_round_uniform_dec_code()
            code_u_names += self.get_boolean_uniform_dec_code()
        code_u_names += obj.ernst.pmods.get_uniform_dec_code(obj)
        return code_u_names

    def set_dirty(self, bool):
        obj = self.id_data
        is_dirty[obj.name] = bool

    def update_uniforms(self, shader):
        obj = self.id_data
        if not is_renderable(obj):
           return
        u_names = self.get_uniform_names()

        if ubo.enabled:
            if not obj.name in is_dirty:
                self.set_dirty(True)
            if is_dirty[obj.name] or ubo.is_dirty:
                v = get_dimensions_xyz(obj)
                ubo.data[u_names['dimensions']] = (v[0], v[1], v[2],0)
                self.update_ubo_shell()
                self.update_ubo_boolean()
                self.update_ubo_round()
                self.set_dirty(False)
        else:
            uniform_float(shader, u_names['dimensions'], get_dimensions_xyz(obj))
            self.update_shell_uniforms(shader)
            self.update_round_uniforms(shader)
            self.update_boolean_uniforms(shader)
        obj.ernst.pmods.update_uniforms(shader, obj)

    def get_shader_code(self, rendables):
        obj = self.id_data
        if not is_renderable(obj):
           return ''
        u_names = self.get_uniform_names()

        loader = sgd.module_lib.sdf3d[obj.ernst.type]
        loader.used = True

        domain = self.get_code_domain()
        if ubo.enabled:
            dimensions = self.get_code_dimensions_xyz(u_names['dimensions']) if is_fixed(obj) else '('+ubo.name(u_names['dimensions'])+'.xyz)'
        else:
            dimensions = self.get_code_dimensions_xyz(u_names['dimensions'])

        rounding = '' if self.round_active == False else self.get_code_round(u_names['round'])
        shell0, shell1, shell2 = '', '', ''
        if self.shell_active:
            shell0, shell1, shell2 = self.get_code_shell(u_names['shell'])

        loader_rot = sgd.module_lib.pmod['PMOD_ROT_3D']
        loader_rot.used = True

        local_domain_name = f'{er_var(obj.name)}_p'
        local_domain = f'vec3 {local_domain_name} = {domain};\n'
        local_domain += obj.ernst.pmods.get_shader_code(obj)

        primitive = '{0}({1}, {2}{3}{4}){3}'.format(
            loader.fncname,
            local_domain_name,
            dimensions,
            rounding,
            shell0
        )
        primitive = f'{shell1}{primitive}{shell2}'

        boolean, mix = self.get_boolean_code(rendables)
        code = ''
        val_type = self.bool_value.type
        val_code = self.bool_value.value_code
        stp_type = self.bool_step.type
        stp_code = self.bool_step.value_code
        if val_type == 'Code' and val_code != '':
            code += self.get_bool_argument_shader_code('bool_value')
        if stp_type == 'Code' and stp_code != '':
            code += self.get_bool_argument_shader_code('bool_step')
        code += f'd = {boolean}{primitive}{mix};'

        code_inline_pre = self.get_code_inline_pre()
        code_inline_post = self.get_code_inline_post()

        return code_inline_pre + local_domain + code + code_inline_post
