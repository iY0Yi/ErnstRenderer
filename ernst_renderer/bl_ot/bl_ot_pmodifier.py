import bpy
from bpy.types import Operator

from .shadergen.shaderizer import shaderizer_watcher


class PMODOperatorBase:
    bl_label = 'method'
    bl_description = 'Add PModifier.'
    bl_options = {'REGISTER', 'UNDO'}

    pmod_name = ''

    def execute(self, context):
        context.view_layer.objects.active.ernst.pmods.add(self.pmod_name)
        shaderizer_watcher.check(self, context)
        return {'FINISHED'}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_Translation(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_translation'
    pmod_name = 'Translation'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_Rotation(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_rotation'
    pmod_name = 'Rotation'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_TRVsTranslation(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_trvs_translation'
    pmod_name = 'TRVsTranslation'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_TRVsRotation(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_trvs_rotation'
    pmod_name = 'TRVsRotation'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_Mirror(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_mirror'
    pmod_name = 'Mirror'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_MirrorTranslation(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_mirror_translation'
    pmod_name = 'MirrorTranslation'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_MirrorRotation(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_mirror_rotation'
    pmod_name = 'MirrorRotation'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_MirrorScale(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_mirror_scale'
    pmod_name = 'MirrorScale'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_Twist(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_twist'
    pmod_name = 'Twist'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_Spin(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_spin'
    pmod_name = 'Spin'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_Elongate(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_elongate'
    pmod_name = 'Elongate'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_Bend(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_bend'
    pmod_name = 'Bend'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_Balloon(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_balloon'
    pmod_name = 'Balloon'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_Shear(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_shear'
    pmod_name = 'Shear'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_Taper(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_taper'
    pmod_name = 'Taper'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_Round(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_round'
    pmod_name = 'Round'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_RepLimited(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_rep_limited'
    pmod_name = 'RepLimited'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_RepPolar(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_rep_polar'
    pmod_name = 'RepPolar'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_IKArmature(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_ik_armature'
    pmod_name = 'IKArmature'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_IKBoneJoint(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_ik_bone_joint'
    pmod_name = 'IKBoneJoint'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_IKBoneTarget(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_ik_bone_target'
    pmod_name = 'IKBoneTarget'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_IKPole(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_ik_pole'
    pmod_name = 'IKPole'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_PMOD_UberScript(PMODOperatorBase, Operator):
    bl_idname = 'ernst.add_pmod_by_code'
    pmod_name = 'UberScript'


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_MakeControlPoint(Operator):
    bl_idname = "ernst.make_control_point"
    bl_label = "Make CP for selected objects."
    COMPAT_ENGINES = {'ERNST'}

    def execute(self, context):
        children = []
        for obj in context.selected_objects:
            children.append(obj)

        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.ernst.add_control_point()
        parent = context.selected_objects[0]

        for child in children:
            child.select_set(True)
        parent.select_set(True)

        context.view_layer.objects.active = parent
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
        bpy.ops.ernst.set_parent()

        for child in children:
            child.select_set(False)

        return {'FINISHED'}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_SetParent(Operator):
    '''
    Parenting(Keep Transform), but without parent inverse.
    '''
    bl_idname = 'ernst.set_parent'
    bl_label = 'SDF(Keep Transform)'
    bl_options = {'REGISTER', 'UNDO'}
    COMPAT_ENGINES = {'ERNST'}

    def execute(self, context):
        parent = bpy.context.active_object

        parent.select_set(False)
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        parent.select_set(True)

        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)

        for obj in bpy.context.selected_objects:
            if obj.name != parent.name:
                obj.matrix_basis = obj.matrix_parent_inverse @ obj.matrix_basis
                obj.matrix_parent_inverse.identity()

        shaderizer_watcher.check(self, context)
        return {'FINISHED'}

