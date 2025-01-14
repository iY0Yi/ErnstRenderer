import bpy
from bpy.props import PointerProperty

from .bl_pg.bl_pg_collection import ERNST_PG_CollectionProperties
from .bl_pg.bl_pg_global import ERNST_PG_GlobalVariables
from .bl_pg.bl_pg_material import ERNST_PG_Material
from .bl_pg.bl_pg_object import ERNST_PG_Object
from .bl_pg.bl_pg_project import ERNST_PG_ProjectProperties
from .bl_pg.bl_pg_render import ERNST_PG_RenderProperties
from .bl_pg.bl_pg_scene import ERNST_PG_Scene
from .bl_pg.bl_pg_world import ERNST_PG_WorldProperties

def register():
    bpy.types.WorkSpace.ernst = PointerProperty(type=ERNST_PG_ProjectProperties)
    bpy.types.World.ernst = PointerProperty(type=ERNST_PG_WorldProperties)
    bpy.types.Scene.render_ernst = PointerProperty(type=ERNST_PG_RenderProperties)
    bpy.types.Object.ernst = PointerProperty(type=ERNST_PG_Object)
    bpy.types.Material.ernst = PointerProperty(type=ERNST_PG_Material)
    bpy.types.Screen.ernst = PointerProperty(type=ERNST_PG_GlobalVariables)
    bpy.types.Collection.ernst = PointerProperty(type=ERNST_PG_CollectionProperties)
    bpy.types.Scene.ernst = PointerProperty(type=ERNST_PG_Scene)

def unregister():
    del bpy.types.World.ernst
    del bpy.types.Scene.render_ernst
    del bpy.types.WorkSpace.ernst
    del bpy.types.Object.ernst
    del bpy.types.Material.ernst
    del bpy.types.Screen.ernst
    del bpy.types.Collection.ernst
    del bpy.types.Scene.ernst
