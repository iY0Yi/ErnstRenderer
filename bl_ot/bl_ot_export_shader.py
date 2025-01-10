import json
from pathlib import Path
from bpy.types import Operator

from ..util.util import *
from .shadergen import shadergen_data as sgd
from .shadergen.shadergen import *
from .shadergen.shadergen_util import *
from .shadergen.shaderizer.shaderizer_formatter import format_code
from .shadergen.shaderizer import shaderizer_trvs

code_common = ''

id_output_image = "4dfGRr"
id_output_buf_a = "4dXGR8"
id_output_buf_b = "XsXGR8"
id_output_buf_c = "4sXGR8"
id_output_buf_d = "XdfGR8"

path_thumb_buf_a = "/media/previz/buffer00.png"
path_thumb_buf_b = "/media/previz/buffer01.png"
path_thumb_buf_c = "/media/previz/buffer02.png"
path_thumb_buf_d = "/media/previz/buffer03.png"

output_image = {"channel": 0, "id": id_output_image}
output_buf_a = {"channel": 0, "id": id_output_buf_a}
output_buf_b = {"channel": 0, "id": id_output_buf_b}
output_buf_c = {"channel": 0, "id": id_output_buf_c}
output_buf_d = {"channel": 0, "id": id_output_buf_d}

def get_shadertoy_type_name(buffer):
    name = buffer.get_buffer_name()
    if name == 'image': return 'image', 'Image'
    if name == 'buffera': return 'buffer', 'Buffer A'
    if name == 'bufferb': return 'buffer', 'Buffer B'
    if name == 'bufferc': return 'buffer', 'Buffer C'
    if name == 'bufferd': return 'buffer', 'Buffer D'

def get_shadertoy_thumb_url(texture):
    if texture.buffer_name == 'buffer_a': return path_thumb_buf_a
    if texture.buffer_name == 'buffer_b': return path_thumb_buf_b
    if texture.buffer_name == 'buffer_c': return path_thumb_buf_c
    if texture.buffer_name == 'buffer_d': return path_thumb_buf_d

def get_shadertoy_buffer_id(texture):
    if texture.buffer_name == 'buffer_a': return id_output_buf_a
    if texture.buffer_name == 'buffer_b': return id_output_buf_b
    if texture.buffer_name == 'buffer_c': return id_output_buf_c
    if texture.buffer_name == 'buffer_d': return id_output_buf_d

def get_input(texture, i):
    if texture.buffer_name == 'none':
        return

    return{
        "channel": i,
        "type": "buffer",
        "id": get_shadertoy_buffer_id(texture),
        "filepath": get_shadertoy_thumb_url(texture),
        "sampler": {
            "filter": texture.interpolation,
            "wrap": texture.wrap,
            "vflip": "true",
            "srgb": "false",
            "internal": "byte"
        }
    }

def get_output(buffer):
    global output_image, output_buf_a, output_buf_b, output_buf_c, output_buf_d
    name = buffer.get_buffer_name()
    if name == 'image': return output_image
    if name == 'buffera': return output_buf_a
    if name == 'bufferb': return output_buf_b
    if name == 'bufferc': return output_buf_c
    if name == 'bufferd': return output_buf_d

def get_renderpass(buffer):
    global code_common
    if buffer.code_name == '':
        return

    print('get_renderpass()>', buffer.code_name)

    st_type, st_name = get_shadertoy_type_name(buffer)

    absolute_path = bpy.path.abspath(buffer.code_name)
    path = Path(absolute_path)

    with path.open() as f:
        code = f.read()
        code = parse_for_includes(code, path)
        # code = format_code(code)
        # code = code.strip()
        code = code.replace(code_common, '')

        inputs = []
        inputs.append(get_input(buffer.ichannel0, 0))
        inputs.append(get_input(buffer.ichannel1, 1))
        inputs.append(get_input(buffer.ichannel2, 2))
        inputs.append(get_input(buffer.ichannel3, 3))
        inputs = list(filter(None, inputs))
        return {
            "outputs": [get_output(buffer)],
            "inputs": inputs,
            "name": st_name,
            "description": "",
            "type": st_type,
            "code": code
        }

