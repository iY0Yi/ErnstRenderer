vec2 hash23(vec3 p){
	uvec3 q = uvec3(ivec3(p)) * UI3;
	uvec2 n = (q.x ^ q.y ^ q.z) * UI2;
	return vec2(n) * UIF;
}
