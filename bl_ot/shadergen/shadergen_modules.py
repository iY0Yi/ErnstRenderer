import re
from ...util.map import Map
from . import shadergen_util
from . import shadergen_data as sgd

def init_module_loaders():
    sgd.module_lib = Map({
        'camera':{
            'CAMERA_PERS': ModuleLoader('camera','camera_perspective.glsl'),
            'CAMERA_ORTHO': ModuleLoader('camera','camera_orthographic.glsl')
        },
        'sdf2d':{
            # 'SDF_2D_ARC': ModuleLoader('sdf2d','sd_arc.glsl'),
            # 'SDF_2D_BOX_ROUND': ModuleLoader('sdf2d','sd_box_round.glsl'),
            'SDF_2D_BOX': ModuleLoader('sdf2d','sd_box.glsl'),
            'SDF_2D_CIRCLE': ModuleLoader('sdf2d','sd_circle.glsl'),
            # 'SDF_2D_CROSS_ROUND': ModuleLoader('sdf2d','sd_cross_round.glsl'),
            # 'SDF_2D_CROSS': ModuleLoader('sdf2d','sd_cross.glsl'),
            # 'SDF_2D_CURVE_QUADRATIC': ModuleLoader('sdf2d','sd_curve_quadratic.glsl'),
            # 'SDF_2D_CUT': ModuleLoader('sdf2d','sd_cut.glsl'),
            # 'SDF_2D_EGG': ModuleLoader('sdf2d','sd_egg.glsl'),
            # 'SDF_2D_ELLIPSE': ModuleLoader('sdf2d','sd_ellipse.glsl'),
            # 'SDF_2D_NGON': ModuleLoader('sdf2d','sd_ngon.glsl'),
            # 'SDF_2D_PARALLELOGRAM': ModuleLoader('sdf2d','sd_parallelogram.glsl'),
            # 'SDF_2D_PIE': ModuleLoader('sdf2d','sd_pie.glsl'),
            # 'SDF_2D_RHOMBUS': ModuleLoader('sdf2d','sd_rhombus.glsl'),
            # 'SDF_2D_STAIRS': ModuleLoader('sdf2d','sd_stairs.glsl'),
            # 'SDF_2D_TRAPEZOID': ModuleLoader('sdf2d','sd_trapezoid.glsl'),
            # 'SDF_2D_TRIANGLE_EQILATERAL': ModuleLoader('sdf2d','sd_triangle_equilateral.glsl'),
            # 'SDF_2D_TRIANGLE_ISOSCELES': ModuleLoader('sdf2d','sd_triangle_isosceles.glsl'),
            # 'SDF_2D_TUNNEL': ModuleLoader('sdf2d','sd_tunnel.glsl'),
        },
        'sdf3d':{
            'SDF_3D_SPHERE': ModuleLoader('sdf3d','sd_sphere.glsl'),
            'SDF_3D_PLANE': ModuleLoader('sdf3d','sd_plane.glsl'),
            'SDF_3D_BOX': ModuleLoader('sdf3d','sd_box.glsl'),
            'SDF_3D_ELLIPSOID': ModuleLoader('sdf3d','sd_ellipsoid.glsl'),
            'SDF_3D_TORUS': ModuleLoader('sdf3d','sd_torus.glsl'),
            'SDF_3D_TORUS_CAPPED': ModuleLoader('sdf3d','sd_torus_capped.glsl'),
            'SDF_3D_CYLINDER': ModuleLoader('sdf3d','sd_cylinder_capped.glsl'),
            'SDF_3D_CYLINDER_PIE': ModuleLoader('sdf3d','sd_cylinder_pie.glsl'),
            'SDF_3D_CAPSULE': ModuleLoader('sdf3d','sd_capsule.glsl'),
            'SDF_3D_CONE': ModuleLoader('sdf3d','sd_cone_section.glsl'),
            'SDF_3D_CONE_ROUND': ModuleLoader('sdf3d','sd_cone_round.glsl'),
            'SDF_3D_CURVE_QUADRATIC': ModuleLoader('sdf3d','sd_curve_quadratic.glsl'),
        },
        'boolean':{
            'BOOL_UNI': ModuleLoader('boolean','uni.glsl'),
            'BOOL_UNI_SMOOTH': ModuleLoader('boolean','uni_smooth.glsl'),
            'BOOL_UNI_LINEAR': ModuleLoader('boolean','uni_linear.glsl'),
            'BOOL_UNI_STAIRS': ModuleLoader('boolean','uni_stairs.glsl'),
            'BOOL_UNI_STAIRS_ROUNDED': ModuleLoader('boolean','uni_stairs_round.glsl'),

            'BOOL_SUB': ModuleLoader('boolean','sub.glsl'),
            'BOOL_SUB_SMOOTH': ModuleLoader('boolean','sub_smooth.glsl'),
            'BOOL_SUB_LINEAR': ModuleLoader('boolean','sub_linear.glsl'),
            'BOOL_SUB_STAIRS': ModuleLoader('boolean','sub_stairs.glsl'),
            'BOOL_SUB_STAIRS_ROUNDED': ModuleLoader('boolean','sub_stairs_round.glsl'),

            'BOOL_INT': ModuleLoader('boolean','int.glsl'),
            'BOOL_INT_SMOOTH': ModuleLoader('boolean','int_smooth.glsl'),
            'BOOL_INT_LINEAR': ModuleLoader('boolean','int_linear.glsl'),
            'BOOL_INT_STAIRS': ModuleLoader('boolean','int_stairs.glsl'),
            'BOOL_INT_STAIRS_ROUNDED': ModuleLoader('boolean','int_stairs_round.glsl'),
        },
        'pmod':{
            'PMOD_ROT_2D': ModuleLoader('pmod','p_rotation_v2.glsl'),
            'PMOD_ROT_3D': ModuleLoader('pmod','p_rotation_v3.glsl'),
            'PMOD_ROT_QUAT': ModuleLoader('pmod','p_rotation_quat.glsl'),
            'PMOD_REP_LIMITED': ModuleLoader('pmod','p_repetition_limited.glsl'),
            'PMOD_REP_POLAR': ModuleLoader('pmod','p_repetition_polar.glsl'),
            'PMOD_BALLOON_V2': ModuleLoader('pmod','p_balloon_v2.glsl'),
            'PMOD_BALLOON_V3': ModuleLoader('pmod','p_balloon_v3.glsl'),
            'PMOD_BEND': ModuleLoader('pmod','p_bend.glsl'),
            'PMOD_SHEAR': ModuleLoader('pmod','p_shear.glsl'),
            'PMOD_TAPER': ModuleLoader('pmod','p_taper.glsl'),
            'PMOD_TWIST': ModuleLoader('pmod','p_twist.glsl'),
            'PMOD_ELONGATE': ModuleLoader('pmod','p_elongate.glsl'),
            'PMOD_CURVE_ELONGATE': ModuleLoader('pmod','p_elongate_curve.glsl'),
            'PMOD_MIRROR': ModuleLoader('pmod','p_mirror.glsl'),
            'PMOD_SPIN': ModuleLoader('pmod','p_spin.glsl'),
        }
    })

    for category in sgd.module_lib.values():
        for loader in category.values():
            loader.load()

