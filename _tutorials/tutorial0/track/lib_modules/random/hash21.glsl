vec2 hash21(float p){
	uvec2 n = uint(int(p)) * UI2;
	n = (n.x ^ n.y) * UI2;
	return vec2(n) * UIF;
}
