import bpy
from bpy.types import PropertyGroup

from ..abstract_primitive import ERNST_PG_Primitive_Abstract
from ....bl_ot.shadergen.shadergen_util import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import is_renderable
from ....bl_ot.shadergen import shadergen_ubo as ubo

is_dirty = {}

def force_dirty(self, context):
    obj = self.id_data
    obj.ernst.shader_proxy.set_dirty(True)

class ERNST_PG_Light_Directional(PropertyGroup, ERNST_PG_Primitive_Abstract):
    icon: bpy.props.StringProperty(default = 'LIGHT_SUN')
    shadow_clip_start : bpy.props.FloatProperty(name='Shadow Clip Start', min = 0.001, max = 100.0, default = 0.05, update=force_dirty)
    shadow_clip_end   : bpy.props.FloatProperty(name = 'Shadow Clip End', min = 0.001, max = 10000.0, default = 30.0, update=force_dirty)
    shadow_softness   : bpy.props.FloatProperty(name = 'Shadow Softness', min = 0.0, max = 1000.0, default = 50.0, update=force_dirty)

    def get_uniform_names(self):
        obj = self.id_data
        u_names = {}
        u_names['direction'] = f'{er_var(obj.name)}_direction'
        u_names['color'] = f'{er_var(obj.name)}_color'
        u_names['shadow'] = f'{er_var(obj.name)}_shadow'
        u_names['intensity'] = f'{er_var(obj.name)}_intensity'
        u_names['shadow_min'] = f'{er_var(obj.name)}_shadow_min'
        u_names['shadow_max'] = f'{er_var(obj.name)}_shadow_max'
        u_names['shadow_softness'] = f'{er_var(obj.name)}_shadow_softness'
        return u_names

    def draw_gui(self, context, layout):
        obj = self.id_data
        row = layout.row()
        row.label(text=obj.name, icon = self.icon)
        row.prop(obj.ernst.shader_proxy.props, "hide",
            icon="HIDE_ON" if obj.ernst.shader_proxy.props.hide else "HIDE_OFF",
            icon_only=True, emboss=False
        )
        col = layout.column(align=True)
        col.active = not obj.ernst.shader_proxy.props.hide
        col.label(text='Color:')
        col.prop(obj.data, 'color', text='')
        col.label(text='Shadow:')
        col.prop(self, 'shadow_clip_start', text='Start')
        col.prop(self, 'shadow_clip_end', text='End')
        col.prop(self, 'shadow_softness', text='Softness')

    def get_uniform_dec_code(self):
        u_names = self.get_uniform_names()
        if ubo.enabled:
            code_u_names  = ''
            ubo.add_vec4(u_names["direction"])
            ubo.add_vec4(u_names["color"])
            ubo.add_vec4(u_names["shadow"])
        else:
            code_u_names = f'uniform vec3 {u_names["direction"]};\n'
            code_u_names += f'uniform vec3 {u_names["color"]};\n'
            code_u_names += f'uniform float {u_names["intensity"]};\n'
            code_u_names += f'uniform float {u_names["shadow_min"]};\n'
            code_u_names += f'uniform float {u_names["shadow_max"]};\n'
            code_u_names += f'uniform float {u_names["shadow_softness"]};\n'
        return code_u_names

    def set_dirty(self, bool):
        obj = self.id_data
        is_dirty[obj.name] = bool

    def update_uniforms(self, shader):
        obj = self.id_data
        if not is_renderable(obj):
           return
        data = obj.data
        vdir = obj.matrix_world.to_quaternion() @ Vector((0,0,1))
        u_names = self.get_uniform_names()
        if ubo.enabled:
            if not obj.name in is_dirty:
                self.set_dirty(True)
            if is_dirty[obj.name] or ubo.is_dirty:
                ubo.data[u_names['direction']] = (vdir.x, vdir.z, vdir.y, 0)
                ubo.data[u_names['color']] = (data.color[0], data.color[1], data.color[2], data.energy)
                ubo.data[u_names['shadow']] = (self.shadow_clip_start, self.shadow_clip_end, self.shadow_softness, 0)
                self.set_dirty(False)
        else:
            uniform_float(shader, u_names['direction'], Vector((vdir.x, vdir.z, vdir.y)))
            uniform_float(shader, u_names['color'], Vector(data.color))
            uniform_float(shader, u_names['intensity'], data.energy)
            uniform_float(shader, u_names['shadow_min'], self.shadow_clip_start)
            uniform_float(shader, u_names['shadow_max'], self.shadow_clip_end)
            uniform_float(shader, u_names['shadow_softness'], self.shadow_softness)

    def get_shader_code(self, rendables):
        obj = self.id_data
        sgd.code_raymarch_buf_init_dec += f'Light {er_var(obj.name)};'
        data = obj.data
        if is_fixed(obj):
            vdir = obj.matrix_world.to_quaternion() @ Vector((0,0,1))
            vcol = Vector(data.color)
            code = f'''
            {er_var(obj.name)}.direction = normalize({er_v3(vdir)});
            {er_var(obj.name)}.color = {er_col(vcol)};
            {er_var(obj.name)}.intensity = {er_f(data.energy)};
            {er_var(obj.name)}.shadowStart = {er_f(abs(self.shadow_clip_start))};
            {er_var(obj.name)}.shadowEnd = {er_f(abs(self.shadow_clip_end))};
            {er_var(obj.name)}.shadowSoft = {er_f(abs(self.shadow_softness))};
            '''
        else:
            u_names = self.get_uniform_names()
            if ubo.enabled:
                code = f'''
                {er_var(obj.name)}.direction = {ubo.name(u_names["direction"])}.xyz;
                {er_var(obj.name)}.color = {ubo.name(u_names["color"])}.rgb;
                {er_var(obj.name)}.intensity = {ubo.name(u_names["color"])}.a;
                {er_var(obj.name)}.shadowStart = {ubo.name(u_names["shadow"])}.x;
                {er_var(obj.name)}.shadowEnd = {ubo.name(u_names["shadow"])}.y;
                {er_var(obj.name)}.shadowSoft = {ubo.name(u_names["shadow"])}.z;
                '''
            else:
                code = f'''
                {er_var(obj.name)}.direction = {u_names["direction"]};
                {er_var(obj.name)}.color = {u_names["color"]};
                {er_var(obj.name)}.intensity = {u_names["intensity"]};
                {er_var(obj.name)}.shadowStart = {u_names["shadow_min"]};
                {er_var(obj.name)}.shadowEnd = {u_names["shadow_max"]};
                {er_var(obj.name)}.shadowSoft = {u_names["shadow_softness"]};
                '''

        return code
