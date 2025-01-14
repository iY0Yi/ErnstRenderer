import bpy

from ...bl_ot.shadergen.shadergen_modules import *
from ...util.util import *
from . import shadergen_data as sgd
from .shadergen_util import *
from .shaderizer.shaderizer import *
from .shaderizer.shaderizer_object import *


def write_init_code():
    f_bl_init = sgd.dir_trk_bl_modules / 'bl_inc_init.glslinc'
    f_tmp_init = sgd.dir_trk_bl_templates / 'temp_inc_init.frag'
    with f_tmp_init.open() as f_tmp:
        code = f_tmp.read()
        code = code.replace('@BL_INIT_DEC', sgd.code_raymarch_buf_init_dec)
        code = code.replace('@BL_INIT_FNC', sgd.code_raymarch_buf_init_fnc)
        with f_bl_init.open(mode='w') as f_bl:
            f_bl.write(code)
