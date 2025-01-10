import platform
import subprocess
import webbrowser
import pathlib
import os
import bpy
from bpy.types import Operator
from mathutils import Matrix, Vector
import math

from ..util import notification
from ..util.util import makeDir
from ..util.notification import Notification
from .shadergen import shadergen_util
from .shadergen.shaderizer import shaderizer_watcher
from .shadergen.shadergen_util import *
from .shadergen import shadergen_data as sgd

class ERNST_OT_OpenTestScene(bpy.types.Operator):
    bl_idname = "ernst.open_test_scene"
    bl_label = "Open Ernst Test Scene"
    bl_description = "Open the Ernst test scene located in the _tests/ernst_test_scene folder"

    def execute(self, context):
        # アドオンのディレクトリを取得
        current_file_path = os.path.realpath(__file__)
        addon_path = os.path.dirname(os.path.dirname(current_file_path))
        blend_file_path = os.path.join(addon_path, "_tests", "ernst_test_scene", "ernst_test_scene.blend")

        # ファイルが存在するか確認
        if os.path.exists(blend_file_path):
            bpy.ops.wm.open_mainfile(filepath=blend_file_path)
            self.report({'INFO'}, "Ernst test scene opened successfully")
        else:
            self.report({'ERROR'}, f"File not found: {blend_file_path}")

        return {'FINISHED'}

class ERNST_OT_FitCameraToView(Operator):
    """Fit Camera to View3D"""
    bl_idname = "ernst.fit_camera_to_view"
    bl_label = "Fit Camera to View3D"
    COMPAT_ENGINES = {'ERNST'}

    def execute(self, context):
        if context.area.type == 'VIEW_3D':
            region = False
            for reg in context.area.regions:
                if(reg.type == 'WINDOW'):
                    region = reg

            if(region):
                context.scene.render.resolution_x = region.width
                context.scene.render.resolution_y = region.height
                # context.space_data.lens = bpy.data.cameras['cam0'].lens
                bpy.data.cameras['cam0'].lens = context.space_data.lens
                is_perspective = context.area.spaces.active.region_3d.is_perspective
                if is_perspective:
                    bpy.data.cameras['cam0'].type = 'PERSP'
                else:
                    bpy.data.cameras['cam0'].type = 'ORTHO'

            context.space_data.region_3d.view_perspective = 'CAMERA'
            context.area.spaces[0].lock_camera = True

            bpy.ops.view3d.zoom_camera_1_to_1()
        return {'FINISHED'}


class ERNST_OT_FreeView(Operator):
    """Free View3D from Camera"""
    bl_idname = "ernst.free_view"
    bl_label = "Free View3D from Camera"
    COMPAT_ENGINES = {'ERNST'}

    def execute(self, context):
        if context.area.type == 'VIEW_3D':
            context.space_data.region_3d.view_perspective = 'ORTHO'
            context.area.spaces[0].lock_camera = False
        return {'FINISHED'}

import os
import time, datetime

def timestamp():
    # convienience function that is available to the user in their calculations
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H_%M')

def fn_prefix(context):
    user_preferences = context.user_preferences
    addon_prefs = user_preferences.addons[__name__].preferences
    return eval(addon_prefs.prefix)

def open_vscode(path):
    os.system('code ' + path)
    # subprocess.Popen(["code", path], shell=True)
    return

class ERNST_OT_OpenTrackInVSCode(Operator):
    bl_idname = "ernst.open_track_in_vscode"
    bl_label = "Open the Track in VSCode"
    COMPAT_ENGINES = {'ERNST'}

    def execute(self, context):
        open_vscode(sgd.dir_trk_root)


