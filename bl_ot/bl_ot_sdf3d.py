import bpy
import math
from bpy.props import StringProperty
from bpy.types import Operator
from mathutils import Matrix, Vector
from .shadergen import shadergen_data as sgd
from .shadergen.shaderizer import shaderizer_watcher

import math
import bpy

# Auto smoothing
# https://blender.stackexchange.com/questions/316696/attributeerror-mesh-object-has-no-attribute-use-auto-smooth

def get_object_override(active_object, objects: list = None):

    if objects is None:
        objects = []
    else:
        objects = list(objects)

    if not active_object in objects:
        objects.append(active_object)

    assert all(isinstance(object, bpy.types.Object) for object in objects)

    return dict(
        selectable_objects = objects,
        selected_objects = objects,
        selected_editable_objects = objects,
        editable_objects = objects,
        visible_objects = objects,
        active_object = active_object,
        object = active_object,
    )

def has_smooth_by_angle(object: bpy.types.Object):
    for modifier in object.modifiers:

        if modifier.type != 'NODES':
            continue

        if modifier.node_group and 'Smooth by Angle' in modifier.node_group.name:
            return True

    return False

def do_auto_smooth(object: bpy.types.Object, angle = 30):

    if not hasattr(object, 'modifiers'):
        return

    if has_smooth_by_angle(object):
        return

    with bpy.context.temp_override(**get_object_override(object)):
        result = bpy.ops.object.modifier_add_node_group(asset_library_type='ESSENTIALS', asset_library_identifier="", relative_asset_identifier="geometry_nodes\\smooth_by_angle.blend\\NodeTree\\Smooth by Angle")
        if 'CANCELLED' in result:
            return

        modifier = object.modifiers[-1]
        modifier["Socket_1"] = True
        modifier["Input_1"] = math.radians(angle)
        object.update_tag()

id_3d_plane = 0
id_3d_sphere = 0
id_3d_ellipsoid = 0
id_3d_cube = 0
id_3d_sd_cube = 0
id_3d_cylinder = 0
id_3d_pie = 0
id_3d_capped_torus = 0
id_3d_capsule = 0
id_3d_cone = 0
id_3d_round_cone = 0
id_3d_quadratic_curve = 0
id_3d_torus = 0
id_3d_uber3d = 0

id_2d_circle = 0
id_2d_box = 0
id_2d_uber = 0

id_control_point = 0
id_ik_armature = 0
id_collection = 0
id_camera = 0
id_light = 0

def get_default_material():
    name = 'ERNST0'
    mat = bpy.data.materials.get(name)
    if mat is None:
        mat = bpy.data.materials.new(name=name)
        mat.ernst.is_ernst_mat = True
    return mat

def get_active_material():
    try:
        obj = bpy.data.objects[str(bpy.context.active_object.name)]
        ernst_type = obj.ernst.type
        if obj.ernst.is_ernst_obj and ernst_type != 'CONTROL_POINT' and ernst_type != 'LIGHT_DIRECTIONAL' and ernst_type != 'SDF_3D_INSTANCE':
            if obj.data.materials:
                return obj.data.materials[0]
        else:
            return get_default_material()
    except AttributeError:
        return get_default_material()

def set_material(obj, mat):
    if len(obj.data.materials)>0:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

def get_active_boolean_order():
    try:
        obj = bpy.data.objects[str(bpy.context.active_object.name)]
        ernst_type = obj.ernst.type
        if obj.ernst.is_ernst_obj and ernst_type != 'CONTROL_POINT' and ernst_type != 'LIGHT_DIRECTIONAL':
            return obj.ernst.shader_proxy.props.boolean_order
        else:
            return 0
    except AttributeError:
        return 0

def copy_transform(ob_org, ob_new):
    ob_new.matrix_basis = ob_org.matrix_world

def copy_parent(ob_org, ob_new):
    if ob_org.parent == None:
        return
    bpy.ops.object.select_all(action='DESELECT')
    parent = bpy.data.objects[ob_org.parent.name]
    ob_new.select_set(True)
    parent.select_set(True)
    bpy.context.view_layer.objects.active = parent
    bpy.ops.ernst.set_parent()

