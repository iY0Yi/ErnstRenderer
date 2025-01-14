import bpy
from bpy.types import PropertyGroup

from ...bl_ot.shadergen import shadergen_data as sgd
from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen.shaderizer import shaderizer_watcher
from ...bl_ot.shadergen.shaderizer.shaderizer_object import is_fixed
from .pmodifier_balloon import *
from .pmodifier_bend import *
from .pmodifier_elongate import *
from .pmodifier_mirror import *
from .pmodifier_mirror_rotation import *
from .pmodifier_mirror_scale import *
from .pmodifier_mirror_translation import *
from .pmodifier_uber import *
from .pmodifier_rep_limited import *
from .pmodifier_rep_polar import *
from .pmodifier_rotation import *
from .pmodifier_shear import *
from .pmodifier_taper import *
from .pmodifier_translation import *
from .pmodifier_trvs_rotation import *
from .pmodifier_trvs_translation import *
from .pmodifier_twist import *
from .pmodifier_spin import *
from .pmodifier_ik_armature import *
from .pmodifier_ik_bone_joint import *
from .pmodifier_ik_bone_target import *
from .pmodifier_ik_pole import *

class ERNST_PG_PmodWrapper(PropertyGroup):
    type : bpy.props.StringProperty(default='Mirror')
    translation : bpy.props.PointerProperty(type=ERNST_PG_PModifier_Translation)
    rotation : bpy.props.PointerProperty(type=ERNST_PG_PModifier_Rotation)
    trvs_translation : bpy.props.PointerProperty(type=ERNST_PG_PModifier_TRVsTranslation)
    trvs_rotation : bpy.props.PointerProperty(type=ERNST_PG_PModifier_TRVsRotation)
    mirror : bpy.props.PointerProperty(type=ERNST_PG_PModifier_Mirror)
    mirror_translation : bpy.props.PointerProperty(type=ERNST_PG_PModifier_MirrorTranslation)
    mirror_rotation : bpy.props.PointerProperty(type=ERNST_PG_PModifier_MirrorRotation)
    mirror_scale : bpy.props.PointerProperty(type=ERNST_PG_PModifier_MirrorScale)
    twist : bpy.props.PointerProperty(type=ERNST_PG_PModifier_Twist)
    spin : bpy.props.PointerProperty(type=ERNST_PG_PModifier_Spin)
    elongate : bpy.props.PointerProperty(type=ERNST_PG_PModifier_Elongate)
    by_code : bpy.props.PointerProperty(type=ERNST_PG_PModifier_UberScript)
    bend : bpy.props.PointerProperty(type=ERNST_PG_PModifier_Bend)
    balloon : bpy.props.PointerProperty(type=ERNST_PG_PModifier_Balloon)
    shear : bpy.props.PointerProperty(type=ERNST_PG_PModifier_Shear)
    taper : bpy.props.PointerProperty(type=ERNST_PG_PModifier_Taper)
    rep_limited : bpy.props.PointerProperty(type=ERNST_PG_PModifier_RepLimited)
    rep_polar : bpy.props.PointerProperty(type=ERNST_PG_PModifier_RepPolar)
    ik_armature : bpy.props.PointerProperty(type=ERNST_PG_PModifier_IKArmature)
    ik_bone_joint : bpy.props.PointerProperty(type=ERNST_PG_PModifier_IKBoneJoint)
    ik_bone_target : bpy.props.PointerProperty(type=ERNST_PG_PModifier_IKBoneTarget)
    ik_pole : bpy.props.PointerProperty(type=ERNST_PG_PModifier_IKPole)

    def get_pmod(self):
        if self.type == 'Mirror':
            return self.mirror
        elif self.type == 'MirrorTranslation':
            return self.mirror_translation
        elif self.type == 'MirrorRotation':
            return self.mirror_rotation
        elif self.type == 'MirrorScale':
            return self.mirror_scale
        elif self.type == 'Translation':
            return self.translation
        elif self.type == 'Rotation':
            return self.rotation
        elif self.type == 'TRVsTranslation':
            return self.trvs_translation
        elif self.type == 'TRVsRotation':
            return self.trvs_rotation
        elif self.type == 'Twist':
            return self.twist
        elif self.type == 'Spin':
            return self.spin
        elif self.type == 'Elongate':
            return self.elongate
        elif self.type == 'UberScript':
            return self.by_code
        elif self.type == 'Bend':
            return self.bend
        elif self.type == 'Balloon':
            return self.balloon
        elif self.type == 'Shear':
            return self.shear
        elif self.type == 'Taper':
            return self.taper
        elif self.type == 'RepLimited':
            return self.rep_limited
        elif self.type == 'RepPolar':
            return self.rep_polar
        elif self.type == 'IKArmature':
            return self.ik_armature
        elif self.type == 'IKBoneJoint':
            return self.ik_bone_joint
        elif self.type == 'IKBoneTarget':
            return self.ik_bone_target
        elif self.type == 'IKPole':
            return self.ik_pole


