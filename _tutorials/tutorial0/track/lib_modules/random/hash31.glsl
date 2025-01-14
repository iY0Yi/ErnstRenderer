vec3 hash31(float p){
	uvec3 n = uint(int(p)) * UI3;
	n = (n.x ^ n.y ^ n.z) * UI3;
	return vec3(n) * UIF;
}