def copy_ernst_props(obj, newer):
    newer.ernst.shader_proxy.props.boolean = obj.ernst.shader_proxy.props.boolean
    newer.ernst.shader_proxy.props.boolean_order = obj.ernst.shader_proxy.props.boolean_order
    newer.ernst.shader_proxy.props.bool_value = obj.ernst.shader_proxy.props.bool_value
    newer.ernst.shader_proxy.props.bool_step = obj.ernst.shader_proxy.props.bool_step
    newer.ernst.shader_proxy.props.percentage = obj.ernst.shader_proxy.props.percentage
    newer.ernst.shader_proxy.props.code_pre = obj.ernst.shader_proxy.props.code_pre
    newer.ernst.shader_proxy.props.code_post = obj.ernst.shader_proxy.props.code_post
    newer.ernst.shader_proxy.props.code_name = obj.ernst.shader_proxy.props.code_name
    newer.ernst.shader_proxy.props.bool_value.type = obj.ernst.shader_proxy.props.bool_value.type
    newer.ernst.shader_proxy.props.bool_value.value_num = obj.ernst.shader_proxy.props.bool_value.value_num
    newer.ernst.shader_proxy.props.bool_value.value_code = obj.ernst.shader_proxy.props.bool_value.value_code
    newer.ernst.shader_proxy.props.bool_step.type = obj.ernst.shader_proxy.props.bool_step.type
    newer.ernst.shader_proxy.props.bool_step.value_num = obj.ernst.shader_proxy.props.bool_step.value_num
    newer.ernst.shader_proxy.props.bool_step.value_code = obj.ernst.shader_proxy.props.bool_step.value_code

def change_primitive(obj, new_type):

    sgd.is_ignoring_watcher = True

    if new_type == 'SDF_3D_SPHERE':
        bpy.ops.ernst.add_sphere()
    if new_type == 'SDF_3D_ELLIPSOID':
        bpy.ops.ernst.add_ellipsoid()
    if new_type == 'SDF_3D_CAPSULE':
        bpy.ops.ernst.add_capsule()
    if new_type == 'SDF_3D_BOX':
        bpy.ops.ernst.add_sd_cube()
    if new_type == 'SDF_3D_PLANE':
        bpy.ops.ernst.add_plane()
    if new_type == 'SDF_3D_CYLINDER':
        bpy.ops.ernst.add_cylinder()
    if new_type == 'SDF_3D_CYLINDER_PIE':
        bpy.ops.ernst.add_pie()
    if new_type == 'SDF_3D_TORUS':
        bpy.ops.ernst.add_torus()
    if new_type == 'SDF_3D_TORUS_CAPPED':
        bpy.ops.ernst.add_capped_torus()
    if new_type == 'SDF_3D_CONE':
        bpy.ops.ernst.add_cone()
    if new_type == 'SDF_3D_CONE_ROUND':
        bpy.ops.ernst.add_round_cone()
    if new_type == 'SDF_3D_UBER':
        bpy.ops.ernst.add_uber()
    if new_type == 'SDF_3D_INSTANCE':
        bpy.ops.ernst.instance_add()
    newer = bpy.context.view_layer.objects.active
    copy_transform(obj, newer)
    copy_parent(obj, newer)
    copy_ernst_props(obj, newer)

    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None
    obj.select_set(True)
    bpy.ops.object.delete(use_global=False)
    newer.select_set(True)
    bpy.context.view_layer.objects.active = newer

    max_scl_xy = max(newer.scale.x, newer.scale.y)
    max_scl_xyz = max(newer.scale.x, newer.scale.y, newer.scale.z)
    if new_type == 'SDF_3D_SPHERE'\
    or new_type == 'SDF_3D_TORUS'\
    or new_type == 'SDF_3D_TORUS_CAPPED':
        newer.scale.z = max_scl_xyz
        newer.scale.y = max_scl_xyz
        newer.scale.x = max_scl_xyz
    if new_type == 'SDF_3D_CAPSULE'\
    or new_type == 'SDF_3D_CYLINDER'\
    or new_type == 'SDF_3D_CYLINDER_PIE'\
    or new_type == 'SDF_3D_CONE'\
    or new_type == 'SDF_3D_CONE_ROUND'\
    or new_type == 'SDF_3D_PLANE':
        newer.scale.x = max_scl_xy
        newer.scale.y = max_scl_xy
    if new_type == 'SDF_3D_INSTANCE':
        newer.scale.x = 1
        newer.scale.y = 1
        newer.scale.z = 1


class ERNST_OT_ChangeTo_Plane(Operator):
    bl_idname = 'ernst.changeto_plane'
    bl_label = 'ernst: change to plane'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        change_primitive(obj, 'SDF_3D_PLANE')
        return {'FINISHED'}

class ERNST_OT_ChangeTo_Sphere(Operator):
    bl_idname = 'ernst.changeto_sphere'
    bl_label = 'ernst: change to sphere'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        change_primitive(obj, 'SDF_3D_SPHERE')
        return {'FINISHED'}

