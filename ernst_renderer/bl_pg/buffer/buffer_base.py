import time
from threading import Timer
import math
import bpy
from pathlib import Path
import gpu
from mathutils import Matrix
from gpu_extras.batch import batch_for_shader
from ...util import notification

from ...util.notification import Notification
from ...bl_ot.shadergen.shaderizer.shaderizer_formatter import format_code

from ...bl_ot.shadergen.shadergen_util import *
from ...bl_ot.shadergen.shaderizer.shaderizer_object import *
from ...bl_ot.shadergen.shaderizer import shaderizer_trvs

from ...bl_ot.shadergen import shadergen_ubo as ubo

def view3d_find():
    # returns first 3d view, normally we get from context
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            v3d = area.spaces[0]
            rv3d = v3d.region_3d
            for region in area.regions:
                if region.type == 'WINDOW':
                    return region, rv3d
    return None, None

def view3d_camera_border(scene):
    obj = scene.camera
    cam = obj.data

    frame = cam.view_frame(scene=scene)

    # move from object-space into world-space
    frame = [obj.matrix_world @ v for v in frame]

    # move into pixelspace
    from bpy_extras.view3d_utils import location_3d_to_region_2d
    region, rv3d = view3d_find()
    frame_px = [location_3d_to_region_2d(region, rv3d, v) for v in frame]
    return frame_px

def add_push_constant(shader_info, type, name):
    if type=='' or name=='':
        return

    try:
        # push_constantを追加
        shader_info.push_constant(type, name)
    except ValueError as e:
        # 値が不正な場合（例えば型がサポートされていない場合）
        print(f"ValueError: Failed to add push constant '{name}' with type '{type}'. Details: {e}")
    except TypeError as e:
        # 型が適切でない場合
        print(f"TypeError: Type '{type}' or name '{name}' is incompatible. Details: {e}")
    except AttributeError as e:
        # shader_infoオブジェクトが無効またはpush_constantが存在しない場合
        print(f"AttributeError: The object 'shader_info' does not support 'push_constant'. Details: {e}")
    except Exception as e:
        # その他の予期しないエラー
        print(f"Unexpected error occurred while adding push constant: {e}")
    else:
        # 成功時の処理（必要なら追加）
        print(f"Push constant '{name}' with type '{type}' added successfully.")
    finally:
        # リソース解放や後処理（必要なら追加）
        pass

