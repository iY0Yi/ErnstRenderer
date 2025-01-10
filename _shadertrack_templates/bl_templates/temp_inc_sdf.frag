// SDF functions
// ---------------------------------------------------------------------
@BL_ERNST_FNCS

#include ../uber_scripts/sdf3d/prim_sd_hand.frag
#include ../uber_scripts/sdf3d/inc_terrain_eroded.glsl

@BL_COLLECTION_FNCS

vec4 sdScene(vec3 p){
	float d = MAX_DIST;
	vec4 res = vec4(MAX_DIST, MAT_VOID);
@BL_MAP_FNC
	return res;
}