class ERNST_OT_SetupMinimumScene(Operator):
    bl_idname = "ernst.setup_minimum_scene"
    bl_label = "Setup a minimum scene"
    COMPAT_ENGINES = {'ERNST'}

    def execute(self, context):

        # Cleanup Objects...
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.data.objects:
            obj.select_set(True)
        bpy.ops.object.delete(use_global=False)

        # Add Minimal Ernst Objects...
        bpy.ops.ernst.add_camera()
        bpy.ops.ernst.add_light_sun()
        bpy.ops.transform.rotate(value=0.785398, orient_axis='Z', orient_type='VIEW', orient_matrix=((1, -0, -0), (-0, -1.34359e-07, 1), (-0, -1, -1.34359e-07)), orient_matrix_type='VIEW',
                                 mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.ernst.add_light_sun()
        bpy.ops.transform.rotate(value=3.14159, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(
            True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.ops.transform.rotate(value=0.785398, orient_axis='Z', orient_type='VIEW', orient_matrix=((1, -0, -0), (-0, -1.34359e-07, 1), (-0, -1, -1.34359e-07)), orient_matrix_type='VIEW',
                                 mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.context.active_object.data.color = [.3, .3, .3]
        bpy.ops.ernst.add_ellipsoid()
        bpy.context.scene.frame_start = 0

        # Setup Views and Camera...
        bpy.data.cameras[0].clip_end = 10000

        for wsp in bpy.data.workspaces:
            for area in wsp.screens[0].areas:
                if area.spaces[0].type == 'VIEW_3D':
                    area.spaces[0].clip_end = 10000

        bpy.context.scene.render.engine = 'ERNST'

        bpy.context.scene.display_settings.display_device = 'None'
        bpy.context.scene.view_settings.view_transform = 'Standard'
        bpy.context.scene.view_settings.look = 'None'
        bpy.context.scene.view_settings.exposure = 0
        bpy.context.scene.view_settings.gamma = 1

        bpy.context.scene.render.engine = 'ERNST'

        outname = 'sketch'+timestamp()
        dir_name = 'C:/Users/atsuh/Dropbox/pworks/sketch/'+outname+'/'
        dir_path = pathlib.Path(make_path_absolute(dir_name))
        makeDir(dir_path)
        bpy.ops.wm.save_mainfile(filepath=os.path.join(dir_path, outname+'.blend'), check_existing=True)
        bpy.data.workspaces["Layout"].ernst.image.code_name = 'None'
        bpy.data.workspaces["Layout"].ernst.buffer_a.code_name = 'None'
        bpy.data.workspaces["Layout"].ernst.buffer_b.code_name = 'None'
        bpy.data.workspaces["Layout"].ernst.buffer_c.code_name = 'None'
        bpy.data.workspaces["Layout"].ernst.buffer_d.code_name = 'None'
        bpy.data.workspaces["Layout"].ernst.image.code_name = 'buf_post_material.frag'
        bpy.data.workspaces["Layout"].ernst.image.ichannel0.buffer_name = 'buffer_a'
        bpy.data.workspaces["Layout"].ernst.buffer_a.code_name = 'buf_renderer.frag'

        open_vscode(sgd.dir_trk_root)

        return {'FINISHED'}



class ERNST_OT_OpenFAQ(Operator):
    bl_idname = "ernst.open_faq"
    bl_label = "Open FAQ page in web browser."
    COMPAT_ENGINES = {'ERNST'}

    def execute(self, context):
        chrome_path = ""
        faq_url = 'https://paper.dropbox.com/doc/--A9Zfi2SlwA~hOLuaYbh2wkH8AQ-3X6zr9pGoUDSh5BLJQPvT'
        plt = platform.system()

        if plt == "Windows":
            print("Open Chrome browser: Windows")
            # Windows
            chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        elif plt == "Linux":
            print("Open Chrome browser: Linux")
            # Linux
            chrome_path = '/usr/bin/google-chrome %s'
        elif plt == "Darwin":
            print("Open Chrome browser: MacOS")
            # MacOS
            chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        else:
            print("Unidentified system")

        webbrowser.get(chrome_path).open(faq_url)

        return {'FINISHED'}


class ERNST_OT_OpenInVSCode(Operator):
    bl_idname = "ernst.open_in_vscode"
    bl_label = "Open file in VSCode"
    COMPAT_ENGINES = {'ERNST'}

    filepath: bpy.props.StringProperty(
        name="File Path",
        description="VSCodeで開きたいファイルのパス"
    )

    def execute(self, context):
        if not self.filepath:
            self.report({'ERROR'}, "ファイルパスが指定されていません。")
            return {'CANCELLED'}

        abs_path = bpy.path.abspath(self.filepath)

        try:
            open_vscode(abs_path)
        except Exception as e:
            self.report({'ERROR'}, f"VSCodeを起動できませんでした:\nエラー: {e}\nパス: {abs_path}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"VSCodeでファイルを開きました: {abs_path}")
        return {'FINISHED'}

class ERNST_OT_FixVersionDiffs(Operator):
    bl_idname = "ernst.fix_version_diffs"
    bl_label = "Fix problems that caused by ErnstRenderer version diffs."
    COMPAT_ENGINES = {'ERNST'}

    def execute(self, context):
        for obj in bpy.data.objects:
            pass

        return {'FINISHED'}

class ERNST_OT_FixParentInverse(Operator):
    bl_idname = "ernst.fix_parent_inverse"
    bl_label = "Fix parent inverse of a bone."
    COMPAT_ENGINES = {'ERNST'}

    def execute(self, context):
        selected_objects = bpy.context.selected_objects

        for empty in selected_objects:
            if empty.type == "EMPTY" and empty.parent and empty.parent_bone:
                armature_name = empty.parent.name
                parent_bone_name = empty.parent_bone
                armature = bpy.data.objects[armature_name]
                parent_bone = armature.pose.bones[parent_bone_name]
                bone_length = parent_bone.length
                empty.matrix_parent_inverse = Matrix.Translation(Vector((0, -bone_length, 0))) @ Matrix.Rotation(math.radians(90), 4, 'X')
            else:
                print("選択中のオブジェクトがEmptyではないか、親が設定されていません。")

        return {'FINISHED'}

class ERNST_OT_FillKeyframes(Operator):
    bl_idname = "ernst.fill_keyframes"
    bl_label = "Fill all frames with temporary keyframes."
    COMPAT_ENGINES = {'ERNST'}

    def execute(self, context):
        scene = context.scene
        frame_start = scene.frame_start
        frame_end = scene.frame_end
        bpy.context.scene.frame_set(frame_start)

        for frame in range(frame_start, frame_end + 1):
            for obj in bpy.context.selected_objects:
                if obj.animation_data is not None:
                    if obj.animation_data.action is not None:
                        if frame not in obj.animation_data.action.frame_range:
                            bpy.context.scene.frame_set(frame)
                            bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")
                else:
                    bpy.ops.anim.keyframe_insert_by_name(type="BUILTIN_KSI_LocRot")
        return {'FINISHED'}


class ERNST_OT_OpenLastRenderResult(Operator):
    bl_idname = "ernst.open_last_render_result"
    bl_label = "Open Last Render Result."
    COMPAT_ENGINES = {'ERNST'}

    def execute(self, context):
        # Modify render settings
        render = bpy.context.scene.render
        leg_resolution_x = render.resolution_x
        leg_resolution_y = render.resolution_y
        leg_resolution_percentage = render.resolution_percentage
        render.resolution_x = 2560
        render.resolution_y = 1440
        render.resolution_percentage = 100

        # Modify preferences (to guaranty new window)
        prefs = bpy.context.preferences
        prefs.view.render_display_type = "WINDOW"

        try:
            # Call image editor window
            bpy.ops.render.view_show("INVOKE_DEFAULT")
            # Change area type
            image =bpy.data.images.load(f"{sgd.dir_working}/render/001.png", check_existing=True)
            area = bpy.data.window_managers[0].windows[-1].screen.areas[0]
            area.type = "IMAGE_EDITOR"
            area.spaces[0].image = image
            area.spaces[0].image.reload()
        except:
            notification.add(Notification('Error: We cant open any window from python...', 5, notification.ERROR))

        render.resolution_x = leg_resolution_x
        render.resolution_y = leg_resolution_y
        render.resolution_percentage = leg_resolution_percentage
        return {'FINISHED'}
