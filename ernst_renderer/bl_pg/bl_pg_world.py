from bpy.props import *
from bpy.types import PropertyGroup


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class ERNST_PG_WorldProperties(PropertyGroup):
    amb_col      : FloatVectorProperty(name='Ambient Color', subtype='COLOR', size = 3, min = 0.0, max = 1.0, default=(0,0,0))
    amb_strength : FloatProperty(name='Ambient Strength', min = 0.0, max = 1.0, default = 0.2)
    fog_col      : FloatVectorProperty(name='Fog Color', subtype='COLOR', size = 3, min = 0.0, max = 1.0, default=(0,0,0))
    fog_start    : FloatProperty(name='Fog Start', min = -1.0, max = 1.0, default = 0.0)
    fog_pow      : FloatProperty(name='Fog Power', min = 0.01, max = 100.0, default = 1.0)
