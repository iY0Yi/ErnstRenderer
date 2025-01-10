import string
import bpy

from .abstract_primitive import ERNST_PG_Primitive_Abstract
from ..bl_pg_uberval import ERNST_PG_UberValueProperties
from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen import shadergen_ubo as ubo
from ...bl_ot.shadergen.shaderizer import shaderizer_watcher
from ...bl_ot.shadergen.shaderizer.shaderizer_object import *
from ...bl_ot.shadergen.shaderizer.shaderizer_object import is_fixed
from ...bl_mt.bl_mt_boolean import ERNST_MT_BooleanSingle
from ...bl_mt.bl_mt_boolean import ERNST_MT_BoolValueCodeName
from ...bl_mt.bl_mt_boolean import ERNST_MT_BoolStepCodeName
from ...bl_mt.bl_mt_boolean import ERNST_MT_BoolCodeName
from ...bl_ot.shadergen.shaderizer import shaderizer_material
from ...util.map import Map

def force_dirty(self, context):
    obj = self.id_data
    obj.ernst.shader_proxy.props.set_dirty(True)

class ERNST_PG_SDF_Abstract(ERNST_PG_Primitive_Abstract):
    render_order    : bpy.props.IntProperty(name = 'render order', min = -999, max = 999, default = 0)

    boolean         : bpy.props.StringProperty(default = 'BOOL_UNI_SMOOTH', update=shaderizer_watcher.check)
    bool_code_name  : bpy.props.StringProperty(default = '', update=shaderizer_watcher.check)
    boolean_order   : bpy.props.IntProperty(name = 'order', min = -99, max = 99, default = 0, update=shaderizer_watcher.check)
    bool_value :bpy.props.PointerProperty(type=ERNST_PG_UberValueProperties)
    bool_step :bpy.props.PointerProperty(type=ERNST_PG_UberValueProperties)
    bool_code_prop0 : bpy.props.FloatProperty(name = 'prop0', min = -10., max = 10., default = 0., update=force_dirty)
    bool_code_prop1 : bpy.props.FloatProperty(name = 'prop1', min = -10., max = 10., default = 0., update=force_dirty)
    bool_code_prop2 : bpy.props.FloatProperty(name = 'prop2', min = -10., max = 10., default = 0., update=force_dirty)

    round_active           : bpy.props.BoolProperty(name = 'Round active', default=False, update=shaderizer_watcher.check)
    round_radius        : bpy.props.FloatProperty(name = 'Round radius', min = 0.0, max = 10.0, default = 0.0, update=force_dirty)

    shell_active: bpy.props.BoolProperty(name = 'Shell active', default=False, update=shaderizer_watcher.check)
    shell_tickness: bpy.props.FloatProperty(name = 'Shell tickness', min = 0, max = 100, default = 0, update=force_dirty)

    def get_code_dimensions_xy(self, u_name):
        obj = self.id_data
        if is_fixed(obj):
            return er_v2(get_dimensions_xy(obj))
        else:
            if ubo.enabled:
                return ubo.name(u_name)+'.xy'
            else:
                return u_name

    def get_code_dimensions_yz(self, u_name):
        obj = self.id_data
        if is_fixed(obj):
            return er_v2(get_dimensions_yz(obj))
        else:
            if ubo.enabled:
                return ubo.name(u_name)+'.xy'
            else:
                return u_name

    def get_code_dimensions_xz(self, u_name):
        obj = self.id_data
        if is_fixed(obj):
            return er_v2(get_dimensions_xz(obj))
        else:
            if ubo.enabled:
                return ubo.name(u_name)+'.xy'
            else:
                return u_name

    def get_code_dimensions_xyz(self, u_name):
        obj = self.id_data
        if is_fixed(obj):
            return er_v3(get_dimensions_xyz(obj).xzy)
        else:
            if ubo.enabled:
                return ubo.name(u_name)+'.xyz'
            else:
                return u_name

    def add_ubo_round(self):
        if not self.round_active:
            return
        u_names = {}
        self.get_round_uniform_name(u_names)
        ubo.add_vec4(u_names["round"])

    def get_round_uniform_name(self, u_names):
        obj = self.id_data
        if self.round_active:
            u_names['round'] = f'{er_var(obj.name)}_round'

    def get_round_uniform_dec_code(self):
        if self.round_active:
            u_names = {}
            self.get_round_uniform_name(u_names)
            return f'uniform float {u_names["round"]};\n'
        else:
            return ''

    def update_ubo_round(self):
        if self.round_active:
            u_names = {}
            self.get_round_uniform_name(u_names)
            ubo.data[u_names['round']] = (self.round_radius,0,0,0)

    def update_round_uniforms(self, shader):
        if self.round_active:
            u_names = {}
            self.get_round_uniform_name(u_names)
            uniform_float(shader, u_names['round'], self.round_radius)

    def get_code_round(self, u_name):
        obj = self.id_data
        if self.round_active:
            code = ''
            if is_fixed(obj):
                code = f'{er_f(self.round_radius)}'
            else:
                if ubo.enabled:
                    code = f'({ubo.name(u_name)}.x)'
                else:
                    code = u_name
            return f'-{code}'

    def get_shell_uniform_name(self, u_names):
        obj = self.id_data
        if self.shell_active:
            u_names['shell'] = f'{er_var(obj.name)}_shell'

    def add_ubo_shell(self):
        if not self.shell_active:
            return
        u_names = {}
        self.get_shell_uniform_name(u_names)
        ubo.add_vec4(u_names["shell"])

    def get_shell_uniform_dec_code(self):
        if self.shell_active:
            u_names = {}
            self.get_shell_uniform_name(u_names)
            return f'uniform float {u_names["shell"]};\n'
        else:
            return ''

    def update_ubo_shell(self):
        if self.shell_active:
            u_names = {}
            self.get_shell_uniform_name(u_names)
            ubo.data[u_names['shell']] = (self.shell_tickness,0,0,0)

    def update_shell_uniforms(self, shader):
        if self.shell_active:
            u_names = {}
            self.get_shell_uniform_name(u_names)
            uniform_float(shader, u_names['shell'], self.shell_tickness)

    def get_code_shell(self, u_name):
        obj = self.id_data
        if self.shell_active:
            code = ''
            if is_fixed(obj):
                code = f'{er_f(self.shell_tickness)}'
            else:
                if ubo.enabled:
                    code = f'({ubo.name(u_name)}.x)'
                else:
                    code = u_name
            return f'-{code}', 'abs(', f')-{code}'

    def is_boolean_root(self, obj_list, obj):
        id = obj.ernst.shader_proxy.props.render_order
        if id == 0:
            return True
        prev_id = id-1
        prev_obj = obj_list[prev_id]

        # if obj.ernst.type == 'SDF_3D_INSTANCE':
        if not shaderizer_material.has_material(obj):
            return False

        # if prev_obj.ernst.type == 'SDF_3D_INSTANCE':
        if not shaderizer_material.has_material(prev_obj):
            return True

        # pbj_mat = obj.material_slots[0].material.name
        # prev_obj_mat = prev_obj.material_slots[0].material.name
        pbj_mat = shaderizer_material.get_material(obj).name
        prev_obj_mat = shaderizer_material.get_material(prev_obj).name
        if pbj_mat == prev_obj_mat:
            return False
        else:
            return True

    def get_uberscript_bool_info(self):
        if not self.bool_code_name in sgd.uberscript_bool_lines.keys():
            sgd.uberscript_bool_lines[self.bool_code_name] = readUberScriptLines('boolean', self.bool_code_name)

        lines = sgd.uberscript_bool_lines[self.bool_code_name]

        def_line = 0
        for i in range(len(lines)):
            if lines[i].count('float') >= 3:
                def_line = i
                break

        names = re.findall(r'float\s([a-z]+)', lines[def_line], flags=re.IGNORECASE)
        prop_names = []

        for i in range(3, len(names)):
            prop_names.append(names[i])

        call_code = names[0]+'({0}, {1}, '
        for i in range(0, len(prop_names)):
            token = ', ' if i < len(prop_names)-1 else ')'
            call_code += f'{{{2+i}}}{token}'

        fnc_info = Map({
            'name': names[0],
            'prop_names': prop_names,
            'code': call_code
        })
        return fnc_info

    def get_varname_bool_value(self):
        obj = self.id_data
        # if ubo.enabled:
        #     return f'ubo.{er_var(obj.name)}_boolean.x'
        # else:
        return f'{er_var(obj.name)}_bool_raw_val'

    def get_varname_bool_step(self):
        obj = self.id_data
        # if ubo.enabled:
        #     return f'ubo.{er_var(obj.name)}_boolean.y'
        # else:
        return f'{er_var(obj.name)}_bool_raw_step'

    def get_mix_code(self, boolean_method, code_strength, code_step):

        if boolean_method in [
            sgd.module_lib.boolean['BOOL_UNI'].fncname,
            sgd.module_lib.boolean['BOOL_SUB'].fncname,
            sgd.module_lib.boolean['BOOL_INT'].fncname
            ]:
            return ''

        if boolean_method in [
            sgd.module_lib.boolean['BOOL_UNI_SMOOTH'].fncname,
            sgd.module_lib.boolean['BOOL_SUB_SMOOTH'].fncname,
            sgd.module_lib.boolean['BOOL_INT_SMOOTH'].fncname,
            sgd.module_lib.boolean['BOOL_UNI_LINEAR'].fncname,
            sgd.module_lib.boolean['BOOL_SUB_LINEAR'].fncname,
            sgd.module_lib.boolean['BOOL_INT_LINEAR'].fncname
            ]:
            return f', {code_strength}'

        elif boolean_method in [
            sgd.module_lib.boolean['BOOL_UNI_STAIRS_ROUNDED'].fncname,
            sgd.module_lib.boolean['BOOL_SUB_STAIRS_ROUNDED'].fncname,
            sgd.module_lib.boolean['BOOL_INT_STAIRS_ROUNDED'].fncname,
            sgd.module_lib.boolean['BOOL_UNI_STAIRS'].fncname,
            sgd.module_lib.boolean['BOOL_SUB_STAIRS'].fncname,
            sgd.module_lib.boolean['BOOL_INT_STAIRS'].fncname
            ]:
            code_step = f'{code_step}.' if code_step.isdecimal() else code_step
            return f', {code_strength}, {code_step}'

        else:
            #UberScript
            sgd.bool_uberscript_txt_name.append(self.bool_code_name)
            if code_strength=='' and code_step=='':
                return ''

            if code_strength!='' and code_step=='':
                return f', {code_strength}'

            if code_strength!='' and code_step!='':
                code_step = f'{code_step}.' if code_step.isdecimal() else code_step
                return f', {code_strength}, {code_step}'


    def get_boolean_uniform_names(self, u_names):
        obj = self.id_data

        if self.boolean in [
            'BOOL_UNI',
            'BOOL_SUB',
            'BOOL_INT'
            ]:
            return ''

        if self.boolean in [
            'BOOL_UNI_SMOOTH',
            'BOOL_SUB_SMOOTH',
            'BOOL_INT_SMOOTH',
            'BOOL_UNI_LINEAR',
            'BOOL_SUB_LINEAR',
            'BOOL_INT_LINEAR'
            ]:
            u_names['bool_val'] = (f'{er_var(obj.name)}_bool_val')

        elif self.boolean in [
            'BOOL_UNI_STAIRS_ROUNDED',
            'BOOL_SUB_STAIRS_ROUNDED',
            'BOOL_INT_STAIRS_ROUNDED',
            'BOOL_UNI_STAIRS',
            'BOOL_SUB_STAIRS',
            'BOOL_INT_STAIRS'
            ]:
            u_names['bool_val'] = (f'{er_var(obj.name)}_bool_val')
            u_names['bool_step'] = (f'{er_var(obj.name)}_bool_step')

        else:
            #UberScript
            sgd.bool_uberscript_txt_name.append(self.bool_code_name)
            fnc_code = self.get_uberscript_bool_info()
            if len(fnc_code.prop_names) > 0:
                u_names['bool_val'] = (f'{er_var(obj.name)}_bool_val')
            if len(fnc_code.prop_names) > 1:
                u_names['bool_step'] = (f'{er_var(obj.name)}_bool_step')


    def add_ubo_boolean(self):
        u_names = {}
        self.get_boolean_uniform_names(u_names)
        # if u_names=={}:
        #     return
        obj = self.id_data
        ubo.add_vec4(f'{er_var(obj.name)}_boolean')

    def get_boolean_uniform_dec_code(self):
        u_names = {}
        self.get_boolean_uniform_names(u_names)
        code_u_names = ''
        if 'bool_val' in u_names:
            code_u_names = f'uniform float {u_names["bool_val"]};\n'
        if 'bool_step' in u_names:
            code_u_names += f'uniform float {u_names["bool_step"]};\n'
        return code_u_names

    def update_ubo_boolean(self):
        u_names = {}
        self.get_boolean_uniform_names(u_names)
        if u_names=={}:
            return
        v = [0]*4
        if 'bool_val' in u_names:
            v[0]=self.bool_value.value_num
        if 'bool_step' in u_names:
            v[1]=self.bool_step.value_num
        obj = self.id_data
        ubo.data[f'{er_var(obj.name)}_boolean'] = (v[0], v[1], 0, 0)

    def update_boolean_uniforms(self, shader):
        u_names = {}
        self.get_boolean_uniform_names(u_names)
        if 'bool_val' in u_names:
            uniform_float(shader, u_names['bool_val'], self.bool_value.value_num)
        if 'bool_step' in u_names:
            uniform_float(shader, u_names['bool_step'], self.bool_step.value_num)

    def get_boolean_code(self, rendables):
        obj = self.id_data
        bool_name = sgd.module_lib.boolean['BOOL_UNI'].fncname
        boolean = sgd.module_lib.boolean['BOOL_UNI'].fncname+'('
        mix = ''
        u_names = {}
        self.get_boolean_uniform_names(u_names)



        if ubo.enabled:
            if 'bool_val' in u_names:
                u_names['bool_val'] = f'(ubo.{er_var(obj.name)}_boolean.x)'
            if 'bool_step' in u_names:
                u_names['bool_step'] = f'(ubo.{er_var(obj.name)}_boolean.y)'

        # if self.boolean == 'UberScript':
        #     if 'bool_val' in u_names:
        #         print('u_names[bool_val]: ', u_names['bool_val'])
        #     if 'bool_step' in u_names:
        #         print('u_names[bool_step]: ', u_names['bool_step'])

        var_name_value = u_names['bool_val'] if 'bool_val' in u_names else ''
        var_name_step = u_names['bool_step'] if 'bool_step' in u_names else ''

        if is_fixed(obj):
            if 'bool_val' in u_names:
                var_name_value = er_f(self.bool_value.value_num)
            if 'bool_step' in u_names:
                var_name_step = er_f(self.bool_step.value_num)

        if not self.is_boolean_root(rendables, obj):
            if self.boolean != 'UberScript':
                bool_name = sgd.module_lib.boolean[self.boolean].fncname
                boolean = bool_name+'('
                sgd.module_lib.boolean[self.boolean].used.fl = True
            else:
                if self.bool_code_name != '':
                    bool_info = self.get_uberscript_bool_info()
                    bool_name = bool_info.name
                    boolean = bool_name+'('

            if var_name_value != '' and self.bool_value.type == 'Code' and self.bool_value.value_code!='':
                if not is_fixed(obj):
                    var_name_value = self.get_varname_bool_value()

            if var_name_step != '' and self.bool_step.type == 'Code' and self.bool_step.value_code!='':
                if not is_fixed(obj):
                    var_name_step = self.get_varname_bool_step()

            # if self.boolean == 'UberScript':
            #     print('var_name_value: ', var_name_value)
            #     print('var_name_step: ', var_name_step)

            mix = ', d' + self.get_mix_code(bool_name, var_name_value, var_name_step) + ')'

            # if self.boolean == 'UberScript':
            #     print('mix: ', mix)

        if mix == '':
            boolean = ''

        return boolean, mix

    def get_code_position_rotation_p_tra_rot(self, obj):
        position = ''
        rotation = ''
        p_tra_rot = ''

        has_Translation = False
        has_Rotation = False

        for i in range(len(obj.ernst.pmods.pmod)):
            pmd = obj.ernst.pmods.pmod[i].get_pmod()
            if pmd != None:
                if pmd.name == 'Translation': has_Translation=True
                if pmd.name == 'Rotation': has_Rotation=True

        if has_Translation:
            position = er_v3(get_local_pos(obj).xzy) if is_fixed(obj) else f'{er_var(obj.name)}_position'
            domain = obj.ernst.shader_proxy.get_code_domain()
            p_tra = f'{domain}+{position}'

        if has_Rotation:
            rotation = er_v3(get_local_rot(obj).xzy) if is_fixed(obj) else f'{er_var(obj.name)}_rotation'
            loader = sgd.module_lib.pmod['PMOD_ROT_3D']
            loader.used = True

        if has_Translation and has_Rotation:
            p_tra_rot = f'{loader.fncname}({p_tra}, {rotation})'

        return position, rotation, p_tra_rot

    def get_bool_argument_shader_code(self, arg_type):
        obj = self.id_data
        filename = ''
        var_name = ''

        if arg_type == 'bool_value':
            var_name = self.get_varname_bool_value()
            filename = self.bool_value.value_code
        if arg_type == 'bool_step':
            var_name = self.get_varname_bool_step()
            filename = self.bool_step.value_code
        if filename == '':
                return ''

        header = f'/*--- {filename} ---*/\nfloat {var_name};\n{{\n'
        footer = '\n}\n'

        return compile_uber_template(obj, None, 'argument', var_name, filename, header, footer)

        # lines = readUberScriptLines('argument', filename)

        # shader_proxy = obj.ernst.shader_proxy
        # domain = shader_proxy.get_code_domain()

        # position, rotation, p_tra_rot = self.get_code_position_rotation_p_tra_rot(obj)

        # loader = sgd.module_lib.pmod['PMOD_ROT_3D']
        # loader.used = True
        # p_tra = f'{domain}+{position}'
        # p_tra_rot = f'{loader.fncname}({p_tra}, {rotation})'
        # p_tra = '('+p_tra+')'

        # parent_var_name = ''
        # parent_position=''
        # parent_rotation=''
        # parent_p_tra=''
        # parent_p_tra_rot=''
        # if obj.parent != None:
        #     parent_var_name = er_var(obj.parent.name)
        #     p_domain = obj.parent.ernst.shader_proxy.get_code_domain()
        #     parent_position, parent_rotation, parent_p_tra_rot = self.get_code_position_rotation_p_tra_rot(obj.parent)
        #     parent_p_tra = f'{p_domain}+{parent_position}'
        #     parent_p_tra_rot = f'{loader.fncname}({parent_p_tra}, {parent_rotation})'
        #     parent_p_tra = '('+parent_p_tra+')'

        # code = ''
        # for line in lines:
        #     line = line.replace('@VAR', var_name)
        #     line = line.replace('@CP_POS', position)
        #     line = line.replace('@CP_ROT', rotation)
        #     line = line.replace('@CP_TR', p_tra_rot)
        #     line = line.replace('@CP_T', p_tra)
        #     line = line.replace('@CP', domain)
        #     line = line.replace('@PARENT_POS', parent_position)
        #     line = line.replace('@PARENT_ROT', parent_rotation)
        #     line = line.replace('@PARENT', parent_var_name)
        #     line = line.replace('@PARENT_TR', parent_p_tra_rot)
        #     line = line.replace('@PARENT_T', parent_p_tra)
        #     code += line

        # code = string.Template(code)
        # variables = {
        #     "var": var_name,

        #     "cp": domain,
        #     "cppos": position,
        #     "cprot": rotation,
        #     "cpt": p_tra,
        #     "cptr": p_tra_rot,

        #     "pppos": parent_position,
        #     "pprot": parent_rotation,
        #     "pp": parent_var_name,
        #     "ppt": parent_p_tra,
        #     "pptr": parent_p_tra_rot,
        # }
        # code = code.substitute(variables)

        # code = header + code + footer

        # return code

    def draw_bool_value(self, bool_col, name):
        row = bool_col.row(align = True)
        icon = 'OPTIONS' if self.bool_value.type == 'Number' else 'TEXT'
        row.prop(self.bool_value, 'type', text='', icon=icon, icon_only=True)
        if self.bool_value.type == 'Number':
            row.prop(self.bool_value, 'value_num', text=name)
        else:
            col = row.column(align=False)
            text = self.bool_value.value_code
            if text=='':
                text = 'undefined'
                col.active = False
            col.menu(ERNST_MT_BoolValueCodeName.bl_idname, text=text)
            col = row.column(align=True)
            op = col.operator('ernst.open_in_vscode', text='', icon='GREASEPENCIL')
            op.filepath = f'//track/uber_scripts/argument/{text}'

    def draw_bool_step(self, bool_col, name):
        row = bool_col.row(align = True)
        icon = 'OPTIONS' if self.bool_step.type == 'Number' else 'TEXT'
        row.prop(self.bool_step, 'type', text='', icon=icon, icon_only=True)
        if self.bool_step.type == 'Number':
            row.prop(self.bool_step, 'value_num', text=name)
        else:
            col = row.column(align=False)
            text = self.bool_step.value_code
            if text=='':
                text = 'undefined'
                col.active = False
            col.menu(ERNST_MT_BoolStepCodeName.bl_idname, text=text)
            col = row.column(align=True)
            op = col.operator('ernst.open_in_vscode', text='', icon='GREASEPENCIL')
            op.filepath = f'//track/uber_scripts/argument/{text}'

    def draw_order(self, bool_col):
        obj = self.id_data
        row = bool_col.row(align=False)
        col = row.column(align=False)
        col_row = col.row(align=True)
        col_row.prop(self, 'boolean_order', text='Order')
        up = col_row.operator("view3d.move_boolean_order", icon='TRIA_UP', emboss=True, text="")
        up.type = 'UP'
        up.name = obj.name
        down = col_row.operator("view3d.move_boolean_order", icon='TRIA_DOWN', emboss=True, text="")
        down.type = 'DOWN'
        down.name = obj.name

    def draw_boolean(self, box_col):
        icon = 'TEXT'
        if self.boolean.find('UNI')>0:
            icon = 'SELECT_EXTEND'
        if self.boolean.find('SUB')>0:
            icon = 'SELECT_SUBTRACT'
        if self.boolean.find('INT')>0:
            icon = 'SELECT_INTERSECT'

        bool_col = box_col.column(align=True)
        bool_col.menu(ERNST_MT_BooleanSingle.bl_idname, text=self.boolean, icon=icon)

        if self.boolean == 'BOOL_UNI':
            self.draw_order(bool_col)
            return

        if self.boolean == 'UberScript' and self.bool_code_name == '':
            row = bool_col.row(align=False)
            row.active = False
            row.menu(ERNST_MT_BoolCodeName.bl_idname, text='undefined', icon='TEXT')
            return

        if self.boolean != 'UberScript':
            self.draw_bool_value(bool_col, 'Mix')
            if self.boolean.find('STAIRS')!=-1:
                self.draw_bool_step(bool_col, 'Steps')
            self.draw_order(bool_col)
        else:
            text = self.bool_code_name
            bool_col.menu(ERNST_MT_BoolCodeName.bl_idname, text=text, icon='TEXT')
            # bool_col = box_col.column(align=True) = row.column(align=True)
            op = bool_col.operator('ernst.open_in_vscode', text='', icon='GREASEPENCIL')
            op.filepath = f'//track/uber_scripts/boolean/{text}'
            fnc_info = self.get_uberscript_bool_info()
            if len(fnc_info.prop_names) >= 1:
                self.draw_bool_value(bool_col, fnc_info.prop_names[0].capitalize())
            if len(fnc_info.prop_names) >= 2:
                self.draw_bool_step(bool_col, fnc_info.prop_names[1].capitalize())
            self.draw_order(bool_col)

