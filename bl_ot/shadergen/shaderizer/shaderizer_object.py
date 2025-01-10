from mathutils import Vector
from ..shadergen_util import *

def convert_axis(vec):
    return Vector((vec.x, vec.z, vec.y))

def get_world_pos(obj):
    loc, rot, scale = obj.matrix_world.decompose()
    return Vector((-loc[0], -loc[2], -loc[1]))

def get_local_pos(obj):
    e = obj.location
    return Vector((-e[0], -e[2], -e[1]))

def get_local_scale(obj):
    e = obj.scale
    return Vector((e[0], e[2], e[1]))

def get_world_scl(obj):
    loc, rot, scale = obj.matrix_world.decompose()
    return Vector((scale[0], scale[2], scale[1]))

def get_world_rot(obj):
    e = obj.matrix_world.to_euler('XZY')
    return Vector((e.x, e.z, e.y))

def get_local_rot(obj):
    e = obj.rotation_euler
    return Vector((e[0], e[2], e[1]))

def get_dimensions_xyz(sdf):
    dimensions = Vector((0, 0, 0))
    dimensions.x = sdf.dimensions[0]*0.5
    dimensions.y = sdf.dimensions[2]*0.5
    dimensions.z = sdf.dimensions[1]*0.5
    return dimensions

def get_dimensions_xy(sdf):
    dimensions = Vector((0, 0))
    dimensions.x = sdf.dimensions[0]*0.5
    dimensions.y = sdf.dimensions[2]*0.5
    return dimensions

def get_dimensions_yz(sdf):
    dimensions = Vector((0, 0))
    dimensions.x = sdf.dimensions[2]*0.5
    dimensions.y = sdf.dimensions[1]*0.5
    return dimensions

def get_dimensions_xz(sdf):
    dimensions = Vector((0, 0))
    dimensions.x = sdf.dimensions[0]*0.5
    dimensions.y = sdf.dimensions[1]*0.5
    return dimensions

def is_fixed(obj):
    return obj.hide_select or sgd.is_exporting

def is_collection_used(obj):
    if len(obj.users_collection)<1:
        return False
    if obj.users_collection[0].name in sgd.used_collections:
        return True
    if obj.users_collection[0].name == 'Collection':
        return True
    return False

def is_renderable(obj):
    hidden = obj.ernst.shader_proxy.props.hide
    parent_obj = obj.parent
    while parent_obj != None:
        if parent_obj.ernst.shader_proxy.props.hide:
            hidden = True
            break
        parent_obj = parent_obj.parent

    hidden = hidden or not is_collection_used(obj)
    return not hidden

def is_sdf_in_scene(obj):
    is_in_scene = get_collection_name(obj) == 'scene'
    is_sdobj = 'SDF_' in obj.ernst.type
    return obj.ernst.is_ernst_obj and is_in_scene and is_sdobj

def is_cp_in_scene(obj):
    is_in_scene = get_collection_name(obj) == 'scene'
    is_cp = obj.ernst.type == 'CONTROL_POINT'
    return obj.ernst.is_ernst_obj and is_in_scene and is_cp

def is_sdf_in_collection(obj):
    is_in_collection = get_collection_name(obj) != 'scene'
    is_sdobj = 'SDF_' in obj.ernst.type
    return obj.ernst.is_ernst_obj and is_in_collection and is_sdobj

def is_cp_in_collection(obj):
    is_in_collection = get_collection_name(obj) != 'scene'
    is_cp = obj.ernst.type == 'CONTROL_POINT'
    return obj.ernst.is_ernst_obj and is_in_collection and is_cp