class ERNST_OT_ChangeTo_Ellipsoid(Operator):
    bl_idname = 'ernst.changeto_ellipsoid'
    bl_label = 'ernst: change to ellipsoid'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        change_primitive(obj, 'SDF_3D_ELLIPSOID')
        return {'FINISHED'}

class ERNST_OT_ChangeTo_Cube(Operator):
    bl_idname = 'ernst.changeto_cube'
    bl_label = 'ernst: change to cube'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        change_primitive(obj, 'SDF_3D_BOX')
        return {'FINISHED'}

class ERNST_OT_ChangeTo_Cylinder(Operator):
    bl_idname = 'ernst.changeto_cylinder'
    bl_label = 'ernst: change to cylinder'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        change_primitive(obj, 'SDF_3D_CYLINDER')
        return {'FINISHED'}

class ERNST_OT_ChangeTo_Pie(Operator):
    bl_idname = 'ernst.changeto_pie'
    bl_label = 'ernst: change to pie'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        change_primitive(obj, 'SDF_3D_CYLINDER_PIE')
        return {'FINISHED'}

class ERNST_OT_ChangeTo_Capsule(Operator):
    bl_idname = 'ernst.changeto_capsule'
    bl_label = 'ernst: change to capsule'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        change_primitive(obj, 'SDF_3D_CAPSULE')
        return {'FINISHED'}

class ERNST_OT_ChangeTo_Cone(Operator):
    bl_idname = 'ernst.changeto_cone'
    bl_label = 'ernst: change to cone'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        change_primitive(obj, 'SDF_3D_CONE')
        return {'FINISHED'}

class ERNST_OT_ChangeTo_RoundCone(Operator):
    bl_idname = 'ernst.changeto_roundcone'
    bl_label = 'ernst: change to roundcone'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        change_primitive(obj, 'SDF_3D_CONE_ROUND')
        return {'FINISHED'}

class ERNST_OT_ChangeTo_Torus(Operator):
    bl_idname = 'ernst.changeto_torus'
    bl_label = 'ernst: change to torus'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        change_primitive(obj, 'SDF_3D_TORUS')
        return {'FINISHED'}

class ERNST_OT_ChangeTo_CappedTorus(Operator):
    bl_idname = 'ernst.changeto_cappedtorus'
    bl_label = 'ernst: change to cappedtorus'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        change_primitive(obj, 'SDF_3D_TORUS_CAPPED')
        return {'FINISHED'}

class ERNST_OT_ChangeTo_UberSDF(Operator):
    bl_idname = 'ernst.changeto_uberscriptprim'
    bl_label = 'ernst: change to uberscriptprim'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        change_primitive(obj, 'SDF_3D_UBER')
        return {'FINISHED'}


def set_ernst_props(obj, ernst_type, mat):
    obj.ernst.type = ernst_type
    obj.ernst.is_ernst_obj = True
    obj.ernst.shader_proxy.props.boolean = 'BOOL_UNI_SMOOTH'
    obj.ernst.shader_proxy.props.boolean_order = get_active_boolean_order()
    obj.ernst.shader_proxy.props.bool_value.value_num = 0.01
    obj.ernst.shader_proxy.props.bool_step.value_num = 1
    obj.ernst.shader_proxy.props.percentage = 100.0
    obj.ernst.shader_proxy.props.code_pre = ''
    obj.ernst.shader_proxy.props.code_post = ''
    obj.ernst.shader_proxy.props.code_name = ''
    if ernst_type != 'SDF_3D_CURVE_QUADRATIC'\
    and ernst_type != 'SDF_3D_UBER'\
    and ernst_type != 'SDF_3D_INSTANCE':
        do_auto_smooth(obj)
    if mat != None:
        set_material(obj, mat)
    bpy.ops.ernst.add_pmod_translation()
    if ernst_type != 'SDF_3D_SPHERE':
        bpy.ops.ernst.add_pmod_rotation()
    sgd.is_ignoring_watcher = False

class ERNST_OT_Add_Sphere(Operator):
    bl_idname = 'ernst.add_sphere'
    bl_label = 'ernst: add sphere'
    bl_description = 'tama'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_3d_sphere
        sgd.is_ignoring_watcher = True
        mat = get_active_material()
        bpy.ops.mesh.primitive_uv_sphere_add()
        obj = bpy.context.object
        obj.name = 'sdSphere'+str(id_3d_sphere).rjust(2, '0')
        id_3d_sphere+=1
        set_ernst_props(obj, 'SDF_3D_SPHERE', mat)
        return {'FINISHED'}

