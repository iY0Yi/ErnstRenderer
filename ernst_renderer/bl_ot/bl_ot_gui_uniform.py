import bpy
import numpy as np
from bpy.types import Operator
from mathutils import Color

from ..util.util import *
from .shadergen import shadergen_data as sgd



class ERNST_OT_BLUGUI_1f(Operator):
    '''
    Build GUI for BLU 1f.
    '''
    bl_idname = 'ernst.blugui_1f'
    bl_label = 'BLU GUI 1f'
    bl_options = {'REGISTER', 'UNDO'}
    COMPAT_ENGINES = {'ERNST'}

    def execute(self, context):
        GUI_NAME = 'BluGui_1f'
        bpy.ops.view3d.snap_cursor_to_center()
        # bpy.ops.object.empty_add(type='CUBE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.active_object.show_in_front = True
        bpy.context.active_object.name = GUI_NAME

        # first knob
        KNOB_NAME = 'u1f'+str(0)
        ZERO_NAME = KNOB_NAME+'_zero'
        bpy.ops.object.empty_add(type='CIRCLE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.context.active_object.empty_display_size = 0.05
        bpy.context.active_object.name = ZERO_NAME
        bpy.context.active_object.parent = bpy.data.objects[GUI_NAME]
        bpy.context.active_object.parent_type = 'OBJECT'
        bpy.context.active_object.hide_select = True

        bpy.ops.object.empty_add(type='CIRCLE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.active_object.empty_display_size = 0.05
        bpy.context.active_object.show_name = True

        bpy.context.active_object.name = KNOB_NAME
        bpy.context.active_object.parent = bpy.data.objects[ZERO_NAME]
        bpy.context.active_object.parent_type = 'OBJECT'
        bpy.context.active_object.empty_display_size = 0.05
        bpy.ops.object.constraint_add(type='LIMIT_LOCATION')
        bpy.context.object.constraints["Limit Location"].use_min_y = True
        bpy.context.object.constraints["Limit Location"].use_min_z = True
        bpy.context.object.constraints["Limit Location"].use_max_y = True
        bpy.context.object.constraints["Limit Location"].use_max_z = True
        bpy.context.object.constraints["Limit Location"].owner_space = 'LOCAL'
        bpy.context.active_object.show_in_front = True

        bpy.data.objects[ZERO_NAME].location.y = .2
        sgd.is_active_blugui1f = True
        select_hierarchy(bpy.data.objects[GUI_NAME])
        return {'FINISHED'}


class ERNST_OT_BLUGUI_2v(Operator):
    '''
    Build GUI for BLU 2v.
    '''
    bl_idname = 'ernst.blugui_2v'
    bl_label = 'BLU GUI 2v'
    bl_options = {'REGISTER', 'UNDO'}
    COMPAT_ENGINES = {'ERNST'}

    def execute(self, context):
        GUI_NAME = 'BluGui_2v'
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.object.empty_add(type='CUBE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.active_object.show_in_front = True
        bpy.context.active_object.name = GUI_NAME

        # first knob
        KNOB_NAME = 'u2v'+str(0)
        bpy.ops.object.empty_add(type='CIRCLE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.context.active_object.name = KNOB_NAME
        bpy.context.active_object.empty_display_size = 0.05
        bpy.context.active_object.parent = bpy.data.objects[GUI_NAME]
        bpy.context.active_object.parent_type = 'OBJECT'
        bpy.context.active_object.show_name = True
        bpy.ops.object.constraint_add(type='LIMIT_LOCATION')
        bpy.context.object.constraints["Limit Location"].use_min_z = True
        bpy.context.object.constraints["Limit Location"].use_max_z = True
        bpy.context.object.constraints["Limit Location"].owner_space = 'LOCAL'
        bpy.context.active_object.show_in_front = True
        sgd.is_active_blugui2v = True
        select_hierarchy(bpy.data.objects[GUI_NAME])
        return {'FINISHED'}


class ERNST_OT_BLUGUI_3v(Operator):
    '''
    Build GUI for BLU 3v.
    '''
    bl_idname = 'ernst.blugui_3v'
    bl_label = 'BLU GUI 3v'
    bl_options = {'REGISTER', 'UNDO'}
    COMPAT_ENGINES = {'ERNST'}

    def execute(self, context):
        GUI_NAME = 'BluGui_3v'
        bpy.ops.view3d.snap_cursor_to_center()
        bpy.ops.object.empty_add(type='CUBE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.active_object.show_in_front = True
        bpy.context.active_object.name = GUI_NAME

        # first knob
        KNOB_NAME = 'u3v'+str(0)
        bpy.ops.object.empty_add(type='SPHERE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.empty_display_size = 0.05
        bpy.context.active_object.name = KNOB_NAME
        bpy.context.active_object.parent = bpy.data.objects[GUI_NAME]
        bpy.context.active_object.parent_type = 'OBJECT'
        bpy.context.active_object.show_name = True
        bpy.context.active_object.show_in_front = True
        sgd.is_active_blugui3v = True
        select_hierarchy(bpy.data.objects[GUI_NAME])
        return {'FINISHED'}


class ERNST_OT_Add_BLUGUI1f(Operator):
    bl_idname = 'ernst.blugui1f_add'
    bl_label = 'Add BLU GUI 1f.'
    bl_description = 'Add BLU GUI 1f.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        GUI_NAME = 'BluGui_1f'
        holder = bpy.data.objects[GUI_NAME]
        new_id = len(holder.children)
        KNOB_NAME = 'u1f'+str(new_id)
        ZERO_NAME = KNOB_NAME+'_zero'
        bpy.ops.object.empty_add(type='CIRCLE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.context.active_object.name = ZERO_NAME
        bpy.context.active_object.parent = bpy.data.objects[GUI_NAME]
        bpy.context.active_object.parent_type = 'OBJECT'
        bpy.context.active_object.empty_display_size = 0.05
        bpy.context.object.hide_select = True

        bpy.ops.object.empty_add(type='CIRCLE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.active_object.show_name = True
        bpy.context.active_object.empty_display_size = 0.05
        bpy.context.active_object.name = KNOB_NAME
        bpy.context.active_object.parent = bpy.data.objects[ZERO_NAME]
        bpy.context.active_object.parent_type = 'OBJECT'
        bpy.ops.object.constraint_add(type='LIMIT_LOCATION')
        bpy.context.object.constraints["Limit Location"].use_min_y = True
        bpy.context.object.constraints["Limit Location"].use_min_z = True
        bpy.context.object.constraints["Limit Location"].use_max_y = True
        bpy.context.object.constraints["Limit Location"].use_max_z = True
        bpy.context.object.constraints["Limit Location"].owner_space = 'LOCAL'
        bpy.context.active_object.show_in_front = True

        bpy.data.objects[ZERO_NAME].location.y = .2*(new_id+1)
        select_hierarchy(bpy.data.objects[GUI_NAME])
        return {'FINISHED'}


class ERNST_OT_Remove_BLUGUI1f(Operator):
    bl_idname = 'ernst.blugui1f_remove'
    bl_label = 'Remove BLU GUI 1f.'
    bl_description = 'Remove BLU GUI 1f.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        GUI_NAME = 'BluGui_1f'
        holder = bpy.data.objects[GUI_NAME]
        newest_id = len(holder.children)-1
        KNOB_NAME = 'u1f'+str(newest_id)
        remove_obj_by_name(KNOB_NAME)
        remove_obj_by_name(KNOB_NAME+'_zero')

        if newest_id == 0:
            remove_obj_by_name(GUI_NAME)
        else:
            select_hierarchy(bpy.data.objects[GUI_NAME])

        return {'FINISHED'}


class ERNST_OT_Add_BLUGUI2v(Operator):
    bl_idname = 'ernst.blugui2v_add'
    bl_label = 'Add BLU GUI 2v.'
    bl_description = 'Add BLU GUI 2v.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        GUI_NAME = 'BluGui_2v'
        holder = bpy.data.objects[GUI_NAME]
        new_id = len(holder.children)
        KNOB_NAME = 'u2v'+str(new_id)
        bpy.ops.object.empty_add(type='CIRCLE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        bpy.context.active_object.name = KNOB_NAME
        bpy.context.active_object.parent = bpy.data.objects[GUI_NAME]
        bpy.context.active_object.parent_type = 'OBJECT'
        bpy.context.active_object.show_name = True
        bpy.context.active_object.empty_display_size = 0.05
        bpy.ops.object.constraint_add(type='LIMIT_LOCATION')
        bpy.context.object.constraints["Limit Location"].use_min_z = True
        bpy.context.object.constraints["Limit Location"].use_max_z = True
        bpy.context.object.constraints["Limit Location"].owner_space = 'LOCAL'
        bpy.context.active_object.show_in_front = True
        select_hierarchy(bpy.data.objects[GUI_NAME])
        return {'FINISHED'}


class ERNST_OT_Remove_BLUGUI2v(Operator):
    bl_idname = 'ernst.blugui2v_remove'
    bl_label = 'Remove BLU GUI 2v.'
    bl_description = 'Remove BLU GUI 2v.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        GUI_NAME = 'BluGui_2v'
        holder = bpy.data.objects[GUI_NAME]
        newest_id = len(holder.children)-1
        KNOB_NAME = 'u2v'+str(newest_id)
        remove_obj_by_name(KNOB_NAME)

        if newest_id == 0:
            remove_obj_by_name(GUI_NAME)
        else:
            select_hierarchy(bpy.data.objects[GUI_NAME])

        return {'FINISHED'}


class ERNST_OT_Add_BLUGUI3v(Operator):
    bl_idname = 'ernst.blugui3v_add'
    bl_label = 'Add BLU GUI 3v.'
    bl_description = 'Add BLU GUI 3v.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        GUI_NAME = 'BluGui_3v'
        holder = bpy.data.objects[GUI_NAME]
        new_id = len(holder.children)
        KNOB_NAME = 'u3v'+str(new_id)
        bpy.ops.object.empty_add(type='SPHERE', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.context.object.empty_display_size = 0.05
        bpy.context.active_object.name = KNOB_NAME
        bpy.context.active_object.parent = holder
        bpy.context.active_object.parent_type = 'OBJECT'
        bpy.context.active_object.show_name = True
        bpy.context.active_object.show_in_front = True
        select_hierarchy(bpy.data.objects[GUI_NAME])
        return {'FINISHED'}


class ERNST_OT_Remove_BLUGUI3v(Operator):
    bl_idname = 'ernst.blugui3v_remove'
    bl_label = 'Remove BLU GUI 3v.'
    bl_description = 'Remove BLU GUI 3v.'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        GUI_NAME = 'BluGui_3v'
        holder = bpy.data.objects[GUI_NAME]
        newest_id = len(holder.children)-1
        KNOB_NAME = 'u3v'+str(newest_id)
        remove_obj_by_name(KNOB_NAME)

        if newest_id == 0:
            remove_obj_by_name(GUI_NAME)
        else:
            select_hierarchy(bpy.data.objects[GUI_NAME])

        return {'FINISHED'}