def get_common_pass():
    global code_common
    path = sgd.dir_trk_bl_modules / 'bl_inc_common.glslinc'
    with path.open() as file_common:
        code = file_common.read()
        code = parse_for_includes(code, path)
        # code = format_code(code)
        # code = code.strip()
        code_common = code
        return {
            "outputs": [],
            "inputs": [],
            "name": "Common",
            "description": "",
            "type": "common",
            "code": code
        }


json_template = {
    "ver": "0.1",
    "renderpass": [],
    "flags": {
        "mFlagVR": False,
        "mFlagWebcam": False,
        "mFlagSoundInput": False,
        "mFlagSoundOutput": False,
        "mFlagKeyboard": False,
        "mFlagMultipass": True,
        "mFlagMusicStream": False
    },
    "info": {
        "id": "-1",
        "date": "1358124981",
        "viewed": 0,
        "name": "",
        "username": "iY0Yi",
        "description": "",
        "likes": 0,
        "hasliked": 0,
        "tags": [],
        "published": 0
    }
}

def export_json():
    global json_template

    process_for_export(bpy.context)

    path_result_json = sgd.dir_trk_root / 'exported_shader.json'
    touchFile(path_result_json)

    image = bpy.context.workspace.ernst.image
    buf_a = bpy.context.workspace.ernst.buffer_a
    buf_b = bpy.context.workspace.ernst.buffer_b
    buf_c = bpy.context.workspace.ernst.buffer_c
    buf_d = bpy.context.workspace.ernst.buffer_d
    json_template['renderpass'] = []
    json_template['renderpass'].append(get_common_pass())
    json_template['renderpass'].append(get_renderpass(buf_d))
    json_template['renderpass'].append(get_renderpass(buf_c))
    json_template['renderpass'].append(get_renderpass(buf_b))
    json_template['renderpass'].append(get_renderpass(buf_a))
    json_template['renderpass'].append(get_renderpass(image))

    for renpass in json_template['renderpass']:
        if renpass is None: continue

        GUI_NAME = 'BluGui_1f'
        if bpy.data.objects.find(GUI_NAME)!=-1:
            holder = bpy.data.objects[GUI_NAME]
            for obj in holder.children:
                renpass['code'] = renpass['code'].replace(str(obj.children[0].name), er_f(obj.children[0].location.x))

        GUI_NAME = 'BluGui_2v'
        if bpy.data.objects.find(GUI_NAME)!=-1:
            holder = bpy.data.objects[GUI_NAME]
            for obj in holder.children:
                x = er_f(obj.location.x)
                y = er_f(obj.location.y)
                bake_code = f'vec2({x},{y})'
                renpass['code'] = renpass['code'].replace(str(obj.name), bake_code)

        GUI_NAME = 'BluGui_3v'
        if bpy.data.objects.find(GUI_NAME)!=-1:
            holder = bpy.data.objects[GUI_NAME]
            for obj in holder.children:
                x = er_f(obj.location.x)
                y = er_f(obj.location.y)
                z = er_f(obj.location.z)
                bake_code = f'vec3({x},{y},{z})'
                renpass['code'] = renpass['code'].replace(str(obj.name), bake_code)

        renpass['code'] = format_code(renpass['code'])
        renpass['code'] = renpass['code'].strip()

    json_template['renderpass'] = list(filter(None, json_template['renderpass']))
    with path_result_json.open(mode='w') as f_result_json:
        f_result_json.write(json.dumps(json_template))


class ERNST_OT_Export_JSON(Operator):
    bl_idname = 'ernst.export_json'
    bl_label = 'Write Shadertoy JSON.'
    bl_description = 'Write Shadertoy JSON.'
    bl_options = {'REGISTER'}

    @classmethod
    def poll(cls, context):
        return sgd.view_shading_type != 'MATERIAL' and sgd.view_shading_type != 'RENDERED'

    def execute(self, context):
        export_json()
        self.report({'INFO'}, 'JSON successfully exported.')
        return {'FINISHED'}
