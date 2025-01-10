import bpy
from bpy.types import Menu
from ..bl_ot.bl_ot_pmodifier import *

class ERNST_MT_PModifiers(Menu):
    bl_idname = 'ERNST_MT_PModifiers'
    bl_label = 'Add PModifier...'
    bl_description = 'Add PModifier.'

    def draw(self, context):
        layout = self.layout
        layout.operator(ERNST_OT_PMOD_Translation.bl_idname, text='Translation', icon='EMPTY_ARROWS')
        layout.operator(ERNST_OT_PMOD_Rotation.bl_idname, text='Rotation', icon='EMPTY_ARROWS')
        layout.operator(ERNST_OT_PMOD_TRVsTranslation.bl_idname, text='TRVsTranslation', icon='EMPTY_ARROWS')
        layout.operator(ERNST_OT_PMOD_TRVsRotation.bl_idname, text='TRVsRotation', icon='EMPTY_ARROWS')
        layout.operator(ERNST_OT_PMOD_Mirror.bl_idname, text='Mirror', icon='MOD_MIRROR')
        layout.operator(ERNST_OT_PMOD_MirrorTranslation.bl_idname, text='MirrorTranslation', icon='EMPTY_ARROWS')
        layout.operator(ERNST_OT_PMOD_MirrorRotation.bl_idname, text='MirrorRotation', icon='EMPTY_ARROWS')
        layout.operator(ERNST_OT_PMOD_MirrorScale.bl_idname, text='MirrorScale', icon='EMPTY_ARROWS')
        layout.operator(ERNST_OT_PMOD_Twist.bl_idname, text='Twist', icon='MOD_SCREW')
        layout.operator(ERNST_OT_PMOD_Spin.bl_idname, text='Spin', icon='MOD_SCREW')
        layout.operator(ERNST_OT_PMOD_Bend.bl_idname, text='Bend', icon='MOD_SIMPLEDEFORM')
        layout.operator(ERNST_OT_PMOD_Balloon.bl_idname, text='Balloon', icon='NODE_MATERIAL')
        layout.operator(ERNST_OT_PMOD_Shear.bl_idname, text='Shear', icon='OUTLINER_OB_LATTICE')
        layout.operator(ERNST_OT_PMOD_Taper.bl_idname, text='Taper', icon='MESH_CONE')
        layout.operator(ERNST_OT_PMOD_Round.bl_idname, text='Round', icon='CON_SHRINKWRAP')
        layout.operator(ERNST_OT_PMOD_Elongate.bl_idname, text='Elongate', icon='STICKY_UVS_VERT')
        layout.operator(ERNST_OT_PMOD_RepLimited.bl_idname, text='RepLimited', icon='MOD_ARRAY')
        layout.operator(ERNST_OT_PMOD_RepPolar.bl_idname, text='RepPolar', icon='MOD_ARRAY')
        layout.operator(ERNST_OT_PMOD_IKArmature.bl_idname, text='IKArmature', icon='CON_KINEMATIC')
        layout.operator(ERNST_OT_PMOD_IKBoneJoint.bl_idname, text='IKBoneJoint', icon='BONE_DATA')
        layout.operator(ERNST_OT_PMOD_IKBoneTarget.bl_idname, text='IKBoneTarget', icon='BONE_DATA')
        layout.operator(ERNST_OT_PMOD_IKPole.bl_idname, text='IKPole', icon='CONSTRAINT_BONE')
        layout.operator(ERNST_OT_PMOD_UberScript.bl_idname, text='UberScript', icon='TEXT')
