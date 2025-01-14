vec2 hash23(uvec3 q){
	q *= UI3;
	uvec2 n = (q.x ^ q.y ^ q.z) * UI2;
	return vec2(n) * UIF;
}
