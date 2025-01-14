uint packUnorm3x10(vec3 x) {
	x = round(clamp(x, 0., 1.) * 1023.);
	uvec3 r = uvec3(x);
	return r.x << 22 | r.y << 12 | r.z << 2;
}
#define packU3(x) uintBitsToFloat(packUnorm3x10(x))
