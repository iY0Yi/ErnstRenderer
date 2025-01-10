
import bpy

from .bl_pg import bl_pg_project


def register():
    bpy.app.handlers.load_post.append(bl_pg_project.touch_project_files)
    bpy.app.handlers.save_post.append(bl_pg_project.touch_project_files)
    # bpy.types.VIEW3D_MT_add.prepend(bl_mt_primitive.Menu_Add_SDF_3D)
    # bpy.types.VIEW3D_MT_add.prepend(bl_mt_primitive.Menu_Change_Primitive)

def unregister():
    # bpy.types.VIEW3D_MT_add.remove(bl_mt_primitive.Menu_Add_SDF_3D)
    # bpy.types.VIEW3D_MT_add.remove(bl_mt_primitive.Menu_Change_Primitive)
    pass
