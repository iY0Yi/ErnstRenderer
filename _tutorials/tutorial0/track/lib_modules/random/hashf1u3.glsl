float hash13(uvec3 q){
	q *= UI3;
	uint n = (q.x ^ q.y ^ q.z) * UI0;
	return float(n) * UIF;
}
