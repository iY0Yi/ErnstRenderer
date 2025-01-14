// clang-format off
#include bl_inc_common.glslinc
// clang-format on

void mainImage(out vec4 fragColor, vec2 fragCoord) {
  ivec2 iCoord = ivec2(fragCoord);
	// clang-format off
  @BL_ANIM_FRAMES_DATA
	// clang-format on
  fragColor = vec4(0, 0, 0, 1);
}
