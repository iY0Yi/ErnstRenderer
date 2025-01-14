uint packSnorm4x8(vec4 x) {
	x = round(clamp(x,-1., 1.) * 127.);
	uvec4 sig = uvec4(mix(vec4(0), vec4(1), greaterThanEqual(sign(x),vec4(0))));
	uvec4 mag = uvec4(abs(x));
	uvec4 r = sig << 7 | mag;
	return r.x << 24 | r.y << 16 | r.z << 8 | r.w;
}
#define packS4(x) uintBitsToFloat(packSnorm4x8(x))
