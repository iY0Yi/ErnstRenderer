import bpy
from bpy.types import PropertyGroup

from ..abstract_primitive import ERNST_PG_Primitive_Abstract
from ....bl_ot.shadergen.shadergen_util import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import is_renderable
from ....bl_mt.bl_mt_pmodifier import ERNST_MT_PModifiers
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_PG_ControlPoint(PropertyGroup, ERNST_PG_Primitive_Abstract):
    icon: bpy.props.StringProperty(default = 'OBJECT_ORIGIN')
    calc_order: bpy.props.IntProperty(name = 'calc order', min = -999, max = 999, default = 0)

    def draw_gui(self, context, layout):
        obj = self.id_data
        self.draw_mini_header(layout)
        box = self.draw_property_box(layout)

        if self.expanded:
            self.draw_parent(context, box)
            self.draw_pmods(box)
            self.draw_inlines(box)

    def get_uniform_dec_code(self):
        obj = self.id_data
        if not is_renderable(obj):
           return ''
        return obj.ernst.pmods.get_uniform_dec_code(obj)

    def update_uniforms(self, shader):
        obj = self.id_data
        if not is_renderable(obj):
           return
        obj.ernst.pmods.update_uniforms(shader, obj)

    def get_shader_code(self, rendables):
        obj = self.id_data
        if not is_renderable(obj):
           return ''
        domain = self.get_code_domain()

        code = f'vec3 {er_var(obj.name)} = {domain};\n'
        code += obj.ernst.pmods.get_shader_code(obj)

        code_inline_pre = self.get_code_inline_pre()
        code_inline_post = self.get_code_inline_post()

        return code_inline_pre + code + code_inline_post
