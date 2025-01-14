from threading import Timer
import bpy
from ...bl_ot.shadergen.shadergen_modules import init_module_loaders
from ...util import notification
from ...util.notification import Notification
from ...util.util import *
from . import shadergen_ubo as ubo
from . import shadergen_data as sgd
from .shadergen_common import write_common_code
from .shadergen_camera import write_camera_code
from .shadergen_init import write_init_code
from .shadergen_sdf import write_sdf_code
from .shadergen_util import *
from .shaderizer import shaderizer_watcher
from .shaderizer.shaderizer import analyze_blender_data
from .shaderizer.shaderizer_object import *
from ...bl_ot.shadergen.shaderizer.shaderizer import get_uniform_code_cameras
from ...bl_ot.shadergen.shaderizer.shaderizer import get_uniform_lights_code

def process(context):

  if not sgd.is_ignoring_watcher:

    init_module_loaders()

    if ubo.enabled:
      ubo.reset()

    notification.add(Notification('Analyzing...', 3, 0))
    analyze_blender_data()
    write_common_code(context)
    write_camera_code()
    write_init_code()
    write_sdf_code()
    if ubo.enabled:
      ubo.add_vec4('renderSettings')
    else:
      sgd.uniform_code.render_settings = '\n'
      sgd.uniform_code.render_settings +='uniform float ufDistMin;\n'
      sgd.uniform_code.render_settings +='uniform float ufDistMax;\n'
      sgd.uniform_code.render_settings +='uniform int uiStepMax;\n'
      sgd.uniform_code.render_settings +='uniform float ufResScale;\n'
    sgd.code_uniform_camera = get_uniform_code_cameras()
    sgd.code_uniform_lights = get_uniform_lights_code()

    notification.add(Notification('Analyzed.', 3, notification.OK))

    notification.add(Notification('Compiling shader files...', 3, 0))
    context.workspace.ernst.image.init_buffer('Image')
    context.workspace.ernst.buffer_a.init_buffer('BufferA')
    context.workspace.ernst.buffer_b.init_buffer('BufferB')
    context.workspace.ernst.buffer_c.init_buffer('BufferC')
    context.workspace.ernst.buffer_d.init_buffer('BufferD')

    if ubo.enabled:
      ubo.init()

    context.workspace.ernst.image.compile(context)
    context.workspace.ernst.buffer_a.compile(context)
    context.workspace.ernst.buffer_b.compile(context)
    context.workspace.ernst.buffer_c.compile(context)
    context.workspace.ernst.buffer_d.compile(context)

    if not sgd.is_exporting:
      shaderizer_watcher.update_filestamps()


def process_for_export(context):
  sgd.is_exporting = True
  process(context)
  sgd.is_exporting = False
