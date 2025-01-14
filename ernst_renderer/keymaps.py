import bpy

from .bl_ot.bl_ot_gui import ERNST_OT_Scale_Boolean_Value
from .bl_ot.bl_ot_render import ERNST_OT_RenderOF
from .bl_ot.bl_ot_util import ERNST_OT_InsertLocRotKeyframe

addon_keymaps = []

def register():
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name = 'Window',space_type='EMPTY', region_type='WINDOW')
    kmi = km.keymap_items.new(ERNST_OT_Scale_Boolean_Value.bl_idname, type = 'E', value = 'PRESS', ctrl=False, alt=False, shift=False)
    kmi = km.keymap_items.new(ERNST_OT_RenderOF.bl_idname, type = 'F12', value = 'PRESS', ctrl=False, alt=False, shift=False)
    kmi = km.keymap_items.new(ERNST_OT_InsertLocRotKeyframe.bl_idname, type = 'I', value = 'PRESS', ctrl=False, alt=False, shift=True)

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
        addon_keymaps.clear()
