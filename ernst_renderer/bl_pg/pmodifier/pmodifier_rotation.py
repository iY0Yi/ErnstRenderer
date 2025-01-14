import bpy
import numpy as np
from bpy.types import PropertyGroup

from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen import shadergen_ubo as ubo
from ...bl_ot.shadergen.shaderizer import shaderizer_watcher
from ...bl_ot.shadergen.shaderizer.shaderizer_object import *

is_dirty = {}

class ERNST_PG_PModifier_Rotation(PropertyGroup):
    name: bpy.props.StringProperty(default = 'Rotation')
    icon: bpy.props.StringProperty(default = 'EMPTY_ARROWS')
    visible: bpy.props.BoolProperty(default = True, update=shaderizer_watcher.check)
    expanded : bpy.props.BoolProperty(default=True)

    def get_uniform_names(self, target_cp_name, id):
        obj = self.id_data
        u_names = {}
        u_names['rotation'] = f'{er_var(obj.name)}_rotation'
        return u_names

    def draw_gui(self, layout, obj, id, active):
        pmod_box = layout.box()
        pmod_box.active = False
        row = pmod_box.row()
        obj_props = bpy.data.objects[obj.name]
        row.label(text='X: {0:.3f}'.format(obj_props.rotation_euler[0]))
        row.label(text='Y: {0:.3f}'.format(obj_props.rotation_euler[1]))
        row.label(text='Z: {0:.3f}'.format(obj_props.rotation_euler[2]))

    def get_uniform_dec_code(self, target_cp_name, id):
        if self.visible==False:
            return ''
        u_names = self.get_uniform_names(target_cp_name, id)
        if ubo.enabled:
            code_u_names = ''
            ubo.add_vec4(u_names["rotation"])
        else:
            code_u_names = f'uniform vec3 {u_names["rotation"]};\n'
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
                v = get_local_rot(obj)
                ubo.data[u_names['rotation']] = (v[0], v[1], v[2], 0)
                self.set_dirty(False)
        else:
            uniform_float(shader, u_names['rotation'], get_local_rot(obj))


    def get_shader_code(self, obj, target_cp_name, id, is_fixed):
        if self.visible==False:
            return ''

        loader = sgd.module_lib.pmod['PMOD_ROT_3D']
        loader.used = True

        u_names = self.get_uniform_names(target_cp_name, id)

        if ubo.enabled:
            rotation = er_v3(get_local_rot(obj).xzy) if is_fixed else ubo.name(u_names['rotation'])+'.xyz'
        else:
            rotation = er_v3(get_local_rot(obj).xzy) if is_fixed else u_names['rotation']
        # rotation = er_v3(get_local_rot(obj).xzy) if is_fixed else ubo.name(u_names['rotation'])+'.xyz'

        # if not is_valid_v3(rotation):
        #     return ''

        code = '{0}({1}, {2});\n'.format(loader.fncname, target_cp_name, rotation)
        return code