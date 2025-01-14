import os
import pathlib
import string

import bpy
import numpy as np
from mathutils import Quaternion, Vector

from ...util.util import *
from . import shadergen_ubo as ubo

def fract(x):
    return x - int(x)

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def float_to_string(num):
    return str(int(num))

def er_var(name):
    return str(name).replace('.', '_')

def er_b(val):
    return 'true' if val else 'false'

def er_i(val):
    return str(val)

def er_f(val, is_vec=False):
    # Original formatting
    code_gl = '{:.6f}'.format(float(val))
    code_gl = code_gl.rstrip('0')

    if is_vec and fract(val) == 0.0:
        code_gl = float_to_string(val)
    if is_vec and code_gl == '-0':
        code_gl = '0'
    if val == -0.0:
        code_gl = '0.'

    absed = abs(val)
    sgn = sign(val)

    if int(absed) == 0 and fract(absed) != 0.0:
        formatted = '{:.6f}'.format(float(absed))
        # Check if the formatted value is of the form '0.XXXXXX' before stripping
        if formatted.startswith('0.') and formatted.endswith('000000'):
            code_gl = '0.'
        elif formatted.startswith('0.'):
            code_gl = formatted[1:]
        else:
            code_gl = formatted.lstrip('0')

        if sgn == -1:
            code_gl = '-' + code_gl
        code_gl = code_gl.rstrip('0')

    if code_gl == '.':
        raise ValueError(f"it became to just a dot! original value: {val}")

    return code_gl

def er_v2(vec):
    res = f'vec2({er_f(vec[0])}, {er_f(vec[1])})'
    if res == 'vec2(0., 0.)': return 'vec2(0)'
    return res

def er_v3(vec):
    res=''
    if type(vec) is Vector:
        res = f'vec3({er_f(vec.x)}, {er_f(vec.z)}, {er_f(vec.y)})'
    else:
        res = f'vec3({er_f(vec[0])}, {er_f(vec[2])}, {er_f(vec[1])})'
    if res == 'vec3(0., 0., 0.)': return 'vec3(0)'
    return res

def er_v4(vec):
    res=''
    if type(vec) is Vector or type(vec) is Quaternion:
        res = f'vec4({er_f(vec.x)}, {er_f(vec.z)}, {er_f(vec.y)}, {er_f(vec.w)})'
    else:
        res = f'vec4({er_f(vec[0])}, {er_f(vec[2])}, {er_f(vec[1])}, {er_f(vec[3])})'
    if res == 'vec4(0., 0., 0., 0.)': return 'vec4(0)'
    return res

def inv_gamma(v):
    return pow(v, 2.2)

def er_col(vec):
    vec[0] = inv_gamma(vec[0])
    vec[1] = inv_gamma(vec[1])
    vec[2] = inv_gamma(vec[2])
    res = f'vec3({er_f(vec[0])}, {er_f(vec[1])}, {er_f(vec[2])})'
    if res == 'vec3(0., 0., 0.)': return 'vec3(0)'
    return res

def er_v4(vec):
    if type(vec) is Quaternion:
        res = f'vec4({er_f(vec.x)}, {er_f(vec.y)}, {er_f(vec.z)}, {er_f(vec.w)})'
    else:
        res = f'vec4({er_f(vec[0])}, {er_f(vec[1])}, {er_f(vec[2])}, {er_f(vec[3])})'
    if res == 'vec4(0., 0., 0., 0.)':
        return 'vec4(0)'
    return res

def is_valid_v3(vec):
    if vec == '':
        return False
    vec = vec.replace('vec3(', '')
    vec = vec.replace(')', '')
    elements = vec.split(',')
    return float(elements[0])!=0. and float(elements[1])!=0. and float(elements[2])!=0.

# Parse for GLSL includes based on
# https://www.opengl.org/discussion_boards/showthread.php/169209-include-in-glsl?p=1192415&viewfull=1#post1192415
#
def parse_for_includes_from(source, sourceDirectoryPath, lib_path):
    filename = pathlib.Path(sourceDirectoryPath).name
    included = []
    return parse_for_includes_loop( source, included, 0, sourceDirectoryPath, lib_path)

