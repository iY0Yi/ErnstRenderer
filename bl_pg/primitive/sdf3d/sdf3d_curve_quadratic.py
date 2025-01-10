import bpy
from bpy.types import PropertyGroup

from ..abstract_sdf import ERNST_PG_SDF_Abstract
from ....bl_ot.shadergen.shadergen_util import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import is_renderable
from ....bl_ot.shadergen.shaderizer.shaderizer_object import is_fixed

from ....bl_ot.shadergen import shadergen_ubo as ubo

is_dirty = {}

class ERNST_PG_SDF3D_CurveQuadratic(PropertyGroup, ERNST_PG_SDF_Abstract):
    icon: bpy.props.StringProperty(default = 'OUTLINER_DATA_CURVE')

    def get_uniform_names(self):
        obj = self.id_data
        u_names = {}
        u_names['p2'] = f'{er_var(obj.name)}_p2'
        u_names['p3'] = f'{er_var(obj.name)}_p3'
        u_names['p1_radius'] = f'{er_var(obj.name)}_p1_radius'
        u_names['p3_radius'] = f'{er_var(obj.name)}_p3_radius'
        u_names['p2_p1_radius'] = f'{er_var(obj.name)}_p2_p1_radius'
        u_names['p3_p3_radius'] = f'{er_var(obj.name)}_p3_p3_radius'
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
            ubo.add_vec4(u_names["p2_p1_radius"])
            ubo.add_vec4(u_names["p3_p3_radius"])
            self.add_ubo_shell()
            self.add_ubo_boolean()
        else:
            code_u_names  = f'uniform vec3 {u_names["p2"]};\n'
            code_u_names += f'uniform vec3 {u_names["p3"]};\n'
            code_u_names += f'uniform float {u_names["p1_radius"]};\n'
            code_u_names += f'uniform float {u_names["p3_radius"]};\n'
            code_u_names += self.get_shell_uniform_dec_code()
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
                p2 = convert_axis(obj.data.splines[0].points[1].co)
                p3 = convert_axis(obj.data.splines[0].points[2].co)
                ubo.data[u_names['p2_p1_radius']] = (p2[0],p2[1],p2[2], obj.data.splines[0].points[0].radius)
                ubo.data[u_names['p3_p3_radius']] = (p3[0],p3[1],p3[2], obj.data.splines[0].points[2].radius)
                self.update_ubo_shell()
                self.update_ubo_boolean()
                self.set_dirty(False)
        else:
            uniform_float(shader, u_names['p2'], convert_axis(obj.data.splines[0].points[1].co))
            uniform_float(shader, u_names['p3'], convert_axis(obj.data.splines[0].points[2].co))
            uniform_float(shader, u_names['p1_radius'], obj.data.splines[0].points[0].radius)
            uniform_float(shader, u_names['p3_radius'], obj.data.splines[0].points[2].radius)
            self.update_shell_uniforms(shader)
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
        if is_fixed(obj):
            p2 = er_v3(convert_axis(obj.data.splines[0].points[1].co).xzy)
            p3 = er_v3(convert_axis(obj.data.splines[0].points[2].co).xzy)
            p1_radius = er_f(obj.data.splines[0].points[0].radius)
            p3_radius = er_f(obj.data.splines[0].points[2].radius)
        else:
            if ubo.enabled:
                p2 = '('+ubo.name(u_names['p2_p1_radius'])+'.xyz)'
                p3 = '('+ubo.name(u_names['p3_p3_radius'])+'.xyz)'
                p1_radius = '('+ubo.name(u_names['p2_p1_radius'])+'.w)'
                p3_radius = '('+ubo.name(u_names['p3_p3_radius'])+'.w)'
            else:
                p2 = u_names['p2']
                p3 = u_names['p3']
                p1_radius = u_names['p1_radius']
                p3_radius = u_names['p3_radius']

        shell0, shell1, shell2 = '', '', ''
        if self.shell_active:
            shell0, shell1, shell2 = self.get_code_shell(u_names['shell'])

        local_domain_name = f'{er_var(obj.name)}_p'
        local_domain = f'vec3 {local_domain_name} = {domain};\n'
        local_domain += obj.ernst.pmods.get_shader_code(obj)

        primitive = '{0}({1}, vec3(0), {2}, {3}, {4}{6}, {5}{6})'.format(
            loader.fncname,
            local_domain_name,
            p2,
            p3,
            p1_radius,
            p3_radius,
            shell0
        )
        primitive = f'{shell1}{primitive}{shell2}'
        boolean, mix = self.get_boolean_code(rendables)
        code = f'd = {boolean}{primitive}{mix};'

        code_inline_pre = self.get_code_inline_pre()
        code_inline_post = self.get_code_inline_post()

        return code_inline_pre + local_domain + code + code_inline_post
