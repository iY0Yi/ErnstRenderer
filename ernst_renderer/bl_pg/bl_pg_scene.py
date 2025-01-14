import bpy
from bpy.types import PropertyGroup
from ..bl_ot.shadergen.shaderizer import shaderizer_watcher

class ERNST_PG_Scene(PropertyGroup):
    enable_edit_trvs : bpy.props.BoolProperty(name='Enable Editing TRVs', default = True, update=shaderizer_watcher.check)
