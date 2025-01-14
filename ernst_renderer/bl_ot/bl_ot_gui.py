import math
import bpy
from bpy.types import Operator

from .shadergen.shadergen import *
from .shadergen.shadergen_util import *
from .shadergen.shaderizer import shaderizer_watcher

running = False


class ERNST_OT_Scale_Boolean_Value(Operator):
    bl_idname = 'ernst.scale_boolean_values'
    bl_label = 'SDF scaling boolean values.'
    bl_description = 'SDF scaling boolean values.'
    bl_options = {'REGISTER', 'UNDO'}

    obj_boolean_scale = 1.0
    orig_x = 0.0
    org_boolean_val = []

    def modal(self, context, event):
        global running
        if running is False:
            return {'PASS_THROUGH'}

        selected_obj = bpy.context.selected_objects
        id = 0
        for obj in selected_obj:
            obj.ernst.shader_proxy.props.bool_value.value_num = self.org_boolean_val[id] * self.obj_boolean_scale
            id+=1

        # 任意のミックス値の最小値と最大値
        MIN_MIX_VALUE = 0.001
        MAX_MIX_VALUE = 100.0

        def exponential_scale(x):
            """
            指数スケールに変換する関数
            """
            return x ** 2  # 任意の指数を調整することで変化の度合いを調整できます

        def inv_exponential_scale(x):
            """
            指数スケールから元のスケールに戻す関数
            """
            return math.sqrt(x)

        def linear_scale(x):
            """
            線形スケールに変換する関数
            """
            return x * (MAX_MIX_VALUE - MIN_MIX_VALUE) + MIN_MIX_VALUE

        def inv_linear_scale(x):
            """
            線形スケールから元のスケールに戻す関数
            """
            return (x - MIN_MIX_VALUE) / (MAX_MIX_VALUE - MIN_MIX_VALUE)

        if event.type == 'MOUSEMOVE':
            context.area.tag_redraw()
            # マウスドラッグの変化量に応じてスケールを適用
            factor = 1.0 / 100.0
            delta = (event.mouse_x - self.orig_x) * factor
            # 指数スケールを適用
            # self.obj_boolean_scale = exponential_scale(self.obj_boolean_scale)
            # self.obj_boolean_scale += delta
            # self.obj_boolean_scale = inv_exponential_scale(self.obj_boolean_scale)

            # 線形スケールを適用
            self.obj_boolean_scale = linear_scale(self.obj_boolean_scale)
            self.obj_boolean_scale += delta
            self.obj_boolean_scale = inv_linear_scale(self.obj_boolean_scale)
            # ミックス値を制限する
            self.obj_boolean_scale = max(MIN_MIX_VALUE, min(MAX_MIX_VALUE, self.obj_boolean_scale))
            return {'RUNNING_MODAL'}


        if event.type == 'RIGHTMOUSE':
            if event.value == 'PRESS':
                self.orig_x = event.mouse_x
                return {'RUNNING_MODAL'}

        if event.type == 'LEFTMOUSE':
            if event.value == 'PRESS':
                running = False
                return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        global running
        self.org_boolean_val = []
        if context.area.type == 'VIEW_3D':
            if running is False:
                running = True
                self.obj_boolean_scale = 1.0
                self.orig_x = event.mouse_x
                selected_objs = bpy.context.selected_objects
                for obj in selected_objs:
                    self.org_boolean_val.append(obj.ernst.shader_proxy.props.bool_value.value_num)

                context.window_manager.modal_handler_add(self)
                return {'RUNNING_MODAL'}
        return {'CANCELLED'}


class ERNST_OT_Set_Multi_Csg_Orders(Operator):
    bl_idname = 'ernst.boolean_order_multi'
    bl_label = 'Set Boolean orders.'
    bl_description = 'Set Boolean orders.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objs = context.selected_objects
        for obj in objs:
            obj.ernst.shader_proxy.props.boolean_order = context.screen.ernst.blui_set_boolean_order
        return {'FINISHED'}


class ERNST_OT_Offset_Multi_Csg_Orders(Operator):
    bl_idname = 'ernst.boolean_order_multi_offset'
    bl_label = 'Offset selected Boolean orders.'
    bl_description = 'Offset Boolean orders.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objs = context.selected_objects
        for obj in objs:
            obj.ernst.shader_proxy.props.boolean_order += context.screen.ernst.blui_offset_boolean_order
        return {'FINISHED'}


