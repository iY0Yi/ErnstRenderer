
import bpy
from bpy.types import Panel
import bl_ui

# RenderEngines also need to tell UI Panels that they are compatible with.
# We recommend to enable all panels marked as BLENDER_RENDER, and then
# exclude any panels that are replaced by custom panels registered by the
# render engine, or that are not supported.
def get_panels():
    exclude_panels = {
        'VIEWLAYER_PT_filter',
        'VIEWLAYER_PT_layer_passes',
        'VIEWLAYER_PT_freestyle',
        'VIEWLAYER_PT_freestyle_lineset',
        'VIEWLAYER_PT_freestyle_linestyle',
        'RENDER_PT_simplify',
        'RENDER_PT_simplify_viewport',
        'RENDER_PT_simplify_render',
        'RENDER_PT_simplify_greasepencil',
        'RENDER_PT_eevee_sampling',
        'RENDER_PT_eevee_indirect_lighting',
        'RENDER_PT_simplify_render',
        'RENDER_PT_eevee_ambient_occlusion',
        'RENDER_PT_eevee_bloom',
        'RENDER_PT_eevee_depth_of_field',
        'RENDER_PT_eevee_subsurface_scattering',
        'RENDER_PT_eevee_screen_space_reflections',
        'RENDER_PT_eevee_motion_blur',
        'RENDER_PT_eevee_volumetric',
        'RENDER_PT_eevee_hair',
        'RENDER_PT_eevee_shadows',
        'RENDER_PT_eevee_film',
        'RENDER_PT_simplify_viewport',
        'RENDER_PT_freestyle',
        'RENDER_PT_color_management',
        'RENDER_PT_stereoscopy',
        'RENDER_PT_stamp',
        'RENDER_PT_stamp_note',
        'RENDER_PT_stamp_burn',
        'RENDER_PT_post_processing',
        'RENDER_PT_eevee_performance',
        'MATERIAL_PT_preview',
        'EEVEE_MATERIAL_PT_settings',
        'EEVEE_WORLD_PT_surface',
        'EEVEE_WORLD_PT_volume',
        'DATA_PT_preview',
        'DATA_PT_light',
        'DATA_PT_EEVEE_light',
        'DATA_PT_EEVEE_shadow',
    }

    exclude_panels2 = [
        'COLLECTION_PT_instancing',
        'COLLECTION_PT_collection_flags',
        'COLLECTION_PT_lineart_collection',
    ]

    panels = []
    for panel in bpy.types.Panel.__subclasses__():
        if hasattr(panel, 'COMPAT_ENGINES') and ('BLENDER_RENDER' in panel.COMPAT_ENGINES or 'BLENDER_EEVEE' in panel.COMPAT_ENGINES):
            if panel.__name__ not in exclude_panels:
                panels.append(panel)
    return panels

# all panels in PROPERTIES > SCENE
collection_prop_panels = [cls for cls in bl_ui.properties_collection.classes
        if issubclass(cls, Panel)]

def register():
    global exclude_panels2
    for panel in get_panels():
        panel.COMPAT_ENGINES.add('ERNST')

    # unregister default scene props panels
    for cls in collection_prop_panels:
        if cls.is_registered:
            bpy.utils.unregister_class(cls)

def unregister():
    for panel in get_panels():
        if 'ERNST' in panel.COMPAT_ENGINES:
            panel.COMPAT_ENGINES.remove('ERNST')

    # unregister default collection props panels
    for cls in reversed(collection_prop_panels):
        if not cls.is_registered:
            bpy.utils.register_class(cls)