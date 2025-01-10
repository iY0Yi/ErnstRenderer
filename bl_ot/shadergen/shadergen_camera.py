import bpy

from ...bl_ot.shadergen.shadergen_modules import *
from ...util.util import *
from . import shadergen_data as sgd
from .shadergen_util import *
from .shaderizer.shaderizer import *
from .shaderizer.shaderizer_object import *


def write_camera_code():
    f_tmp_camera = sgd.dir_trk_bl_templates / 'temp_inc_camera.frag'
    f_bl_camera = sgd.dir_trk_bl_modules / 'bl_inc_camera.glslinc'
    with f_tmp_camera.open() as f_tmp:
        code = f_tmp.read()

        module_camera_pers = sgd.module_lib.camera['CAMERA_PERS']
        module_camera_ortho = sgd.module_lib.camera['CAMERA_ORTHO']
        module_rot_quat = sgd.module_lib.pmod['PMOD_ROT_QUAT']
        module_camera_pers.used = True
        module_camera_ortho.used = True
        module_rot_quat.used = True

        if sgd.is_exporting:
            code = code.replace('@BL_CAMERA_FNCS', (module_rot_quat.get_code() + module_camera_pers.get_code()))
            code_camera_ex = f'{sgd.module_lib.camera["CAMERA_PERS"].fncname}(uv);'
            code = code.replace('@BL_CAMERA_CODE', code_camera_ex)
        else:
            code = code.replace('@BL_CAMERA_FNCS', (module_rot_quat.get_code() + module_camera_pers.get_code() + module_camera_ortho.get_code()))
            code_camera_bl = f'''
                if(cam0.is_perspective)
                    {module_camera_pers.fncname}(uv);
                else
                    {module_camera_ortho.fncname}(uv);
            '''
            code = code.replace('@BL_CAMERA_CODE', code_camera_bl)

        with f_bl_camera.open(mode='w') as f_bl:
            f_bl.write(code)