class ERNST_OT_Increment_Multi_Csg_Orders(Operator):
    bl_idname = 'ernst.boolean_order_multi_increment'
    bl_label = 'Increment selected Boolean orders.'
    bl_description = 'Increment Boolean orders.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objs = context.selected_objects
        for obj in objs:
            obj.ernst.shader_proxy.props.boolean_order += 1
        return {'FINISHED'}


class ERNST_OT_Decrement_Multi_Csg_Orders(Operator):
    bl_idname = 'ernst.boolean_order_multi_decrement'
    bl_label = 'Decrement selected Boolean orders.'
    bl_description = 'Decrement Boolean orders.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objs = context.selected_objects
        for obj in objs:
            obj.ernst.shader_proxy.props.boolean_order -= 1
        return {'FINISHED'}


class ERNST_OT_Lock_ERNST_Objects(Operator):
    bl_idname = 'ernst.lock_in_scene_sdfs'
    bl_label = 'Lock all selected SDF objects'
    bl_description = 'Lock all selected SDF objects. Parameters will be hardcorded'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objs = bpy.data.objects
        for obj in objs:
            if (obj.name == 'Camera' or obj.ernst.is_ernst_obj) and obj.select_get():
                obj.hide_select=True
                obj.select_set(False)
        return {'FINISHED'}


class ERNST_OT_Unlock_ERNST_Objects(Operator):
    bl_idname = 'ernst.unlock_in_scene_sdfs'
    bl_label = 'Unlock all SDF objects'
    bl_description = 'Unlock all SDF objects. Parameters live as uniform variables'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objs = bpy.data.objects
        for obj in objs:
            if (obj.name == 'Camera' or obj.ernst.is_ernst_obj) and obj.hide_select:
                obj.hide_select=False
                obj.select_set(True)
        return {'FINISHED'}


class ERNST_OT_Reload_Shader(Operator):
    bl_idname = 'ernst.reload_shader'
    bl_label = 'Reload Shader'
    bl_description = 'Assign a base shader.'
    bl_options = {'REGISTER'}

    def execute(self, context):
        bpy.ops.ernst.recompile_shader('EXEC_DEFAULT')
        return {'FINISHED'}


class ERNST_OT_RemovePModifier(Operator):
    bl_idname = "view3d.my_uilist_remove_item"
    bl_label = "Remove Item"
    bl_options = {'REGISTER', 'UNDO'}

    id : bpy.props.IntProperty(default=0)

    def execute(self, context):
        name = context.view_layer.objects.active.name
        obj_props = bpy.data.objects[name]
        obj_props.ernst.pmods.remove(self.id)
        shaderizer_watcher.check(self, context)
        return {'FINISHED'}


class ERNST_OT_MovePModifier(Operator):
    bl_idname = "view3d.my_uilist_move_item"
    bl_label = "Move Item"
    bl_options = {'REGISTER', 'UNDO'}

    type : bpy.props.StringProperty(default='UP')
    id : bpy.props.IntProperty(default=0)

    def execute(self, context):
        name = context.view_layer.objects.active.name
        obj_props = bpy.data.objects[name]
        pm_prop = obj_props.ernst.pmods
        id = self.id
        if self.type == 'UP':
            pm_prop.move(id, id-1)
        elif self.type == 'DOWN':
            pm_prop.move(id, id+1)
        shaderizer_watcher.check(self, context)
        return {'FINISHED'}


class ERNST_OT_MoveBooleanOrder(Operator):
    bl_idname = "view3d.move_boolean_order"
    bl_label = "Move boolean order"
    bl_options = {'REGISTER', 'UNDO'}

    type : bpy.props.StringProperty(default='UP')
    name : bpy.props.StringProperty(default='')

    def execute(self, context):
        if self.type == 'UP':
            bpy.data.objects[self.name].ernst.shader_proxy.props.boolean_order-=1
        elif self.type == 'DOWN':
            bpy.data.objects[self.name].ernst.shader_proxy.props.boolean_order+=1
        shaderizer_watcher.check(self, context)
        return {'FINISHED'}
