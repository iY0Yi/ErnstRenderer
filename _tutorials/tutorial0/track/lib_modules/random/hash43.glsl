vec4 hash43(vec3 p){
	uvec4 q = uvec4(ivec4(p.xyzx)) * UI4;
	q = (q.x ^ q.y ^ q.z ^ q.w)*UI4;
	return vec4(q) * UIF;
}