def parse_for_includes(source, sourceDirectoryPath):
    filename = pathlib.Path(sourceDirectoryPath).name
    included = []
    return parse_for_includes_loop( source, included, 0, sourceDirectoryPath, None)

def parse_for_includes_loop(source, included, level, sourceDirectoryPath, lib_path):

    if level > 32:
        return ''

    output = ''
    input = source

    def match_include(s_):
        filename_ = ''

        s = s_

        # eat up any leading whitespace.
        s = s.replace("\t", " ")

        if s[0] != '#': return False, filename_

        # -----| invariant: found '#'
        s = s.replace('#', '') # move forward one character

        ss = s.split()
        if len(ss)<2: return False, filename_

        i = ss[0]
        f = ss[1]

        # while skipping whitespace, read in tokens for: pragma, include, and filename
        if i == '' or (len(f) < 2): return False, filename_
        # -----| invariant: all tokens have values
        if i != 'include': return False, filename_

        # first and last character of filename token must match and be either
        # '<' and '>', or '"
        if f[0] == '<' and f[len(f)-1] != '>': return False, filename_ #< mismatching brackets
        if (f[0] == '"' or f[0] == '\'') and (f[0] != f[len(f)-1]): return False, filename_ # mismatching quotes

        # invariant: filename properly quoted.
        filename_ = f[0:len(f)]
        return True, filename_

    p_file = pathlib.Path(sourceDirectoryPath)
    with p_file.open() as f:
        line = f.readline()
        filename = p_file.name
        if lib_path == None:
            p_dir = p_file.parent
        else:
            p_dir = lib_path


        while line != '':
            is_matched, include = match_include(line)

            if is_matched == False:
                output += line
                line = f.readline()
                continue

            include = str(p_dir / include)

            line = f.readline()

            # --------| invariant: '#pragma include' has been requested
            is_existed = False
            for i in range(0, len(included)):
                if included[i] == include:
                    is_existed = True
                    break
            if is_existed:
                continue

            # we store the absolute paths so as have (more) unique file identifiers.
            included.append( include )

            # ofBuffer buffer = ofBufferFromFile( include )
            p_inc = pathlib.Path(include)
            with p_inc.open() as incf:
                buffer = incf.read()

                if len(buffer)<1:
                    continue

                currentDir = include
                output += parse_for_includes_loop( buffer, included, level + 1, currentDir, None )

    return output

def get_cp_names():
    cp_names = []
    for i in range(len(bpy.data.objects)):
        if bpy.data.objects[i].ernst.type == 'CONTROL_POINT':
            cp_names.append(bpy.data.objects[i].name)
    return cp_names

def get_collection_name(obj):
    for collection in bpy.data.collections:
        if collection.ernst.type == 'SDF_FUNCTION':
            is_in_collection = False
            for coll_obj in collection.objects:
                if obj.name == coll_obj.name:
                    is_in_collection = True
            if is_in_collection:
                return collection.name
    return 'scene'

def make_path_absolute(path):
    """ Prevent Blender's relative paths of doom """
    sane_path = lambda p: os.path.abspath(bpy.path.abspath(p))
    return sane_path(path)

COLOR_MAP = {
    "black": 30, "red": 31, "green": 32, "yellow": 33,
    "blue": 34, "magenta": 35, "cyan": 36, "white": 37,
}

def printc(*args, color="white", sep=' ', end='\n'):
    """
    カラー付きで複数の文字列を出力する。

    :param args: 出力する複数の文字列
    :param color: 色名（例: "red", "green", "blue"）
    :param sep: 引数間の区切り文字（デフォルトは空白）
    :param end: 最後に付加する文字（デフォルトは改行）
    """
    color_code = COLOR_MAP.get(color.lower(), 37)  # デフォルトは白
    text = sep.join(map(str, args))
    print(f"\033[{color_code}m{text}\033[0m", end=end)

