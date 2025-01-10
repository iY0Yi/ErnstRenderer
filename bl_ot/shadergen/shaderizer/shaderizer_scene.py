from .. import shadergen_data as sgd
from ..shadergen_util import *
from .shaderizer_material import *
from .shaderizer_object import *
from ....util.map import Map
def get_collection_dependencies(collection):
    dependencies = []

    # コレクション内のオブジェクトをチェック
    for obj in collection.objects:
        # オブジェクトがコレクションインスタンスの場合
        if obj.type == 'EMPTY' and obj.instance_collection:
            dependencies.append(obj.instance_collection)

    return dependencies

def set_gl_order(all_collections):
    order = 0
    processed = set()

    while len(processed) < len(all_collections):
        for collection in all_collections:
            if collection in processed:
                continue

            dependencies = get_collection_dependencies(collection)

            all_dependencies_processed = True
            for dep in dependencies:
                if dep not in processed:
                    all_dependencies_processed = False
                    break

            if all_dependencies_processed:
                collection["gl_order"] = order
                order += 1
                processed.add(collection)

    result = {}
    for col in all_collections:
        result[col.name] = col["gl_order"]
    return result

def get_shader_code_collections():
  for key, data in sgd.in_collection_sdfs.items():
    collection_data =  bpy.data.collections[key]
    data = collection_data.ernst
    offset = data.bounding_offset
    radius = data.bounding_sphere_radius
    size = data.bounding_box_size
    sgd.in_collection_sdfs[key].code  = f'''
vec4 {er_var(key)}(vec3 p){{
  float d = MAX_DIST;
  vec4 res = vec4(MAT_VOID, d);
    '''
    if data.enable_bounding:
      if data.bounding_type == 'sphere':
        sgd.in_collection_sdfs[key].code += f'''
    float bsd = length(p+{er_v3([offset[0],offset[1],offset[2]])}), bsr={er_f(radius*0.5)};
    if (bsd > 2.*bsr) return vec4(MAT_VOID, bsd-bsr);
        '''
      else:
        sgd.in_collection_sdfs[key].code += f'''
    float bsd = length(max(abs(p+{er_v3([offset[0],offset[1],offset[2]])})-{er_v3([size[0]*.5,size[1]*.5,size[2]*.5])},0.));
    if (bsd > .1) return vec4(MAT_VOID, bsd);
        '''

  for key, data in sgd.in_collection_cps.items():
    sgd.code_uniform += get_uniform_code_primitives(data.objs)
    sgd.in_collection_sdfs[key].code += get_shader_code_primitives(data.objs)

  for key, data in sgd.in_collection_sdfs.items():
    sgd.code_uniform += get_uniform_code_primitives(data.objs)
    sgd.in_collection_sdfs[key].code += get_shader_code_primitives(data.objs)
    sgd.in_collection_sdfs[key].code += '''
  return res;
}
    '''

  all_collections = list(bpy.data.collections)
  gl_orders = set_gl_order(all_collections)

  # Sort sdFunctions
  sdfnc_list = []
  for key, code_collection in sgd.in_collection_sdfs.items():
    if code_collection.name in sgd.used_collections:
      sdfnc_list.append(Map({'order':gl_orders[code_collection.name], 'code':code_collection.code}))

  sdfnc_list = sorted(sdfnc_list, key=lambda x:x['order'], reverse=False)

  code_sdfncs = ''
  for sdfnc in sdfnc_list:
    code_sdfncs += sdfnc.code

  return code_sdfncs

def get_shader_code_cached_collections():
  res = ''
  for key, data in sgd.in_collection_sdfs.items():
    collection_data =  bpy.data.collections[key]
    data = collection_data.ernst
    code = data.get_cached_dec_code()
    if not code in res:
      res += code
  return res

def get_shader_code_uber_booleans():
  uberscript_bool_lines = ''
  sgd.bool_uberscript_txt_name = list(set(sgd.bool_uberscript_txt_name))
  for txt_name in sgd.bool_uberscript_txt_name:
    uberscript_bool_lines+='\n'
    lines = readUberScriptLines('boolean', txt_name)
    uberscript_bool_lines += f'\n/*--- {txt_name} ---*/\n'
    for line in lines:
      uberscript_bool_lines+= line
    uberscript_bool_lines+='\n'
  return uberscript_bool_lines


def get_uniform_code_primitives(obj_list):
  code = ''
  for obj in obj_list:
    if is_renderable(obj):
      if is_fixed(obj):
        sgd.fixed_num += 1
      else:
        code += obj.ernst.shader_proxy.get_uniform_dec_code()
  return code

def get_shader_code_primitives(obj_list):
  sgd.is_1st_material = True
  code_scene = ''
  code_scene_lines = ''
  for obj in obj_list:
    if is_renderable(obj):
      code_scene += obj.ernst.shader_proxy.get_shader_code(obj_list)

      if obj.ernst.type != 'CONTROL_POINT':
        code_material = get_scene_material_change_code(obj_list, obj)
        if code_material != '' or obj.instance_type == 'COLLECTION':
          code_scene_lines += code_scene + code_material
          code_scene = ''
      else:
        code_scene_lines = code_scene

  return code_scene_lines
