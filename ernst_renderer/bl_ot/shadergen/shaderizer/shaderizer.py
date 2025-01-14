import bpy

from ....util.map import Map
from ....util.util import *
from .. import shadergen_data as sgd
from ..shadergen_util import *
from .shaderizer_material import *
from .shaderizer_object import *
from .shaderizer_scene import *
from .shaderizer_trvs import *
from . import shaderizer_trvs

def gather_objs():
  sgd.in_scene_sdfs = []
  sgd.in_scene_cps = []
  sgd.in_collection_sdfs = {}
  sgd.in_collection_cps = {}
  sgd.materials = []

  for obj in bpy.data.objects:

    if is_sdf_in_scene(obj) and is_renderable(obj):
      sgd.in_scene_sdfs.append(obj)
      if obj.instance_type != 'COLLECTION':
        sgd.materials.append(obj.material_slots[0].name)

    if is_cp_in_scene(obj) and is_renderable(obj):
      sgd.in_scene_cps.append(obj)

    if is_sdf_in_collection(obj) and is_renderable(obj):
      collection_name = get_collection_name(obj)
      if (collection_name in sgd.used_collections):
        if (collection_name in sgd.in_collection_sdfs)==False:
          sgd.in_collection_sdfs[collection_name] = Map({'name':collection_name, 'code':'', 'order':1, 'objs':[]})
        sgd.in_collection_sdfs[collection_name].objs.append(obj)
        if obj.instance_type != 'COLLECTION':
          sgd.materials.append(obj.material_slots[0].name)

    if is_cp_in_collection(obj) and is_renderable(obj):
      collection_name = get_collection_name(obj)
      if (collection_name in sgd.used_collections):
        if (collection_name in sgd.in_collection_cps)==False:
          sgd.in_collection_cps[collection_name] = Map({'name':collection_name, 'code':'', 'order':1, 'objs':[]})
        sgd.in_collection_cps[collection_name].objs.append(obj)

def gather_used_collectons(coll_name):
  for obj in bpy.data.collections[coll_name].objects:
    if obj.ernst.is_ernst_obj and obj.instance_type == 'COLLECTION' and is_renderable(obj):
      if not obj.instance_collection.name in sgd.used_collections:
        sgd.used_collections.append(obj.instance_collection.name)
        gather_used_collectons(obj.instance_collection.name)

def gather_force_export_collectons():
  for coll in bpy.data.collections:
    if coll.ernst.force_export_function and not(coll.name in sgd.used_collections):
      # print('gather_force_export_collectons()>coll.name: ', coll.name)
      sgd.used_collections.append(coll.name)

def sort_sdfs_by_boolean_orders(sdfs):
	sdfs.sort(key=lambda sdf: sdf.ernst.shader_proxy.props.boolean_order, reverse=False)
	for i in range(0, len(sdfs)):
		sdfs[i].ernst.shader_proxy.props.render_order = i
	return sdfs

def sort_cps_by_calculation_orders(cps):
	for cp in cps:
		cp.ernst.shader_proxy.props.calc_order = 0

		ITERATE_LIMIT = 10
		iterate_count = 0

		parent_obj = cp.parent
		has_parent_cp = True

		while has_parent_cp:
			if parent_obj != None:
				if parent_obj.ernst.type == 'CONTROL_POINT':
					has_parent_cp = True
					cp.ernst.shader_proxy.props.calc_order+=1
				else:
					has_parent_cp = False
				parent_obj = parent_obj.parent

			else:
				has_parent_cp = False

			iterate_count += 1
			if iterate_count >= ITERATE_LIMIT: break

	cps.sort(key=lambda cp: cp.ernst.shader_proxy.props.calc_order, reverse=False)
	for i in range(0, len(cps)):
		cps[i].ernst.shader_proxy.props.calc_order = i

	return cps

def sort_objs():
  sgd.in_scene_sdfs = sort_sdfs_by_boolean_orders(sgd.in_scene_sdfs)
  sgd.in_scene_cps = sort_cps_by_calculation_orders(sgd.in_scene_cps)

  for key, data in sgd.in_collection_sdfs.items():
    sgd.in_collection_sdfs[key].objs = sort_sdfs_by_boolean_orders(data.objs)

  for key, data in sgd.in_collection_cps.items():
    sgd.in_collection_cps[key].objs = sort_cps_by_calculation_orders(data.objs)

