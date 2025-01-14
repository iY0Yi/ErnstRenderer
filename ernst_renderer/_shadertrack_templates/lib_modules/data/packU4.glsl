uint packUnorm4x8(vec4 x) {
	x = round(clamp(x, 0., 1.) * 255.);
	uvec4 r = uvec4(x);
	return r.x << 24 | r.y << 16 | r.z << 8 | r.w;
}
#define packU4(x) uintBitsToFloat(packUnorm4x8(x))
