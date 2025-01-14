from ...util.map import Map

buffers = Map({
    'image' : None,
    'buffera' : None,
    'bufferb' : None,
    'bufferc' : None,
    'bufferd' : None
})

uniform_code = Map({
    'render_settings' : '',
})

view_shading_type = 'SOLID'

in_scene_sdfs = []
in_scene_cps = []
in_collection_sdfs = {}
in_collection_cps = {}
used_collections = []
is_1st_material = True
TRVs_objs = Map({'trans':{}, 'rot':{}})
materials = Map({})
boolean_orders = []
boolean_methods = []
uberscript_bool_lines = {}
is_active_blugui1f = False
is_active_blugui2v = False
is_active_blugui3v = False
is_active_bluguiCC = False

is_exporting = False
is_rendering = False
is_ignoring_watcher = False
fixed_num = 0

dir_trk_root = ''
dir_trk_uber_scripts = ''
dir_trk_lib_modules = ''
dirp_addon = None
dirp_temp_root = None
dirp_temp_inc = None
dirp_working = None
dirp_root = None
dirp_blex = None
dirp_lib = None

code_uber_scripts_info = {}

bool_uberscript_txt_name = []
code_uniform = ''
code_funcs = ''
code_scene = ''
code_collections = ''
code_material_dec = ''
code_material_params = ''

code_raymarch_buf_init_dec = ''
code_raymarch_buf_init_fnc = ''

module_lib = None