class ModuleLoader:
    def __init__(self, category, filename):
        self.category = category
        self.filename = filename
        self.clear()

    def clear(self):
        self.fncname = ''
        if self.category == 'boolean':
            self.code = Map({'fl':'', 'v4':''})
            self.used = Map({'fl':False, 'v4':False})
        else:
            self.code = False
            self.used = False

    def load(self):
        self.clear()
        fl = sgd.dir_trk_lib_modules / self.category /self.filename
        with fl.open() as f:
            code = f.read()

            if self.category == 'camera':
                for l in code.splitlines():
                    if l.count('void') > 0 and l.count('vec2') > 0 and l.count('(') > 0 and l.count(')') > 0:
                        p = r'void\s(.*)\('
                        self.fncname = re.findall(p, l)[0]
                self.code = code.strip()

            if self.category == 'boolean':
                for l in code.splitlines():
                    if l.count('float') >= 3:
                        p = r'float\s(.*)\('
                        self.fncname = re.findall(p, l)[0]
                splited = re.split("\nvec4\s", code, 1)
                self.code.fl = splited[0].strip()
                self.code.v4 = 'vec4 ' + splited[1].strip()

            if self.category == 'sdf2d':
                for l in code.splitlines():
                    if l.count('float') > 0 and l.count('vec2') > 0 and l.count('(') > 0 and l.count(')') > 0:
                        p = r'float\s(.*)\('
                        self.fncname = re.findall(p, l)[0]
                self.code = code.strip()

            if self.category == 'sdf3d':
                for l in code.splitlines():
                    if l.count('float') > 0 and l.count('vec3') > 0 and l.count('(') > 0 and l.count(')') > 0:
                        p = r'float\s(.*)\('
                        self.fncname = re.findall(p, l)[0]
                self.code = code.strip()

            if self.category == 'pmod':
                for l in code.splitlines():
                    if l.count('void') > 0 and l.count('inout') > 0:
                        self.fncname = re.findall(r'void\s(.*)\(', l)[0]
                    if l.count('vec3') > 1 and l.count('inout vec3') > 0:
                        self.fncname = re.findall(r'vec3\s(.*)\(', l)[0]
                    if l.count('vec2') > 1 and l.count('inout vec2') > 0:
                        self.fncname = re.findall(r'vec2\s(.*)\(', l)[0]
                self.code = code.strip()

    def get_code(self):
        code = ''
        if self.category == 'boolean':
            code += (self.code.fl+'\n') if self.used.fl else ''
            code += (self.code.v4+'\n') if self.used.v4 else ''
        else:
            code += (self.code+'\n') if self.used else ''

        return code+'\n'

    def check_used(self, code_analyzed):
        if self.category == 'boolean':
            if self.used.fl == False or self.used.v4 == False:
                if re.search(self.fncname, code_analyzed) != None:
                    self.used.fl = True
                    self.used.v4 = True
        else:
            if self.used == False:
                if re.search(self.fncname, code_analyzed) != None:
                    self.used = True


