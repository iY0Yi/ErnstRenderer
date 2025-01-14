vec3 unpackUnorm3x10(uint x) {
	uvec3 r = (uvec3(x) >> uvec3(22, 12, 2)) & uvec3(0x3FF);
	vec3 v = vec3(r) / 1023.0;
	return v;
}
#define unpackU3(x) unpackUnorm3x10(floatBitsToUint(x))
