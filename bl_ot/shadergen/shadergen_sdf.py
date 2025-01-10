import bpy

from ...bl_ot.shadergen.shadergen_modules import *
from ...util.util import *
from . import shadergen_data as sgd
from .shadergen_util import *
from .shaderizer.shaderizer import *
from .shaderizer.shaderizer_object import *

def write_sdf_code():
    f_bl_sdf = sgd.dir_trk_bl_modules / 'bl_inc_sdf.glslinc'
    f_tmp_sdf = sgd.dir_trk_bl_templates / 'temp_inc_sdf.frag'
    with f_tmp_sdf.open() as f_tmp:
        code = f_tmp.read()

        sgd.code_funcs = ''
        code_temp = code
        code_temp = code_temp.replace('@BL_ERNST_FNCS', '')
        code_temp = code_temp.replace('@BL_COLLECTION_FNCS', sgd.code_collections)
        code_temp = code_temp.replace('@BL_MAP_FNC', sgd.code_scene)
        code_temp = shadergen_util.parse_for_includes(code_temp, f_tmp_sdf)
        for key, category in sgd.module_lib.items():
            if key != 'camera':
                for key, loader in category.items():
                    if key != 'PMOD_ROT_QUAT':
                        loader.check_used(code_temp)
                        sgd.code_funcs += loader.get_code()

        sgd.code_funcs += get_shader_code_uber_booleans()

        code = code.replace('@BL_ERNST_FNCS', sgd.code_funcs)
        code = code.replace('@BL_COLLECTION_FNCS', sgd.code_collections)
        code = code.replace('@BL_MAP_FNC', sgd.code_scene)
        with f_bl_sdf.open(mode='w') as f_bl:
            f_bl.write(code)