vec4 unpackUnorm4x8(uint x) {
	uvec4 r = (uvec4(x) >> uvec4(24, 16, 8, 0)) & uvec4(0xFF);
	vec4 v = vec4(r) / 255.0;
	return v;
}
#define unpackU4(x) unpackUnorm4x8(floatBitsToUint(x))
