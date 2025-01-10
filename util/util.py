import os
import re
import shutil

from ..bl_ot.shadergen import shadergen_data as sgd

def readFile(path):
    with open(path, "r", encoding='utf-8') as file:
        return file.read()

def readUberScript(typ, name):
    if typ in sgd.code_uber_scripts_info.values(): # avoid adding uber uberscript
        sgd.code_uber_scripts_info[typ][name].used_count +=1
    return readFile(sgd.dir_trk_uber_scripts / typ / name)

def readLines(path):
    with open(path, mode='rt', encoding='utf-8') as f:
        return f.readlines()

def readUberScriptLines(typ, name):
    if typ in sgd.code_uber_scripts_info.values(): # avoid adding uber uberscript
        sgd.code_uber_scripts_info[typ][name].used_count +=1
    return readLines(sgd.dir_trk_uber_scripts / typ / name)

def extractFuncName(typ, name):
    lines = readUberScriptLines(typ, name)
    decline = ''
    try:
        decline = next(l for l in lines if 'float' in l and '(' in l and ')' in l and ',' in l)
        return re.findall(r'float\s*(.*?)\s*\(', decline)[0]
    except StopIteration:
        return None  # Handle case when no matching line is found

def getFileNames(typ):
    path = sgd.dir_trk_root / typ
    files = os.listdir(path)
    return [f for f in files if os.path.isfile(os.path.join(path, f))]

def drawUberScriptFileNames(layout, typ, op_class, prop):
    files_names = getFileNames(f'uber_scripts/{typ}')
    for filename in files_names:
        # fncname = extractFuncName(typ, filename)
        props = layout.operator(op_class.bl_idname, text=filename, icon='TEXT')
        props[prop] = filename

def touchDefaultFile(file_path):
    f_track = sgd.dir_trk_root / file_path
    if f_track.exists() == False:
        f_track.touch()
        f_tmplate = sgd.dir_addon / '_shadertrack_templates' / file_path
        with f_tmplate.open() as f_tmp:
            code = f_tmp.read()
            with f_track.open(mode='w') as f_track:
                f_track.write(code)

def touchFile(path):
    if path.exists() == False:
        path.touch()

def makeDir(path):
    try:
        if path.exists()==False:
            path.mkdir()
    except PermissionError:
        print('Permission error.')
    except FileNotFoundError:
        print('File not found.')

def cloneDirTree(src_path, dest_path):
    if dest_path.exists() == False:
        shutil.copytree(src_path, dest_path)

# https://blender.stackexchange.com/questions/78133/dynamic-enumproperty-values-changing-unexpectedly
# NEW CODE - Create a list to assign unique identifier to each mesh name
def find_or_add_file_id(name, cached_items):
    try:
        return next(item[0] for item in cached_items if item[1] == name)
    except StopIteration:
        new_id = max((item[0] for item in cached_items), default=-1) + 1
        cached_items.append((new_id, name))
        return new_id

def dynamic_enum_files(path, cached_items):
    names = getFileNames(path) + ['undefined']
    return [(name, name, "", find_or_add_file_id(name, cached_items))
            for name in names]


def is_armature_object(self, obj):
    if not (obj.ernst.is_ernst_obj and obj.ernst.type == 'CONTROL_POINT'):
        return False
    return any(pmod.get_pmod() and pmod.get_pmod().name == 'IKArmature'
              for pmod in obj.ernst.pmods.pmod)

def dynamic_enum_armature(cached_items):
    items = []
    for obj in bpy.data.objects:
        if not is_armature_object(None, obj):
            continue

        item_id = find_or_add_file_id(obj.name, cached_items)
        items.append((obj.name, obj.name, "", item_id))
    return items


# Draw Info on View3D
import blf
import bpy
import gpu
from gpu_extras.batch import batch_for_shader

if bpy.app.version < (4, 0, 0):
    shader_name = '2D_UNIFORM_COLOR'
else:
    shader_name = 'UNIFORM_COLOR'

shader = gpu.shader.from_builtin(shader_name)
# shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
# shader = gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')

def render_rect(x, y, w, h, base_col):
    shader.bind()
    shader.uniform_float("color", base_col)
    vertices = (
        (x, y), (x+w, y),
        (x, y+h), (x+w, y+h))

    indices = (
        (0, 1, 2), (2, 1, 3))
    batch = batch_for_shader(shader, 'TRIS', {"pos": vertices}, indices=indices)
    batch.draw(shader)

def draw_info(x, y, w, h, level, info):
    base_col = (1,0,0,1)
    if level=='INFO':
        base_col = (0,.5,0,1)
    margin = 1.;
    font_id = 0
    blf.size(font_id, h, 72)
    dim = blf.dimensions(font_id, info)
    offset = 2
    rw = dim[0] + dim[1]*margin*2+offset
    rh = dim[1] + dim[1]*margin*2
    render_rect(x, y, rw, rh, base_col)

    blf.position(font_id, offset+x+rh*margin*.5-dim[1]*.5, offset+y+rh*margin*.5-dim[1]*.5, 0)
    blf.size(font_id, h, 72)
    blf.color(font_id, 1, 1, 1, 1)
    blf.draw(font_id, info)

def get_child_names(obj, names=None):
    # Make recursive function more reusable
    if names is None:
        names = set()
    names.add(obj.name)
    for child in obj.children:
        get_child_names(child, names)
    return names

def select_hierarchy(obj):
    bpy.ops.object.select_all(action='DESELECT')
    names = get_child_names(obj)
    for name in names:
        bpy.data.objects[name].select_set(True)

def remove_hierarchy(obj):
    names = get_child_names(obj)
    for name in names:
        remove_obj_by_name(name)

def remove_obj(obj):
    objs = bpy.data.objects
    objs.remove(objs[obj.name], do_unlink=True)

def remove_obj_by_name(name):
    objs = bpy.data.objects
    objs.remove(objs[name], do_unlink=True)