class ERNST_OT_Add_2D_Circle(Operator):
    bl_idname = 'ernst.add_circle'
    bl_label = 'ernst: add circle'
    bl_description = 'tama'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_2d_circle
        sgd.is_ignoring_watcher = True
        mat = get_active_material()
        # obj = bpy.ops.mesh.primitive_uv_sphere_add()
        bpy.ops.mesh.primitive_circle_add(radius=1, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.edge_face_add()
        bpy.ops.object.editmode_toggle()

        obj = bpy.context.object
        obj.name = 'sd2DCircle'+str(id_2d_circle).rjust(2, '0')
        id_2d_circle+=1
        set_ernst_props(obj, 'SDF_2D_CIRCLE', mat)
        return {'FINISHED'}

class ERNST_OT_Add_2D_Box(Operator):
    bl_idname = 'ernst.add_box'
    bl_label = 'ernst: add box'
    bl_description = 'tama'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_2d_box
        sgd.is_ignoring_watcher = True
        mat = get_active_material()
        bpy.ops.mesh.primitive_plane_add()
        obj = bpy.context.object
        obj.name = 'sd2DBox'+str(id_2d_box).rjust(2, '0')
        id_2d_box+=1
        set_ernst_props(obj, 'SDF_2D_BOX', mat)
        return {'FINISHED'}

class ERNST_OT_Add_Ellipsoid(Operator):
    bl_idname = 'ernst.add_ellipsoid'
    bl_label = 'ernst: add ellipsoid'
    bl_description = 'daen'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_3d_ellipsoid
        sgd.is_ignoring_watcher = True
        mat = get_active_material()
        bpy.ops.mesh.primitive_uv_sphere_add()
        obj = bpy.context.object
        obj.name = 'sdEllipsoid'+str(id_3d_ellipsoid).rjust(2, '0')
        id_3d_ellipsoid+=1
        set_ernst_props(obj, 'SDF_3D_ELLIPSOID', mat)
        return {'FINISHED'}

class ERNST_OT_Add_Capsule(Operator):
    bl_idname = 'ernst.add_capsule'
    bl_label = 'ernst: add capsule'
    bl_description = 'capsule'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_3d_capsule
        sgd.is_ignoring_watcher = True
        mat = get_active_material()
        bpy.ops.mesh.make_wcapsule(radius=0.59, height=2.06, seg_height=9, centered=True)
        obj = bpy.context.object
        obj.name = 'sdCapsule'+str(id_3d_capsule).rjust(2, '0')
        id_3d_capsule+=1
        set_ernst_props(obj, 'SDF_3D_CAPSULE', mat)
        return {'FINISHED'}

class ERNST_OT_Add_Cube(Operator):
    bl_idname = 'ernst.add_sd_cube'
    bl_label = 'ernst: add sd_cube'
    bl_description = 'sd_cube'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_3d_sd_cube
        sgd.is_ignoring_watcher = True
        mat = get_active_material()
        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.object
        obj.name = 'sdBox'+str(id_3d_sd_cube).rjust(2, '0')
        id_3d_sd_cube+=1
        set_ernst_props(obj, 'SDF_3D_BOX', mat)
        return {'FINISHED'}

class ERNST_OT_Add_Plane(Operator):
    bl_idname = 'ernst.add_plane'
    bl_label = 'ernst: add plane'
    bl_description = 'plane'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_3d_plane
        sgd.is_ignoring_watcher = True
        mat = get_active_material()
        bpy.ops.mesh.primitive_plane_add()
        obj = bpy.context.object
        obj.name = 'sdPlane'+str(id_3d_plane).rjust(2, '0')
        id_3d_plane+=1
        set_ernst_props(obj, 'SDF_3D_PLANE', mat)
        return {'FINISHED'}

class ERNST_OT_Add_Cylinder(Operator):
    bl_idname = 'ernst.add_cylinder'
    bl_label = 'ernst: add cylinder'
    bl_description = 'cylinder'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_3d_cylinder
        sgd.is_ignoring_watcher = True
        mat = get_active_material()
        bpy.ops.mesh.primitive_cylinder_add()
        obj = bpy.context.object
        obj.name = 'sdCappedCylinder'+str(id_3d_cylinder).rjust(2, '0')
        id_3d_cylinder+=1
        set_ernst_props(obj, 'SDF_3D_CYLINDER', mat)
        return {'FINISHED'}

class ERNST_OT_Add_Pie(Operator):
    bl_idname = 'ernst.add_pie'
    bl_label = 'ernst: add pie'
    bl_description = 'pie'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_3d_pie
        sgd.is_ignoring_watcher = True
        mat = get_active_material()
        bpy.ops.mesh.primitive_cylinder_add()
        obj = bpy.context.object
        obj.name = 'sdPieCylinder'+str(id_3d_pie).rjust(2, '0')
        id_3d_pie+=1
        set_ernst_props(obj, 'SDF_3D_CYLINDER_PIE', mat)
        return {'FINISHED'}

class ERNST_OT_Add_Torus(Operator):
    bl_idname = 'ernst.add_torus'
    bl_label = 'ernst: add torus'
    bl_description = 'torus'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_3d_torus
        sgd.is_ignoring_watcher = True
        mat = get_active_material()
        bpy.ops.mesh.make_wtorus(radius_main=1, radius_minor=0.5)
        obj = bpy.context.object
        obj.name = 'sdTorus'+str(id_3d_torus).rjust(2, '0')
        id_3d_torus+=1
        set_ernst_props(obj, 'SDF_3D_TORUS', mat)
        return {'FINISHED'}

class ERNST_OT_Add_CappedTorus(Operator):
    bl_idname = 'ernst.add_capped_torus'
    bl_label = 'ernst: add capped torus'
    bl_description = 'capped torus'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_3d_capped_torus
        sgd.is_ignoring_watcher = True
        mat = get_active_material()
        bpy.ops.mesh.make_wtorus(radius_main=1, radius_minor=0.5)
        obj = bpy.context.object
        obj.name = 'sdCappedTorus'+str(id_3d_capped_torus).rjust(2, '0')
        id_3d_capped_torus+=1
        set_ernst_props(obj, 'SDF_3D_TORUS_CAPPED', mat)
        return {'FINISHED'}

class ERNST_OT_Add_Cone(Operator):
    bl_idname = 'ernst.add_cone'
    bl_label = 'ernst: add cone'
    bl_description = 'cone'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_3d_cone
        sgd.is_ignoring_watcher = True
        mat = get_active_material()
        bpy.ops.mesh.make_wcone(rad_top=0, rad_main=1.02, height=2, seg_perimeter=24, seg_height=1, seg_radius=1)
        obj = bpy.context.object
        obj.name = 'sdConeSection'+str(id_3d_cone).rjust(2, '0')
        id_3d_cone+=1
        bpy.data.meshes[obj.data.name].WCone.centered = True
        set_ernst_props(obj, 'SDF_3D_CONE', mat)
        return {'FINISHED'}

class ERNST_OT_Add_RoundCone(Operator):
    bl_idname = 'ernst.add_round_cone'
    bl_label = 'ernst: add round cone'
    bl_description = 'round cone'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_3d_round_cone
        sgd.is_ignoring_watcher = True
        mat = get_active_material()
        bpy.ops.mesh.make_wcone(rad_top=0, rad_main=1.02, height=2, seg_perimeter=24, seg_height=1, seg_radius=1)
        obj = bpy.context.object
        obj.name = 'sdRoundCone'+str(id_3d_round_cone).rjust(2, '0')
        id_3d_round_cone+=1
        bpy.data.meshes[obj.data.name].WCone.centered = True
        set_ernst_props(obj, 'SDF_3D_CONE_ROUND', mat)
        return {'FINISHED'}

class ERNST_OT_Add_CurveQ(Operator):
    bl_idname = 'ernst.add_quadratic_curve'
    bl_label = 'ernst: add quadratic curve'
    bl_description = 'quadratic curve'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_3d_quadratic_curve
        sgd.is_ignoring_watcher = True

        mat = get_active_material()

        bpy.ops.curve.primitive_bezier_curve_add()

        bpy.ops.object.editmode_toggle()

        bpy.ops.curve.spline_type_set(type='POLY')
        sp = bpy.context.active_object.data.splines[0]

        bpy.ops.curve.select_all(action='DESELECT')
        sp.points[1].select = True
        bpy.ops.transform.translate(value=(-1, 0, 0))
        bpy.ops.curve.extrude_move(CURVE_OT_extrude={"mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(1, 0, 0)})

        bpy.ops.curve.select_all(action='DESELECT')
        sp.points[1].select = True
        bpy.ops.transform.translate(value=(0, 1, 0))

        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.transform.translate(value=(1, 0, 0))

        sp.points[0].radius = .2
        sp.points[1].radius = 0
        sp.points[2].radius = .1

        bpy.ops.object.editmode_toggle()

        obj = bpy.context.object
        obj.name = 'sdCurveQuadratic'+str(id_3d_quadratic_curve).rjust(2, '0')
        id_3d_quadratic_curve+=1
        set_ernst_props(obj, 'SDF_3D_CURVE_QUADRATIC', mat)
        return {'FINISHED'}

class ERNST_OT_ChooseCodeName(Operator):
    bl_idname = 'ernst.choose_code_prim'
    bl_label = 'method'
    bl_description = 'Choose code primitive'
    bl_options = {'REGISTER'}
    code_name: StringProperty(name='code_NAME', default='')

    def execute(self, context):
        obj = context.view_layer.objects.active
        obj.ernst.shader_proxy.props.code_name = self.code_name
        shaderizer_watcher.check(self, context)
        return {'FINISHED'}

class ERNST_OT_Add_Uber2D(Operator):
    bl_idname = 'ernst.add_uber_2d'
    bl_label = 'ernst: add uber 2D SDF'
    bl_description = 'Add a sdf defined by code'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_2d_uber
        sgd.is_ignoring_watcher = True
        mat = get_active_material()
        bpy.ops.mesh.primitive_plane_add()
        obj = bpy.context.object
        obj.name = 'sdUber2D'+str(id_2d_uber).rjust(2, '0')
        id_2d_uber+=1
        set_ernst_props(obj, 'SDF_2D_UBER', mat)
        return {'FINISHED'}

class ERNST_OT_Add_Uber3D(Operator):
    bl_idname = 'ernst.add_uber_3d'
    bl_label = 'ernst: add uber 3D SDF'
    bl_description = 'Add a sdf defined by code'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_3d_uber3d
        sgd.is_ignoring_watcher = True
        mat = get_active_material()
        bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, location=(0, 0, 0))
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete(type='ONLY_FACE')
        bpy.ops.object.editmode_toggle()
        obj = bpy.context.object
        obj.name = 'sdUber3D'+str(id_3d_uber3d).rjust(2, '0')
        id_3d_uber3d+=1
        set_ernst_props(obj, 'SDF_3D_UBER', mat)
        return {'FINISHED'}

class ERNST_OT_Add_ControlPoint(Operator):
    bl_idname = 'ernst.add_control_point'
    bl_label = 'ernst: add control_point'
    bl_description = 'control position for child primitives'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_control_point
        sgd.is_ignoring_watcher = True
        obj = bpy.ops.object.empty_add()
        obj = bpy.context.object
        obj.empty_display_size = 0.1
        obj.show_in_front = True
        obj.name = 'cp'+str(id_control_point).rjust(2, '0')
        id_control_point+=1

        obj.ernst.type = 'CONTROL_POINT'
        obj.ernst.is_ernst_obj = True
        # defalut modifiers for Translation & Rotation
        bpy.ops.ernst.add_pmod_translation()
        bpy.ops.ernst.add_pmod_rotation()

        return {'FINISHED'}

class ERNST_OT_Add_IKArmature(Operator):
    bl_idname = 'ernst.add_ik_armature'
    bl_label = 'ernst: add ik_armature'
    bl_description = 'control position for child primitives'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_ik_armature
        sgd.is_ignoring_watcher = True

        bpy.ops.object.armature_add(enter_editmode=False, location=(0, 0, 0))
        armature = bpy.context.view_layer.objects.active
        armature.name = armature.data.name = f'ika{id_ik_armature}'
        data = armature.data

        bpy.ops.object.editmode_toggle()
        bpy.ops.armature.select_all(action='SELECT')
        bpy.ops.armature.delete()

        bone_name_root = armature.name + '_root'
        data.edit_bones.new(bone_name_root)
        bone_root = data.edit_bones[bone_name_root]
        bone_root.roll = -math.pi*.5
        bone_root.head = Vector((0,0,0))
        bone_root.tail = Vector((0,0.001,-1))

        bone_name_ik = armature.name + '_ik'
        data.edit_bones.new(bone_name_ik)
        bone_ik = data.edit_bones[bone_name_ik]
        bone_ik.parent = data.edit_bones[bone_name_root]
        bone_ik.use_connect = True
        bone_ik.tail = Vector((0,0,-2))

        bone_name_target = armature.name + '_target'
        data.edit_bones.new(bone_name_target)
        bone_target = data.edit_bones[bone_name_target]
        bone_target.parent = None
        bone_target.use_connect = False
        bone_target.head = Vector((0,0,-2))
        bone_target.tail = Vector((0,-.25,-2))

        bone_name_pole = armature.name + '_pole'
        data.edit_bones.new(bone_name_pole)
        bone_pole = data.edit_bones[bone_name_pole]
        bone_pole.parent = None
        bone_pole.use_connect = False
        bone_pole.head = Vector((0,-.99,-1))
        bone_pole.tail = Vector((0,-1,-1))

        bpy.ops.object.editmode_toggle()

        rootb = armature.pose.bones.get(bone_name_root)
        ikb = armature.pose.bones.get(bone_name_ik)
        ikc = ikb.constraints.new('IK')
        ikc.target = armature
        ikc.subtarget = bone_name_target
        ikc.pole_target = armature
        ikc.pole_subtarget = bone_name_pole
        bpy.ops.ernst.add_control_point()
        cp_root = bpy.context.view_layer.objects.active
        bpy.ops.view3d.my_uilist_remove_item(id=0)
        bpy.ops.view3d.my_uilist_remove_item(id=0)
        bpy.ops.ernst.add_pmod_ik_armature()
        cp_root.name = 'ikcp0_' + bone_name_root
        cp_root.parent = armature
        cp_root.parent_type = 'BONE'
        cp_root.parent_bone = bone_name_root
        b = armature.pose.bones.get(bone_name_root)
        cp_root.matrix_parent_inverse = Matrix.Translation(Vector((0,-1,0))) @ Matrix.Rotation(math.radians(90), 4, 'X')
        cp_root.empty_display_type = 'ARROWS'

        bpy.ops.ernst.add_control_point()
        cp_ik = bpy.context.view_layer.objects.active
        bpy.ops.view3d.my_uilist_remove_item(id=0)
        bpy.ops.view3d.my_uilist_remove_item(id=0)
        bpy.ops.ernst.add_pmod_ik_bone_joint()
        cp_ik.ernst.pmods.pmod[0].ik_bone_joint.object_root = cp_root
        cp_ik.name = 'ikcp1_' + bone_name_ik
        cp_ik.parent = armature
        cp_ik.parent_type = 'BONE'
        cp_ik.parent_bone = bone_name_ik
        b = data.bones[bone_name_ik]
        cp_ik.matrix_parent_inverse = Matrix.Translation(Vector((0,-1,0))) @ Matrix.Rotation(math.radians(90), 4, 'X')
        cp_ik.empty_display_type = 'ARROWS'

        bpy.ops.ernst.add_control_point()
        cp_target = bpy.context.view_layer.objects.active
        bpy.ops.view3d.my_uilist_remove_item(id=0)
        bpy.ops.view3d.my_uilist_remove_item(id=0)
        bpy.ops.ernst.add_pmod_ik_bone_target()
        bpy.ops.ernst.add_pmod_rotation()
        cp_target.ernst.pmods.pmod[0].ik_bone_target.object_root = cp_root
        cp_target.name = 'ikcp2_' + bone_name_target
        b = armature.pose.bones.get(bone_name_target)
        bc = b.constraints.new('COPY_LOCATION')
        bc.target = cp_target
        cp_target.location = Vector((0,0,-2))
        cp_target.empty_display_type = 'CONE'

        bpy.ops.ernst.add_control_point()
        cp_pole = bpy.context.view_layer.objects.active
        bpy.ops.view3d.my_uilist_remove_item(id=0)
        bpy.ops.view3d.my_uilist_remove_item(id=0)
        bpy.ops.ernst.add_pmod_ik_pole()
        cp_pole.ernst.pmods.pmod[0].ik_pole.object_root = cp_root
        cp_pole.name = 'ikcp3_' + bone_name_pole
        b = armature.pose.bones.get(bone_name_pole)
        bc = b.constraints.new('COPY_LOCATION')
        bc.target = cp_pole
        cp_pole.location = Vector((0,-1,-1))
        cp_pole.empty_display_type = 'CONE'

        return {'FINISHED'}

class ERNST_OT_Add_Camera(Operator):
    bl_idname = 'ernst.add_camera'
    bl_label = 'ernst: add camera'
    bl_description = 'add a shader camera'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_camera
        sgd.is_ignoring_watcher = True
        obj = bpy.ops.object.camera_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), rotation=(3.14/2, 0, 0))
        obj = bpy.context.object
        obj.show_in_front = True
        obj.name = 'cam'+str(id_camera).rjust(1, '0')
        id_camera+=1

        obj.ernst.type = 'CAMERA'
        obj.ernst.is_ernst_obj = True

        return {'FINISHED'}

