import bpy
from bpy.types import PropertyGroup

from ...bl_ot.shadergen import shadergen_data as sgd
from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen.shaderizer import shaderizer_watcher
from ...bl_ot.shadergen.shaderizer.shaderizer_object import is_fixed
from .sdf3d.sdf3d_sphere import ERNST_PG_SDF3D_Sphere
from .sdf3d.sdf3d_box import ERNST_PG_SDF3D_Box
from .sdf3d.sdf3d_cylinder import ERNST_PG_SDF3D_Cylinder
from .sdf3d.sdf3d_cylinder_pie import ERNST_PG_SDF3D_CylinderPie
from .sdf3d.sdf3d_plane import ERNST_PG_SDF3D_Plane
from .sdf3d.sdf3d_capsule import ERNST_PG_SDF3D_Capsule
from .sdf3d.sdf3d_ellipsoid import ERNST_PG_SDF3D_Ellipsoid
from .sdf3d.sdf3d_torus import ERNST_PG_SDF3D_Torus
from .sdf3d.sdf3d_torus_capped import ERNST_PG_SDF3D_TorusCapped
from .sdf3d.sdf3d_cone import ERNST_PG_SDF3D_Cone
from .sdf3d.sdf3d_cone_round import ERNST_PG_SDF3D_ConeRound
from .sdf3d.sdf3d_curve_quadratic import ERNST_PG_SDF3D_CurveQuadratic
from .sdf3d.sdf3d_uber import ERNST_PG_SDF3D_Uber
from .sdf3d.sdf3d_instance import ERNST_PG_SDF3D_Instance
from .sdf2d.sdf2d_circle import ERNST_PG_SDF_2D_Circle
from .sdf2d.sdf2d_box import ERNST_PG_SDF_2D_Box
from .sdf2d.sdf2d_uber import ERNST_PG_SDF2D_Uber
from .general.control_point import ERNST_PG_ControlPoint
from .general.light_directional import ERNST_PG_Light_Directional
from .general.camera import ERNST_PG_Camera

class ERNST_PG_PrimitiveManager(PropertyGroup):
    type : bpy.props.StringProperty(default='SDF_3D_SPHERE')

    sphere : bpy.props.PointerProperty(type=ERNST_PG_SDF3D_Sphere)
    box : bpy.props.PointerProperty(type=ERNST_PG_SDF3D_Box)
    cylinder : bpy.props.PointerProperty(type=ERNST_PG_SDF3D_Cylinder)
    cylinder_pie : bpy.props.PointerProperty(type=ERNST_PG_SDF3D_CylinderPie)
    plane : bpy.props.PointerProperty(type=ERNST_PG_SDF3D_Plane)
    capsule : bpy.props.PointerProperty(type=ERNST_PG_SDF3D_Capsule)
    ellipsoid : bpy.props.PointerProperty(type=ERNST_PG_SDF3D_Ellipsoid)
    torus : bpy.props.PointerProperty(type=ERNST_PG_SDF3D_Torus)
    torus_capped : bpy.props.PointerProperty(type=ERNST_PG_SDF3D_TorusCapped)
    cone : bpy.props.PointerProperty(type=ERNST_PG_SDF3D_Cone)
    cone_round : bpy.props.PointerProperty(type=ERNST_PG_SDF3D_ConeRound)
    curve_quadratic : bpy.props.PointerProperty(type=ERNST_PG_SDF3D_CurveQuadratic)
    uber_3d : bpy.props.PointerProperty(type=ERNST_PG_SDF3D_Uber)
    instance : bpy.props.PointerProperty(type=ERNST_PG_SDF3D_Instance)
    control_point : bpy.props.PointerProperty(type=ERNST_PG_ControlPoint)
    circle_2d : bpy.props.PointerProperty(type=ERNST_PG_SDF_2D_Circle)
    box_2d : bpy.props.PointerProperty(type=ERNST_PG_SDF_2D_Box)
    uber_2d : bpy.props.PointerProperty(type=ERNST_PG_SDF2D_Uber)
    light_directional : bpy.props.PointerProperty(type=ERNST_PG_Light_Directional)
    camera : bpy.props.PointerProperty(type=ERNST_PG_Camera)

    def get_shader_proxy(self):
        obj = self.id_data
        if obj.ernst.type == 'SDF_3D_SPHERE': return self.sphere
        if obj.ernst.type == 'SDF_3D_BOX': return self.box
        if obj.ernst.type == 'SDF_3D_CYLINDER': return self.cylinder
        if obj.ernst.type == 'SDF_3D_PLANE': return self.plane
        if obj.ernst.type == 'SDF_3D_CAPSULE': return self.capsule
        if obj.ernst.type == 'SDF_3D_ELLIPSOID': return self.ellipsoid
        if obj.ernst.type == 'SDF_3D_TORUS': return self.torus
        if obj.ernst.type == 'SDF_3D_TORUS_CAPPED': return self.torus_capped
        if obj.ernst.type == 'SDF_3D_CYLINDER_PIE': return self.cylinder_pie
        if obj.ernst.type == 'SDF_3D_CONE': return self.cone
        if obj.ernst.type == 'SDF_3D_CONE_ROUND': return self.cone_round
        if obj.ernst.type == 'SDF_3D_CURVE_QUADRATIC': return self.curve_quadratic
        if obj.ernst.type == 'SDF_3D_UBER': return self.uber_3d
        if obj.ernst.type == 'SDF_3D_INSTANCE': return self.instance
        if obj.ernst.type == 'CONTROL_POINT': return self.control_point
        if obj.ernst.type == 'SDF_2D_CIRCLE': return self.circle_2d
        if obj.ernst.type == 'SDF_2D_BOX': return self.box_2d
        if obj.ernst.type == 'SDF_2D_UBER': return self.uber_2d
        if obj.ernst.type == 'LIGHT_DIRECTIONAL': return self.light_directional
        if obj.ernst.type == 'CAMERA': return self.camera
        return self.sphere

    @property
    def props(self):
        pass

    @props.getter
    def props(self):
        return self.get_shader_proxy()

    def get_code_domain(self):
        return self.get_shader_proxy().get_code_domain()

    def get_code_position(self, u_name):
        return self.get_shader_proxy().get_code_position(u_name)

    def get_code_rotation(self, u_name):
        return self.get_shader_proxy().get_code_rotation(u_name)

    def get_uniform_names(self):
        return self.get_shader_proxy().get_uniform_names()

    def draw_gui(self, context, layout):
        self.get_shader_proxy().draw_gui(context, layout)

    def get_uniform_dec_code(self):
        obj = self.id_data
        if is_fixed(obj):
            return ''
        return self.get_shader_proxy().get_uniform_dec_code()

    def update_uniforms(self, shader):
        obj = self.id_data
        if is_fixed(obj):
            return
        self.get_shader_proxy().update_uniforms(shader)

    def get_shader_code(self, rendables):
        return self.get_shader_proxy().get_shader_code(rendables)
