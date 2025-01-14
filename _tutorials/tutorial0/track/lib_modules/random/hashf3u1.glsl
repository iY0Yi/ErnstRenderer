vec3 hash31(uint q){
	uvec3 n = q * UI3;
	n = (n.x ^ n.y ^ n.z) * UI3;
	return vec3(n) * UIF;
}
