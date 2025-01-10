import bpy

from ...bl_ot.shadergen.shadergen_modules import *
from ...util.util import *
from . import shadergen_data as sgd
from .shadergen_util import *
from .shaderizer.shaderizer import *
from .shaderizer.shaderizer_object import *
from ...bl_ot.shadergen import shadergen_ubo as ubo

def write_common_code(context):
  f_tmp_common =sgd.dir_trk_bl_templates / 'temp_inc_common.frag'
  f_bl_common =sgd.dir_trk_bl_modules / 'bl_inc_common.glslinc'

  with f_tmp_common.open() as f_tmp:
    code = f_tmp.read()

    code = code.replace('@BL_UNIFORMS', sgd.code_uniform + sgd.uniform_code.render_settings)
    code = code.replace('@BL_MATERIAL_ID_DEC',sgd.code_material_dec)
    code = code.replace('@BL_MATERIAL_PARAMS',sgd.code_material_params)
    code = code.replace('@BL_FRAMERATE', er_f(context.workspace.ernst.framerate))
    if sgd.is_exporting:
      code = code.replace('@BL_RESOLUTION_SCALE', er_f(1))
      code = code.replace('@BL_HIT_DIST', er_f(context.workspace.ernst.hit_distance))
      code = code.replace('@BL_END_DIST', er_f(context.workspace.ernst.end_distance))
      code = code.replace('@BL_MAX_STEPS', er_i(context.workspace.ernst.max_marching_steps))
    else:
      if ubo.enabled:
        u_dist_min = 'ubo.renderSettings.x'
        u_dist_max = 'ubo.renderSettings.y'
        u_steps_max = 'int(ubo.renderSettings.z)'
        u_scale = 'ubo.renderSettings.w'
      else:
        u_dist_min = 'ufDistMin'
        u_dist_max = 'ufDistMax'
        u_steps_max = 'uiStepMax'
        u_scale = 'ufResScale'
      code = code.replace('@BL_RESOLUTION_SCALE', u_scale)
      code = code.replace('@BL_HIT_DIST', u_dist_min)
      code = code.replace('@BL_END_DIST', u_dist_max)
      code = code.replace('@BL_MAX_STEPS', u_steps_max)

    code_canvas_uniform = '\n'
    code_canvas_offset = 'return;'
    if not sgd.is_exporting:
      if ubo.enabled:
        code_canvas_uniform = ''
        ubo.add_vec4('canvas_offset')
        is_canvas_mode = f'bool({ubo.name("canvas_offset")}.z)'
        u_name = ubo.name('canvas_offset')+'.xy'
      else:
        u_name = 'canvas_offset'
        code_canvas_uniform = f'uniform bool is_canvas_mode;\n'
        code_canvas_uniform += f'uniform vec2 {u_name};\n'
        is_canvas_mode = 'is_canvas_mode'
      render = context.scene.render
      resx = math.floor(render.resolution_x * render.resolution_percentage/100)
      resy = math.floor(render.resolution_y * render.resolution_percentage/100)
      code_canvas_offset = f'''
      if({is_canvas_mode} == false) return;
        const vec2 FULL_RESOLUTION = vec2({resx},{resy});
        coord += {u_name}*FULL_RESOLUTION;
        coord /= FULL_RESOLUTION/res;
      '''

    code_canvas = f'''
    {code_canvas_uniform}
    void offsetCanvasCoord(inout vec2 coord, vec2 res){{
        {code_canvas_offset}
    }}
    '''
    code = code.replace('@CANVAS_MODE', code_canvas)

    code_world = ''
    wld = bpy.data.worlds[0]
    if sgd.is_exporting:
      code_world += f'#define AMB_COL {er_col(wld.ernst.amb_col)}\n'
      code_world += f'#define AMB_STRENGTH {er_f(wld.ernst.amb_strength)}\n'
      code_world += f'#define FOG_COL {er_col(wld.ernst.fog_col)}\n'
      code_world += f'#define FOG_START {er_f(wld.ernst.fog_start)}\n'
      code_world += f'#define FOG_POW {er_f(wld.ernst.fog_pow)}\n'
    else:
      if ubo.enabled:
        ubo.add_vec4('bl_wld_amb')
        ubo.add_vec4('bl_wld_fog_col')
        ubo.add_vec4('bl_wld_fog_start_pow')
        code_world += f'#define AMB_COL {ubo.name("bl_wld_amb")}.rgb\n'
        code_world += f'#define AMB_STRENGTH {ubo.name("bl_wld_amb")}.a\n'
        code_world += f'#define FOG_COL {ubo.name("bl_wld_fog_col")}.rgb\n'
        code_world += f'#define FOG_START {ubo.name("bl_wld_fog_start_pow")}.x\n'
        code_world += f'#define FOG_POW {ubo.name("bl_wld_fog_start_pow")}.y\n'
      else:
        code_world += 'uniform vec3 bl_wld_amb_col;\n'
        code_world += 'uniform float bl_wld_amb_strength;\n'
        code_world += 'uniform vec3 bl_wld_fog_col;\n'
        code_world += 'uniform float bl_wld_fog_start;\n'
        code_world += 'uniform float bl_wld_fog_pow;\n'
        code_world += '#define AMB_COL bl_wld_amb_col\n'
        code_world += '#define AMB_STRENGTH bl_wld_amb_strength\n'
        code_world += '#define FOG_COL bl_wld_fog_col\n'
        code_world += '#define FOG_START bl_wld_fog_start\n'
        code_world += '#define FOG_POW bl_wld_fog_pow\n'

    code = code.replace('@BL_WORLD_PARAMS', code_world)

    code_blugui = ''
    if not sgd.is_exporting:
      GUI_NAME = 'BluGui_1f'
      if bpy.data.objects.find(GUI_NAME)!=-1:
        holder = bpy.data.objects[GUI_NAME]
        for obj in holder.children:
          code_blugui += 'uniform float '+ str(obj.children[0].name) +';\n'

      GUI_NAME = 'BluGui_2v'
      if bpy.data.objects.find(GUI_NAME)!=-1:
        holder = bpy.data.objects[GUI_NAME]
        for obj in holder.children:
          code_blugui += 'uniform vec2 '+ str(obj.name) +';\n'

      GUI_NAME = 'BluGui_3v'
      if bpy.data.objects.find(GUI_NAME)!=-1:
        holder = bpy.data.objects[GUI_NAME]
        for obj in holder.children:
          code_blugui += 'uniform vec3 '+ str(obj.name) +';\n'

    if code.find('@BLU_GUI')==-1:
      code_blu = '// BLU_GUI\n//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n@BLU_GUI\n'
      code = code_blu + code
    code = code.replace('@BLU_GUI', code_blugui)

    with f_bl_common.open(mode='w') as f_bl:
      f_bl.write(code)
