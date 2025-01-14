import bpy
from bpy.types import PropertyGroup

from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen.shaderizer import shaderizer_watcher
from ...bl_ot.shadergen.shaderizer.shaderizer_object import *
from ...util.util import *

class ERNST_PG_PModifier_IKPole(PropertyGroup):
    name: bpy.props.StringProperty(default = 'IKPole')
    icon: bpy.props.StringProperty(default = 'CONSTRAINT_BONE')
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
        return ''