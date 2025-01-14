import gpu
import ctypes
from ...util.map import Map

data = None
datalist = Map({'fields': [], 'shader_code':''})
instance = None

TYPE_NAME = 'Data'
SHADER_NAME = 'ubo'

is_dirty = False

enabled = True

def reset():
    global datalist
    datalist.fields.clear()
    datalist.shader_code = ''

def add_int(name):
    global datalist
    datalist.fields.append((name, ctypes.c_int))
    datalist.shader_code += f'int {name};\n'

def add_float(name):
    global datalist
    datalist.fields.append((name, ctypes.c_float))
    datalist.shader_code += f'float {name};\n'

def add_vec2(name):
    global datalist
    datalist.fields.append((name, ctypes.c_float*2))
    datalist.shader_code += f'vec2 {name};\n'

def add_vec3(name):
    global datalist
    datalist.fields.append((name, 3*ctypes.c_float))
    datalist.shader_code += f'vec3 {name};\n'

def add_vec4(name):
    global datalist
    datalist.fields.append((name, ctypes.c_float*4))
    datalist.shader_code += f'vec4 {name};\n'

# dynamic ctypes structures
# https://stackoverflow.com/questions/57417435/dynamically-defining-updating-ctypes-structure-in-python/57438020#57438020
def get_dynamic_UBO_class():
    global datalist
    class UBO_struct(ctypes.Structure):
        _pack_ = 16
        _fields_ = datalist.fields
        _shader_code = datalist.shader_code

        def __getitem__(self, key):
            return getattr(self, key)

        def __setitem__(self, key, value):
            setattr(self, key, value)

        def get_shader_code(self):
            return f'struct {TYPE_NAME}{{\n{self._shader_code}\n}};'

        def to_dict(self):
            # インスタンスのフィールドを辞書型に変換
            ubo_dict = {}
            for field in self._fields_:
                field_name, field_type = field[0], field[1]
                field_value = getattr(self, field_name)
                # if field_type == ctypes.c_float_Array_4:
                    # c_float_Array_4型をリストに変換して追加
                field_value = [field_value[i] for i in range(4)]
                ubo_dict[field_name] = field_value
            return ubo_dict

    return UBO_struct

def name(name):
    return f'{SHADER_NAME}.{name}'

def init():
    global data, instance, is_dirty
    print('ubo.init()')
    is_dirty = True
    data = get_dynamic_UBO_class()()
    instance = gpu.types.GPUUniformBuf(gpu.types.Buffer("UBYTE", ctypes.sizeof(data), data))

def update(shader):
    global data, instance, is_dirty
    instance.update(gpu.types.Buffer("UBYTE", ctypes.sizeof(data), data))
    shader.uniform_block(SHADER_NAME, instance)

