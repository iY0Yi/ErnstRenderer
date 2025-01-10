import bpy
from bpy.types import PropertyGroup

from ..abstract_sdf import ERNST_PG_SDF_Abstract
from ....bl_ot.shadergen.shadergen_util import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import *
from ....bl_mt.bl_mt_sdf3d import ERNST_MT_Uber3D_CodeName
from ....bl_ot.shadergen.shaderizer.shaderizer_object import is_renderable
from ....bl_ot.shadergen.shaderizer.shaderizer_object import is_fixed

from ....bl_ot.shadergen import shadergen_ubo as ubo

def force_dirty(self, context):
    obj = self.id_data
    obj.ernst.shader_proxy.props.set_dirty(True)

is_dirty = {}

class ERNST_PG_SDF3D_Uber(PropertyGroup, ERNST_PG_SDF_Abstract):
    icon: bpy.props.StringProperty(default = 'TEXT')
    prop0: bpy.props.FloatProperty(name = 'prop0', min = -100.0, max = 100.0, default = 0., update=force_dirty)
    prop1: bpy.props.FloatProperty(name = 'prop1', min = -100.0, max = 100.0, default = 0., update=force_dirty)
    prop2: bpy.props.FloatProperty(name = 'prop2', min = -100.0, max = 100.0, default = 0., update=force_dirty)

    def get_uniform_names(self):
        obj = self.id_data
        u_names = {}
        u_names['dimensions'] = f'{er_var(obj.name)}_dimensions'
        u_names['properties'] = f'{er_var(obj.name)}_properties'
        self.get_round_uniform_name(u_names)
        self.get_shell_uniform_name(u_names)
        self.get_boolean_uniform_names(u_names)
        return u_names

    def draw_gui(self, context, layout):
        self.draw_mini_header(layout)

        col = layout.column(align=True)
        row = col.row(align=True)
        tcol = row.column(align=True)
        tcol.menu(ERNST_MT_Uber3D_CodeName.bl_idname, text=self.code_name, icon='TEXT')
        tcol = row.column(align=True)
        op = tcol.operator('ernst.open_in_vscode', text='', icon='GREASEPENCIL')
        op.filepath = f'//track/uber_scripts/sdf3d/{self.code_name}'

        col.prop(self, 'prop0', text='Prop0:')
        col.prop(self, 'prop1', text='Prop1:')
        col.prop(self, 'prop2', text='Prop2:')

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
            ubo.add_vec4(u_names["properties"])
            self.add_ubo_shell()
            self.add_ubo_round()
            self.add_ubo_boolean()
        else:
            code_u_names  = f'uniform vec3 {u_names["dimensions"]};\n'
            code_u_names += f'uniform vec3 {u_names["properties"]};\n'
            code_u_names += self.get_shell_uniform_dec_code()
            code_u_names += self.get_round_uniform_dec_code()
            code_u_names += self.get_boolean_uniform_dec_code()
        code_u_names += obj.ernst.pmods.get_uniform_dec_code(obj)
        return code_u_names

    def set_dirty(self, bool):
        obj = self.id_data
        is_dirty[obj.name] = bool

    def get_code_properties(self, u_name):
        obj = self.id_data
        if is_fixed(obj):
            return f'vec3({er_f(self.prop0)}, {er_f(self.prop1)}, {er_f(self.prop2)})'
        else:
            if ubo.enabled:
                u_names = self.get_uniform_names()
                return '('+ubo.name(u_names['properties'])+'.xyz)'
            else:
                return u_name

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
                ubo.data[u_names['dimensions']] = (v[0],v[1],v[2], 0)
                ubo.data[u_names['properties']] = (self.prop0, self.prop1, self.prop2, 0)
                self.update_ubo_shell()
                self.update_ubo_round()
                self.update_ubo_boolean()
                self.set_dirty(False)
        else:
            uniform_float(shader, u_names['dimensions'], get_dimensions_xyz(obj))
            uniform_float(shader, u_names['properties'], Vector((self.prop0, self.prop1, self.prop2)))
            self.update_shell_uniforms(shader)
            self.update_round_uniforms(shader)
            self.update_boolean_uniforms(shader)
        obj.ernst.pmods.update_uniforms(shader, obj)

    def get_shader_code(self, rendables):
        obj = self.id_data
        if not is_renderable(obj):
           return ''

        if self.code_name == '':
            return ''

        u_names = self.get_uniform_names()

        domain = self.get_code_domain()
        dimensions = self.get_code_dimensions_xyz(u_names['dimensions'])
        properties = self.get_code_properties(u_names['properties'])
        boolean, mix = self.get_boolean_code(rendables)

        rounding = '' if self.round_active == False else self.get_code_round(u_names['round'])
        shell0, shell1, shell2 = '', '', ''
        if self.shell_active:
            shell0, shell1, shell2 = self.get_code_shell(u_names['shell'])

        local_domain_name = f'{er_var(obj.name)}_p'
        local_domain = f'vec3 {local_domain_name} = {domain};\n'
        local_domain += obj.ernst.pmods.get_shader_code(obj)

        code_inline_pre = self.get_code_inline_pre()
        code_inline_post = self.get_code_inline_post()

        header = code_inline_pre
        header+= local_domain
        header+= f'{{/*--- {self.code_name} ---*/\n'
        header+= f'vec3 tp = {domain};\n'
        header+= f'vec3 trp = {local_domain_name};\n'
        header+= f'vec3 dim = {dimensions}{rounding}{shell0};\n'
        header+= f'vec3 props = {properties};\n'
        header+= 'float td = MAX_DIST;\n'

        val_type = self.bool_value.type
        val_code = self.bool_value.value_code
        stp_type = self.bool_step.type
        stp_code = self.bool_step.value_code
        if val_type == 'Code' and val_code != '':
            header += self.get_bool_argument_shader_code('bool_value')
        if stp_type == 'Code' and stp_code != '':
            header += self.get_bool_argument_shader_code('bool_step')

        footer = f'\nd={boolean}{shell1}td{rounding}{shell2}{mix};\n'
        footer+= '}\n'
        footer+= code_inline_post
        return compile_uber_template(obj, domain, 'sdf3d', '', self.code_name, header, footer)
