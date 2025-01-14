import bpy
from bpy.types import Menu

from ..bl_ot import *
from ..util.util import *
from ..bl_ot.bl_ot_sdf3d import *

class ERNST_MT_Uber2D_CodeName(Menu):
    bl_idname = 'ERNST_MT_Uber2D_CodeName'
    bl_label = 'Code Name'

    def draw(self, context):
        layout = self.layout
        drawUberScriptFileNames(layout, 'sdf2d', ERNST_OT_ChooseCodeName, 'code_name')

class ERNST_MT_Uber3D_CodeName(Menu):
    bl_idname = 'ERNST_MT_Uber3D_CodeName'
    bl_label = 'Code Name'

    def draw(self, context):
        layout = self.layout
        drawUberScriptFileNames(layout, 'sdf3d', ERNST_OT_ChooseCodeName, 'code_name')

class ERNST_MT_PreCode(Menu):
    bl_idname = 'ERNST_MT_PreCode'
    bl_label = 'Code Name'

    def draw(self, context):
        layout = self.layout
        drawUberScriptFileNames(layout, 'inline', ERNST_OT_ChoosePreCode, 'code_pre')

class ERNST_MT_PostCode(Menu):
    bl_idname = 'ERNST_MT_PostCode'
    bl_label = 'Code Name'

    def draw(self, context):
        layout = self.layout
        drawUberScriptFileNames(layout, 'inline', ERNST_OT_ChoosePostCode, 'code_post')

class ERNST_MT_General_Primitive_Menu(Menu):
    bl_label = 'Add Generals'
    bl_idname = 'ERNST_MT_General_Primitive_Menu'
    COMPAT_ENGINES = {'ERNST'}

    def draw(self,context):
        layout = self.layout
        row = layout.row()
        col = row.column(align=True)
        col.operator(ERNST_OT_Add_ControlPoint.bl_idname, text = 'Control Position', icon = 'OBJECT_ORIGIN')
        col.operator(ERNST_OT_Add_IKArmature.bl_idname, text = 'IK Armature', icon = 'CON_KINEMATIC')
        layout.separator()
        row = layout.row()
        col = row.column(align=True)
        col.operator(ERNST_OT_Add_Light_Point.bl_idname, text = 'Light: Point', icon = 'LIGHT_POINT')
        col.operator(ERNST_OT_Add_Light_Sun.bl_idname, text = 'Light: Sun', icon = 'LIGHT_SUN')
        col.operator(ERNST_OT_Add_Light_Spot.bl_idname, text = 'Light: Spot', icon = 'LIGHT_SPOT')
        col.operator(ERNST_OT_Add_Light_Area.bl_idname, text = 'Light: Area', icon = 'LIGHT_AREA')
        layout.separator()
        row = layout.row()
        col = row.column(align=True)
        col.operator(ERNST_OT_Add_Camera.bl_idname, text = 'Camera', icon = 'CAMERA_DATA')

def Menu_Add_General_Primitive(self, context):
    if bpy.data.scenes['Scene'].render.engine == 'ERNST':
        layout = self.layout
        layout.menu(ERNST_MT_General_Primitive_Menu.bl_idname, icon = 'OBJECT_ORIGIN')

class ERNST_MT_SDF_3D_Menu(Menu):
    bl_label = 'Add 3D SDF'
    bl_idname = 'ERNST_MT_SDF_3D_Menu'
    COMPAT_ENGINES = {'ERNST'}

    def draw(self,context):
        layout = self.layout
        row = layout.row()
        col = row.column(align=True)
        col.operator(ERNST_OT_Add_Plane.bl_idname, text = 'Plane', icon = 'MESH_PLANE')
        col.operator(ERNST_OT_Add_Sphere.bl_idname, text = 'Sphere', icon = 'MESH_UVSPHERE')
        col.operator(ERNST_OT_Add_Ellipsoid.bl_idname, text = 'Ellipsoid', icon = 'MESH_UVSPHERE')
        col.operator(ERNST_OT_Add_Cube.bl_idname, text = 'Cube', icon = 'MESH_CUBE')
        col.operator(ERNST_OT_Add_Cylinder.bl_idname, text = 'Cylinder', icon = 'MESH_CYLINDER')
        col.operator(ERNST_OT_Add_Pie.bl_idname, text = 'Pie', icon = 'MESH_CYLINDER')
        col.operator(ERNST_OT_Add_Capsule.bl_idname, text = 'Capsule', icon = 'MESH_CAPSULE')
        col.operator(ERNST_OT_Add_Cone.bl_idname, text = 'Cone', icon = 'MESH_CONE')
        col.operator(ERNST_OT_Add_RoundCone.bl_idname, text = 'RoundCone', icon = 'MESH_CONE')
        col.operator(ERNST_OT_Add_CurveQ.bl_idname, text = 'CurveQ', icon = 'OUTLINER_DATA_CURVE')
        col.operator(ERNST_OT_Add_Torus.bl_idname, text = 'Torus', icon = 'MESH_TORUS')
        col.operator(ERNST_OT_Add_CappedTorus.bl_idname, text = 'CappedTorus', icon = 'MESH_TORUS')
        col.operator(ERNST_OT_Add_Uber3D.bl_idname, text = 'Uber3D', icon = 'TEXT')
        col.operator_menu_enum(ERNST_OT_Add_Instance.bl_idname, "collections", text=ERNST_OT_Add_Instance.bl_label)
        layout.separator()
        row = layout.row()
        col = row.column(align=True)
        col.operator(ERNST_OT_Add_Collection.bl_idname, icon='COLLECTION_NEW')