class BufferBase():
    vertices = ((-1,-1, 0), (1,-1, 0), (-1,1, 0), (1,1, 0))
    indices = ((0, 1, 2), (2, 1, 3))

    unifroms_bl = '\n'
    unifroms_bl+='uniform sampler2D matcap;\n'
    unifroms_bl+='uniform sampler2D iChannel0;\n'
    unifroms_bl+='uniform sampler2D iChannel1;\n'
    unifroms_bl+='uniform sampler2D iChannel2;\n'
    unifroms_bl+='uniform sampler2D iChannel3;\n'

    code_vert = '''
    //in vec3 position;
    void main(){gl_Position = vec4(position, 1);}'''

    common_header_bl = '''
    #extension GL_ARB_uniform_buffer_object : require
    //in vec3 pos;
    //out vec4 outColor;
    //uniform float iTime;
    //uniform int iFrame;
    //uniform vec2 iResolution;
    //uniform vec2 iOffset;
    // Visual Debugging Util by iY0Yi
    // dbg_1F() / dbg_2V() / dbg_3V() / drawDebug()
    // https://www.shadertoy.com/view/ttVcWD
    vec4 dbC=vec4(0);
    void dbg_1F(float v){dbC=vec4(v,v,v,1);}
    void dbg_2V(vec2 v) {dbC=vec4(v,0,1);}
    void dbg_3V(vec3 v) {dbC=vec4(v,1);}
    void drawDebug(inout vec4 frC)
    {if(dbC.w>0.)frC=pow(dbC,vec4(.4545));}
    '''

    common_footer_bl = '''
    void main(){
        //*
        if(
            any(lessThan(gl_FragCoord.xy,iOffset)) ||
            any(greaterThanEqual(gl_FragCoord.xy-iOffset,iResolution.xy))
        ){
            discard;
        }
        //*/
        vec4 color = vec4(1);
        mainImage(color, gl_FragCoord.xy-iOffset);
        drawDebug(color);
        outColor = color;
    }
    '''

    shader = None
    batch = None
    offscreen = gpu.types.GPUOffScreen(512, 512)
    name = ''
    code_name_real = ''
    ichannel0 = None
    ichannel1 = None
    ichannel2 = None
    ichannel3 = None
    interpolation = 'linear'
    wrap = 'clamp'
    texture_h = 0
    uniforms = []

    def __init__(self, name):
        self.name = name.strip().lower()

    def compile(self, context, code_name_real):

        self.code_name_real = code_name_real

        if self.code_name_real == None:
            return

        if not sgd.is_exporting:
            if self.name != 'image':
                vw = vh = 0
                for region in context.area.regions:
                    if region.type == 'WINDOW':
                        vw = region.width
                        vh = region.height
                self.resize_offscreen(vw, vh)

        path = Path(self.code_name_real)

        with path.open() as file:
            code = self.common_header_bl

            if not sgd.is_exporting:
                code += self.unifroms_bl
                code += sgd.code_uniform_camera
                code += sgd.code_uniform_lights
            code += parse_for_includes(file.read(), str(path))

            code += self.common_footer_bl

            shader_info = gpu.types.GPUShaderCreateInfo()

            #  extract uniforms with borrowed code by leon.
            # https://github.com/leon196/blender-glsl-addon
            rows = code.split("\n")
            lines = []
            images = 0
            code = format_code(code)

            for row in rows:
                if "uniform" in row:
                    column = row.split(" ")
                    type = column[1].upper()
                    name = column[2].rstrip(';')
                    if "SAMPLER2D" in type:
                        shader_info.sampler(images,"FLOAT_2D", name)
                        images += 1
                    else:
                        add_push_constant(shader_info, type, name)

                if "uniform" not in row and "attribute" not in row and "varying" not in row:
                    lines.append(row)

            code = "\n".join(lines)

            if bpy.context.workspace.ernst.print_code: print(code)


            if ubo.enabled:
                shader_info.typedef_source(ubo.data.get_shader_code())
                shader_info.uniform_buf(0, ubo.TYPE_NAME, ubo.SHADER_NAME)
            shader_info.push_constant('FLOAT', "iTime")
            shader_info.push_constant('INT', "iFrame")
            shader_info.push_constant('VEC2', "iOffset")
            shader_info.push_constant('VEC2', "iResolution")
            shader_info.vertex_in(0, 'VEC3', "position")
            shader_info.vertex_source(self.code_vert)
            shader_info.fragment_out(0, 'VEC4', "outColor")
            shader_info.fragment_source(code)
            start_time = time.time()
            self.shader = gpu.shader.create_from_info(shader_info)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"gpu.types.GPUShader: {elapsed_time:.5f}sec")
            del shader_info
            try:
                self.batch = batch_for_shader(self.shader, 'TRIS', {'position': self.vertices}, indices=self.indices)
                notification.add(Notification(f'Compiled: {self.name}', 5, notification.OK))
            except:
                notification.add(Notification('Error on compiling', 5, notification.ERROR))

    def update_sb_uniforms(self, context):
        ox = oy = 0
        vw = vh = 0
        for region in context.area.regions:
            if region.type == 'WINDOW':
                vw = region.width
                vh = region.height

        area = context.area
        pers = area.spaces.active.region_3d.view_perspective

        if pers == 'CAMERA':
            frame_px = view3d_camera_border(context.scene)
            ox = frame_px[2].x if self.name == 'image' else 0
            oy = frame_px[2].y if self.name == 'image' else 0
            vw = frame_px[0].x - frame_px[2].x
            vh = frame_px[0].y - frame_px[2].y

        #https://docs.blender.org/api/master/gpu.types.html?highlight=uniform_float#gpu.types.GPUShader.uniform_float
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        # ml = vh/vw if min(vw, vh)==vw else 1.0
        # uniform_float(self.shader, 'iOffset', (ox, oy))      #viewport resolution (in pixels)
        # uniform_float(self.shader, 'iResolution', (vw, vh))      #viewport resolution (in pixels)
        self.shader.uniform_float('iOffset', (ox, oy))

        # settings = bpy.context.workspace.ernst
        # u_res_scale = settings.resolution_scale
        # self.shader.uniform_float('iResolution', (int(vw/u_res_scale), int(vh/u_res_scale)))
        self.shader.uniform_float('iResolution', (vw, vh))

        # self.shader.uniform_float('iResolution', (vw, vh))

        # self.shader.uniform_float('iTime', bpy.data.scenes['Scene'].frame_current/bpy.data.scenes['Scene'].render.fps)
        uniform_float(self.shader, 'iTime', bpy.data.scenes['Scene'].frame_current/bpy.data.scenes['Scene'].render.fps)
        #self.shader.uniform_float('iTimeDelta', 1/60)              #render time (in seconds)
        # self.shader.uniform_int('iFrame', bpy.data.scenes['Scene'].frame_current)
        # uniform_int(self.shader, 'iFrame', bpy.data.scenes['Scene'].frame_current)                       # shader playback frame
        #self.shader.uniform_float('iFrameRate', 60)                # shader playback frame
        #self.shader.uniform_float('iChannelTime', (512,512))       #channel playback time (in seconds)
        #self.shader.uniform_float('iChannelResolution', (512,512)) #channel resolution (in pixels)
        #self.shader.uniform_float('iMouse', (512,512,512,512))     #mouse pixel coords. xy: current (if MLB down), zw: click
        #self.shader.uniform_float('iChannel0', 0)                  #input channel. XX = 2D/Cube
        #self.shader.uniform_float('iChannel1', 1)                  #input channel. XX = 2D/Cube
        #self.shader.uniform_float('iChannel2', 2)                  #input channel. XX = 2D/Cube
        #self.shader.uniform_float('iChannel3', 3)                  #input channel. XX = 2D/Cube
        #self.shader.uniform_float('iDate', 512)                    #(year, month, day, time in seconds)
        #self.shader.uniform_float('iSampleRate', 44100)            #sound sample rate (i.e., 44100)

    def update_gui_uniforms(self):
        GUI_NAME = 'BluGui_1f'
        if bpy.data.objects.find(GUI_NAME)!=-1:
            holder = bpy.data.objects[GUI_NAME]
            for obj in holder.children:
                if len(obj.children)>=1:
                    uniform_float(self.shader, str(obj.children[0].name), obj.children[0].location.x)#0.025)

        GUI_NAME = 'BluGui_2v'
        if bpy.data.objects.find(GUI_NAME)!=-1:
            holder = bpy.data.objects[GUI_NAME]
            for obj in holder.children:
                uniform_float(self.shader, str(obj.name), (obj.location.x, obj.location.y))

        GUI_NAME = 'BluGui_3v'
        if bpy.data.objects.find(GUI_NAME)!=-1:
            holder = bpy.data.objects[GUI_NAME]
            for obj in holder.children:
                uniform_float(self.shader, str(obj.name), (obj.location.x, obj.location.y, obj.location.z))

    def update_scene_uniforms(self, context):
        wld = bpy.data.worlds[0]
        if ubo.enabled:
            ubo.data['bl_wld_amb'] = (wld.ernst.amb_col[0], wld.ernst.amb_col[1], wld.ernst.amb_col[2], wld.ernst.amb_strength)
            ubo.data['bl_wld_fog_col'] = (wld.ernst.fog_col[0], wld.ernst.fog_col[1], wld.ernst.fog_col[2], 0)
            ubo.data['bl_wld_fog_start_pow'] = (wld.ernst.fog_start, wld.ernst.fog_pow, 0, 0)
        else:
            uniform_float(self.shader, 'bl_wld_amb_col', wld.ernst.amb_col)
            uniform_float(self.shader, 'bl_wld_amb_strength', wld.ernst.amb_strength)
            uniform_float(self.shader, 'bl_wld_fog_col', wld.ernst.fog_col)
            uniform_float(self.shader, 'bl_wld_fog_start', wld.ernst.fog_start)
            uniform_float(self.shader, 'bl_wld_fog_pow', wld.ernst.fog_pow)

        er = context.workspace.ernst
        off_x = er.canvas_offset_x/100
        off_y = er.canvas_offset_y/100
        if ubo.enabled:
            ubo.data['canvas_offset'] = (off_x, off_y, int(er.canvas_mode),0)
        else:
            uniform_bool(self.shader, 'is_canvas_mode', er.canvas_mode)
            uniform_float(self.shader, 'canvas_offset', (off_x, off_y))

        for obj in bpy.data.objects:
            if obj.ernst.is_ernst_obj:
                obj.ernst.shader_proxy.update_uniforms(self.shader)

        for material in bpy.data.materials:
            if material.ernst.is_ernst_mat:
                material.ernst.shader_proxy.update_uniforms(self.shader)

    def update_uniforms(self, context, need_UBO):
        if self.shader == None:
            return

        vw = vh = 0
        for region in context.area.regions:
            if region.type == 'WINDOW':
                vw = region.width
                vh = region.height

                area = context.area
                pers = area.spaces.active.region_3d.view_perspective

                if pers == 'CAMERA':
                    frame_px = view3d_camera_border(context.scene)
                    vw = math.floor(frame_px[0].x - frame_px[2].x)
                    vh = math.floor(frame_px[0].y - frame_px[2].y)

        self.resize_offscreen(vw, vh)
        self.shader.bind()

        if(self.ichannel0!=None):self.ichannel0.update_uniform(context, self.shader, 'iChannel0')
        if(self.ichannel1!=None):self.ichannel1.update_uniform(context, self.shader, 'iChannel1')
        if(self.ichannel2!=None):self.ichannel2.update_uniform(context, self.shader, 'iChannel2')
        if(self.ichannel3!=None):self.ichannel3.update_uniform(context, self.shader, 'iChannel3')
        shaderizer_trvs.bind_texture(self.shader)
        self.update_sb_uniforms(context)
        self.update_gui_uniforms()
        self.update_scene_uniforms(context)
        img_matcap = bpy.data.images[bpy.context.workspace.ernst.matcap]
        tx_matcap = gpu.texture.from_image(img_matcap)

        settings = bpy.context.workspace.ernst
        u_dist_min = settings.hit_distance
        u_dist_max = settings.end_distance
        u_steps_max = settings.max_marching_steps
        u_res_scale = settings.resolution_scale
        if ubo.enabled:
            ubo.data['renderSettings'] = (u_dist_min, u_dist_max, u_steps_max, u_res_scale)
        else:
            uniform_float(self.shader, 'ufDistMin', u_dist_min)
            uniform_float(self.shader, 'ufDistMax', u_dist_max)
            uniform_int(self.shader, 'uiStepMax', u_steps_max)
            uniform_float(self.shader, 'ufResScale', u_res_scale)
        # uniform_int(self.shader, 'matcap', img_matcap.bindcode)
        uniform_sampler(self.shader, 'matcap', tx_matcap)

        if ubo.enabled:
            ubo.update(self.shader)

    def render(self):
        if self.batch == None:
            return

        if self.name == 'image':
            self.batch.draw(self.shader)
            return

        with self.offscreen.bind():
            with gpu.matrix.push_pop():
                gpu.matrix.load_matrix(Matrix.Identity(4))
                gpu.matrix.load_projection_matrix(Matrix.Identity(4))
                self.batch.draw(self.shader)

    def resize_offscreen(self, vw, vh):
        settings = bpy.context.workspace.ernst
        u_res_scale = settings.resolution_scale

        if self.offscreen == None:
            return

        if self.offscreen.width == int(vw/u_res_scale) or self.offscreen.height == int(vh/u_res_scale):
            return

        try:
            self.offscreen = gpu.types.GPUOffScreen(int(vw/u_res_scale), int(vh/u_res_scale), format="RGBA32F")
        except:
            self.offscreen = gpu.types.GPUOffScreen(int(vw/u_res_scale), int(vh/u_res_scale))

        def hack_draw():
            camera_select = bpy.data.objects['cam0'].select_get()
            bpy.data.objects['cam0'].select_set(camera_select)

        if not sgd.is_exporting:
            # Hack for force redraw the View3D...
            camera_select = bpy.data.objects['cam0'].select_get()
            bpy.data.objects['cam0'].select_set(camera_select)
            timer = Timer(1./120., hack_draw)
            timer.start()
