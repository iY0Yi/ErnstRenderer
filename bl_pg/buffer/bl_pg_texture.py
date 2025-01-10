import bpy
from bpy.types import PropertyGroup
from bgl import glActiveTexture
from bgl import glBindTexture
from bgl import glBindTexture
from bgl import GL_TEXTURE0
from bgl import GL_TEXTURE_2D
from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen.shaderizer import shaderizer_watcher
from ...bl_ot.shadergen.shaderizer.shaderizer_object import *

class ERNST_PG_Texture(PropertyGroup):
    buffer_name: bpy.props.EnumProperty(
        name = '',
        default = 'none',
        items = (
            ("none", "None", "Texture"),
            ("buffer_a", "BufferA", "Texture"),
            ("buffer_b", "BufferB", "Texture"),
            ("buffer_c", "BufferC", "Texture"),
            ("buffer_d", "BufferD", "Texture")
        ))

    interpolation: bpy.props.EnumProperty(
        name = '',
        default = 'linear',
        items = (
            ("linear", "Linear", "Interpolation"),
            ("nearest", "Nearest", "Interpolation"),
            ("mipmap", "Mipmap", "Interpolation")
        ))

    wrap: bpy.props.EnumProperty(
        name = '',
        default = 'clamp',
        items = (
            ("clamp", "Clamp", "Wrap"),
            ("wrap", "Wrap", "Wrap")
        ))

    def draw_gui(self, layout, name):
        is_active = self.buffer_name != 'none'
        box = layout.box()
        col = box.column(align = True)
        row = col.row(align = True)
        row.active = is_active
        row.label(text=name)
        row.prop(self, 'buffer_name', text='')
        row = col.row(align = True)
        row.active = is_active
        row.prop(self, 'interpolation', text='')
        row.prop(self, 'wrap', text='')

    def update_uniform(self, context, shader, u_name):
        if self.buffer_name == 'none':
            return

        buffer = None
        if self.buffer_name == 'buffer_a':
            buffer = context.workspace.ernst.buffer_a
        if self.buffer_name == 'buffer_b':
            buffer = context.workspace.ernst.buffer_b
        if self.buffer_name == 'buffer_c':
            buffer = context.workspace.ernst.buffer_c
        if self.buffer_name == 'buffer_d':
            buffer = context.workspace.ernst.buffer_d

        channel = buffer.get_texture()

        glActiveTexture(GL_TEXTURE0+channel)
        buffer.set_texture_interpolation(self.interpolation)
        buffer.set_texture_wrap(self.wrap)
        glBindTexture(GL_TEXTURE_2D, channel)
        uniform_int(shader, u_name, channel)
