import bpy
from bpy.types import PropertyGroup

from ..abstract_sdf import ERNST_PG_SDF_Abstract
from ....bl_ot.shadergen.shadergen_util import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import is_renderable
from ....bl_ot.shadergen.shaderizer.shaderizer_object import is_fixed

from ....bl_ot.shadergen import shadergen_ubo as ubo

is_dirty = {}

class ERNST_PG_SDF3D_Torus(PropertyGroup, ERNST_PG_SDF_Abstract):
    icon: bpy.props.StringProperty(default = 'MESH_TORUS')

    def get_uniform_names(self):
        obj = self.id_data
        u_names = {}
        u_names['radius_main'] = f'{er_var(obj.name)}_radius_main'
        u_names['radius_minor'] = f'{er_var(obj.name)}_radius_minor'
        u_names['radiuses'] = f'{er_var(obj.name)}_radiuses'
        self.get_shell_uniform_name(u_names)
        self.get_boolean_uniform_names(u_names)
        return u_names

    def draw_gui(self, context, layout):
        self.draw_mini_header(layout)

        col = layout.column(align = True)
        obj = self.id_data
        props = bpy.data.objects[obj.name]
        wdata = props.data.wData
        col.prop(wdata, "rad_1", text="Radius Main")
        col.prop(wdata, "rad_2", text="Minor")

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
            ubo.add_vec4(u_names["radiuses"])
            self.add_ubo_shell()
            self.add_ubo_boolean()
        else:
            code_u_names  = f'uniform float {u_names["radius_main"]};\n'
            code_u_names += f'uniform float {u_names["radius_minor"]};\n'
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
                ubo.data[u_names['radiuses']] = (obj.dimensions[0]*.5-obj.dimensions[2]*.5, obj.dimensions[2]*.5, 0,0)
                self.update_ubo_shell()
                self.update_ubo_boolean()
                self.set_dirty(False)
        else:
            uniform_float(shader, u_names['radius_main'], obj.dimensions[0]*.5-obj.dimensions[2]*.5)
            uniform_float(shader, u_names['radius_minor'], obj.dimensions[2]*.5)
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

        loader_rot = sgd.module_lib.pmod['PMOD_ROT_3D']
        loader_rot.used = True

        domain = self.get_code_domain()
        if is_fixed(obj):
            radius_main = er_f(obj.dimensions[0]*.5-obj.dimensions[2]*.5)
            radius_minor = er_f(obj.dimensions[2]*.5)
        else:
            if ubo.enabled:
                radius_main = '('+ubo.name(u_names['radiuses'])+'.x)'
                radius_minor = '('+ubo.name(u_names['radiuses'])+'.y)'
            else:
                radius_main = u_names['radius_main']
                radius_minor = u_names['radius_minor']

        shell0, shell1, shell2 = '', '', ''
        if self.shell_active:
            shell0, shell1, shell2 = self.get_code_shell(u_names['shell'])

        local_domain_name = f'{er_var(obj.name)}_p'
        local_domain = f'vec3 {local_domain_name} = {domain};\n'
        local_domain += obj.ernst.pmods.get_shader_code(obj)

        primitive = '{0}({1}, vec2({2}, {3}){4})'.format(
            loader.fncname,
            local_domain_name,
            radius_main,
            radius_minor,
            shell0
        )
        primitive = f'{shell1}{primitive}{shell2}'

        boolean, mix = self.get_boolean_code(rendables)
        code = f'd = {boolean}{primitive}{mix};'

        code_inline_pre = self.get_code_inline_pre()
        code_inline_post = self.get_code_inline_post()

        return code_inline_pre + local_domain + code + code_inline_post
