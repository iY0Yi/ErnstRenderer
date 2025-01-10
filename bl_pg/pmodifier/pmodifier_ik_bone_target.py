import bpy
from bpy.types import PropertyGroup

from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen.shaderizer import shaderizer_watcher
from ...bl_ot.shadergen.shaderizer.shaderizer_object import *
from ...util.util import *

class ERNST_PG_PModifier_IKBoneTarget(PropertyGroup):
    name: bpy.props.StringProperty(default = 'IKBoneTarget')
    icon: bpy.props.StringProperty(default = 'BONE_DATA')
    visible: bpy.props.BoolProperty(default = True, update=shaderizer_watcher.check)
    expanded : bpy.props.BoolProperty(default=True)

    object_root: bpy.props.PointerProperty(
        name="IK Armature",
        description="IK Armature",
        type=bpy.types.Object,
        poll=is_armature_object,
        update=shaderizer_watcher.check
    )

    def get_uniform_names(self, target_cp_name, id):
        u_names = {}
        return u_names

    def draw_gui(self, layout, obj, id, active):
        pmod_box = layout.box()
        row = pmod_box.row()
        row.prop(self, "object_root", expand=False, icon='CON_KINEMATIC')

    def get_uniform_dec_code(self, target_cp_name, id):
        return ''

    def update_uniforms(self, shader, target_cp_name, id):
        return

    def get_shader_code(self, obj, target_cp_name, id, is_fixed):
        if self.visible==False:
            return ''

        loader = sgd.module_lib.pmod['PMOD_ROT_2D']
        loader.used = True

        var_ika = f'ika_{er_var(self.object_root.name)}'
        var_ika_base = f'ika_{er_var(self.object_root.name)}_base'

        code = f'''
        // rig target
        {target_cp_name}+={var_ika}.bon[2].tail;
        '''
        return code