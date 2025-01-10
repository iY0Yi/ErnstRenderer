import bpy
from bpy.types import Operator

class ERNST_OT_InsertLocRotKeyframe(Operator):
    bl_idname = "ernst.insert_loc_rot_keyframe"
    bl_label = "Insert Loc Rot Keyframe. (Mainly used for TRV modifier)"
    COMPAT_ENGINES = {'ERNST'}

    def execute(self, context):
        bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")
        return {'FINISHED'}

class ERNST_OT_OpenFileBrowser(Operator):
    bl_idname = "ernst.open_file_browser"
    bl_label = "Open File Browser"
    COMPAT_ENGINES = {'ERNST'}
    bl_options = {'REGISTER'}

    file_path: bpy.props.StringProperty(
        name="File Path",
        description="The path to open in the file browser",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
    )

    def execute(self, context):
        # ファイルブラウザを開く
        bpy.ops.wm.path_open(filepath=self.file_path)
        return {'FINISHED'}