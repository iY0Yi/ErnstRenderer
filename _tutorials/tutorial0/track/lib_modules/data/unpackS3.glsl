vec3 unpackSnorm3x10(uint x) {
	uvec3 r = (uvec3(x) >> uvec3(22, 12, 2)) & uvec3(0x3FF);
	uvec3 sig = r >> 9;
	uvec3 mag = r & uvec3(0x1FF);
	vec3 fsig = mix(vec3(-1), vec3(1), greaterThanEqual(sig, uvec3(1)));
	vec3 fmag = vec3(mag) / 511.;
	return fsig * fmag;
}
#define unpackS3(x) unpackSnorm3x10(floatBitsToUint(x))
