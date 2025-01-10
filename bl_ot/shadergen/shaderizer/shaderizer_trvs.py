import math
import string
import numpy as np
import bgl
import gpu
from mathutils import Vector
from ....util.map import Map
from .. import shadergen_data as sgd
from ..shadergen_util import *
from .shaderizer_material import *
from .shaderizer_object import *

use_texture = True
texture_id = None
uniform_name = 'txTRVs'
trvs_id = 0
texture = None

def addTRVobj(obj, trans_rot):
  global trvs_id
  sgd.TRVs_objs[trans_rot][obj.name] = trvs_id
  trvs_id+=1

def get_TRV_trans_name(obj):
  return er_var(obj.name)+'_TRV_trans'

def get_TRV_rot_name(obj):
  return er_var(obj.name)+'_TRV_rot'

def has_keyframes(obj):
  anim = obj.animation_data
  return anim and anim.action

# get keyframes of object list
# https://blender.stackexchange.com/questions/27889/how-to-find-number-of-animated-frames-in-a-scene-via-python
def get_keyframes_from_list(obj_list):
  keyframes = []
  for key in obj_list.keys():
    obj = bpy.data.objects[key]
    anim = obj.animation_data
    if anim and anim.action:
      for fcu in anim.action.fcurves:
        for keyframe in fcu.keyframe_points:
          x, y = keyframe.co
          if x not in keyframes:
            keyframes.append(math.ceil(x))
  return keyframes

def get_keyframes(obj):
  anim = obj.animation_data
  if anim and anim.action:
    tmp = Map({'tx':[], 'ty':[], 'tz':[], 'rx':[], 'ry':[], 'rz':[]})
    for i, fcu in enumerate(anim.action.fcurves):

      prefix = ''
      element = ''
      if fcu.data_path == 'location':
        prefix = 't'
      if fcu.data_path == 'rotation_euler':
        prefix = 'r'
      if fcu.array_index == 0:
        element = 'x'
      if fcu.array_index == 1:
        element = 'y'
      if fcu.array_index == 2:
        element = 'z'

      path = f'{prefix}{element}'

      for keyframe in fcu.keyframe_points:
        x, y = keyframe.co
        tmp[path].append(y)
    return tmp
  return None

# get keyframes of object list
def get_keyframes_vec4(obj):
  kfs = get_keyframes(obj)
  res = Map({'trans':[], 'rot':[]})
  for i in range(len(kfs.tx)):
    res.trans.append([-kfs.tx[i], -kfs.tz[i], -kfs.ty[i], 0])
    res.rot.append([kfs.rx[i], kfs.rz[i], kfs.ry[i], 0])
  return res

# get keyframes of object list
def get_keyframes_vec3(obj):
  kfs = get_keyframes(obj)
  res = Map({'trans':[], 'rot':[]})
  for i in range(len(kfs.tx)):
    res.trans.append(er_v3([-kfs.tx[i], -kfs.ty[i], -kfs.tz[i]]))
    res.rot.append(er_v3([kfs.rx[i], kfs.ry[i], kfs.rz[i]]))
  return res

def get_code(obj, trans_rot):
  global trvs_id, uniform_name, use_texture
  has_anim = has_keyframes(obj)

  if not has_anim:
    return ''

  coord_y = sgd.TRVs_objs[trans_rot][obj.name]
  if use_texture:
    # return f'getData(vec2(TRVsID, {coord_y})'
    return f'texelFetch(iChannel1, ivec2(TRVsID, {coord_y}), 0).xyz'
    # return f'texelFetch({uniform_name}, ivec2(TRVsID, {coord_y}), 0).xyz'
  else:
    return f'{get_TRV_trans_name(obj)}[int(TRVsID)]'

# def save_opengl_texture_as_image(texture_id, width, height, image_name, file_path):
#     # 1. OpenGLテクスチャからデータを読み取る
#     bgl.glBindTexture(bgl.GL_TEXTURE_2D, texture_id[0])
#     buffer = bgl.Buffer(bgl.GL_FLOAT, width * height * 4)
#     bgl.glGetTexImage(bgl.GL_TEXTURE_2D, 0, bgl.GL_RGBA, bgl.GL_FLOAT, buffer)