def uniform_setter(shader, method_name, u_name, val):
    """
    任意のuniform設定メソッドを汎用的に処理する関数。
    """
    try:
        method = getattr(shader, method_name)
        method(u_name, val)
    except ValueError as e:
        printc(f"Error: Uniform '{u_name}' not found or incompatible. Details: {e}", color='yellow')
    except TypeError as e:
        printc(f"Error: Value for '{u_name}' is of an incompatible type. Details: {e}", color='red')
    except AttributeError as e:
        printc(f"Error: Shader does not have method '{method_name}'. Details: {e}", color='red')
    except Exception as e:
        printc(f"Unexpected error occurred while setting uniform '{u_name}' using '{method_name}': {e}", color='red')
    else:
        printc(f"Success: Uniform '{u_name}' set with: {val} using '{method_name}'", color='green')


# 各既存関数のラッパー
def uniform_bool(shader, u_name, val):
    uniform_setter(shader, "uniform_bool", u_name, val)


def uniform_sampler(shader, u_name, val):
    uniform_setter(shader, "uniform_sampler", u_name, val)


def uniform_int(shader, u_name, val):
    uniform_setter(shader, "uniform_int", u_name, val)


def uniform_float(shader, u_name, val):
    uniform_setter(shader, "uniform_float", u_name, val)

def miniFloatToUint(x):
    x = np.clip(np.float64(x), np.float64(-1),np.float64(1))*np.float64(127.00)
    sgn = np.float64(x>0.)
    x = np.absolute([x])[0]
    if x<.5: return np.uint32(0)
    exponent = np.floor(np.log2([x]))[0]
    mantissa = np.floor(np.float64(8)*(x / np.exp2([exponent]) - np.float64(1)))[0]
    if exponent>=np.float64(16):
        exponent=np.float64(15)
        mantissa=np.float64(7)
    res = np.uint32(sgn)<< np.uint32(7) | np.uint32(exponent) << np.uint32(3) | np.uint32(mantissa)
    return res


def packUnorm4x8(v):
    return miniFloatToUint(v.x) | miniFloatToUint(v.y)<<np.uint32(8) | miniFloatToUint(v.z)<<np.uint32(16) | miniFloatToUint(v.w)<<np.uint32(24)


def miniFloatToUint10(x):
    x = np.clip(x, np.float64(-1),np.float64(1))#*np.float64(511.00)
    sgn = np.float64(x>0.)
    x = np.absolute([x])[0]
    if x<.5: return np.uint32(0)
    exponent = np.floor(np.log2([x]))[0]
    mantissa = np.floor(np.float64(10)*(x / np.exp2([exponent]) - np.float64(1)))[0]
    if exponent>=np.float64(32):
        exponent=np.float64(31)
        mantissa=np.float64(15)
    res = np.uint32(sgn)<< np.uint32(9) | np.uint32(exponent) << np.uint32(4) | np.uint32(mantissa)
    return res


def sig_mag(x):
    usig = np.uint32(0) if np.sign(x)>=0 else np.uint32(1)
    x = np.clip(x, np.float64(-1), np.float64(1))*np.float64(511.00)
    umag = np.absolute([x])[0]
    return usig, umag


def packSnorm3x10miniF(vx, vy, vz):
    rx = miniFloatToUint10(vx)
    ry = miniFloatToUint10(vy)
    rz = miniFloatToUint10(vz)
    res = (rx << np.uint32(22)) | (ry << np.uint32(12)) | (rz << np.uint32(2))
    return res

def formatted_hex_upper(packed_val, length=10):
    """
    Convert the result of packSnorm3x10 to a fixed-length hexadecimal string in uppercase with a 'U' suffix.
    """
    return '0x' + format(packed_val, f'0{length-2}X') + 'U'

def packSnorm3x10(vx, vy, vz):
    xsig, xmag = sig_mag(vx)
    ysig, ymag = sig_mag(vy)
    zsig, zmag = sig_mag(vz)
    rx = (xsig << np.uint32(9) | np.uint32(xmag))
    ry = (ysig << np.uint32(9) | np.uint32(ymag))
    rz = (zsig << np.uint32(9) | np.uint32(zmag))
    res = (rx << np.uint32(22))| (ry << np.uint32(12))| (rz << np.uint32(2))
    return formatted_hex_upper(res)

