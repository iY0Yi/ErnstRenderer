import string
import bpy

from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen import shadergen_ubo as ubo
from ...bl_ot.shadergen.shaderizer import shaderizer_watcher
from ...bl_ot.shadergen.shaderizer.shaderizer_object import *
from ...bl_ot.bl_ot_pmodifier import ERNST_OT_MakeControlPoint
from ...bl_mt.bl_mt_sdf3d import ERNST_MT_PreCode, ERNST_MT_PostCode
from ...bl_mt.bl_mt_pmodifier import ERNST_MT_PModifiers
from ...bl_ot.shadergen.shaderizer.shaderizer_object import is_fixed

class ERNST_PG_Primitive_Abstract():
    visible: bpy.props.BoolProperty(default = True, update=shaderizer_watcher.check)
    expanded : bpy.props.BoolProperty(default=True)
    hide            : bpy.props.BoolProperty(default=False, update=shaderizer_watcher.check)

    need_code_pre   : bpy.props.BoolProperty(default=False, update=shaderizer_watcher.check)
    code_pre        : bpy.props.StringProperty(default = '')#, update=shaderizer_watcher.check)
    need_code_post  : bpy.props.BoolProperty(default=False, update=shaderizer_watcher.check)
    code_post       : bpy.props.StringProperty(default = '')#, update=shaderizer_watcher.check)
    code_name       : bpy.props.StringProperty(default = '')#, update=shaderizer_watcher.check)

    def get_code_domain(self):
        obj = self.id_data
        if obj.parent!=None and obj.parent.ernst.type == 'CONTROL_POINT':
            return er_var(obj.parent.name)
        else:
            return 'p'

    def get_code_position(self, u_name):
        obj = self.id_data
        if is_fixed(obj):
            return er_v3(get_local_pos(obj).xzy)
        else:
            if ubo.enabled and not 'ubo' in u_name:
                return f'{ubo.name(u_name)}.xyz'
            else:
                return u_name

    def get_code_rotation(self, u_name):
        obj = self.id_data
        if is_fixed(obj):
            return er_v3(get_local_rot(obj).xzy)
        else:
            if ubo.enabled and not 'ubo' in u_name:
                return f'{ubo.name(u_name)}.xyz'
            else:
                return u_name

    def get_code_scale(self, u_name):
        obj = self.id_data
        if is_fixed(obj):
            return er_f(get_local_scale(obj).x)
        else:
            if ubo.enabled and not 'ubo' in u_name:
                return f'{ubo.name(u_name)}.x'
            else:
                return u_name

    def get_code_inline(self, obj, code_name):
        code = ''
        if code_name != '':
            header = f'\n/*--- {code_name} ---*/\n'
            footer = '\n\n'
            code = compile_uber_template(obj, None, 'inline', '', code_name, header, footer)
        return code

    def get_code_inline_pre(self):
        if self.need_code_pre:
            return self.get_code_inline(self.id_data, self.code_pre)
        else:
            return ''

    def get_code_inline_post(self):
        if self.need_code_post:
            return self.get_code_inline(self.id_data, self.code_post)
        else:
            return ''

    def draw_mini_header(self, layout):
        obj = self.id_data
        layout_row = layout.row()
        layout_row.prop(obj, "name", icon = self.icon, text="", emboss=True)
        layout_row.prop(self, "hide",
            icon="HIDE_ON" if self.hide else "HIDE_OFF",
            icon_only=True, emboss=False
        )

    def draw_property_box(self, box):
        box_col = box.column(align=False)
        box_col.active = not self.hide

        col = box_col.box()
        row = col.row()
        row.alignment="LEFT"
        row.prop(self, "expanded",
            icon="TRIA_DOWN" if self.expanded else "TRIA_RIGHT",
            text='Modifiers', emboss=False
        )
        return col

    def draw_parent(self, context, box_col):
        obj = self.id_data
        if obj.parent != None:
            box_col.prop_search(obj, 'parent', context.scene, 'objects', text='Parent', icon ='OBJECT_ORIGIN')
        # else:
        #     box_col.operator(ERNST_OT_MakeControlPoint.bl_idname, text = 'Create Parent CP', icon='DECORATE_LINKED')

    def draw_pmods(self, box):
        obj = self.id_data
        box.menu(ERNST_MT_PModifiers.bl_idname, text='Add PModifier')
        if len(obj.ernst.pmods.pmod)>0:
            obj.ernst.pmods.draw_gui(box, obj)

    def draw_inlines(self, col):
        row = col.row()
        row.prop(self, "need_code_pre", text='Inline (Pre):')
        row.active = self.need_code_pre
        text = self.code_pre if self.code_pre != '' else 'undefined'
        row.menu(ERNST_MT_PreCode.bl_idname, text=text, icon='TEXT')

        row = col.row()
        row.prop(self, "need_code_post", text='Inline (Post):')
        row.active = self.need_code_post
        text = self.code_post if self.code_post != '' else 'undefined'
        row.menu(ERNST_MT_PostCode.bl_idname, text=text, icon='TEXT')
