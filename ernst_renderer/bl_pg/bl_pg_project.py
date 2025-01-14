import pathlib

import bpy
from bpy.app.handlers import persistent
from bpy.props import *
from bpy.types import PropertyGroup

from ..bl_ot.shadergen import shadergen_data as sgd
from ..bl_ot.shadergen.shadergen_util import *
from ..bl_ot.shadergen.shaderizer import shaderizer_watcher
from ..util.util import *
from .buffer.bl_pg_buffer import ERNST_PG_Buffer

from pathlib import Path

def get_addon_root_directory():
    # このスクリプトファイルの絶対パスを取得し、Pathオブジェクトに変換
    current_file_path = Path(__file__).resolve()
    # アドオンのルートディレクトリを取得（親ディレクトリを辿る）
    addon_root_directory = current_file_path.parent.parent
    return addon_root_directory

@persistent
def touch_project_files(dummy):
    print('touch_project_files')
    if bpy.data.scenes['Scene'].render.engine == 'ERNST':
        sgd.dir_addon = get_addon_root_directory()
        sgd.dir_org_root = sgd.dir_addon / '_shadertrack_templates'
        sgd.dir_org_bl_templates = sgd.dir_org_root / 'bl_templates'
        sgd.dir_org_lib_modules = sgd.dir_org_root / 'lib_modules'
        sgd.dir_org_uber_scripts = sgd.dir_org_root / 'uber_scripts'

        sgd.dir_working = pathlib.Path(make_path_absolute(bpy.context.workspace.ernst.dir_working))
        sgd.dir_trk_root = sgd.dir_working / ('track')
        sgd.dir_trk_bl_templates = sgd.dir_trk_root / 'bl_templates'
        sgd.dir_trk_lib_modules = sgd.dir_trk_root / 'lib_modules'
        sgd.dir_trk_uber_scripts = sgd.dir_trk_root / 'uber_scripts'
        sgd.dir_trk_bl_modules = sgd.dir_trk_root / 'bl_modules'

        if sgd.dir_trk_root.exists():
            print(f"Directory '{sgd.dir_trk_root}' already exists. Skipping.")
            return

        makeDir(sgd.dir_working)
        makeDir(sgd.dir_trk_root)
        makeDir(sgd.dir_trk_bl_modules)
        cloneDirTree(sgd.dir_org_bl_templates, sgd.dir_trk_bl_templates)
        cloneDirTree(sgd.dir_org_lib_modules, sgd.dir_trk_lib_modules)
        cloneDirTree(sgd.dir_org_uber_scripts, sgd.dir_trk_uber_scripts)

        f_bl_common = sgd.dir_trk_bl_modules / 'bl_inc_common.glslinc'
        f_bl_camera = sgd.dir_trk_bl_modules / 'bl_inc_camera.glslinc'
        f_bl_init = sgd.dir_trk_bl_modules / 'bl_inc_init.glslinc'
        f_bl_sdf = sgd.dir_trk_bl_modules / 'bl_inc_sdf.glslinc'
        touchFile(f_bl_common)
        touchFile(f_bl_camera)
        touchFile(f_bl_init)
        touchFile(f_bl_sdf)

        touchDefaultFile('buf_renderer.frag')
        touchDefaultFile('buf_post_material.frag')
        touchDefaultFile('buf_post_rendered.frag')

def get_image_items(self, context):
    items = [(img.name, img.name, "") for img in bpy.data.images]
    items.append(("None", "None", ""))
    return items

class ERNST_PG_ProjectProperties(PropertyGroup):
    dir_working        : bpy.props.StringProperty(default = '//', subtype='FILE_PATH')
    framerate          : bpy.props.IntProperty(name = 'Set orders', min = 1, max = 60, default = 24, update=shaderizer_watcher.force_compile, options=set([]))
    hit_distance       : bpy.props.FloatProperty(name = 'Hit Distance', min = 0.00001, max = 1.0, default = 0.01, options=set([]))
    end_distance       : bpy.props.FloatProperty(name = 'End Distance', min = 10.0, max = 30000.0, default = 1000.0, options=set([]))
    max_marching_steps : bpy.props.IntProperty(name = 'Max Marching Steps', min = 10, max = 1500, default = 100, options=set([]))
    resolution_scale   : bpy.props.IntProperty(name = 'Resolution Scale', min = 1, max = 64, default = 1, options=set([]))
    print_code         : bpy.props.BoolProperty(name = 'export comment', description="Print Code at compiling", update=shaderizer_watcher.force_compile, default = False, options=set([]))
    canvas_mode   : bpy.props.BoolProperty(name='Canvas Mode', default=False)#, update=shaderizer_watcher.force_compile, options=set([]))
    canvas_offset_x : bpy.props.IntProperty(name='Canvas Offset X(%)', subtype='NONE', step=1, min = 0, max = 100, default=0)
    canvas_offset_y : bpy.props.IntProperty(name='Canvas Offset Y(%)', subtype='NONE', step=1, min = 0, max = 100, default=0)

    image : bpy.props.PointerProperty(type=ERNST_PG_Buffer, update=shaderizer_watcher.check)
    buffer_a : bpy.props.PointerProperty(type=ERNST_PG_Buffer, update=shaderizer_watcher.check)
    buffer_b : bpy.props.PointerProperty(type=ERNST_PG_Buffer, update=shaderizer_watcher.check)
    buffer_c : bpy.props.PointerProperty(type=ERNST_PG_Buffer, update=shaderizer_watcher.check)
    buffer_d : bpy.props.PointerProperty(type=ERNST_PG_Buffer, update=shaderizer_watcher.check)

    matcap: bpy.props.EnumProperty(
        name="Matcap",
        description="Select a Matcap Image",
        items=get_image_items
    )
