vec2 hash22(uvec2 q){
	q *= UI2;
	q = (q.x ^ q.y) * UI2;
	return vec2(q) * UIF;
}