class ERNST_OT_Add_Light_Sun(Operator):
    bl_idname = 'ernst.add_light_sun'
    bl_label = 'ernst: add light_sun'
    bl_description = 'add a shader light. Type: "sun"'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_light
        sgd.is_ignoring_watcher = True
        obj = bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
        obj = bpy.context.object
        obj.show_in_front = True
        obj.name = 'lit'+str(id_light).rjust(1, '0')
        id_light+=1

        obj.ernst.type = 'LIGHT_DIRECTIONAL'
        obj.ernst.is_ernst_obj = True

        return {'FINISHED'}

class ERNST_OT_Add_Light_Spot(Operator):
    bl_idname = 'ernst.add_light_spot'
    bl_label = 'ernst: add light_spot'
    bl_description = 'add a shader light. Type: "spot"'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_light
        sgd.is_ignoring_watcher = True
        obj = bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
        obj = bpy.context.object
        obj.show_in_front = True
        obj.name = 'lit'+str(id_light).rjust(1, '0')
        id_light+=1

        obj.ernst.type = 'LIGHT_DIRECTIONAL'
        obj.ernst.is_ernst_obj = True

        return {'FINISHED'}

class ERNST_OT_Add_Light_Area(Operator):
    bl_idname = 'ernst.add_light_area'
    bl_label = 'ernst: add light_area'
    bl_description = 'add a shader light. Type: "area"'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_light
        sgd.is_ignoring_watcher = True
        obj = bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
        obj = bpy.context.object
        obj.show_in_front = True
        obj.name = 'lit'+str(id_light).rjust(1, '0')
        id_light+=1

        obj.ernst.type = 'LIGHT_DIRECTIONAL'
        obj.ernst.is_ernst_obj = True

        return {'FINISHED'}

