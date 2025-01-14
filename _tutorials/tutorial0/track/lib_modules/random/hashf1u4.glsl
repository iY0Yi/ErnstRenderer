float hash14(uvec4 q){
	q *= UI4;
	uint n = (q.x ^ q.y ^ q.z ^ q.w) * UI0;
	return float(n) * UIF;
}
