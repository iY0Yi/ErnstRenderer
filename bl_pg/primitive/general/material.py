import bpy
from bpy.types import PropertyGroup

from ....bl_ot.shadergen.shadergen_util import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import is_renderable
from ....bl_ot.shadergen import shadergen_ubo as ubo

is_dirty = {}

def force_dirty(self, context):
    material = self.id_data
    material.ernst.shader_proxy.set_dirty(True)

class ERNST_PG_Proxy_Material(PropertyGroup):
    icon: bpy.props.StringProperty(default = 'MATERIAL')
    specular_intensity : bpy.props.FloatProperty(name = 'specular_intensity', min = 0, max = 1, default = .5, update = force_dirty)
    specular_roughness    : bpy.props.FloatProperty(name = 'specular_roughness', min = 0, max = 1, default = .5, update = force_dirty)

    def get_uniform_names(self):
        material = self.id_data
        u_names = {}
        u_names['color'] = f'{er_var(material.name)}_color'
        u_names['specular_roughness'] = f'{er_var(material.name)}_specular_roughness'
        u_names['specular_intensity'] = f'{er_var(material.name)}_specular_intensity'
        u_names['specular'] = f'{er_var(material.name)}_specular'
        return u_names

    def draw_gui(self, context, layout):
        material = self.id_data
        row = layout.row(align=True)
        row.prop(material, 'diffuse_color', text='', icon='MATERIAL')
        row.prop(material, 'roughness', text='Roughness', icon='MATERIAL')
        row.prop(material, 'specular_intensity', text='Intensity', icon='MATERIAL')

    def get_uniform_dec_code(self):
        u_names = self.get_uniform_names()
        if ubo.enabled:
            code_u_names  = ''
            ubo.add_vec4(u_names["color"])
            ubo.add_vec4(u_names["specular"])
        else:
            code_u_names  = f'uniform vec3 {u_names["color"]};\n'
            code_u_names += f'uniform float {u_names["specular_roughness"]};\n'
            code_u_names += f'uniform float {u_names["specular_intensity"]};\n'
        return code_u_names

    def set_dirty(self, bool):
        obj = self.id_data
        is_dirty[obj.name] = bool

    def update_uniforms(self, shader):
        material = self.id_data
        color = list(material.diffuse_color)
        color[0] = inv_gamma(color[0])
        color[1] = inv_gamma(color[1])
        color[2] = inv_gamma(color[2])
        specular_intensity = material.specular_intensity
        specular_roughness = material.roughness
        u_names = self.get_uniform_names()
        if ubo.enabled:
            if not material.name in is_dirty:
                self.set_dirty(True)
            if is_dirty[material.name] or ubo.is_dirty:
                ubo.data[u_names['color']] = (color[0], color[1], color[2], 0)
                ubo.data[u_names['specular']] = (specular_intensity, specular_roughness, 0, 0)
                self.set_dirty(False)
        else:
            uniform_float(shader, u_names['color'], (color[0], color[1], color[2]))
            uniform_float(shader, u_names['specular_roughness'], specular_intensity)
            uniform_float(shader, u_names['specular_intensity'], specular_roughness)

    def get_shader_code(self):
        material = self.id_data

        if sgd.is_exporting:
            code_color = er_col(list(material.diffuse_color))
            code_specular_roughness = er_f(material.specular_intensity)
            code_specular_intensity = er_f(material.roughness)
        else:
            u_names = self.get_uniform_names()
            if ubo.enabled:
                code_color = '('+ubo.name(u_names['color'])+'.rgb)'
                code_specular_roughness = '('+ubo.name(u_names['specular'])+'.x)'
                code_specular_intensity = '('+ubo.name(u_names['specular'])+'.y)'
            else:
                code_color = u_names['color']
                code_specular_roughness = u_names['specular_roughness']
                code_specular_intensity = u_names['specular_intensity']

        code_mat_name = er_var(material.name).upper()

        code_def = f'''
        #define MAT_{code_mat_name}_COL {code_color}
        #define MAT_{code_mat_name}_SPEC_ROUGHNESS {code_specular_roughness}
        #define MAT_{code_mat_name}_SPEC_INTENSITY {code_specular_intensity}
        '''
        code_params = f'''
        if(isMaterial(MAT_{code_mat_name}_COL)){{
        specular = MAT_{code_mat_name}_SPEC_ROUGHNESS;
        roughness = MAT_{code_mat_name}_SPEC_INTENSITY;
        return;
        }}
        '''
        return code_def, code_params
