vec3 hash32(vec2 q){
	uvec3 n = uvec3(ivec3(q.xyx)) * UI3;
	n = (n.x ^ n.y ^ n.z) * UI3;
	return vec3(n) * UIF;
}
