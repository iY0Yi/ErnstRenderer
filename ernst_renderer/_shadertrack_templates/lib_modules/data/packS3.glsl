uint packSnorm3x10(vec3 x) {
	x = round(clamp(x,-1., 1.) *.997 * 511.);
	uvec3 sig = uvec3(mix(vec3(0), vec3(1), greaterThanEqual(sign(x),vec3(0))));
	uvec3 mag = uvec3(abs(x));
	uvec3 r = sig.xyz << 9 | mag.xyz;
	return r.x << 22 | r.y << 12 | r.z << 2;
}
#define packS3(x) uintBitsToFloat(packSnorm3x10(x))
