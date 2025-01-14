import os
import time

import bpy

from ....util.util import *
from .. import shadergen
from .. import shadergen_data as sgd
from ..shadergen_util import *

need_analyze = True
last_update = None

def force_compile(self, context):
    global need_analyze
    if sgd.view_shading_type == 'MATERIAL' or sgd.view_shading_type == 'RENDERED':
        need_analyze = True
        print('shadergen.process(): shaderizer_watcher.force_compile')
        shadergen.process(context)

def check(self, context):
    global need_analyze

    need_analyze = True

def update_filestamps():
    global need_analyze, last_update
    need_analyze = False
    if sgd.dir_working != None:
        last_update = {}
        files = sgd.dir_working.glob("**/*.frag")
        for file in files:
            path_str = str(file)
            if not 'bl_modules' in path_str:
                props = os.stat(path_str)
                last_update[path_str] = props.st_mtime
        files = sgd.dir_working.glob("**/*.glsl*")
        for file in files:
            path_str = str(file)
            if not 'bl_modules' in path_str:
                props = os.stat(path_str)
                last_update[path_str] = props.st_mtime

def watch_codes():
    global need_analyze, last_update

    INTERVAL = .5

    # shader template was changed...
    if need_analyze == False:
        files = sgd.dir_working.glob("**/*.frag")
        for file in files:
            path_str = str(file)
            if not 'bl_modules' in path_str:
                props = os.stat(path_str)
                newest_update = props.st_mtime
                if newest_update > last_update[path_str]:
                    print('Shader file was updated: ', file.stem)
                    print('newest_update: ', newest_update)
                    print('last_update[path_str]: ', last_update[path_str])
                    last_update[path_str] = newest_update
                    need_analyze = True

        files = sgd.dir_working.glob("**/*.glsl*")
        for file in files:
            path_str = str(file)
            if not 'bl_modules' in path_str:
                props = os.stat(path_str)
                newest_update = props.st_mtime
                if newest_update > last_update[path_str]:
                    print('Shader file was updated: ', file.stem)
                    last_update[path_str] = newest_update
                    need_analyze = True

    if need_analyze:
        # Hack for force redraw the View3D...
        camera_select = bpy.data.objects['cam0'].select_get()
        bpy.data.objects['cam0'].select_set(camera_select)

    return INTERVAL

def watch(context):
    global need_analyze
    if not sgd.is_ignoring_watcher:
        blui_set_boolean_orders = []
        temp_boolean_methods = []
        has_need = 0
        fixed_num = 0
        for obj in bpy.data.objects:
            if obj.ernst.is_ernst_obj and obj.type != 'LIGHT':
                has_need += 1
                if obj.hide_select:
                    fixed_num += 1
                if 'SDF_' in obj.ernst.type:
                    temp_boolean_methods.append(obj.ernst.shader_proxy.props.boolean)
                    blui_set_boolean_orders.append(obj.ernst.shader_proxy.props.boolean_order)

        # A number of objects or A number of fixed objects was changed...
        if need_analyze == False:
            if sgd.fixed_num != fixed_num:
                print(':: COMPILE: A number of objects or A number of fixed objects was changed... ::')
                need_analyze = True

        # boolean method was changed...
        if need_analyze == False:
            for i in range(len( sgd.boolean_methods)):
                if sgd.boolean_methods[i] != temp_boolean_methods[i]:
                    print(':: COMPILE: boolean method was changed... ::')
                    need_analyze = True

        # boolean order was changed...
        if need_analyze == False:
            for j in range(len( sgd.boolean_orders)):
                if sgd.boolean_orders[j] != blui_set_boolean_orders[j]:
                    print(':: COMPILE: boolean order was changed... ::')
                    need_analyze = True

        if need_analyze:
            print('shadergen.process(): shaderizer_watcher.watch')
            shadergen.process(context)

