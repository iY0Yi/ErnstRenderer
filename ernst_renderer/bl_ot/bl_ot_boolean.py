import bpy
from bpy.types import Operator

from .shadergen.shaderizer import shaderizer_watcher


class BooleanOperatorBase:
    bl_label = 'method'
    bl_description = 'Change Boolean method.'
    bl_options = {'REGISTER'}
    method_type : bpy.props.StringProperty()
    code_float = ''
    code_v4 = ''

    def execute(self, context):
        if context.screen.ernst.edit_in == 'SINGLE':
            obj = context.view_layer.objects.active
            obj.ernst.shader_proxy.props.boolean = self.fnc_name
        elif context.screen.ernst.edit_in == 'MULTI':
            for obj in context.selected_objects:
                obj.ernst.shader_proxy.props.boolean = self.fnc_name
        shaderizer_watcher.check(self, context)
        return {'FINISHED'}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_Union(BooleanOperatorBase, Operator):
    bl_idname  = 'ernst.change_boolean_method_uni'
    fnc_name = 'BOOL_UNI'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_UnionLinear(BooleanOperatorBase, Operator):
    bl_idname  = 'ernst.change_boolean_method_uni_linear'
    fnc_name = 'BOOL_UNI_LINEAR'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_UnionSmooth(BooleanOperatorBase, Operator):
    bl_idname  = 'ernst.change_boolean_method_uni_smooth'
    fnc_name = 'BOOL_UNI_SMOOTH'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_UnionStep(BooleanOperatorBase, Operator):
    bl_idname  = 'ernst.change_boolean_method_uni_step'
    fnc_name = 'BOOL_UNI_STAIRS'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_UnionStepSmooth(BooleanOperatorBase, Operator):
    bl_idname  = 'ernst.change_boolean_method_uni_step_smooth'
    fnc_name = 'BOOL_UNI_STAIRS_ROUNDED'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_Substraction(BooleanOperatorBase, Operator):
    bl_idname = 'ernst.change_boolean_method_sub'
    fnc_name = 'BOOL_SUB'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_SubstractionLinear(BooleanOperatorBase, Operator):
    bl_idname = 'ernst.change_boolean_method_sub_linear'
    fnc_name = 'BOOL_SUB_LINEAR'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_SubstractionSmooth(BooleanOperatorBase, Operator):
    bl_idname = 'ernst.change_boolean_method_sub_smooth'
    fnc_name = 'BOOL_SUB_SMOOTH'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_SubstractionStep(BooleanOperatorBase, Operator):
    bl_idname = 'ernst.change_boolean_method_sub_step'
    fnc_name = 'BOOL_SUB_STAIRS'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_SubstractionStepSmooth(BooleanOperatorBase, Operator):
    bl_idname = 'ernst.change_boolean_method_sub_step_smooth'
    fnc_name = 'BOOL_SUB_STAIRS_ROUNDED'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_Intersection(BooleanOperatorBase, Operator):
    bl_idname = 'ernst.change_boolean_method_int'
    fnc_name = 'BOOL_INT'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_IntersectionLinear(BooleanOperatorBase, Operator):
    bl_idname = 'ernst.change_boolean_method_int_linear'
    fnc_name = 'BOOL_INT_LINEAR'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_IntersectionSmooth(BooleanOperatorBase, Operator):
    bl_idname = 'ernst.change_boolean_method_int_smooth'
    fnc_name = 'BOOL_INT_SMOOTH'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_IntersectionStep(BooleanOperatorBase, Operator):
    bl_idname = 'ernst.change_boolean_method_int_step'
    fnc_name = 'BOOL_INT_STAIRS'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_IntersectionStepSmooth(BooleanOperatorBase, Operator):
    bl_idname = 'ernst.change_boolean_method_int_step_smooth'
    fnc_name = 'BOOL_INT_STAIRS_ROUNDED'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_UberScript(BooleanOperatorBase, Operator):
    bl_idname = 'ernst.change_boolean_method_custom'
    src_code: bpy.props.StringProperty()
    fnc_name = 'UberScript'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_ChooseBoolCodeName(Operator):
    bl_idname = 'ernst.choose_bool_code'
    bl_label = 'method'
    bl_description = 'Choose Boolean code'
    bl_options = {'REGISTER'}
    bool_code_name: bpy.props.StringProperty(name='code_NAME', default='')

    bool_file_name: bpy.props.StringProperty(
        name="",
        description="Choose a file",
        default="",
        maxlen=1024,
        subtype='FILE_PATH',
        update=shaderizer_watcher.check
    )

    def execute(self, context):
        obj = context.view_layer.objects.active
        obj.ernst.shader_proxy.props.bool_code_name = self.bool_code_name
        shaderizer_watcher.check(self, context)

        return {'FINISHED'}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_ChooseBoolValueCodeName(Operator):
    bl_idname = 'ernst.choose_bool_value_code'
    bl_label = 'method'
    bl_description = 'Choose Boolean Value code'
    bl_options = {'REGISTER'}
    bool_value_code_name: bpy.props.StringProperty(name='code_NAME', default='')

    bool_value_file_name: bpy.props.StringProperty(
        name="",
        description="Choose a file",
        default="",
        maxlen=1024,
        subtype='FILE_PATH',
        update=shaderizer_watcher.check
    )

    def execute(self, context):
        obj = context.view_layer.objects.active
        obj.ernst.shader_proxy.props.bool_value.value_code = self.bool_value_code_name
        shaderizer_watcher.check(self, context)

        return {'FINISHED'}

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_OT_ChooseBoolStepCodeName(Operator):
    bl_idname = 'ernst.choose_bool_step_code'
    bl_label = 'method'
    bl_description = 'Choose Boolean Step code'
    bl_options = {'REGISTER'}
    bool_step_code_name: bpy.props.StringProperty(name='code_NAME', default='')

    bool_step_file_name: bpy.props.StringProperty(
        name="",
        description="Choose a file",
        default="",
        maxlen=1024,
        subtype='FILE_PATH',
        update=shaderizer_watcher.check
    )

    def execute(self, context):
        obj = context.view_layer.objects.active
        obj.ernst.shader_proxy.props.bool_step.value_code = self.bool_step_code_name
        shaderizer_watcher.check(self, context)

        return {'FINISHED'}
