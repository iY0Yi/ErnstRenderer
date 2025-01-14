float hash13(vec3 p){
	uvec3 q = uvec3(ivec3(p)) * UI3;
	uint n = (q.x ^ q.y ^ q.z) * UI0;
	return float(n) * UIF;
}