def Menu_Add_SDF_3D(self, context):
    if bpy.data.scenes['Scene'].render.engine == 'ERNST':
        layout = self.layout
        layout.menu(ERNST_MT_SDF_3D_Menu.bl_idname, icon = 'META_DATA')

class ERNST_MT_SDF_2D_Menu(Menu):
    bl_label = 'Add 2D SDF'
    bl_idname = 'ERNST_MT_SDF_2D_Menu'
    COMPAT_ENGINES = {'ERNST'}

    def draw(self,context):
        layout = self.layout
        row = layout.row()
        col = row.column(align=True)
        col.operator(ERNST_OT_Add_2D_Circle.bl_idname, text = 'Circle', icon = 'MESH_CIRCLE')
        col.operator(ERNST_OT_Add_2D_Box.bl_idname, text = 'Box', icon = 'META_PLANE')
        col.operator(ERNST_OT_Add_Uber2D.bl_idname, text = 'Uber2D', icon = 'TEXT')

def Menu_Add_SDF_2D(self, context):
    if bpy.data.scenes['Scene'].render.engine == 'ERNST':
        layout = self.layout
        layout.menu(ERNST_MT_SDF_2D_Menu.bl_idname, icon = 'OUTLINER_DATA_META')

class ERNST_MT_Change_Primitive_Menu(Menu):
    bl_label = 'Change Primitive'
    bl_idname = 'ERNST_MT_Change_Primitive_Menu'
    COMPAT_ENGINES = {'ERNST'}

    def draw(self,context):
        layout = self.layout
        row = layout.row()
        col = row.column(align=True)
        col.operator(ERNST_OT_ChangeTo_Plane.bl_idname, text = 'Plane', icon = 'MESH_PLANE')
        col.operator(ERNST_OT_ChangeTo_Sphere.bl_idname, text = 'Sphere', icon = 'MESH_UVSPHERE')
        col.operator(ERNST_OT_ChangeTo_Ellipsoid.bl_idname, text = 'Ellipsoid', icon = 'MESH_UVSPHERE')
        col.operator(ERNST_OT_ChangeTo_Cube.bl_idname, text = 'Cube', icon = 'MESH_CUBE')
        col.operator(ERNST_OT_ChangeTo_Cylinder.bl_idname, text = 'Cylinder', icon = 'MESH_CYLINDER')
        col.operator(ERNST_OT_ChangeTo_Pie.bl_idname, text = 'Pie', icon = 'MESH_CYLINDER')
        col.operator(ERNST_OT_ChangeTo_Capsule.bl_idname, text = 'Capsule', icon = 'MESH_CAPSULE')
        col.operator(ERNST_OT_ChangeTo_Cone.bl_idname, text = 'Cone', icon = 'MESH_CONE')
        col.operator(ERNST_OT_ChangeTo_RoundCone.bl_idname, text = 'RoundCone', icon = 'MESH_CONE')
        col.operator(ERNST_OT_ChangeTo_Torus.bl_idname, text = 'Torus', icon = 'MESH_TORUS')
        col.operator(ERNST_OT_ChangeTo_CappedTorus.bl_idname, text = 'CappedTorus', icon = 'MESH_TORUS')
        col.operator(ERNST_OT_ChangeTo_UberSDF.bl_idname, text = 'UberSDF', icon = 'TEXT')

def Menu_Change_Primitive(self, context):
    if bpy.data.scenes['Scene'].render.engine == 'ERNST':
        layout = self.layout
        layout.menu(ERNST_MT_Change_Primitive_Menu.bl_idname, icon = 'META_DATA')
