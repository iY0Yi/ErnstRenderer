//SDF functions
#include ../lib_modules/colorblending/oklab_mix.glsl
#include ../lib_modules/colorblending/sub_mix.glsl
#include ../lib_modules/colorblending/ryb_mix.glsl
#include ../lib_modules/colorblending/perceptual_mix.glsl
#include ../lib_modules/colorblending/hsv_mix.glsl
#include ../lib_modules/colorblending/lch_mix.glsl
#include ../lib_modules/colorblending/nmz_mix.glsl
#include ../lib_modules/colorblending/pow_mix.glsl

@BL_ERNST_FNCS

@BL_COLLECTION_FNCS

vec4 sdScene(vec3 p) {
  float d = MAX_DIST;
  vec4 res = vec4(MAT_VOID, d);
  @BL_MAP_FNC
  return res;
}
