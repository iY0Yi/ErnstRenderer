import bpy
from bpy.types import Menu

from ..bl_ot.bl_ot_boolean import *
from ..bl_ot.shadergen import shadergen_data as sgd
from ..util.util import *

class ERNST_MT_BoolCodeName(Menu):
    bl_idname = 'ERNST_MT_Bool_CodeName'
    bl_label = 'Bool Code Name'

    def draw(self, context):
        layout = self.layout
        drawUberScriptFileNames(layout, 'boolean', ERNST_OT_ChooseBoolCodeName, 'bool_code_name')

class ERNST_MT_BoolValueCodeName(Menu):
    bl_idname = 'ERNST_MT_Bool_Value_CodeName'
    bl_label = 'Bool Value Code Name'

    def draw(self, context):
        layout = self.layout
        drawUberScriptFileNames(layout, 'argument', ERNST_OT_ChooseBoolValueCodeName, 'bool_value_code_name')

class ERNST_MT_BoolStepCodeName(Menu):
    bl_idname = 'ERNST_MT_Bool_Step_CodeName'
    bl_label = 'Bool Step Code Name'

    def draw(self, context):
        layout = self.layout
        drawUberScriptFileNames(layout, 'argument', ERNST_OT_ChooseBoolStepCodeName, 'bool_step_code_name')

def boolean_method_list(instance):
    layout = instance.layout
    layout.operator(ERNST_OT_Union.bl_idname, text='Union', icon='SELECT_EXTEND')
    layout.operator(ERNST_OT_UnionLinear.bl_idname, text='Union: Linear', icon='SELECT_EXTEND')
    layout.operator(ERNST_OT_UnionSmooth.bl_idname, text='Union: Smooth', icon='SELECT_EXTEND')
    layout.operator(ERNST_OT_UnionStep.bl_idname, text='Union: Step', icon='SELECT_EXTEND')
    layout.operator(ERNST_OT_UnionStepSmooth.bl_idname, text='Union: StepSmooth', icon='SELECT_EXTEND')
    layout.operator(ERNST_OT_Substraction.bl_idname, text='Substraction', icon='SELECT_SUBTRACT')
    layout.operator(ERNST_OT_SubstractionLinear.bl_idname, text='Substraction: Linear', icon='SELECT_SUBTRACT')
    layout.operator(ERNST_OT_SubstractionSmooth.bl_idname, text='Substraction: Smooth', icon='SELECT_SUBTRACT')
    layout.operator(ERNST_OT_SubstractionStep.bl_idname, text='Substraction: Step', icon='SELECT_SUBTRACT')
    layout.operator(ERNST_OT_SubstractionStepSmooth.bl_idname, text='Substraction: StepSmooth', icon='SELECT_SUBTRACT')
    layout.operator(ERNST_OT_Intersection.bl_idname, text='Intersection', icon='SELECT_INTERSECT')
    layout.operator(ERNST_OT_IntersectionLinear.bl_idname, text='Intersection: Linear', icon='SELECT_INTERSECT')
    layout.operator(ERNST_OT_IntersectionSmooth.bl_idname, text='Intersection: Smooth', icon='SELECT_INTERSECT')
    layout.operator(ERNST_OT_IntersectionStep.bl_idname, text='Intersection: Step', icon='SELECT_INTERSECT')
    layout.operator(ERNST_OT_IntersectionStepSmooth.bl_idname, text='Intersection: StepSmooth', icon='SELECT_INTERSECT')
    layout.operator(ERNST_OT_UberScript.bl_idname, text='UberScript', icon='TEXT')

class ERNST_MT_BooleanSingle(Menu):
    bl_idname = 'ERNST_MT_BooleanSingle'
    bl_label = 'BOOL_UNI'
    bl_description = 'Change Boolean method'

    def draw(self, context):
        context.screen.ernst.edit_in = 'SINGLE'
        boolean_method_list(self)

class ERNST_MT_BooleanMulti(Menu):
    bl_idname = 'ERNST_MT_BooleanMulti'
    bl_label = 'BOOL_UNI'
    bl_description = 'Change Boolean method'

    def draw(self, context):
        context.screen.ernst.edit_in = 'MULTI'
        boolean_method_list(self)
