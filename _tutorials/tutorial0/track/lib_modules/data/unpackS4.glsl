vec4 unpackSnorm4x8(uint x) {
	uvec4 r = (uvec4(x) >> uvec4(24, 16, 8, 0)) & uvec4(0xFF);
	uvec4 sig = r >> 7;
	uvec4 mag = r & uvec4(0x7F);
	vec4 fsig = mix(vec4(-1), vec4(1), greaterThanEqual(sig,uvec4(1)));
	vec4 fmag = vec4(mag) / 127.;
	return fsig * fmag;
}
#define unpackS4(x) unpackSnorm4x8(floatBitsToUint(x))