class ERNST_PG_PModifier(PropertyGroup):
    active_id : bpy.props.IntProperty()
    pmod : bpy.props.CollectionProperty(type=ERNST_PG_PmodWrapper)


    def add(self, type):
        self.active_id = len(self.pmod)-1
        pm_prop = self.pmod.add()
        pm_prop.type = type


    def remove(self, id):
        if len(self.pmod):
            self.pmod.remove(id)
            if len(self.pmod)-1 < self.active_id:
                self.active_id = len(self.pmod)-1
                if self.active_id < 0:
                    self.active_id = 0


    def move(self, index1, index2):
        if len(self.pmod) < 2:
            return
        if 0 <= index1 < len(self.pmod):
            if 0 <= index2 < len(self.pmod):
                self.pmod.move(index1, index2)
                self.active_id = index2


    def clear(self):
        self.pmod.clear()


    def draw_gui(self, layout, obj):
        for i in range(len(self.pmod)):
            pmd = self.pmod[i].get_pmod()
            if pmd != None:
                box_col_col = layout.column(align=True)
                pmod_box = box_col_col.box()
                row = pmod_box.row()
                col = row.column(align=False)
                col.prop(pmd, 'visible', text='')
                col = row.column(align=False)
                col.label(icon=pmd.icon, text=pmd.name)
                col.active = pmd.visible

                col = row.column(align=False)
                col.alignment = 'RIGHT'
                col_row = col.row(align = True)
                up = col_row.operator("view3d.my_uilist_move_item", icon='TRIA_UP', emboss=True, text="")
                up.type = 'UP'
                up.id = i
                down = col_row.operator("view3d.my_uilist_move_item", icon='TRIA_DOWN', emboss=True, text="")
                down.type = 'DOWN'
                down.id = i
                col_col = col_row.column(align=False)
                col_col.alignment = 'RIGHT'
                delete = col_col.operator("view3d.my_uilist_remove_item", icon='X', emboss=False, text="")
                delete.id = i
                # if pmd.expanded:
                pmd.draw_gui(box_col_col, obj, i, pmd.visible)


    def get_uniform_dec_code(self, obj):
        if is_fixed(obj):
            return ''

        code = ''
        target_cp_name = er_var(obj.name)
        if obj.ernst.type != 'CONTROL_POINT':
            target_cp_name = f'{er_var(obj.name)}_p'

        pmods = self.pmod
        mirror_id = -1
        for i in range(len(pmods)):
            pmod = pmods[i].get_pmod()
            pmod_id = i
            if pmod != None:
                if pmod.name == 'Mirror':
                    mirror_id += 1
                if pmod.name == 'Mirror' or pmod.name == 'Mirror Translation' or pmod.name == 'Mirror Rotation' or pmod.name == 'Mirror Scale':
                    pmod_id = mirror_id
                code += pmod.get_uniform_dec_code(target_cp_name, pmod_id)
        return code


    def update_uniforms(self, shader, obj):
        if not is_fixed(obj):
            target_cp_name = er_var(obj.name)
            if obj.ernst.type != 'CONTROL_POINT':
                target_cp_name = f'{er_var(obj.name)}_p'

            pmods = self.pmod
            mirror_id = -1
            for i in range(len(pmods)):
                pmod = pmods[i].get_pmod()
                pmod_id = i
                if pmod != None:
                    if pmod.name == 'Mirror':
                        mirror_id += 1
                    if pmod.name == 'Mirror' or pmod.name == 'Mirror Translation' or pmod.name == 'Mirror Rotation' or pmod.name == 'Mirror Scale':
                        pmod_id = mirror_id
                    pmod.update_uniforms(shader, target_cp_name, pmod_id)


    def get_shader_code(self, obj):
        code = ''
        target_cp_name = er_var(obj.name)
        if obj.ernst.type != 'CONTROL_POINT':
            target_cp_name = f'{er_var(obj.name)}_p'

        pmods = self.pmod
        mirror_id = -1
        for i in range(len(pmods)):
            pmod = pmods[i].get_pmod()
            pmod_id = i
            if pmod != None:
                if pmod.name == 'Mirror':
                    mirror_id += 1
                if pmod.name == 'Mirror' or pmod.name == 'Mirror Translation' or pmod.name == 'Mirror Rotation' or pmod.name == 'Mirror Scale':
                    pmod_id = mirror_id
                code += pmod.get_shader_code(obj, target_cp_name, pmod_id,  is_fixed(obj))
        return code + '\n'
