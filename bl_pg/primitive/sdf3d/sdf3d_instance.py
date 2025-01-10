import bpy
from bpy.types import PropertyGroup

from ..abstract_sdf import ERNST_PG_SDF_Abstract
from ....bl_ot.shadergen.shadergen_util import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import *
from ....bl_ot.shadergen.shaderizer.shaderizer_object import is_renderable

from ....bl_ot.shadergen import shadergen_ubo as ubo

is_dirty = {}

class ERNST_PG_SDF3D_Instance(PropertyGroup, ERNST_PG_SDF_Abstract):
    icon: bpy.props.StringProperty(default = 'OUTLINER_OB_GROUP_INSTANCE')
    use_cache: bpy.props.BoolProperty(default=False)
    material: bpy.props.PointerProperty(
        name="Material",
        type=bpy.types.Material,
        description="Custom material to override the collection's objects materials",
    )

    def get_uniform_names(self):
        obj = self.id_data
        u_names = {}
        u_names['scale'] = f'{er_var(obj.name)}_scale'
        self.get_round_uniform_name(u_names)
        self.get_shell_uniform_name(u_names)
        self.get_boolean_uniform_names(u_names)
        return u_names

    def draw_gui(self, context, layout):
        self.draw_mini_header(layout)

        obj = self.id_data
        col = layout.column(align = True)
        collection = obj.instance_collection.ernst
        col.prop(obj, 'instance_collection', text='')
        collection.draw_gui(context, col)

        # print('collection.enable_cache?', collection.enable_cache)
        if collection.enable_cache:
            col.prop(self, 'use_cache', text='Use Cached')

        box = self.draw_property_box(layout)
        if self.expanded:
            self.draw_parent(context, box)
            self.draw_pmods(box)

            row = box.row(align=True)
            row.prop(self, 'round_active', text='Round:')
            row.active = self.round_active
            row.prop(self, 'round_radius', text='')

            row = box.row(align=True)
            row.prop(self, 'shell_active', text='Shell:')
            row.active = self.shell_active
            row.prop(self, 'shell_tickness', text='')

            self.draw_inlines(box)

        self.draw_boolean(layout)

        layout.prop(self, "material", text='')

    def get_uniform_dec_code(self):
        obj = self.id_data
        if not is_renderable(obj):
           return ''
        u_names = self.get_uniform_names()
        if ubo.enabled:
            code_u_names  = ''
            ubo.add_vec4(u_names["scale"])
            self.add_ubo_shell()
            self.add_ubo_round()
            self.add_ubo_boolean()
        else:
            code_u_names  = f'uniform float {u_names["scale"]};\n'
            code_u_names += self.get_shell_uniform_dec_code()
            code_u_names += self.get_round_uniform_dec_code()
            code_u_names += self.get_boolean_uniform_dec_code()
        code_u_names += obj.ernst.pmods.get_uniform_dec_code(obj)
        return code_u_names

    def set_dirty(self, bool):
        obj = self.id_data
        is_dirty[obj.name] = bool

    def update_uniforms(self, shader):
        obj = self.id_data
        if not is_renderable(obj):
           return
        u_names = self.get_uniform_names()
        if ubo.enabled:
            if not obj.name in is_dirty:
                self.set_dirty(True)
            if is_dirty[obj.name] or ubo.is_dirty:
                ubo.data[u_names['scale']] = (get_local_scale(obj).x, 0,0,0)
                self.update_ubo_shell()
                self.update_ubo_round()
                self.update_ubo_boolean()
                self.set_dirty(False)
        else:
            uniform_float(shader, u_names['scale'], get_local_scale(obj).x)
            self.update_shell_uniforms(shader)
            self.update_round_uniforms(shader)
            self.update_boolean_uniforms(shader)
        obj.ernst.pmods.update_uniforms(shader, obj)

    def get_shader_code(self, rendables):
        obj = self.id_data
        if not is_renderable(obj):
           return ''

        code = ''
        local_domain = ''

        if self.use_cache:
            collection = obj.instance_collection.ernst
            if collection.enable_cache:
                code = f'vec4 ins_{er_var(obj.name)} = {collection.get_cached_name()};\n'
        else:
            u_names = self.get_uniform_names()
            domain = self.get_code_domain()
            if ubo.enabled:
                scale = er_f(get_local_scale(obj).x) if is_fixed(obj) else '('+ubo.name(u_names['scale'])+'.x)'
            else:
                scale = self.get_code_scale(u_names['scale'])

            rounding = '' if self.round_active == False else self.get_code_round(u_names['round'])
            shell0, shell1, shell2 = '', '', ''
            if self.shell_active:
                shell0, shell1, shell2 = self.get_code_shell(u_names['shell'])

            if self.boolean != 'UberScript':
                sgd.module_lib.boolean[self.boolean].used.v4 = True

            local_domain_name = f'{er_var(obj.name)}_p'
            local_domain = f'vec3 {local_domain_name} = {domain};\n'
            local_domain += obj.ernst.pmods.get_shader_code(obj)

            res_type = 'float'
            elem1 = '.w'
            elem2 = ''
            if self.material == None:
                res_type = 'vec4'
                elem1 = ''
                elem2 = '.w'

            dom = f'{local_domain_name}/{scale}'
            code = f'{res_type} ins_{er_var(obj.name)} = {er_var(obj.instance_collection.name)}({dom}){elem1};\n'

            code += f'ins_{er_var(obj.name)}{elem2} *= {scale};\n'

            collection = obj.instance_collection.ernst
            if collection.enable_cache:
                code += f'{collection.get_cached_name()} = ins_{er_var(obj.name)};\n'

        if self.round_active:
            code += f'ins_{er_var(obj.name)}{elem2} = ins_{er_var(obj.name)}{elem2}{rounding};\n'
        if self.shell_active:
            code += f'ins_{er_var(obj.name)}{elem2} = {shell1}ins_{er_var(obj.name)}{elem2}{shell2};\n'

        boolean, mix = self.get_boolean_code(rendables)
        var_res = 'd'
        if self.material == None:
            mix = mix.replace(', d', ', res')
            var_res = 'res'
        val_type = self.bool_value.type
        val_code = self.bool_value.value_code
        stp_type = self.bool_step.type
        stp_code = self.bool_step.value_code
        if val_type == 'Code' and val_code != '':
            code += self.get_bool_argument_shader_code('bool_value')
        if stp_type == 'Code' and stp_code != '':
            code += self.get_bool_argument_shader_code('bool_step')
        code += f'{var_res} = {boolean}ins_{er_var(obj.name)}{mix};\n'

        # boolean, mix = self.get_boolean_code(rendables)
        # mix = mix.replace(', d', ', res')
        # code += f'res = {boolean}{er_var(obj.name)}{mix};\n'

        code_inline_pre = self.get_code_inline_pre()
        code_inline_post = self.get_code_inline_post()

        return code_inline_pre + local_domain + code + code_inline_post
