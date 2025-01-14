from .. import shadergen_data as sgd
from ..shadergen_util import *
from .shaderizer_object import is_fixed
from ....bl_ot.shadergen import shadergen_ubo as ubo

def has_material(obj):
  if obj.ernst.type == 'SDF_3D_INSTANCE':
    if obj.ernst.shader_proxy.props.material:
      return True
    else:
      return False
  else:
    return True

def get_material(obj):
  if obj.ernst.type == 'SDF_3D_INSTANCE':
    return obj.ernst.shader_proxy.props.material
  else:
    return obj.material_slots[0].material

def get_material_root_obj(renderables, obj):

  if obj.ernst.shader_proxy.props.render_order==0:
    return obj
  else:
    mat_name = get_material(obj).name
    order = obj.ernst.shader_proxy.props.render_order-1
    while order>=0:
      if not has_material(renderables[order]):
        return renderables[order+1]
      if mat_name != get_material(renderables[order]).name:
        return renderables[order+1]
      order -= 1

  return renderables[0]

def get_scene_material_change_code(renderables, obj):
  order = obj.ernst.shader_proxy.props.render_order

  if not has_material(obj): # TODO: modify here
    sgd.is_1st_material = False
    return ''

  is_not_mat_last_prim = True
  is_not_last_prim = False

  if order < len(renderables)-1:
    is_not_last_prim = True

    if not has_material(renderables[order+1]): # TODO: modify here
      is_not_mat_last_prim = False
    else:
      material = get_material(renderables[order])
      curr_mat_name = material.name # TODO: modify here

      material = get_material(renderables[order+1])
      next_mat_name = material.name # TODO: modify here
      if curr_mat_name != next_mat_name:
        is_not_mat_last_prim = False

  if is_not_last_prim and is_not_mat_last_prim:
    return ''

  code_boolean = ''
  material_root_obj = get_material_root_obj(renderables, obj)
  bool_name = material_root_obj.ernst.shader_proxy.props.boolean
  if sgd.is_1st_material:
    bool_name = 'BOOL_UNI'

  if bool_name == 'UberScript' and obj.ernst.shader_proxy.props.bool_code_name == '':
    bool_name = 'BOOL_UNI'

  if bool_name == 'UberScript':
    code_boolean = obj.ernst.shader_proxy.props.get_uberscript_bool_info().name
  else:
    code_boolean = sgd.module_lib.boolean[bool_name].fncname
    sgd.module_lib.boolean[bool_name].used.v4 = True

  boolean_mix_strength = ''
  boolean_mix_step = ''
  u_names = material_root_obj.ernst.shader_proxy.get_uniform_names()

  if is_fixed(obj):
    if 'bool_val' in u_names:
      boolean_mix_strength = er_f(material_root_obj.ernst.shader_proxy.props.bool_value.value_num)
    if 'bool_step' in u_names:
      boolean_mix_step = er_f(material_root_obj.ernst.shader_proxy.props.bool_step.value_num)
  else:
    if ubo.enabled:
      if 'bool_val' in u_names:
        boolean_mix_strength = f'(ubo.{er_var(obj.name)}_boolean.x)'
      if 'bool_step' in u_names:
        boolean_mix_step = f'(ubo.{er_var(obj.name)}_boolean.y)'
    else:
      if 'bool_val' in u_names:
        boolean_mix_strength = u_names['bool_val']
      if 'bool_step' in u_names:
        boolean_mix_step = u_names['bool_step']

  code_mix = obj.ernst.shader_proxy.props.get_mix_code(code_boolean, boolean_mix_strength, boolean_mix_step)
  code_color = f'MAT_{er_var(get_material(obj).name).upper()}_COL' # TODO: modify here
  code_res = f'res = {code_boolean}(vec4({code_color}, d), res{code_mix});'

  ### Start: mirror pmodifiers
  if obj.parent != None and obj.parent.ernst.type == 'CONTROL_POINT':
    cpobj = obj.parent
    if len(cpobj.ernst.pmods.pmod)>0:
      for pmod in cpobj.ernst.pmods.pmod:
        if pmod != None and pmod.get_pmod() != None:
          pmod_name = pmod.get_pmod().name
          if pmod.get_pmod().visible:
            if pmod_name == 'Mirror Scale':
              ### See also: "pmodifier_mirror_scale.py"
              pmod_mirror_scale = pmod.get_pmod()
              target_cp_name = er_var(cpobj.name)
              u_name = target_cp_name+'_scale'
              code_res += f'res.w *= {er_f(pmod_mirror_scale.value) if is_fixed(obj) else u_name};'
            elif pmod_name == 'Round':
              ### See also: "pmodifier_round.py"
              pmod_round = pmod.get_pmod()
              target_cp_name = er_var(cpobj.name)
              u_name = pmod_round.get_uniform_names(target_cp_name, pmod_round.id)
              code_res += f'res.w -= {er_f(pmod_round.value) if is_fixed(obj) else u_name};'
  ### End: mirror pmodifiers

  sgd.is_1st_material = False
  code_res+= '\n'
  return code_res
