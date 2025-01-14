import math
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

class ERNST_PG_Camera(PropertyGroup, ERNST_PG_Primitive_Abstract):
    icon: bpy.props.StringProperty(default = 'OUTLINER_OB_CAMERA')

    def get_uniform_names(self):
        obj = self.id_data
        u_names = {}
        u_names['position'] = f'{er_var(obj.name)}_position'
        u_names['pivot'] = f'{er_var(obj.name)}_pivot'
        u_names['quaternion'] = f'{er_var(obj.name)}_quaternion'
        u_names['props'] = f'{er_var(obj.name)}_props'
        u_names['is_perspective'] = f'{er_var(obj.name)}_is_perspective'
        u_names['fov'] = f'{er_var(obj.name)}_fov'
        u_names['ortho_dist'] = f'{er_var(obj.name)}_orthoDist'
        u_names['ortho_scale'] = f'{er_var(obj.name)}_orthoScale'
        return u_names

    def draw_gui(self, context, layout):
        obj = self.id_data
        row = layout.row()
        row.label(text=obj.name, icon = self.icon)
        row = layout.row()
        col = layout.column(align=True)
        col.label(text='FOV:')
        col.prop(obj.data, 'angle', text='')

        col = layout.column(align=True)
        col.prop(bpy.context.workspace.ernst, 'canvas_mode', text='Canvas Mode:')
        col.prop(bpy.context.workspace.ernst, 'canvas_offset_x', text='')
        col.prop(bpy.context.workspace.ernst, 'canvas_offset_y', text='')

    def get_uniform_dec_code(self):
        obj = self.id_data
        if not is_renderable(obj):
           return ''
        u_names = self.get_uniform_names()
        if ubo.enabled:
            code_u_names  = ''
            ubo.add_vec4(u_names["position"])
            ubo.add_vec4(u_names["pivot"])
            ubo.add_vec4(u_names["quaternion"])
            ubo.add_vec4(u_names["props"])
        else:
            code_u_names = '\n'
            code_u_names += f'uniform vec3 {u_names["position"]};\n'
            code_u_names += f'uniform vec3 {u_names["pivot"]};\n'
            code_u_names += f'uniform vec4 {u_names["quaternion"]};\n'
            code_u_names += f'uniform bool {u_names["is_perspective"]};\n'
            code_u_names += f'uniform float {u_names["fov"]};\n'
            code_u_names += f'uniform float {u_names["ortho_dist"]};\n'
            code_u_names += f'uniform float {u_names["ortho_scale"]};\n'
        return code_u_names

    def set_dirty(self, bool):
        obj = self.id_data
        is_dirty[obj.name] = bool

    def get_real_values(self):
        context = bpy.context
        obj = self.id_data
        data = obj.data
        camera_type = obj.data.type
        area = context.area
        pers = area.spaces.active.region_3d.view_perspective

        values = {}

        if pers == 'CAMERA':
            mat = obj.matrix_world
            if camera_type == 'PERSP':
                values['quaternion'] = mat.to_quaternion()
                values['pivot'] = area.spaces.active.region_3d.view_location
                values['position'] = (mat.translation.x, mat.translation.z, mat.translation.y)
                values['fov'] = data.angle*0.5
                values['ortho_dist'] = context.area.spaces.active.region_3d.view_distance
                values['ortho_scale'] = data.ortho_scale
                values['is_perspective'] = True
            else:
                values['quaternion'] = mat.to_quaternion()
                values['pivot'] = area.spaces.active.region_3d.view_location
                values['position'] = (mat.translation.x, mat.translation.y, mat.translation.z)
                values['fov'] = data.angle*0.5
                values['ortho_dist'] = context.area.spaces.active.region_3d.view_distance
                values['ortho_scale'] = data.ortho_scale
                values['is_perspective'] = False
        else:
            mat = area.spaces.active.region_3d.view_matrix.inverted()
            is_perspective = context.area.spaces.active.region_3d.is_perspective
            angle = 2.0 * math.atan((72 / 2.0) / area.spaces.active.lens)
            if is_perspective:
                values['quaternion'] = mat.to_quaternion()
                values['pivot'] = area.spaces.active.region_3d.view_location
                values['position'] = (mat.translation.x, mat.translation.z, mat.translation.y)
                values['fov'] = angle*0.5
                values['ortho_dist'] = context.area.spaces.active.region_3d.view_distance
                values['ortho_scale'] = data.ortho_scale
                values['is_perspective'] = True
            else:
                values['quaternion'] = mat.to_quaternion()
                values['pivot'] = area.spaces.active.region_3d.view_location
                values['position'] = (mat.translation.x, mat.translation.y, mat.translation.z)
                values['fov'] = angle*0.5
                values['ortho_dist'] = context.area.spaces.active.region_3d.view_distance
                values['ortho_scale'] = values['ortho_dist']*3.0*(16/50)*(50/area.spaces.active.lens)
                values['is_perspective'] = False

        return values


    def update_uniforms(self, shader):
        # obj = self.id_data
        values = self.get_real_values()
        u_names = self.get_uniform_names()
        if ubo.enabled:
            # if not obj.name in is_dirty:
            #     self.set_dirty(True)
            # if is_dirty[obj.name] or ubo.is_dirty:
            ubo.data[u_names['position']] = (values['position'][0], values['position'][1], values['position'][2], 0)
            ubo.data[u_names['pivot']] = (values['pivot'][0], values['pivot'][1], values['pivot'][2], 0)
            ubo.data[u_names['quaternion']] = (values['quaternion'].x, values['quaternion'].y, values['quaternion'].z, -values['quaternion'].w)
            ubo.data[u_names['props']] = (int(values['is_perspective']), values['fov'], values['ortho_dist'], values['ortho_scale'])
            self.set_dirty(False)
        else:
            uniform_bool(shader, u_names['is_perspective'], values['is_perspective'])
            uniform_float(shader, u_names['position'], values['position'])
            uniform_float(shader, u_names['pivot'], values['pivot'])
            uniform_float(shader, u_names['quaternion'], values['quaternion'])
            uniform_float(shader, u_names['fov'], values['fov'])
            uniform_float(shader, u_names['ortho_dist'], values['ortho_dist'])
            uniform_float(shader, u_names['ortho_scale'], values['ortho_scale'])

    def get_shader_code(self, rendables):
        obj = self.id_data
        data = obj.data
        sgd.code_raymarch_buf_init_dec +='Ray ray;\n'
        sgd.code_raymarch_buf_init_dec +=f'Camera {er_var(obj.name)};\n'

        if is_fixed(obj):
            # values = self.get_real_values()
            mat = obj.matrix_world
            cam_quat = mat.to_quaternion()
            cam_quat.w *= -1
            # {er_var(obj.name)}.position = {er_v3(mat.translation)};
            # {er_var(obj.name)}.quaternion = {er_v4(cam_quat)};
            # {er_var(obj.name)}.fov = {er_f(data.angle*0.5)};
            code = f'''
            {er_var(obj.name)}.position = {er_v3(mat.translation)};
            {er_var(obj.name)}.quaternion = {er_v4(cam_quat)};
            {er_var(obj.name)}.fov = {er_f(data.angle*0.5)};
            {er_var(obj.name)}.orthoDist = 0.;
            {er_var(obj.name)}.orthoScale = 0.;
            '''
        else:
            u_names = self.get_uniform_names()
            if ubo.enabled:
                code = f'''
                {er_var(obj.name)}.position = {ubo.name(u_names["position"])}.xyz;
                {er_var(obj.name)}.pivot = {ubo.name(u_names["pivot"])}.xyz;
                {er_var(obj.name)}.quaternion = {ubo.name(u_names["quaternion"])};
                {er_var(obj.name)}.is_perspective = bool({ubo.name(u_names["props"])}.x);
                {er_var(obj.name)}.fov = {ubo.name(u_names["props"])}.y;
                {er_var(obj.name)}.orthoDist = {ubo.name(u_names["props"])}.z;
                {er_var(obj.name)}.orthoScale = {ubo.name(u_names["props"])}.w;
                '''
            else:
                code = f'''
                {er_var(obj.name)}.position = {u_names["position"]};
                {er_var(obj.name)}.pivot = {u_names["pivot"]};
                {er_var(obj.name)}.quaternion = {u_names["quaternion"]};
                {er_var(obj.name)}.is_perspective = {u_names["is_perspective"]};
                {er_var(obj.name)}.fov = {u_names["fov"]};
                {er_var(obj.name)}.orthoDist = {u_names["ortho_dist"]};
                {er_var(obj.name)}.orthoScale = {u_names["ortho_scale"]};
                '''

        return code
