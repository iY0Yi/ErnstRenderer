from bpy.types import Operator
from .shadergen import shadergen
from .shadergen.shadergen import *
from .shadergen.shadergen_util import *

class ERNST_OT_ShaderCompiler(Operator):
    bl_idname = 'ernst.recompile_shader'
    bl_label = 'Compile Shader'
    bl_description = 'Compile your scene and GLSL into shader.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        print('recompile_shader()')
        shadergen.process(context)
        self.report({'INFO'}, 'Recompiled successfully.')
        return {'FINISHED'}
