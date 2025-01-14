import bpy
from bpy.types import PropertyGroup

from ..abstract_sdf import ERNST_PG_SDF_Abstract
from ....bl_ot.shadergen.shadergen_util import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import is_renderable
from ....bl_ot.shadergen.shaderizer.shaderizer_object import is_fixed

from ....bl_ot.shadergen import shadergen_ubo as ubo

is_dirty = {}

class ERNST_PG_SDF3D_ConeRound(PropertyGroup, ERNST_PG_SDF_Abstract):
    icon: bpy.props.StringProperty(default = 'CONE')

    def get_uniform_names(self):
        obj = self.id_data
        u_names = {}
        u_names['radius_top'] = f'{er_var(obj.name)}_radius_top'
        u_names['radius_bottom'] = f'{er_var(obj.name)}_radius_bottom'
        u_names['height'] = f'{er_var(obj.name)}_height'
        u_names['radiuses_height'] = f'{er_var(obj.name)}_radiuses_height'
        self.get_shell_uniform_name(u_names)
        self.get_boolean_uniform_names(u_names)
        return u_names

    def draw_gui(self, context, layout):
        self.draw_mini_header(layout)
        col = layout.column(align = True)
        obj = self.id_data
        props = bpy.data.objects[obj.name]
        wdata = props.data.WCone
        col.prop(wdata, "rad_top", text="Radius Top")
        col.prop(wdata, "rad_main", text="Radius Main")
        col.prop(wdata, "height", text="Height")

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
            ubo.add_vec4(u_names["radiuses_height"])
            self.add_ubo_shell()
            self.add_ubo_boolean()
        else:
            code_u_names  = f'uniform float {u_names["radius_top"]};\n'
            code_u_names += f'uniform float {u_names["radius_bottom"]};\n'
            code_u_names += f'uniform float {u_names["height"]};\n'
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
        props = bpy.data.objects[obj.name]
        wdata = props.data.WCone
        rad_top = wdata.rad_top
        rad_main = wdata.rad_main
        height = wdata.height
        u_names = self.get_uniform_names()
        if ubo.enabled:
            if not obj.name in is_dirty:
                self.set_dirty(True)
            if is_dirty[obj.name] or ubo.is_dirty:
                ubo.data[u_names['radiuses_height']] = (rad_top*obj.scale[0], rad_main*obj.scale[0], obj.dimensions[2]*.5+rad_top*obj.scale[0]+rad_main*obj.scale[0],0)
                self.update_ubo_shell()
                self.update_ubo_boolean()
                self.set_dirty(False)
        else:
            uniform_float(shader, u_names['radius_top'], rad_top*obj.scale[0])
            uniform_float(shader, u_names['radius_bottom'], rad_main*obj.scale[0])
            uniform_float(shader, u_names['height'], obj.dimensions[2]*.5+rad_top*obj.scale[0]+rad_main*obj.scale[0])
            self.update_shell_uniforms(shader)
            self.update_boolean_uniforms(shader)
        obj.ernst.pmods.update_uniforms(shader, obj)

    def get_shader_code(self, rendables):
        obj = self.id_data
        if not is_renderable(obj):
            return ''

        props = bpy.data.objects[obj.name]
        wdata = props.data.WCone
        rad_top = wdata.rad_top
        rad_main = wdata.rad_main
        height = wdata.height
        u_names = self.get_uniform_names()

        loader = sgd.module_lib.sdf3d[obj.ernst.type]
        loader.used = True

        domain = self.get_code_domain()
        if is_fixed(obj):
            radius_top = er_f(rad_main*obj.scale[0])
            radius_bottom = er_f(rad_top*obj.scale[0])
            height = er_f(obj.dimensions[2]*.5+rad_top*obj.scale[0]+rad_main*obj.scale[0])
        else:
            if ubo.enabled:
                radius_top = '('+ubo.name(u_names['radiuses_height'])+'.x)'
                radius_bottom = '('+ubo.name(u_names['radiuses_height'])+'.y)'
                height = '('+ubo.name(u_names['radiuses_height'])+'.z)'
            else:
                radius_top = u_names['radius_top']
                radius_bottom = u_names['radius_bottom']
                height = u_names['height']

        shell0, shell1, shell2 = '', '', ''
        if self.shell_active:
            shell0, shell1, shell2 = self.get_code_shell(u_names['shell'])

        local_domain_name = f'{er_var(obj.name)}_p'
        local_domain = f'vec3 {local_domain_name} = {domain};\n'
        local_domain += obj.ernst.pmods.get_shader_code(obj)

        primitive = '{0}({1}, {2}{5}, {3}{5}, {4}{5})'.format(
            loader.fncname,
            local_domain_name,
            height,
            radius_bottom,
            radius_top,
            shell0
        )
        primitive = f'{shell1}{primitive}{shell2}'

        boolean, mix = self.get_boolean_code(rendables)
        code = f'd = {boolean}{primitive}{mix};'

        code_inline_pre = self.get_code_inline_pre()
        code_inline_post = self.get_code_inline_post()

        return code_inline_pre + local_domain + code + code_inline_post