class ERNST_OT_Add_Light_Point(Operator):
    bl_idname = 'ernst.add_light_point'
    bl_label = 'ernst: add light_point'
    bl_description = 'add a shader light. Type: "point"'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global id_light
        sgd.is_ignoring_watcher = True
        obj = bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
        obj = bpy.context.object
        obj.show_in_front = True
        obj.name = 'lit'+str(id_light).rjust(1, '0')
        id_light+=1

        obj.ernst.type = 'LIGHT_DIRECTIONAL'
        obj.ernst.is_ernst_obj = True

        return {'FINISHED'}

class ERNST_OT_Add_Collection(Operator):
    """Add a ERNST collection"""
    bl_idname = "ernst.collection_add"
    bl_label = "Add ERNST Collection"
    bl_options = {'REGISTER', 'UNDO'}
    name: StringProperty(default = 'sdObj')

    def execute(self, context):
        global id_collection
        sgd.is_ignoring_watcher = True

        self.name = 'sd'+str(id_collection).rjust(2, '0')
        col = bpy.data.collections.new(self.name)
        bpy.context.scene.collection.children.link(col)
        id_collection+=1

        col.ernst.type = 'SDF_FUNCTION'
        col.ernst.is_ernst_obj = True

        return {'FINISHED'}

class ERNST_OT_ChoosePreCode(Operator):
    bl_idname = 'ernst.choose_pre_code'
    bl_label = 'method'
    bl_description = 'Choose precal code'
    bl_options = {'REGISTER'}
    code_pre: StringProperty(name='code_NAME', default='')

    def execute(self, context):
        obj = context.view_layer.objects.active
        obj.ernst.shader_proxy.props.code_pre = self.code_pre
        shaderizer_watcher.check(self, context)

        return {'FINISHED'}

