import bpy
from bpy.types import Panel

from ..bl_ot.bl_ot_helper import *


class ERNST_PT_Helpers(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_label = 'Helpers'
    bl_category = 'Ernst'
    COMPAT_ENGINES = {'ERNST'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = False

        col = layout.column(align=False)

        # row = col.row(align = True)
        # row.operator(ERNST_OT_FixVersionDiffs.bl_idname, text = 'Fix Version Diffs', icon='SHADERFX')

        row = col.row(align = True)
        row.operator(ERNST_OT_SetupMinimumScene.bl_idname, text = 'Setup Scene', icon='SCENE_DATA')

        row = col.row(align = True)
        row.operator(ERNST_OT_FitCameraToView.bl_idname, text = 'Fit Camera', icon='OUTLINER_OB_CAMERA')

        row = col.row(align = True)
        row.operator(ERNST_OT_FillKeyframes.bl_idname, text = 'Fill Keyframes', icon='DECORATE_KEYFRAME')

        row = col.row(align = True)
        row.operator(ERNST_OT_FixParentInverse.bl_idname, text = 'Fix Parent Inverse', icon='BONE_DATA')

        row = col.row(align = True)
        row.operator(ERNST_OT_OpenLastRenderResult.bl_idname, text = 'Last Render', icon='IMAGE_RGB')

        # row = col.row(align = True)
        # row.operator(ERNST_OT_OpenFAQ.bl_idname, text = 'FAQ', icon='HELP')

        row = col.row(align = True)
        row.operator(ERNST_OT_OpenTestScene.bl_idname, text = 'Test Scene', icon='SCRIPTPLUGINS')

        row = col.row(align = True)
        row.operator(ERNST_OT_OpenTrackInVSCode.bl_idname, text = 'VS Code', icon='TEXT')
