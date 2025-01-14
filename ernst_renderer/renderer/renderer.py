import math
import bpy
from bpy.types import RenderEngine

from ..bl_ot.bl_ot_shader_compiler import *
from ..bl_ot.shadergen import shadergen
from ..bl_ot.shadergen import shadergen_data as sgd
from ..bl_ot.shadergen import shadergen_ubo as ubo
from ..bl_ot.shadergen.shadergen_util import *
from ..bl_ot.shadergen.shaderizer import shaderizer_watcher

initial_objects_names = None

class ErnstRenderEngine(RenderEngine):
    bl_idname = "ERNST"
    bl_label = "Ernst"
    bl_use_preview = False
    bl_use_shading_nodes_custom = False

    # Enable an OpenGL context for the engine (2.91+ only)
    bl_use_gpu_context = True

    # Apply Blender's compositing on render results.
    # This enables the "Color Management" section of the scene settings
    bl_use_postprocess = True

    def __init__(self):
        global initial_objects_names
        print('ErnstRenderEngine.__init__()')
        self.exist_datablock = None
        self.need_compile = True
        self.is_init = True
        # Start hot reloading...
        initial_objects_names = [obj.name for obj in bpy.context.scene.objects if obj.ernst.is_ernst_obj]
        bpy.app.timers.register(shaderizer_watcher.watch_codes)

    def __del__(self):
        print('ErnstRenderEngine.__del__()')
        if sgd.view_shading_type != 'SOLID':
            bpy.app.timers.unregister(shaderizer_watcher.watch_codes)

        sgd.view_shading_type = 'SOLID'

    def render(self, depsgraph):
        print('ErnstRenderEngine.render()')
        pass

    def view_update(self, context, depsgraph):
        print('ErnstRenderEngine.view_update()')
        global initial_objects_names

        if sgd.is_rendering == False and self.need_compile == False:
            if not self.exist_datablock:
                self.exist_datablock = []
                pass

            view = context.space_data
            shading = view.shading
            if sgd.view_shading_type != shading.type:
                sgd.view_shading_type = shading.type
                self.need_compile = True

            if shaderizer_watcher.need_analyze:
                print("RenderEngine: Codes updated.")
                self.need_compile = True

            if depsgraph.id_type_updated('MATERIAL'):
                for update in depsgraph.updates:
                    # print('update.is_updated_geometry: ', update.is_updated_geometry)
                    # print('update.is_updated_transform: ', update.is_updated_transform)
                    # print('update.is_updated_shading: ', update.is_updated_shading)
                    # print('update.id.rna_type.name: ', update.id.rna_type.name)
                    if update.id.rna_type.name == 'Material':
                        if not update.is_updated_geometry and not update.is_updated_transform and update.is_updated_shading:
                            update.id.ernst.shader_proxy.set_dirty(True)
                        if update.is_updated_geometry and update.is_updated_shading and update.is_updated_transform:
                            if update.id.rna_type.name != 'World':
                                print("RenderEngine: Materials updated.")
                                self.need_compile = True

            if depsgraph.id_type_updated('COLLECTION'):
                for update in depsgraph.updates:
                    data_block = update.id
                    data_block_type = data_block.rna_type.name
                    if self.need_compile:
                        break
                    # print('update.is_updated_geometry: ', update.is_updated_geometry)
                    # print('update.is_updated_transform: ', update.is_updated_transform)
                    # print('update.id.rna_type.name: ', update.id.rna_type.name)
                    # if update.is_updated_geometry and update.is_updated_transform and data_block_type=='Mesh':
                    #     print("RenderEngine: Collections updated.")
                    #     self.need_compile = True

            if depsgraph.id_type_updated('OBJECT'):
                for update in depsgraph.updates:
                    if self.need_compile:
                        break
                    if update.is_updated_geometry and not update.is_updated_transform:
                        # if ubo.enabled:
                        if update.id.rna_type.name == 'Object':
                            obj = update.id
                            if obj.ernst.type == 'SDF_3D_CAPSULE'\
                            or obj.ernst.type == 'SDF_3D_TORUS'\
                            or obj.ernst.type == 'SDF_3D_TORUS_CAPPED'\
                            or obj.ernst.type == 'SDF_3D_CONE'\
                            or obj.ernst.type == 'SDF_3D_CONE_ROUND'\
                            or obj.ernst.type == 'SDF_3D_CURVE_QUADRATIC'\
                            or obj.ernst.type == 'LIGHT_DIRECTIONAL'\
                            or obj.ernst.type == 'CAMERA'\
                            or obj.ernst.type == 'SDF_3D_CYLINDER_PIE':
                                print("RenderEngine: Objects updated.")
                                obj.ernst.shader_proxy.props.set_dirty(True)

                    if not update.is_updated_geometry and update.is_updated_transform:
                        # print("RenderEngine: Objects transform updated.")
                        if ubo.enabled:
                            if update.id.rna_type.name == 'Object':
                                obj = update.id
                                if obj.ernst.type == 'SDF_3D_SPHERE'\
                                or obj.ernst.type == 'SDF_3D_BOX'\
                                or obj.ernst.type == 'SDF_3D_ELLIPSOID'\
                                or obj.ernst.type == 'SDF_3D_CAPSULE'\
                                or obj.ernst.type == 'SDF_3D_CYLINDER'\
                                or obj.ernst.type == 'SDF_3D_CYLINDER_PIE'\
                                or obj.ernst.type == 'SDF_3D_TORUS'\
                                or obj.ernst.type == 'SDF_3D_TORUS_CAPPED'\
                                or obj.ernst.type == 'SDF_3D_CONE'\
                                or obj.ernst.type == 'SDF_3D_CONE_ROUND'\
                                or obj.ernst.type == 'SDF_3D_CURVE_QUADRATIC'\
                                or obj.ernst.type == 'SDF_3D_UBER'\
                                or obj.ernst.type == 'SDF_3D_INSTANCE'\
                                or obj.ernst.type == 'SDF_2D_CIRCLE'\
                                or obj.ernst.type == 'SDF_2D_UBER'\
                                or obj.ernst.type == 'LIGHT_DIRECTIONAL'\
                                or obj.ernst.type == 'CAMERA'\
                                or obj.ernst.type == 'SDF_2D_BOX':
                                    print("RenderEngine: Objects updated 2.", obj.name)
                                    obj.ernst.shader_proxy.props.set_dirty(True)

                                pmods = obj.ernst.pmods.pmod
                                for pmod in pmods.values():
                                    pmd = pmod.get_pmod()
                                    if type(pmd).__name__ == 'ERNST_PG_PModifier_Translation'\
                                    or type(pmd).__name__ == 'ERNST_PG_PModifier_Rotation'\
                                    or type(pmd).__name__ == 'ERNST_PG_PModifier_TRVsTranslation'\
                                    or type(pmd).__name__ == 'ERNST_PG_PModifier_TRVsRotation'\
                                    or type(pmd).__name__ == 'ERNST_PG_PModifier_IKArmature':
                                        print("RenderEngine: Pmods updated.")
                                        pmd.set_dirty(True)

            if not self.need_compile:
                current_objects_names = [obj.name for obj in bpy.context.scene.objects if obj.ernst.is_ernst_obj]
                changed_num = len(initial_objects_names) - len(current_objects_names)
                if math.fabs(changed_num)>0:
                    self.need_compile = True
                initial_objects_names = current_objects_names

            if self.need_compile:
                print('--------------------------------------------')
                print('shadergen.process(): renderer.view_update')
                shadergen.process(context)

                self.report({'INFO'}, 'Recompiled successfully.')
                self.need_compile = False

        if self.is_init:
            print('shadergen.process(): renderer.is_init')
            shadergen.process(context)
            self.is_init = False
            self.need_compile = False


    def view_draw(self, context, depsgraph):
        print('ErnstRenderEngine.view_draw()')
        scene = depsgraph.scene

        if not self.need_compile:
            self.bind_display_space_shader(scene)
            context.workspace.ernst.buffer_d.update_uniforms(context, False)
            context.workspace.ernst.buffer_d.render()
            context.workspace.ernst.buffer_c.update_uniforms(context, False)
            context.workspace.ernst.buffer_c.render()
            context.workspace.ernst.buffer_b.update_uniforms(context, False)
            context.workspace.ernst.buffer_b.render()
            context.workspace.ernst.buffer_a.update_uniforms(context, True)
            context.workspace.ernst.buffer_a.render()
            context.workspace.ernst.image.update_uniforms(context, False)
            context.workspace.ernst.image.render()
            ubo.is_dirty = False
            self.unbind_display_space_shader()
