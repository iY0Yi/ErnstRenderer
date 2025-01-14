import bpy
from bpy.types import AddonPreferences, Operator
from bpy.props import StringProperty


# アドオンのPreferencesクラス
class ERNSTAddonPreferences(AddonPreferences):
    bl_idname = "ernst_renderer"

    # アドオンの設定用プロパティ
    dir_sketch: StringProperty(
        name="Sketch Directory",
        description="Directory for saving sketches",
        subtype='DIR_PATH',
        default=""
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "dir_sketch")
