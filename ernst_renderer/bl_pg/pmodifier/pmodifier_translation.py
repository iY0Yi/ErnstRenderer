import bpy
from mathutils import Vector
import numpy as np
from bpy.types import PropertyGroup

from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen.shaderizer import shaderizer_watcher
from ...bl_ot.shadergen.shaderizer.shaderizer_object import *
from ...bl_ot.shadergen import shadergen_ubo as ubo

is_dirty = {}

class ERNST_PG_PModifier_Translation(PropertyGroup):
    name: bpy.props.StringProperty(default = 'Translation', update=shaderizer_watcher.check)
    icon: bpy.props.StringProperty(default = 'EMPTY_ARROWS', update=shaderizer_watcher.check)
    visible: bpy.props.BoolProperty(default = True, update=shaderizer_watcher.check)
    expanded : bpy.props.BoolProperty(default=True)

    def get_uniform_names(self, target_cp_name, id):
        obj = self.id_data
        u_names = {}
        u_names['position'] = f'{er_var(obj.name)}_position'
        return u_names

    def draw_gui(self, layout, obj, id, active):
        pmod_box = layout.box()
        pmod_box.active = False
        row = pmod_box.row()
        obj_props = bpy.data.objects[obj.name]
        row.label(text='X: {0:.3f}'.format(obj_props.location.x))
        row.label(text='Y: {0:.3f}'.format(obj_props.location.y))
        row.label(text='Z: {0:.3f}'.format(obj_props.location.z))

    def get_uniform_dec_code(self, target_cp_name, id):
        if self.visible==False:
            return ''

        u_names = self.get_uniform_names(target_cp_name, id)

        if ubo.enabled:
            code_u_names = ''
            ubo.add_vec4(u_names["position"])
        else:
            code_u_names = f'uniform vec3 {u_names["position"]};\n'

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
                v = get_local_pos(obj)
                ubo.data[u_names['position']] = (v[0], v[1], v[2], 0)
                self.set_dirty(False)
        else:
            uniform_float(shader, u_names['position'], get_local_pos(obj))

    def get_shader_code(self, obj, target_cp_name, id, is_fixed):
        if self.visible==False:
            return ''

        u_names = self.get_uniform_names(target_cp_name, id)

        if ubo.enabled:
            position = er_v3(get_local_pos(obj).xzy) if is_fixed else ubo.name(u_names['position'])+'.xyz'
        else:
            position = er_v3(get_local_pos(obj).xzy) if is_fixed else u_names['position']

        # if not is_valid_v3(position):
        #     return ''

        code = f'{target_cp_name}.xyz += {position};\n'

        return code
