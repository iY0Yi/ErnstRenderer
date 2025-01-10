import os
import subprocess
import bpy
from bpy.types import PropertyGroup

from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen.shaderizer import shaderizer_watcher
from ...bl_ot.shadergen.shaderizer.shaderizer_object import *
from ...util.util import *


def open_in_vscode(filepath):
    """
    指定されたファイルを VSCode で開く。
    既に VSCode が起動中であっても問題なく動作する。
    """
    subprocess.run(["code", filepath])

cached_items = []
def enum_items(self, context):
    return dynamic_enum_files('uber_scripts/pmod', cached_items)

class ERNST_PG_PModifier_UberScript(PropertyGroup):
    name: bpy.props.StringProperty(default = 'UberScript')
    icon: bpy.props.StringProperty(default = 'TEXT')
    visible: bpy.props.BoolProperty(default = True, update=shaderizer_watcher.check)
    expanded : bpy.props.BoolProperty(default=True)

    # code_name: bpy.props.EnumProperty(
    #         name="",
    #         description="pModifier with code",
    #         items=enum_items,
    #            update=shaderizer_watcher.check
    #     )

    file_name: bpy.props.StringProperty(
        name="",
        description="Choose a file",
        default="",
        maxlen=1024,
        subtype='FILE_PATH',
        update=shaderizer_watcher.check
    )

    def get_uniform_names(self, target_cp_name, id):
        return ''

    def draw_gui(self, layout, obj, id, active):
        pmod_box = layout.box()
        pmod_box.active = active
        row = pmod_box.row(align=True)

        # col = row.column(align=True)
        # col.prop(self, "code_name", expand=False, icon='TEXT')
        col = row.column(align=True)
        col.prop(self, "file_name", expand=False, icon='NONE')
        col = row.column(align=True)
        op = col.operator('ernst.open_in_vscode', text='', icon='GREASEPENCIL')
        op.filepath = self.file_name

    def get_uniform_dec_code(self, target_cp_name, id):
        return ''

    def update_uniforms(self, shader, target_cp_name, id):
        pass

    def get_shader_code(self, obj, target_cp_name, id, is_fixed):
        if self.visible==False:
            return ''

        # if self.code_name == 'undefined':
        #     return ''

        if self.file_name == '':
            return ''

        file_name = os.path.basename(self.file_name)

        # self.file_name = '//track/uber_scripts/pmod/'+self.code_name

        header = f'\n/*--- {file_name} ---*/\n{{\n'
        footer = '\n}\n'
        return compile_uber_template(obj, target_cp_name, 'pmod', '', file_name, header, footer)
