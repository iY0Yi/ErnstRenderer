import bpy
from bpy.props import *
from bpy.types import PropertyGroup
from .primitive.general.material import ERNST_PG_Proxy_Material

class ERNST_PG_Material(PropertyGroup):
    is_ernst_mat      : bpy.props.BoolProperty(default = False)
    shader_proxy   : bpy.props.PointerProperty(type=ERNST_PG_Proxy_Material)
