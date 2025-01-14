vec3 hash32(uvec2 q){
	uvec3 n = q.xyx * UI3;
	n = (n.x ^ n.y ^n.z) * UI3;
	return vec3(n) * UIF;
}
