from bpy.props import *
from bpy.types import PropertyGroup

from ..bl_ot.shadergen.shaderizer import shaderizer_watcher

def force_dirty(self, context):
    obj = self.id_data
    obj.ernst.shader_proxy.props.set_dirty(True)

class ERNST_PG_UberValueProperties(PropertyGroup):
    type      : EnumProperty(
                                name="Parameter Type",
                                description="Choose value type Number/Code",
                                default='Number',
                                items=[
                                    ('Number', "Number", "Pass the number as parameter."),
                                    ('Code', "Code", "Pass the code as parameter.")
                                ], update=shaderizer_watcher.check)
    value_code : StringProperty(default = '', update=shaderizer_watcher.check)

    value_file_name: StringProperty(
        name="",
        description="Choose a file",
        default="",
        maxlen=1024,
        subtype='FILE_PATH',
        update=shaderizer_watcher.check
    )

    value_num : FloatProperty(name = '', default = 0.0001, update=force_dirty)
