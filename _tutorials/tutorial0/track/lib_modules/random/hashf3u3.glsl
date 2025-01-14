vec3 hash33(uvec3 q){
	q *= UI3;
	q = (q.x ^ q.y ^ q.z)*UI3;
	return vec3(q) * UIF;
}
