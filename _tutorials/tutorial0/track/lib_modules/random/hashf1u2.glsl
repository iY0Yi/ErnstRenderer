float hash12(uvec2 q){
	q *= UI2;
	uint n = (q.x ^ q.y) * UI0;
	return float(n) * UIF;
}