class ERNST_OT_ChoosePostCode(Operator):
    bl_idname = 'ernst.choose_post_code'
    bl_label = 'method'
    bl_description = 'Choose postcal code'
    bl_options = {'REGISTER'}
    code_post: StringProperty(name='code_NAME', default='')

    def execute(self, context):
        obj = context.view_layer.objects.active
        obj.ernst.shader_proxy.props.code_post = self.code_post
        shaderizer_watcher.check(self, context)

        return {'FINISHED'}

id_collections = {}
def enum_items(self, context):
    collections = []
    for coll in bpy.data.collections:
        if coll.ernst.type=='SDF_FUNCTION':
            collections.append((coll.name.upper(), coll.name, f'Add an instance of "{coll.name}"'))
    enum_items.lookup = {id: name for id, name, desc in collections}
    return collections

class ERNST_OT_Add_Instance(Operator):
    """Add a ERNST instance"""
    bl_idname = "ernst.instance_add"
    bl_label = "Add ERNST Instance"
    bl_options = {'REGISTER', 'UNDO'}

    collections : bpy.props.EnumProperty(items=enum_items)

    def execute(self, context):
        global id_collections
        sgd.is_ignoring_watcher = True

        self.report({'INFO'}, enum_items.lookup[self.collections])
        bpy.ops.object.collection_instance_add(collection=enum_items.lookup[self.collections], location=(0, 0, 0))
        inst = context.view_layer.objects.active
        collection_name = inst.instance_collection.name
        try:
            id_collections[collection_name] += 1
        except KeyError:
            id_collections[collection_name] = 0

        inst.empty_display_type = 'SPHERE'
        inst.empty_display_size = 0.25
        inst.name = collection_name+'_'+str(id_collections[collection_name]).rjust(2, '0')
        set_ernst_props(inst, 'SDF_3D_INSTANCE', None)
        return {'FINISHED'}
