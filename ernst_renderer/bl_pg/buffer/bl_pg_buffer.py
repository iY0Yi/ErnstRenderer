import bpy
from bpy.types import PropertyGroup
from .bl_pg_texture import ERNST_PG_Texture
from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen.shaderizer import shaderizer_watcher
from ...bl_ot.shadergen.shaderizer.shaderizer_object import *
from .buffer_base import BufferBase

from ...bl_ot.shadergen import shadergen_data as sgd
from ...util.util import *

def update_code_name(self, context):
    if self.code_name:
        self.code_name = bpy.path.relpath(self.code_name)
        shaderizer_watcher.check

class ERNST_PG_Buffer(PropertyGroup):
    name: bpy.props.StringProperty(default = 'Image')
    expanded: bpy.props.BoolProperty(default = False)
    ichannel0: bpy.props.PointerProperty(type=ERNST_PG_Texture)
    ichannel1: bpy.props.PointerProperty(type=ERNST_PG_Texture)
    ichannel2: bpy.props.PointerProperty(type=ERNST_PG_Texture)
    ichannel3: bpy.props.PointerProperty(type=ERNST_PG_Texture)
    buffer = None

    def __init__(self):
        super.__init__()

    def get_buffer_name(self):
        return self.name.strip().lower()

    code_name: bpy.props.StringProperty(
        name="",
        description="Choose a file",
        default="",
        maxlen=1024,
        subtype='FILE_PATH',
        update=update_code_name
    )

    def init_buffer(self, name):
        print('init_buffer(): ', name)
        self.name = name
        buf_name = name.strip().lower()
        sgd.buffers[buf_name] = BufferBase(buf_name)

    def compile(self, context):
        print(self.code_name, 'compile()')
        if self.code_name != '':
            buf_name = self.get_buffer_name()
            sgd.buffers[buf_name].compile(context, bpy.path.abspath(self.code_name))
            sgd.buffers[buf_name].ichannel0 = self.ichannel0
            sgd.buffers[buf_name].ichannel1 = self.ichannel1
            sgd.buffers[buf_name].ichannel2 = self.ichannel2
            sgd.buffers[buf_name].ichannel3 = self.ichannel3

    def update_uniforms(self, context, need_UBO):
        sgd.buffers[self.get_buffer_name()].update_uniforms(context, need_UBO)

    def render(self):
        sgd.buffers[self.get_buffer_name()].render()

    def get_texture(self):
        return sgd.buffers[self.get_buffer_name()].offscreen.texture_color

    def set_texture_interpolation(self, interpolation):
        sgd.buffers[self.get_buffer_name()].interpolation = interpolation

    def set_texture_wrap(self, wrap):
        sgd.buffers[self.get_buffer_name()].wrap = wrap

    def draw_property_box(self, box):
        row = box.row(align=True)
        is_active = self.code_name != ''
        row.active = is_active
        row.alignment = 'LEFT'
        col = row.column()
        col.prop(self, "expanded",
            icon="TRIA_DOWN" if self.expanded else "TRIA_RIGHT",
            text=self.name, emboss=False
        )
        col = row.column()
        col.scale_x = 1.5
        col.prop(self, "code_name")
        return col

    def draw_gui(self, context, box):
        col = self.draw_property_box(box)
        if self.expanded:
            col = box.column(align = True)
            self.ichannel0.draw_gui(col, 'iChannel0')
            self.ichannel1.draw_gui(col, 'iChannel1')
            self.ichannel2.draw_gui(col, 'iChannel2')
            self.ichannel3.draw_gui(col, 'iChannel3')
