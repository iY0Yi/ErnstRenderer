import bpy
from bpy.types import Panel

from ..bl_mt.bl_mt_boolean import *
from ..bl_mt.bl_mt_pmodifier import *
from ..bl_mt.bl_mt_sdf3d import *
from ..bl_ot.bl_ot_boolean import *
from ..bl_ot.bl_ot_gui import *
from ..bl_ot.bl_ot_pmodifier import *
from ..bl_ot.bl_ot_sdf3d import *

def get_icon_by_type(type):
	if type == 'LIGHT_DIRECTIONAL': return 'LIGHT_SUN'
	if type == 'Camera': return 'CAMERA_DATA'
	return 'CAMERA_DATA'

class ERNST_PT_Modeling(Panel):
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	bl_label = 'Modeling'
	bl_category = 'Ernst'
	COMPAT_ENGINES = {'ERNST'}

	def draw_multi_editor(self, context, col):
		num_ernst_obj = 0
		num_ernst_prim = 0
		for obj in context.selected_objects:
			if obj.ernst.is_ernst_obj:
				num_ernst_obj+=1
				if 'SDF_' in obj.ernst.type:
					num_ernst_prim+=1

		if context.active_object != None and context.active_object.ernst.type == 'CONTROL_POINT' and num_ernst_obj>=2:
			row = col.row()
			row.label(text='Parenting:')
			row = col.row()
			row.operator(ERNST_OT_SetParent.bl_idname, text = 'Set ERNST Parent', icon='DECORATE_LINKED')

		if num_ernst_prim>=2:
			row = col.row()
			row.label(text='Boolean(Batch edit)')
			row = col.row()
			row.menu(ERNST_MT_BooleanMulti.bl_idname, text='Set methods:')
			row = col.row(align=True)
			row.prop(context.screen.ernst, 'blui_set_boolean_order', text='Set orders:')
			row.operator(ERNST_OT_Set_Multi_Csg_Orders.bl_idname, text = '', icon = 'TRIA_RIGHT')
			row = col.row(align=True)
			row.prop(context.screen.ernst, 'blui_offset_boolean_order', text='Offset orders:')
			row.operator(ERNST_OT_Offset_Multi_Csg_Orders.bl_idname, text = '', icon = 'TRIA_RIGHT')
			row = col.row(align=True)
			row.operator('ernst.boolean_order_multi_decrement', text = 'Dec orders', icon = 'REMOVE')
			row.operator('ernst.boolean_order_multi_increment', text = 'Add orders', icon = 'ADD')
		col.separator()

	def draw(self, context):
		layout = self.layout
		layout.use_property_split = False

		col = layout.column(align=False)
		row = col.row(align=True)
		row.label(text='Uniform Variables:')
		row = col.row(align=True)
		row.operator(ERNST_OT_Lock_ERNST_Objects.bl_idname, text = 'Lock', icon = 'LOCKED')
		row.operator(ERNST_OT_Unlock_ERNST_Objects.bl_idname, text = 'Unlock', icon = 'UNLOCKED')

		row = col.row(align=True)
		row.label(text='Transform Variables:')
		row = col.row(align=True)
		is_editing = bpy.context.scene.ernst.enable_edit_trvs
		if is_editing:
			row.prop(bpy.context.scene.ernst, 'enable_edit_trvs', text='Editing', icon = 'GREASEPENCIL')
		else:
			row.prop(bpy.context.scene.ernst, 'enable_edit_trvs', text='Fixed', icon = 'LINK_BLEND')

		col = layout.column(align=False)
		if len(context.selected_objects) > 0:

			self.draw_multi_editor(context, col)

			sdfs = []
			for obj in context.selected_objects:
				if 'SDF_' in obj.ernst.type:
					sdfs.append(obj)
			sdfs.sort(key=lambda obj: obj.ernst.shader_proxy.props.boolean_order, reverse=False)

			for sdf in sdfs:
				box = col.box()
				sdf.ernst.shader_proxy.draw_gui(context, box)
				if sdf.ernst.type != 'SDF_3D_INSTANCE':
					material = sdf.material_slots[0].material
					material.ernst.shader_proxy.draw_gui(context, box)

			for obj in context.selected_objects:
				if not 'SDF_' in obj.ernst.type:
					box = col.box()
					obj.ernst.shader_proxy.draw_gui(context, box)

		else:
			row = col.row()
			row.label(text='Select SDF objects.', icon = 'QUESTION')
