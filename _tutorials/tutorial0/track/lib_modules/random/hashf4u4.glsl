vec4 hash44(uvec4 q){
	q *= UI4;
	q = (q.x ^ q.y ^ q.z ^ q.w)*UI4;
	return vec4(q) * UIF;
}
