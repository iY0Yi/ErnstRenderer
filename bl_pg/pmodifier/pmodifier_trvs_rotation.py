import bpy
from bpy.types import PropertyGroup
from ...bl_ot.shadergen.shaderizer import shaderizer_trvs
from ...bl_ot.shadergen import shadergen_data as sgd
from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen.shaderizer import shaderizer_watcher
from ...bl_ot.shadergen.shaderizer.shaderizer_object import *
from ...util.map import Map

is_dirty = {}

class ERNST_PG_PModifier_TRVsRotation(PropertyGroup):
    name: bpy.props.StringProperty(default = 'TRVsRotation', update=shaderizer_watcher.check)
    icon: bpy.props.StringProperty(default = 'EMPTY_ARROWS', update=shaderizer_watcher.check)
    visible: bpy.props.BoolProperty(default = True, update=shaderizer_watcher.check)
    expanded : bpy.props.BoolProperty(default=True)

    def get_uniform_names(self, target_cp_name, id):
        obj = self.id_data
        u_names = {}
        u_names['rotation'] = f'{er_var(obj.name)}_trv_rotation'
        return u_names

    def draw_gui(self, layout, obj, id, active):
        pmod_box = layout.box()
        pmod_box.active = False
        row = pmod_box.row()

        is_editing = bpy.context.scene.ernst.enable_edit_trvs
        if is_editing:
            obj_props = bpy.data.objects[obj.name]
            row.label(text='X: {0:.3f}'.format(obj_props.rotation_euler[0]))
            row.label(text='Y: {0:.3f}'.format(obj_props.rotation_euler[1]))
            row.label(text='Z: {0:.3f}'.format(obj_props.rotation_euler[2]))
        else:
            row.label(text='TRV name: {0}'.format(shaderizer_trvs.get_TRV_rot_name(obj)))

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

        is_editing = bpy.context.scene.ernst.enable_edit_trvs

        if is_editing:
            u_names = self.get_uniform_names(target_cp_name, id)

            if ubo.enabled:
                rotation = ubo.name(u_names['rotation'])+'.xyz'
            else:
                rotation = u_names['rotation']
            return '{0}({1}, {2});\n'.format(loader.fncname, target_cp_name, rotation)
        else:
            shaderizer_trvs.addTRVobj(obj, 'rot')
            key_code = shaderizer_trvs.get_code(obj, 'rot')
            return f'{loader.fncname}({target_cp_name}, {key_code});\n'
