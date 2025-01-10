# https://docs.blender.org/api/current/bpy.types.RenderEngine.html

bl_info = {
    'name': 'Ernst',
    'author': 'iY0Yi',
    'version': (0, 9),
    'blender': (3, 6, 1),
    'description': 'Ernst is a signed distanced field renderer.',
    'warning': '',
    'support': 'COMMUNITY',
    'wiki_url': '',
    'tracker_url': '',
    'category': 'Render'
}

import bpy

from ernst_renderer import auto_load

from .bl_mt import bl_mt_sdf3d

auto_load.init()

def register():
    auto_load.register()
    bpy.types.VIEW3D_MT_add.prepend(bl_mt_sdf3d.Menu_Add_General_Primitive)
    bpy.types.VIEW3D_MT_add.prepend(bl_mt_sdf3d.Menu_Add_SDF_2D)
    bpy.types.VIEW3D_MT_add.prepend(bl_mt_sdf3d.Menu_Add_SDF_3D)
    # bpy.types.VIEW3D_MT_add.prepend(bl_mt_sdf3d.Menu_Change_Primitive)

def unregister():
    auto_load.unregister()
    bpy.types.VIEW3D_MT_add.remove(bl_mt_sdf3d.Menu_Add_SDF_3D)
    bpy.types.VIEW3D_MT_add.remove(bl_mt_sdf3d.Menu_Add_SDF_2D)
    bpy.types.VIEW3D_MT_add.remove(bl_mt_sdf3d.Menu_Add_General_Primitive)
    # bpy.types.VIEW3D_MT_add.remove(bl_mt_sdf3d.Menu_Change_Primitive)


