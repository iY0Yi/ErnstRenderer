import string
import math
import bpy
from bpy.types import PropertyGroup

from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen.shaderizer import shaderizer_watcher
from ...bl_ot.shadergen.shaderizer import shaderizer_trvs
from ...bl_ot.shadergen.shaderizer.shaderizer_object import *
from ...util.util import *
from ...util.map import Map
from ...bl_ot.shadergen import shadergen_ubo as ubo

is_dirty = {}

def force_dirty(self, context):
    pmods = self.id_data.ernst.pmods.pmod
    for pmod in pmods.values():
        pmd = pmod.get_pmod()
        if pmd != None and pmd.name == 'IKArmature':
            pmd.set_dirty(True)

cached_items = []
def enum_items(self, context):
    return dynamic_enum_files('uber_scripts/ik', cached_items)

class ERNST_PG_PModifier_IKArmature(PropertyGroup):
    name: bpy.props.StringProperty(default = 'IKArmature')
    icon: bpy.props.StringProperty(default = 'CON_KINEMATIC')
    visible: bpy.props.BoolProperty(default = True, update=shaderizer_watcher.check)
    expanded : bpy.props.BoolProperty(default=True)
    use_keyframe_anim : bpy.props.BoolProperty(default=True, update=shaderizer_watcher.check)

    file_name: bpy.props.StringProperty(
        name="",
        description="Choose a file",
        default="",
        maxlen=1024,
        subtype='FILE_PATH',
        update=shaderizer_watcher.check
    )

    def get_uniform_names(self, target_cp_name, id):
        obj = self.id_data
        u_names = {}
        u_names['root_pos'] = f'{er_var(obj.name)}_ik_root_pos'
        u_names['root_rot'] = f'{er_var(obj.name)}_ik_root_rot'
        u_names['pole_pos'] = f'{er_var(obj.name)}_ik_pole_pos'
        u_names['target_pos'] = f'{er_var(obj.name)}_ik_target_pos'
        u_names['length_a'] = f'{er_var(obj.name)}_ik_length_a'
        u_names['length_b'] = f'{er_var(obj.name)}_ik_length_b'
        u_names['root_pos_length_a'] = f'{er_var(obj.name)}_ik_root_pos_length_a'
        u_names['root_rot_length_b'] = f'{er_var(obj.name)}_ik_root_rot_length_b'
        return u_names

    def draw_gui(self, layout, obj, id, active):
        pmod_box = layout.box()

        obj_name_joint = []
        obj_name_target = []
        obj_name_pole = []
        for ob in bpy.data.objects:
            if ob.ernst.is_ernst_obj and ob.ernst.type == 'CONTROL_POINT':
                pmods = ob.ernst.pmods.pmod
                for pmod in pmods.values():
                    pmd = pmod.get_pmod()
                    if pmd != None:
                        if pmd.name == 'IKBoneJoint' and pmd.object_root==obj:
                            obj_name_joint.append(ob.name)
                        if pmd.name == 'IKBoneTarget' and pmd.object_root==obj:
                            obj_name_target.append(ob.name)
                        if pmd.name == 'IKPole' and pmd.object_root==obj:
                            obj_name_pole.append(ob.name)


        target_box = pmod_box.box()
        row = target_box.row()
        if len(obj_name_target)==0:
            row.alert = True
            row.label(text=f'Target: (Empty)', icon='BONE_DATA')
        elif len(obj_name_target)==1:
            row.label(text=f'Target: {obj_name_target[0]}', icon='BONE_DATA')
        else:
            row.alert = True
            row.label(text=f'Target: (Too Many Targets!)', icon='BONE_DATA')

        joint_box = pmod_box.box()
        row = joint_box.row()
        if len(obj_name_joint)==0:
            row.alert = True
            row.label(text=f'Joint: (Empty)', icon='BONE_DATA')
        elif len(obj_name_joint)==1:
            row.label(text=f'Joint: {obj_name_joint[0]}', icon='BONE_DATA')
        else:
            row.alert = True
            row.label(text=f'Joint: (Too Many Joints!)', icon='BONE_DATA')

        pole_box = pmod_box.box()
        row = pole_box.row()
        if len(obj_name_pole)==0:
            row.alert = True
            row.label(text=f'Pole: (Empty)', icon='CONSTRAINT_BONE')
        elif len(obj_name_pole)==1:
            row.label(text=f'Pole: {obj_name_pole[0]}', icon='CONSTRAINT_BONE')
        else:
            row.alert = True
            row.label(text=f'Pole: (Too Many Poles!)', icon='CONSTRAINT_BONE')

        row = pmod_box.row(align=True)
        col = row.column(align=True)
        col.prop(self, "file_name", expand=False, icon='TEXT')
        is_active = self.file_name != ''
        col.active = is_active

        row = pmod_box.row(align=True)
        col = row.column(align=True)
        col.prop(self, "use_keyframe_anim", text='Use TRV translation')


    def get_uniform_dec_code(self, target_cp_name, id):
        if self.visible==False:
            return ''
        u_names = self.get_uniform_names(target_cp_name, id)
        if ubo.enabled:
            code_u_names = ''
            ubo.add_vec4(u_names['root_pos_length_a'])
            ubo.add_vec4(u_names['root_rot_length_b'])
            ubo.add_vec4(u_names['pole_pos'])
            ubo.add_vec4(u_names['target_pos'])
        else:
            code_u_names = f'''
            uniform vec3 {u_names['root_pos']};
            uniform vec3 {u_names['root_rot']};
            uniform vec3 {u_names['pole_pos']};
            uniform vec3 {u_names['target_pos']};
            uniform float {u_names['length_a']};
            uniform float {u_names['length_b']};
            '''
        return code_u_names

    def set_dirty(self, bool):
        obj = self.id_data
        is_dirty[obj.name] = bool

    def update_uniforms(self, shader, target_cp_name, id):
        if self.visible==False:
           return
        obj = self.id_data
        obj_name_joint = []
        obj_name_target = []
        obj_name_pole = []
        for ob in bpy.data.objects:
            if ob.ernst.is_ernst_obj and ob.ernst.type == 'CONTROL_POINT':
                pmods = ob.ernst.pmods.pmod
                for pmod in pmods.values():
                    pmd = pmod.get_pmod()
                    if pmd != None:
                        if pmd.name == 'IKBoneJoint' and pmd.object_root==obj:
                            obj_name_joint.append(ob.name)
                        if pmd.name == 'IKBoneTarget' and pmd.object_root==obj:
                            obj_name_target.append(ob.name)
                        if pmd.name == 'IKPole' and pmd.object_root==obj:
                            obj_name_pole.append(ob.name)
        obj_target = bpy.data.objects[obj_name_target[0]]
        obj_joint = bpy.data.objects[obj_name_joint[0]]
        obj_pole = bpy.data.objects[obj_name_pole[0]]

        u_names = self.get_uniform_names(target_cp_name, id)
        if ubo.enabled:
            if not obj.name in is_dirty:
                self.set_dirty(True)
            if is_dirty[obj.name] or ubo.is_dirty:
                v = get_world_pos(obj)
                l = math.dist(get_world_pos(obj), get_world_pos(obj_joint))
                ubo.data[u_names['root_pos_length_a']] = (v[0], v[1], v[2], l)
                v = get_world_rot(obj)
                l = math.dist(get_world_pos(obj_joint), get_world_pos(obj_target))
                ubo.data[u_names['root_rot_length_b']] = (v[0], v[1], v[2], l)
                v = get_world_pos(obj_pole)
                ubo.data[u_names['pole_pos']] = (v[0], v[1], v[2], 0)
                v = get_world_pos(obj_target)
                ubo.data[u_names['target_pos']] = (v[0], v[1], v[2], 0)
                self.set_dirty(False)
        else:
            v = get_world_pos(obj)
            uniform_float(shader, u_names['root_pos'], v)
            v = get_world_rot(obj)
            uniform_float(shader, u_names['root_rot'], v)
            v = get_world_pos(obj_pole)
            uniform_float(shader, u_names['pole_pos'], v)
            v = get_world_pos(obj_target)
            uniform_float(shader, u_names['target_pos'], v)
            l = math.dist(get_world_pos(obj), get_world_pos(obj_joint))
            uniform_float(shader, u_names['length_a'], l)
            l = math.dist(get_world_pos(obj_joint), get_world_pos(obj_target))
            uniform_float(shader, u_names['length_b'], l)

    def get_shader_code(self, obj, target_cp_name, id, is_fixed):
        if self.visible==False:
            return ''

        # self.file_name = '//track/uber_scripts/ik/'+self.code_name

        file_name = os.path.basename(self.file_name)

        loader = sgd.module_lib.pmod['PMOD_ROT_3D']
        loader.used = True

        u_names = self.get_uniform_names(target_cp_name, id)

        obj_name_joint = []
        obj_name_target = []
        obj_name_pole = []
        for ob in bpy.data.objects:
            if ob.ernst.is_ernst_obj and ob.ernst.type == 'CONTROL_POINT':
                pmods = ob.ernst.pmods.pmod
                for pmod in pmods.values():
                    pmd = pmod.get_pmod()
                    if pmd != None:
                        if pmd.name == 'IKBoneJoint' and pmd.object_root==obj:
                            obj_name_joint.append(ob.name)
                        if pmd.name == 'IKBoneTarget' and pmd.object_root==obj:
                            obj_name_target.append(ob.name)
                        if pmd.name == 'IKPole' and pmd.object_root==obj:
                            obj_name_pole.append(ob.name)


        obj_target = bpy.data.objects[obj_name_target[0]]
        obj_joint = bpy.data.objects[obj_name_joint[0]]
        obj_pole = bpy.data.objects[obj_name_pole[0]]

        ika = f'ika_{er_var(obj.name)}'
        ika_base = f'ika_{er_var(obj.name)}_base'

        if is_fixed:
            root_pos = er_v3(get_local_pos(obj).xzy)
            pole_pos = er_v3(get_local_pos(obj_pole).xzy)
            target_pos = er_v3(get_local_pos(obj_target).xzy)
        else:
            if ubo.enabled:
                root_pos = f'ubo.{u_names["root_pos_length_a"]}.xyz'
                pole_pos = f'ubo.{u_names["pole_pos"]}.xyz'
                target_pos = f'ubo.{u_names["target_pos"]}.xyz'
            else:
                root_pos = u_names['root_pos']
                pole_pos = u_names['pole_pos']
                target_pos = u_names['target_pos']

        length_a = er_f(math.dist(get_world_pos(obj),get_world_pos(obj_joint)))# if is_fixed else u_names['length_a']
        length_b = er_f(math.dist(get_world_pos(obj_joint),get_world_pos(obj_target)))# if is_fixed else u_names['length_b']

        loader_rot = sgd.module_lib.pmod['PMOD_ROT_2D']
        loader_rot.used = True
        rot = er_v3(get_local_rot(obj).xzy) if is_fixed else u_names['root_rot']

        def get_key_code(obj, u_name):
            key_code = 'vec3(0)'
            if self.use_keyframe_anim:
                is_editing = bpy.context.scene.ernst.enable_edit_trvs
                if is_editing:
                    key_code = u_name
                else:
                    shaderizer_trvs.addTRVobj(obj, 'trans')
                    key_code = shaderizer_trvs.get_code(obj, 'trans')
            return key_code

        key_target = get_key_code(obj_target, target_pos)
        key_pole = get_key_code(obj_pole, pole_pos)

        print('key_target: ', key_target)
        print('key_pole: ', key_pole)

        code_ik_script = ''
        is_active = file_name != ''
        if is_active:
            code_ik_script = readUberScript('ik', file_name)
            code_ik_script = '{\n' + code_ik_script + '}\n'
        code_ik_script = string.Template(code_ik_script)
        variables = {
            "ika": ika,
            "ika_base": ika_base,
            "root_pos": root_pos,
            "pole_pos": pole_pos,
            "target_pos": target_pos,
            "length_a": length_a,
            "length_b": length_b,
            "key_target": key_target,
            "key_pole": key_pole,
        }
        code_ik_script = code_ik_script.substitute(variables)

        code = f'''
        // calc IK
        IKArmature {ika};

        // Bone 1 initialization
        {ika}.bon[0].len = 0.;
        {ika}.bon[0].tail = {root_pos};
        {ika}.bon[0].quat = vec4(0);

        // Bone 2 initialization
        {ika}.bon[1].len = {length_a};
        {ika}.bon[1].tail = vec3(0);
        {ika}.bon[1].quat = vec4(0);

        // Target initialization
        {ika}.bon[2].len = {length_b};
        {ika}.bon[2].tail = {target_pos};
        {ika}.bon[2].quat = vec4(0);

        // Pole vector initialization
        {ika}.pol = {pole_pos};

        {code_ik_script}

        calcIK({ika});

        // base rotation
        vec3 {ika_base} = {target_cp_name};

        // rig root
        {target_cp_name} = {ika_base};

        pIKRig({target_cp_name}, {ika}.bon[0]);

        '''
        return code