#     # 2. データをBlenderのImageオブジェクトに変換する
#     if image_name not in bpy.data.images:
#         bpy.data.images.new(image_name, width=width, height=height, alpha=True, float_buffer=True)
#     image = bpy.data.images[image_name]

#     # 画像のサイズが異なる場合、新しい画像を作成
#     if image.size[0] != width or image.size[1] != height:
#         bpy.data.images.remove(image)
#         bpy.data.images.new(image_name, width=width, height=height, alpha=True, float_buffer=True)
#         image = bpy.data.images[image_name]

#     image.pixels = [v for v in buffer]

#     # 3. Imageオブジェクトをファイルとして保存する
#     image.filepath_raw = file_path
#     image.file_format = 'OPEN_EXR'
#     image.save()

def analyze_trvs():
  global use_texture, texture_id, uniform_name, trvs_id, texture
  # count min/max frame
  min_frame_num = 1000
  max_frame_num = -1000
  keys_num = 0

  if sgd.TRVs_objs.trans:
    keys = get_keyframes_from_list(sgd.TRVs_objs.trans)
    keys_num = len(keys)
    if keys_num != 0:
      min_frame_num = keys[0]
      max_frame_num = keys[-1]

  if sgd.TRVs_objs.rot:
    keys = get_keyframes_from_list(sgd.TRVs_objs.rot)
    keys_num = max(keys_num, len(keys))
    if keys_num != 0:
      min_frame_num = min(min_frame_num, keys[0])
      max_frame_num = max(max_frame_num, keys[-1])

  f_tmp_trvs_data =sgd.dir_trk_bl_templates / 'temp_inc_trvs_data.frag'
  f_tmp_trvs =sgd.dir_trk_bl_templates / 'temp_inc_trvs.frag'
  f_bl_trvs_data =sgd.dir_trk_bl_modules / 'bl_inc_trvs_data.glslinc'
  f_bl_trvs =sgd.dir_trk_bl_modules / 'bl_inc_trvs.glslinc'

  is_editing = bpy.context.scene.ernst.enable_edit_trvs

  dbg_num_trvs = 0

  if not is_editing and use_texture and keys_num != 0:

    data = [None] * (len(sgd.TRVs_objs.trans)+len(sgd.TRVs_objs.rot))*keys_num

    for key in sgd.TRVs_objs.trans.keys():
      obj = bpy.data.objects[key]
      keys = get_keyframes_vec4(obj)
      for i in range(len(keys.trans)):
        data[sgd.TRVs_objs.trans[key]*keys_num+i]=keys.trans[i]
      dbg_num_trvs+=1

    for key in sgd.TRVs_objs.rot.keys():
      obj = bpy.data.objects[key]
      keys = get_keyframes_vec4(obj)
      for i in range(len(keys.rot)):
        data[sgd.TRVs_objs.rot[key]*keys_num+i]=keys.rot[i]
      dbg_num_trvs+=1

    # buffer = gpu.types.Buffer('FLOAT', len(data)*4, np.array([el for vec in data for el in vec], dtype=np.float32))
    # texture = gpu.types.GPUTexture(size=(keys_num, trvs_id), layers=0, is_cubemap=False, data=buffer, format='RGBA32F')

    bake_width_code = keys_num
    bake_height_code = trvs_id
    bake_vals_code = ''

    max_range = 0.0
    for id, vec in enumerate(data):
      max_range = max( max(abs(vec[0]), max(abs(vec[1]), abs(vec[2]) ) ), max_range)
    print('max_range: ', max_range)

    for id, vec in enumerate(data):
      bake_vals_code += packSnorm3x10(vec[0]*-1.0/max_range, vec[1]*-1.0/max_range, vec[2]*-1.0/max_range)
      # bake_vals_code += f'vec3({er_f(vec[0])},{er_f(vec[1])},{er_f(vec[2])})'
      if id!=len(data)-1:
        bake_vals_code += ','
        if (id+1)%keys_num == 0:
          bake_vals_code += '\n'

    with f_tmp_trvs_data.open() as fr:
      code = fr.read()
      code = string.Template(code)
      variables = {
          "width": bake_width_code,
          "height": bake_height_code,
          "vals": bake_vals_code,
          "max_range": max_range
      }
      code = code.substitute(variables)

      with f_bl_trvs_data.open(mode='w') as fw:
        fw.write(code)

    # Create a buffer
    # buffer = bgl.Buffer(bgl.GL_FLOAT, len(data)*4, [el for vec in data for el in vec])

    # If texture id doesn't exist, generate a new one
    # if texture_id is None:
    #   texture_id = bgl.Buffer(bgl.GL_INT, 1)
    #   bgl.glGenTextures(1, texture_id)

    # Bind the texture
    # bgl.glBindTexture(bgl.GL_TEXTURE_2D, texture_id[0])

    # Set texture parameters
    # bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_WRAP_S, bgl.GL_CLAMP_TO_EDGE)
    # bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_WRAP_T, bgl.GL_CLAMP_TO_EDGE)
    # bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER, bgl.GL_NEAREST)
    # bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MAG_FILTER, bgl.GL_NEAREST)

    # Upload data to GPU
    # bgl.glTexImage2D(bgl.GL_TEXTURE_2D, 0, bgl.GL_RGBA32F, keys_num, trvs_id, 0, bgl.GL_RGBA, bgl.GL_FLOAT, buffer)

    # Generate TRVs texture to use on oF
    # save_opengl_texture_as_image(texture_id, keys_num, trvs_id, 'tx_trvs', bpy.context.scene.render.filepath+'tx_trvs.exr')
    # save_opengl_texture_as_image(texture_id, keys_num, trvs_id, 'tx_trvs', str(sgd.dir_trk_root)+'/tx_trvs.exr')

  with f_tmp_trvs.open() as f_tmp:

    code = f_tmp.read()

    code = code.replace('@BL_IS_EDITING_TRVS', '1' if is_editing else '0')

    if is_editing or (not sgd.TRVs_objs.trans and not sgd.TRVs_objs.rot) or keys_num == 0 or use_texture:
    # if is_editing or (not sgd.TRVs_objs.trans and not sgd.TRVs_objs.rot) or keys_num == 0 or use_texture:
      code = code.replace('@BL_TRVS_NUM', str(keys_num))
      code = code.replace('@BL_TRVS_DEF', '')
      # if not is_editing and use_texture and keys_num != 0:
      #   code = code.replace('@BL_TRVS_DEF', f'uniform sampler2D {uniform_name};')
      # else:
      #   code = code.replace('@BL_TRVS_DEF', '')
    else:
      trans_code = ''
      rot_code = ''

      for key in sgd.TRVs_objs.trans.keys():
        obj = bpy.data.objects[key]
        trans_code += f'const vec3[TRVS_NUM] {get_TRV_trans_name(obj)} = vec3[](\n'
        keys = get_keyframes_vec3(obj)
        for i in range(len(keys.trans)):
          trans_code += f'{keys.trans[i]}{", " if i<(keys_num-1) else ""}\n'
        trans_code += ');\n'
        dbg_num_trvs+=1

      for key in sgd.TRVs_objs.rot.keys():
        obj = bpy.data.objects[key]
        rot_code += f'const vec3[TRVS_NUM] {get_TRV_rot_name(obj)} = vec3[](\n'
        keys = get_keyframes_vec3(obj)
        for i in range(len(keys.rot)):
          rot_code += f'{keys.rot[i]}{", " if i<(keys_num-1) else ""}\n'
        rot_code += ');\n'
        dbg_num_trvs+=1

      code = code.replace('@BL_TRVS_NUM', str(keys_num))
      code = code.replace('@BL_TRVS_DEF', trans_code + rot_code)

      print('TRVs[ keys: {keys_num} / num: {dbg_num_trvs}vec4s / total: {keys_num*dbg_num_trvs}comps]')

    with f_bl_trvs.open(mode='w') as f_bl:
      f_bl.write(code)

def bind_texture(shader):
  global use_texture, texture_id, uniform_name, trvs_id, texture
  pass
  # shader.uniform_sampler(uniform_name, texture)
  # if texture_id is not None:
  #   bgl.glActiveTexture(bgl.GL_TEXTURE0+texture_id[0])
  #   bgl.glBindTexture(bgl.GL_TEXTURE_2D, texture_id[0])
  #   uniform_int(shader, uniform_name, texture_id[0])