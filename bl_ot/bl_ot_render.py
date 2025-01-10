import json
import math
import subprocess
from concurrent.futures import ThreadPoolExecutor

import bpy
from bpy.types import Operator

from ..util.util import *
from .shadergen import shadergen_data as sgd
from .shadergen.shadergen import *
from .shadergen.shadergen_util import *
from .bl_ot_export_shader import export_json

def get_shadertoy_type_name(buffer):
    name = buffer.get_buffer_name()
    print('get_shadertoy_type_name: ', name)
    if name == 'image': return 'image', 'Image'
    if name == 'buffera': return 'buffer', 'Buffer A'
    if name == 'bufferb': return 'buffer', 'Buffer B'
    if name == 'bufferc': return 'buffer', 'Buffer C'
    if name == 'bufferd': return 'buffer', 'Buffer D'

def get_input(texture, i):
    if texture.buffer_name == 'none':
        return

    return{
        "channel": i,
        "source": texture.buffer_name,
        "sampler": {
            "filter": texture.interpolation,
            "wrap": texture.wrap
        }
    }

def get_renderpass(buffer):
    if buffer.code_name == '':
        return

    st_type, st_name = get_shadertoy_type_name(buffer)

    inputs = []
    inputs.append(get_input(buffer.ichannel0, 0))
    inputs.append(get_input(buffer.ichannel1, 1))
    inputs.append(get_input(buffer.ichannel2, 2))
    inputs.append(get_input(buffer.ichannel3, 3))
    inputs = list(filter(None, inputs))
    return {
        "name": st_name,
        "source_path": str(bpy.path.abspath('//'))+'track\\'+buffer.code_name,
        "inputs": inputs
    }

def render_callback(future):
    sgd.is_rendering = False
    print('Finished rendering in another thread.')

class ERNST_OT_RenderOF(Operator):
    bl_idname = 'ernst.render_in_of'
    bl_label = 'Render in openframeworks.'
    bl_description = 'Render in openframeworks.'
    bl_options = {'REGISTER'}
    COMPAT_ENGINES = {'ERNST'}

    def execute(self, context):
        if context.scene.render.engine == 'ERNST':
            sgd.is_rendering = True
            export_json()
            scene = context.scene
            render = scene.render
            render_ernst = scene.render_ernst
            pool = ThreadPoolExecutor(max_workers=1)
            args = '{0} -path {1} -w {2} -h {3} -tg {4} -fg {5} -aa {6} -frm {7} -trgt {8} -tlid {9} -flid {10} -out {11}'.format(
                'C:/Users/atsuh/Dropbox/dev/of_v0.11.0_vs2017_release/apps/shaderBoy/shaderCapture/bin/shaderCapture.exe',
                bpy.path.abspath('//'),
                math.floor(render.resolution_x * render.resolution_percentage/100),
                math.floor(render.resolution_y * render.resolution_percentage/100),
                render_ernst.tile_grid,
                render_ernst.file_grid,
                render_ernst.anti_aliasing,
                # scene.frame_current,
                1,
                render_ernst.target_mode,
                render_ernst.target_tile,
                render_ernst.target_file,
                render.filepath
                )
            future = pool.submit(subprocess.call, args, shell=True)
            future.run_type = "run_type"
            future.jid = "jid"
            future.add_done_callback(render_callback)
            pool.shutdown(wait=False)

            self.report({'INFO'}, 'Rendering started...')
        else:
            self.report({'WARNING'}, 'Ernst addon is active. Must be turn off the addon to render in Cycles or EEVEE.')
            print('Ernst addon is active. Must be turn off the addon to render in Cycles or EEVEE.')

        return {'FINISHED'}