def compile_uber_template(obj, target_cp_name, type, var_name, code_name, header, footer):
    if target_cp_name:
        domain = target_cp_name
    else:
        domain = obj.ernst.shader_proxy.get_code_domain()

    position = ''
    rotation = ''
    for i in range(len(obj.ernst.pmods.pmod)):
        pmd = obj.ernst.pmods.pmod[i].get_pmod()
        if pmd != None:
            if pmd.name == 'Translation':
                position = f'{er_var(obj.name)}_position'
                if ubo.enabled:
                    position = f'{ubo.name(position)}.xyz'
            if pmd.name == 'Rotation':
                rotation = f'{er_var(obj.name)}_rotation'
                if ubo.enabled:
                    rotation = f'{ubo.name(rotation)}.xyz'
    p_tra = f'{domain}+{position}'
    loader = sgd.module_lib.pmod['PMOD_ROT_3D']
    loader.used = True
    p_tra_rot = f'{loader.fncname}({p_tra}, {rotation})'
    p_tra = '('+p_tra+')'

    parent_position = ''
    parent_rotation = ''
    parent_p_tra=''
    parent_p_tra_rot=''
    parent_var_name = ''
    if obj.parent != None:
        for i in range(len(obj.parent.ernst.pmods.pmod)):
            pmd = obj.parent.ernst.pmods.pmod[i].get_pmod()
            if pmd != None:
                if pmd.name == 'Translation':
                    parent_position = f'{er_var(obj.parent.name)}_position'
                    if ubo.enabled:
                        parent_position = f'{ubo.name(parent_position)}.xyz'
                if pmd.name == 'Rotation':
                    parent_rotation = f'{er_var(obj.parent.name)}_rotation'
                    if ubo.enabled:
                        parent_rotation = f'{ubo.name(parent_rotation)}.xyz'
        p_domain = obj.parent.ernst.shader_proxy.get_code_domain()
        parent_p_tra = f'{p_domain}+{parent_position}'
        parent_p_tra_rot = f'{loader.fncname}({parent_p_tra}, {parent_rotation})'
        parent_p_tra = '('+parent_p_tra+')'

    position = obj.ernst.shader_proxy.get_code_position(position)
    rotation = obj.ernst.shader_proxy.get_code_rotation(rotation)
    if obj.parent != None:
        parent_position = obj.parent.ernst.shader_proxy.get_code_position(parent_position)
        parent_rotation = obj.parent.ernst.shader_proxy.get_code_rotation(parent_rotation)
        parent_var_name = er_var(obj.parent.name)

    lines = readUberScriptLines(type, code_name)
    code = ''
    for line in lines:
        line = line.replace('@VAR', var_name)
        line = line.replace('@CP_POS', position)
        line = line.replace('@CP_ROT', rotation)
        line = line.replace('@CP_TR', p_tra_rot)
        line = line.replace('@CP_T', p_tra)
        line = line.replace('@CP', domain)
        line = line.replace('@PARENT_POS', parent_position)
        line = line.replace('@PARENT_ROT', parent_rotation)
        line = line.replace('@PARENT', parent_var_name)
        line = line.replace('@PARENT_TR', parent_p_tra_rot)
        line = line.replace('@PARENT_T', parent_p_tra)
        code += line

    code = string.Template(code)
    variables = {
        "var": var_name,

        "d": 'td',
        "res": 'res',
        "dim": 'dim',
        "prp": 'props',
        "tp": 'tp',
        "trp": 'trp',

        "cp": domain,
        "cppos": position,
        "cprot": rotation,
        "cpt": p_tra,
        "cptr": p_tra_rot,

        "pppos": parent_position,
        "pprot": parent_rotation,
        "pp": parent_var_name,
        "ppt": parent_p_tra,
        "pptr": parent_p_tra_rot,
    }
    code = code.substitute(variables)

    code = header + code + footer

    return code