def get_uber_scripts_info_by_type(type):
  file_names = getFileNames(f'uber_scripts/{type}')
  info = {}
  for name in file_names:
    info[name] = Map({})
    info[name].type = type
    info[name].file_name = name
    info[name].used_count = 0
  return info

def get_shader_code_cameras():
  code = ''
  for obj in bpy.data.objects:
    if obj.ernst.type == 'CAMERA':
      code += obj.ernst.shader_proxy.get_shader_code(None)
  return code

def get_uniform_code_cameras():
  code = ''
  for obj in bpy.data.objects:
    if obj.ernst.type == 'CAMERA':
      code += obj.ernst.shader_proxy.get_uniform_dec_code()
  return code

def get_shader_code_lights():
  code = ''
  for obj in bpy.data.objects:
    if obj.ernst.type == 'LIGHT_DIRECTIONAL':
      code += obj.ernst.shader_proxy.get_shader_code(None)
  return code

def get_uniform_lights_code():
  code = ''
  for obj in bpy.data.objects:
    if obj.ernst.type == 'LIGHT_DIRECTIONAL':
      code += obj.ernst.shader_proxy.get_uniform_dec_code()
  return code

def get_shader_code_materials():
  code_defs = ''
  code_params = ''
  for material in bpy.data.materials:
    if material.ernst.is_ernst_mat:
      code_def, code_param = material.ernst.shader_proxy.get_shader_code()
      code_defs += code_def
      code_params += code_param
  return code_defs, code_params

def get_uniform_code_materials():
  if sgd.is_exporting:
    return ''

  code = ''
  for material in bpy.data.materials:
    if material.ernst.is_ernst_mat:
      code += material.ernst.shader_proxy.get_uniform_dec_code()
  return code

def reset_shader_data():
  sgd.is_1st_material = True
  sgd.fixed_num = 0
  sgd.bool_uberscript_txt_name = []
  sgd.used_collections = []
  sgd.TRVs_objs = Map({'trans':{}, 'rot':{}})
  sgd.code_uber_scripts_info = {}
  sgd.code_uber_scripts_info['argument'] = get_uber_scripts_info_by_type('argument')
  sgd.code_uber_scripts_info['boolean'] = get_uber_scripts_info_by_type('boolean')
  sgd.code_uber_scripts_info['inline'] = get_uber_scripts_info_by_type('inline')
  sgd.code_uber_scripts_info['ik'] = get_uber_scripts_info_by_type('ik')
  sgd.code_uber_scripts_info['pmod'] = get_uber_scripts_info_by_type('pmod')
  sgd.code_uber_scripts_info['sdf3d'] = get_uber_scripts_info_by_type('sdf3d')
  sgd.code_uniform = ''
  sgd.code_scene = ''
  sgd.code_raymarch_buf_init_dec = ''
  sgd.code_raymarch_buf_init_fnc = ''
  shaderizer_trvs.trvs_id = 0


def analyze_blender_data():
  reset_shader_data()
  gather_used_collectons('Collection')
  gather_force_export_collectons()
  gather_objs()
  sort_objs()

  sgd.code_raymarch_buf_init_fnc += get_shader_code_cameras()
  sgd.code_raymarch_buf_init_fnc += get_shader_code_lights()
  sgd.code_collections = get_shader_code_cached_collections()
  sgd.code_collections += get_shader_code_collections()
  sgd.code_uniform += get_uniform_code_primitives(sgd.in_scene_cps)
  sgd.code_scene += get_shader_code_primitives(sgd.in_scene_cps)
  analyze_trvs()
  sgd.code_uniform += get_uniform_code_primitives(sgd.in_scene_sdfs)
  sgd.code_scene += get_shader_code_primitives(sgd.in_scene_sdfs)
  sgd.code_uniform += get_uniform_code_materials()
  sgd.code_material_dec, sgd.code_material_params = get_shader_code_materials()

  # Count used numbers of UberScripts
  # for uberscript_type in sgd.code_uber_scripts_info:
  #   code_list = sgd.code_uber_scripts_info[uberscript_type]
  #   print(f'{uberscript_type}----------------------------------------------------------------')
  #   for code_name in code_list:
  #     info = sgd.code_uber_scripts_info[uberscript_type][code_name]
  #     is_used = 'O' if info.used_count > 0 else 'X'
  #     print(f'{is_used} {info.file_name} ({info.used_count})')
