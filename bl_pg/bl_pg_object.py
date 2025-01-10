import bpy

from ..bl_ot.shadergen.shaderizer import shaderizer_watcher
from .bl_pg_uberval import ERNST_PG_UberValueProperties
from .pmodifier.pmodifier import ERNST_PG_PModifier
from .primitive.primitive import ERNST_PG_PrimitiveManager

class ERNST_PG_Object(bpy.types.PropertyGroup):
	is_ernst_obj    : bpy.props.BoolProperty(default = False)
	type            : bpy.props.StringProperty(default = '')
	shader_proxy   : bpy.props.PointerProperty(type=ERNST_PG_PrimitiveManager)
	pmods           : bpy.props.PointerProperty(type=ERNST_PG_PModifier)
